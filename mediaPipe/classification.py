import mediapipe as mp
import cv2 as cv

"""- Add model file
- Get the model file path
"""

model_path = 'efficientdet_lite0.tflite'

"""### Init some object to use"""

BaseOptions = mp.tasks.BaseOptions
ObjectDetector = mp.tasks.vision.ObjectDetector
ObjectDetectorOptions = mp.tasks.vision.ObjectDetectorOptions
VisionRunningMode = mp.tasks.vision.RunningMode

options = ObjectDetectorOptions (
    base_options = BaseOptions(model_asset_path=model_path),
    running_mode = VisionRunningMode.IMAGE,
    max_results = 5,
    score_threshold = 0.5
)

"""### Start detecting"""

with ObjectDetector.create_from_options(options) as detector:
  # Upload img from file
  image = mp.Image.create_from_file('c:/Users/ADMIN/Desktop/PythonCoding/openCV/asset/chair.jpg')
  showed_image = cv.imread('c:/Users/ADMIN/Desktop/PythonCoding/openCV/asset/chair.jpg')

  # Formatting the img to num array
  image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image.numpy_view())

  # Perform object detection on the provided single image.
  detection_result = detector.detect(image).detections
  print(detection_result)

  for obj in detection_result:
    round_box = obj.bounding_box
    x, y, w, h = int(round_box.origin_x), int(round_box.origin_y), int(round_box.width), int(round_box.height)
    cv.rectangle(showed_image, (x, y), (x+w, y+h), (0, 255, 0), 2)

  cv.imshow('Image', showed_image)
  cv.waitKey(0)
  cv.destroyAllWindows()