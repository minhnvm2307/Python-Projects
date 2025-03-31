import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Import your methods and utils
from methods import newton_method, bisection_method, secant_method
from utils import plot_orbit, animate_orbit # Ensure ani is handled in utils

# --- Main Calculation and Update Function ---
def calculate_and_visualize(entries, method_var, result_vars, history_table, canvas, ax, fig):
    """Handles input gathering, calculation, and updating the UI."""
    try:
        # --- Get Inputs ---
        e_str = entries['e'].get()
        M_deg_str = entries['M'].get()
        E0_str = entries['E0'].get() # Initial guess (for Newton/Secant)

        e = float(e_str)
        M_deg = float(M_deg_str)
        M_rad = np.radians(M_deg) # Convert M to radians for calculations

        # Validate inputs
        if not (0 <= e < 1):
            messagebox.showerror("Input Error", "Eccentricity (e) must be between 0 (inclusive) and 1 (exclusive).")
            return
        if not (-360 <= M_deg <= 360): # Allow one full circle +/-
             print(f"Warning: Mean Anomaly M={M_deg}° is outside typical [0, 360] range, but proceeding.")
             # Normalize M to [0, 2*pi) if desired
             # M_rad = M_rad % (2 * np.pi)


        method = method_var.get()
        E0 = 0.0 # Default E0
        if method == "Newton":
             if not E0_str: # Use M as default guess if E0 is empty
                 E0 = M_rad
                 entries['E0'].delete(0, tk.END)
                 entries['E0'].insert(0, f"{E0:.4f}") # Show default guess used
             else:
                 E0 = float(E0_str)
        # Secant needs two points, let's derive the second from E0 if needed
        elif method == "Secant":
             if not E0_str:
                 E0_val1 = M_rad # First guess based on M
                 E0_val2 = M_rad + 0.1 # Slightly perturbed second guess
                 entries['E0'].delete(0, tk.END)
                 entries['E0'].insert(0, f"{E0_val1:.4f}") # Show primary guess used
             else:
                 E0_val1 = float(E0_str)
                 E0_val2 = E0_val1 + 0.1 # Perturb the user's guess

        # --- Select Solver ---
        result, history, error, steps = None, [], None, 0
        tol = 1e-8 # Define tolerance
        max_iter = 100 # Define max iterations

        if method == "Newton":
            result, history, error, steps = newton_method(e, M_rad, E0, tol=tol, max_iter=max_iter)
            result_vars['method'].set("Newton-Raphson")
        elif method == "Bisection":
            # Bisection needs an interval [a, b] where f(a) and f(b) have opposite signs.
            # A common safe interval for 0 <= M <= pi is [0, M+e]. For pi < M < 2pi is [M-e, 2pi]
            # Let's try a robust interval [M-e, M+e] clipped to [0, 2*pi] initially.
            a_bis = max(0.0, M_rad - e)
            b_bis = min(2 * np.pi, M_rad + e)
            # Check signs; fallback to [0, 2*pi] if needed and valid
            f_a_check = a_bis - e * np.sin(a_bis) - M_rad
            f_b_check = b_bis - e * np.sin(b_bis) - M_rad
            if np.sign(f_a_check) == np.sign(f_b_check):
                 print(f"Warning (Bisection): Initial interval [{a_bis:.2f}, {b_bis:.2f}] doesn't bracket root. Trying [0, 2*pi].")
                 a_bis = 0.0
                 b_bis = 2 * np.pi

            result, history, error, steps = bisection_method(e, M_rad, a_bis, b_bis, tol=tol, max_iter=max_iter)
            result_vars['method'].set("Bisection")
        elif method == "Secant":
            # Use the E0_val1 and E0_val2 derived earlier
            result, history, error, steps = secant_method(e, M_rad, E0_val1, E0_val2, tol=tol, max_iter=max_iter)
            result_vars['method'].set("Secant")
        else:
            messagebox.showerror("Error", "Invalid method selected.")
            return

        # --- Update Results ---
        # Clear previous history
        for item in history_table.get_children():
            history_table.delete(item)
        # Populate history table
        if history:
            for item in history:
                # Format numbers for display
                formatted_item = [f"{item[0]}", f"{item[1]:.8f}", f"{item[2]:.3e}"]
                history_table.insert("", tk.END, values=formatted_item)

        # Update result labels
        if result is not None:
            result_vars['E'].set(f"{result:.8f} rad")
            result_vars['error'].set(f"{error:.3e}" if error is not None else "N/A")
            result_vars['steps'].set(f"{steps}")
            # --- Plotting and Animation ---
            # plot_orbit(e, result, M_rad, canvas, ax) # Static plot
            animate_orbit(e, result, M_rad, canvas, ax, fig) # Animate
        else:
            result_vars['E'].set("Failed")
            result_vars['error'].set("N/A")
            result_vars['steps'].set(f"{steps}")
            plot_orbit(e, None, M_rad, canvas, ax) # Show orbit even on failure, but no object position
            messagebox.showwarning("Convergence Warning", f"{method} method did not converge within {max_iter} iterations.")

    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers for e, M, and E0 (if applicable).")
    except Exception as ex:
        messagebox.showerror("Error", f"An unexpected error occurred: {ex}")
        print(f"Traceback: {ex}") # Print details to console for debugging

