import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.patches as patches # For drawing arcs


# Global variable to store the animation object to prevent garbage collection
ani = None
# Keep track of artists added for easy clearing/updating
plot_elements = {}


def calculate_true_anomaly(E, e):
    """
    Tính toán True Anomaly (nu) từ Eccentric Anomaly (E) và độ lệch tâm (e).
    => Góc giữa vecto bán kính (vị trí của hành tinh trên quỹ đạo) và đường cận điểm (điểm gần Mặt Trời nhất), đo từ tiêu điểm chính của quỹ đạo.
    Args:
        E (float): Eccentric Anomaly (radians).
        e (float): Eccentricity.
    Returns:
        float: True Anomaly (nu) in radians.
    """
    cos_E = np.cos(E)
    sin_E = np.sin(E)
    nu = np.arctan2(np.sqrt(1.0 - e**2) * sin_E, cos_E - e)
    return nu


def plot_orbit(e, E, M, canvas, ax):
    """
    Draws a detailed static orbit visualization.
    Args:
        e (float): Eccentricity.
        E (float): Calculated Eccentric Anomaly (radians). Can be None if calculation failed.
        M (float): Mean Anomaly (radians).
        canvas (FigureCanvasTkAgg): Matplotlib canvas linked to Tkinter.
        ax (matplotlib.axes.Axes): Axes object to plot on.
    """
    global ani, plot_elements
    if ani is not None:
        # Stop the previous animation if it's running
        try:
            if hasattr(ani, '_stop'):
                ani._stop()
            elif hasattr(ani, 'event_source') and ani.event_source is not None:
                 ani.event_source.stop()
        except AttributeError:
            pass # Already stopped or None
        ani = None # Clear the reference

    # Clear previous plot elements managed by us and the axes
    for key, artist_list in plot_elements.items():
        for artist in artist_list:
            artist.remove()
    plot_elements = {}
    ax.clear() # Clear axes completely

    # --- Orbit Parameters ---
    a = 1.0 # Semi-major axis (normalized)
    if not (0 <= e < 1): # Basic validation
        ax.set_title("Invalid Eccentricity (e must be 0 <= e < 1)")
        canvas.draw()
        return
    b = a * np.sqrt(1.0 - e**2) # Semi-minor axis
    c = a * e # Distance from center to focus

    # --- Plot Ellipse Orbit Path ---
    theta_ellipse = np.linspace(0, 2 * np.pi, 200)
    x_ellipse = a * np.cos(theta_ellipse) - c # Centered at (-c, 0)
    y_ellipse = b * np.sin(theta_ellipse)
    orbit_line, = ax.plot(x_ellipse, y_ellipse, 'b-', linewidth=1.5, label='Orbit Path')
    plot_elements['orbit'] = [orbit_line]

    # --- Plot Focus (Sun) and Ellipse Center ---
    focus_marker, = ax.plot(0, 0, 'yo', markersize=10, label='Focus (F)') # Focus F at origin
    center_marker, = ax.plot(-c, 0, 'ko', markersize=5, label='Center (C)') # Center C
    plot_elements['markers'] = [focus_marker, center_marker]

    # --- Plot Major Axis Segment ---
    periapsis_x = a - c
    apoapsis_x = -a - c
    major_axis, = ax.plot([apoapsis_x, periapsis_x], [0, 0], 'k--', linewidth=0.7, alpha=0.8, label='Major Axis')
    peri_marker, = ax.plot(periapsis_x, 0, 'k>', markersize=6, alpha=0.8) # Point towards periapsis
    apo_marker, = ax.plot(apoapsis_x, 0, 'k<', markersize=6, alpha=0.8) # Point towards apoapsis
    plot_elements['axis'] = [major_axis, peri_marker, apo_marker]
    plot_elements['axis_text'] = [
        ax.text(periapsis_x, 0.05 * a, 'Periapsis', ha='center', va='bottom', fontsize=8, color='gray'),
        ax.text(apoapsis_x, 0.05 * a, 'Apoapsis', ha='center', va='bottom', fontsize=8, color='gray')
    ]

    # --- Plot Auxiliary Circle ---
    aux_circle = patches.Circle((-c, 0), a, fill=False, linestyle='--', color='gray', linewidth=0.8, label='Auxiliary Circle (radius a)')
    ax.add_patch(aux_circle)
    plot_elements['aux_circle'] = [aux_circle]

    # --- Plot Elements Related to E and nu (if E is valid) ---
    plot_elements['object'] = []
    plot_elements['lines'] = []
    plot_elements['angles'] = []
    plot_elements['labels'] = []

    final_nu = None
    if E is not None:
        # --- Calculate Object Position (P) ---
        cos_E = np.cos(E)
        sin_E = np.sin(E)
        x_obj = a * (cos_E - e) # Position relative to focus F (origin)
        y_obj = b * sin_E       # Position relative to focus F (origin)
        object_marker, = ax.plot(x_obj, y_obj, 'ro', markersize=8, label=f'Object (P)')
        object_label = ax.text(x_obj, y_obj + 0.05*a, 'P', ha='center', va='bottom', color='red', fontsize=9, fontweight='bold')
        plot_elements['object'] = [object_marker]
        plot_elements['labels'].append(object_label)

        # --- Auxiliary Point (Q) on Auxiliary Circle ---
        aux_x = a * cos_E - c # Relative to origin (Focus F)
        aux_y = a * sin_E     # Relative to origin (Focus F)
        aux_point_marker, = ax.plot(aux_x, aux_y, 'go', markersize=4, alpha=0.7, label='Auxiliary Pt (Q)')
        plot_elements['markers'].append(aux_point_marker)

        # --- Lines for Visualizing E ---
        # Line from Center (C) to Auxiliary Point (Q)
        line_cq, = ax.plot([-c, aux_x], [0, aux_y], 'g--', linewidth=1.0, label='Line C-Q (defines E)')
        # Line from Object (P) perpendicular to major axis
        line_p_proj, = ax.plot([x_obj, x_obj], [y_obj, 0], 'r:', linewidth=0.8)
        # Line connecting projection on axis to Q
        line_proj_q, = ax.plot([x_obj, aux_x], [0, aux_y], 'g:', linewidth=0.8)
        plot_elements['lines'].extend([line_cq, line_p_proj, line_proj_q])

        # --- Draw Arc for Eccentric Anomaly (E) ---
        E_degrees = np.degrees(E)
        # Draw arc centered at C=(-c, 0)
        arc_E = patches.Arc((-c, 0), 0.4*a, 0.4*a, angle=0, theta1=0, theta2=E_degrees,
                            color='green', linestyle='-', linewidth=1.5, label=f'E = {E_degrees:.2f}°')
        ax.add_patch(arc_E)
        # Add text label for E near the arc end
        E_label_rad = 0.25 * a # Radius for placing the 'E' label
        E_label_angle = E / 2.0 # Place label roughly halfway along arc
        E_label_x = -c + E_label_rad * np.cos(E_label_angle)
        E_label_y = 0 + E_label_rad * np.sin(E_label_angle)
        E_text = ax.text(E_label_x, E_label_y, 'E', color='green', fontsize=12, ha='center', va='center')
        plot_elements['angles'].append(arc_E)
        plot_elements['labels'].append(E_text)

        # --- Calculate and Draw True Anomaly (ν) ---
        final_nu = calculate_true_anomaly(E, e)
        nu_degrees = np.degrees(final_nu)

        # Line from Focus (F) to Object (P)
        line_fp, = ax.plot([0, x_obj], [0, y_obj], 'm-', linewidth=1.0, label='Line F-P (defines ν)')
        plot_elements['lines'].append(line_fp)

        # Draw arc centered at F=(0, 0)
        arc_nu = patches.Arc((0, 0), 0.6*a, 0.6*a, angle=0, theta1=0, theta2=nu_degrees,
                             color='magenta', linestyle='-', linewidth=1.5, label=f'ν = {nu_degrees:.2f}°')
        ax.add_patch(arc_nu)
        # Add text label for nu near the arc end
        nu_label_rad = 0.35 * a # Radius for placing the 'ν' label
        nu_label_angle = final_nu / 2.0 # Place label roughly halfway along arc
        nu_label_x = 0 + nu_label_rad * np.cos(nu_label_angle)
        nu_label_y = 0 + nu_label_rad * np.sin(nu_label_angle)
        nu_text = ax.text(nu_label_x, nu_label_y, 'ν', color='magenta', fontsize=12, ha='center', va='center')
        plot_elements['angles'].append(arc_nu)
        plot_elements['labels'].append(nu_text)

        # --- Add Text with Key Values ---
        info_text = (f"Inputs: e = {e:.3f}, M = {np.degrees(M):.2f}°\n"
                 f"Result: E = {E_degrees:.2f}°, ν = {nu_degrees:.2f}°")
        # Position text box in upper right corner using axes coordinates
        info_label = ax.text(0.98, 0.98, info_text, transform=ax.transAxes, fontsize=9,
                     verticalalignment='top', horizontalalignment='right',
                     bbox=dict(boxstyle='round,pad=0.3', fc='wheat', alpha=0.5))
        plot_elements['labels'].append(info_label)


    # --- Plot Settings ---
    ax.set_xlabel("X (units of a)")
    ax.set_ylabel("Y (units of a)")
    title_str = f"Kepler Orbit Visualization (e={e:.3f})"
    if E is None:
         title_str += " - E Calculation Failed"
    ax.set_title(title_str)
    ax.set_aspect('equal', adjustable='box')
    ax.grid(True, linestyle=':', alpha=0.5)

    # Adjust limits dynamically based on orbit size
    max_extent = a + c # Farthest point from origin is apoapsis at -(a+c)
    ax.set_xlim(-max_extent - 0.1*a, max_extent + 0.1*a)
    ax.set_ylim(-a - 0.1*a, a + 0.1*a) # Use 'a' for y-limits as max vertical extent

    # Add legend - might get crowded, consider removing if labels are clear
    # ax.legend(fontsize='small', loc='lower right')

    canvas.draw()


