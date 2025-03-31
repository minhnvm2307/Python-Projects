import mediapipe as mp
import cv2 as cv
import time

# Cấu hình MediaPipe
BaseOptions = mp.tasks.BaseOptions
ObjectDetector = mp.tasks.vision.ObjectDetector
ObjectDetectorOptions = mp.tasks.vision.ObjectDetectorOptions
VisionRunningMode = mp.tasks.vision.RunningMode

# Đường dẫn tới mô hình
model_path = 'efficientdet_lite0.tflite'

# Cấu hình tùy chọn cho chế độ VIDEO
options = ObjectDetectorOptions(
    base_options=BaseOptions(model_asset_path=model_path),
    running_mode=VisionRunningMode.VIDEO,  # Chuyển sang chế độ VIDEO
    max_results=5,
    score_threshold=0.3
)

# Khởi tạo ObjectDetector
detector = ObjectDetector.create_from_options(options)

# Mở webcam (0 là webcam mặc định)
cap = cv.VideoCapture(0)

# Kiểm tra xem webcam có mở thành công không
if not cap.isOpened():
    print("Không thể mở webcam")
    exit()

# Biến để theo dõi thời gian (timestamp)
frame_timestamp_ms = 0

# Vòng lặp để xử lý video từ webcam
while True:
    # Đọc khung hình từ webcam
    ret, frame = cap.read()
    if not ret:
        print("Không thể đọc khung hình từ webcam")
        break

    # Chuyển khung hình sang định dạng MediaPipe Image
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)

    # Thực hiện phát hiện đối tượng (dùng detect_for_video với timestamp)
    detection_result = detector.detect_for_video(mp_image, frame_timestamp_ms)

    # Tăng timestamp cho khung tiếp theo (đơn vị là millisecond)
    frame_timestamp_ms += 33  # Giả sử 30 FPS (1000ms / 30 ≈ 33ms)

    # Lấy danh sách các đối tượng được phát hiện
    objects_detected = detection_result.detections

    # Vẽ hộp giới hạn và nhãn lên khung hình
    for obj in objects_detected:
        # Lấy bounding box
        round_box = obj.bounding_box
        start_point = (round_box.origin_x, round_box.origin_y)
        end_point = (round_box.origin_x + round_box.width, round_box.origin_y + round_box.height)

        # Vẽ hộp giới hạn
        cv.rectangle(frame, start_point, end_point, (0, 255, 0), 2)

        # Lấy nhãn và điểm tin cậy
        category = obj.categories[0]  # Lấy danh mục đầu tiên
        label = f"{category.category_name} ({category.score:.2f})"

        # Vị trí nhãn (phía trên hộp)
        label_position = (round_box.origin_x, round_box.origin_y - 10)

        # Vẽ nhãn lên khung hình
        cv.putText(frame, label, label_position, 
                   cv.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2, cv.LINE_AA)

    # Hiển thị khung hình
    cv.imshow('Object Detection - Webcam', frame)

    # Nhấn 'q' để thoát
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# Giải phóng tài nguyên
cap.release()
cv.destroyAllWindows()
detector.close()  # Đóng detector để giải phóng tài nguyên