# --- GUI Creation Functions ---




# This function creates the input frame for user inputs and method selection.
def create_input_frame(root, calculate_callback):
    """Creates the left frame for inputs and controls."""
    input_frame = ttk.Frame(root, padding="10")
    input_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)

    ttk.Label(input_frame, text="Tham số", font="-weight bold").grid(row=0, column=0, columnspan=2, pady=(0, 10))

    # Eccentricity (e)
    ttk.Label(input_frame, text="Eccentricity (e):").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
    entry_e = ttk.Entry(input_frame, width=15)
    entry_e.grid(row=1, column=1, padx=5, pady=2)
    entry_e.insert(0, "0.5") # Default value

    # Mean Anomaly (M)
    ttk.Label(input_frame, text="Mean Anomaly (M, deg):").grid(row=2, column=0, sticky=tk.W, padx=5, pady=2)
    entry_M = ttk.Entry(input_frame, width=15)
    entry_M.grid(row=2, column=1, padx=5, pady=2)
    entry_M.insert(0, "45.0") # Default value

    # Initial Guess (E0) - Relevant for Newton/Secant
    ttk.Label(input_frame, text="Initial E0 (rad, optional):").grid(row=3, column=0, sticky=tk.W, padx=5, pady=2)
    entry_E0 = ttk.Entry(input_frame, width=15)
    entry_E0.grid(row=3, column=1, padx=5, pady=2)
    entry_E0.insert(0, "") # Default empty, calculated if needed

    # Method Selection
    ttk.Label(input_frame, text="Chọn phương pháp lặp:", font="-weight bold").grid(row=4, column=0, columnspan=2, pady=(10, 5))
    method_var = tk.StringVar(value="Newton") # Default method

    ttk.Radiobutton(input_frame, text="Newton-Raphson", variable=method_var, value="Newton").grid(row=5, column=0, columnspan=2, sticky=tk.W, padx=5)
    ttk.Radiobutton(input_frame, text="Secant", variable=method_var, value="Secant").grid(row=6, column=0, columnspan=2, sticky=tk.W, padx=5)
    ttk.Radiobutton(input_frame, text="Bisection", variable=method_var, value="Bisection").grid(row=7, column=0, columnspan=2, sticky=tk.W, padx=5)

    # Calculate Button
    calc_button = ttk.Button(input_frame, text="Bắt đầu tính toán", command=calculate_callback)
    calc_button.grid(row=8, column=0, columnspan=2, pady=(15, 5))

    # Store entry widgets for easy access in callback
    entries = {'e': entry_e, 'M': entry_M, 'E0': entry_E0}
    return input_frame, entries, method_var