def animate_orbit(e, E_final, M, canvas, ax, fig):
    """
    Animates the object moving along the orbit path up to the final E.
    Updates object marker and key lines connected to it.
    """
    global ani, plot_elements
    if E_final is None:
        plot_orbit(e, None, M, canvas, ax) # Plot static orbit without object if E failed
        print("Animation skipped: E calculation failed.")
        return

    # --- Setup basic orbit plot first (draws all static elements and final state) ---
    plot_orbit(e, E_final, M, canvas, ax)

    # --- Identify elements to animate ---
    # These should have been created and stored in plot_elements by plot_orbit
    object_marker = plot_elements.get('object', [None])[0]
    line_cq = next((line for line in plot_elements.get('lines', []) if line.get_label() == 'Line C-Q (defines E)'), None)
    line_p_proj = next((line for line in plot_elements.get('lines', []) if line.get_linestyle() == ':'), None) # Assuming this is unique enough
    line_proj_q = next((line for line in plot_elements.get('lines', []) if line.get_linestyle() == ':'), None) # Needs better identification maybe
    line_fp = next((line for line in plot_elements.get('lines', []) if line.get_label() == 'Line F-P (defines ν)'), None)
    # Arcs and text are generally hard to animate efficiently with blitting, so we won't update them dynamically.

    elements_to_animate = [elem for elem in [object_marker, line_cq, line_p_proj, line_fp] if elem is not None] # line_proj_q excluded for simplicity maybe

    if not object_marker:
        print("Error: Could not find object plot element for animation.")
        canvas.draw()
        return
    if not all(elements_to_animate):
         print("Warning: Could not find all expected line elements for animation.")


    # --- Animation Parameters ---
    a = 1.0
    b = a * np.sqrt(1.0 - e**2)
    c = a * e
    num_frames = 100 # Number of steps in the animation
    E_values = np.linspace(0, E_final, num_frames) # Animate E from 0 to E_final

    # --- Update function for animation ---
    def update(frame_E):
        artists_updated = []
        # Calculate instantaneous positions based on frame_E
        cos_E = np.cos(frame_E)
        sin_E = np.sin(frame_E)
        x_obj = a * (cos_E - e)
        y_obj = b * sin_E
        aux_x = a * cos_E - c
        aux_y = a * sin_E

        # Update Object Marker
        if object_marker:
            object_marker.set_data([x_obj], [y_obj])
            artists_updated.append(object_marker)

        # Update Line C-Q
        if line_cq:
            line_cq.set_data([-c, aux_x], [0, aux_y])
            artists_updated.append(line_cq)

        # Update Line P-Projection
        if line_p_proj:
            line_p_proj.set_data([x_obj, x_obj], [y_obj, 0])
            artists_updated.append(line_p_proj)

        # Update Line F-P
        if line_fp:
            line_fp.set_data([0, x_obj], [0, y_obj])
            artists_updated.append(line_fp)

        # Update Object Label 'P' position (optional, might need blit=False)
        # object_label = next((txt for txt in plot_elements.get('labels', []) if txt.get_text() == 'P'), None)
        # if object_label:
        #     object_label.set_position((x_obj, y_obj + 0.05*a))
        #     artists_updated.append(object_label)

        # Note: Arcs (E, nu) and their text labels are NOT updated here for blitting performance.
        # They remain showing the final calculated values.

        return artists_updated # Return list/tuple of artists modified for blitting

    # --- Create and store the animation ---
    if ani is not None:
        try:
            if hasattr(ani, '_stop'): ani._stop()
            elif hasattr(ani, 'event_source') and ani.event_source is not None: ani.event_source.stop()
        except AttributeError: pass
        ani = None

    ani = FuncAnimation(fig, update, frames=E_values,
                        interval=50, # ms delay between frames
                        blit=True,   # Use blitting for performance
                        repeat=False, # Don't repeat the animation
                        save_count=num_frames)

    canvas.draw() # Start the drawing process