import cv2
import mediapipe as mp
import numpy as np

# Khởi tạo MediaPipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

# Mở webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Không thể mở webcam")
    exit()

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Không thể đọc khung hình")
        break

    # Chuyển sang RGB để xử lý
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(image)

    # Chuyển lại sang BGR để hiển thị
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # Vẽ các điểm khớp và phân tích
    if results.pose_landmarks:
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        # Lấy tọa độ các khớp (ví dụ: vai, khuỷu tay, cổ tay)
        landmarks = results.pose_landmarks.landmark
        shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                    landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
        elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                 landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
        wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                 landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

        # Tính góc khuỷu tay (đơn vị: độ)
        def calculate_angle(a, b, c):
            a = np.array(a)  # Điểm đầu (vai)
            b = np.array(b)  # Điểm giữa (khuỷu tay)
            c = np.array(c)  # Điểm cuối (cổ tay)
            radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
            angle = np.abs(radians * 180.0 / np.pi)
            if angle > 180.0:
                angle = 360 - angle
            return angle

        angle = calculate_angle(shoulder, elbow, wrist)
        print(f"Góc khuỷu tay: {angle:.2f} độ")

        # Hiển thị góc trên hình ảnh
        cv2.putText(image, f"Angle: {angle:.2f}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Hiển thị khung hình
    cv2.imshow('Pose Detection', image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Giải phóng tài nguyên
cap.release()
cv2.destroyAllWindows()
pose.close()