# --- Output Frame Creation ---
# This function creates the output frame for results and plotting.
def create_output_frame(root):
    """Creates the right frame for results and plotting."""
    output_frame = ttk.Frame(root, padding="5")
    output_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH, padx=5, pady=5)

    # --- Results Area ---
    results_area = ttk.LabelFrame(output_frame, text="Kết quả", padding="10")
    results_area.pack(side=tk.TOP, fill=tk.X, pady=(0, 5))

    result_vars = {
        'method': tk.StringVar(value="N/A"),
        'E': tk.StringVar(value="N/A"),
        'error': tk.StringVar(value="N/A"),
        'steps': tk.StringVar(value="N/A")
    }

    ttk.Label(results_area, text="Phương pháp lặp:").grid(row=0, column=0, sticky=tk.W, padx=5)
    ttk.Label(results_area, textvariable=result_vars['method']).grid(row=0, column=1, sticky=tk.W, padx=5)
    ttk.Label(results_area, text="Số lần lặp:").grid(row=0, column=2, sticky=tk.W, padx=15)
    ttk.Label(results_area, textvariable=result_vars['steps']).grid(row=0, column=3, sticky=tk.W, padx=5)

    ttk.Label(results_area, text="Kết quả (rad):").grid(row=1, column=0, sticky=tk.W, padx=5)
    ttk.Label(results_area, textvariable=result_vars['E'], font="-weight bold").grid(row=1, column=1, sticky=tk.W, padx=5)
    ttk.Label(results_area, text="Sai số ≈").grid(row=1, column=2, sticky=tk.W, padx=15)
    ttk.Label(results_area, textvariable=result_vars['error']).grid(row=1, column=3, sticky=tk.W, padx=5)

    # --- History Table Area ---
    history_frame = ttk.LabelFrame(output_frame, text="History", padding="10")
    history_frame.pack(side=tk.TOP, fill=tk.X, pady=5)

    history_cols = ("#1", "#2", "#3") # Step, E_value, Error
    history_table = ttk.Treeview(history_frame, columns=history_cols, show='headings', height=6)
    history_table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Define headings
    history_table.heading("#1", text="Bước lặp")
    history_table.heading("#2", text="Giá trị E (rad) - Dị thường lệch tâm")
    history_table.heading("#3", text="Sai số") # Could be |f(E)| or interval width
    # Define column widths
    history_table.column("#1", width=50, anchor=tk.CENTER)
    history_table.column("#2", width=150, anchor=tk.W)
    history_table.column("#3", width=100, anchor=tk.W)

    # Add scrollbar
    scrollbar = ttk.Scrollbar(history_frame, orient=tk.VERTICAL, command=history_table.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    history_table.configure(yscrollcommand=scrollbar.set)


    # --- Plotting Area ---
    plot_frame = ttk.Frame(output_frame)
    plot_frame.pack(side=tk.BOTTOM, expand=True, fill=tk.BOTH, pady=(5,0))

    fig = plt.Figure(figsize=(6, 5), dpi=100) # Create Matplotlib Figure
    ax = fig.add_subplot(111) # Add axes to the figure

    canvas = FigureCanvasTkAgg(fig, master=plot_frame) # Link fig to Tkinter
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    canvas.draw() # Initial draw

    return output_frame, result_vars, history_table, canvas, ax, fig

# --- Main Application Setup ---
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Kepler's Equation Solver & Visualizer")
    # Optional: Set a minimum size
    root.minsize(850, 600)

    # Use themed widgets for a more modern look
    style = ttk.Style(root)
    # print(style.theme_names()) # See available themes
    try:
       style.theme_use('clam') # Or 'alt', 'default', 'classic', 'vista', 'xpnative'
    except tk.TclError:
        print("Clam theme not available, using default.")


    # Create output frame first (to get handles like canvas, ax)
    output_frame, result_vars, history_table, canvas, ax, fig = create_output_frame(root)

    # Create input frame, passing the calculate function which needs access to output widgets
    # Use lambda to pass the necessary arguments to the callback
    input_frame, entries, method_var = create_input_frame(root,
        lambda: calculate_and_visualize(entries, method_var, result_vars, history_table, canvas, ax, fig)
    )

    # Start with an initial plot (optional)
    # plot_orbit(0.1, None, np.radians(30), canvas, ax) # Example initial plot

    root.mainloop()