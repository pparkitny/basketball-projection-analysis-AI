from imageai.Detection import VideoObjectDetection
import os

execution_path = os.getcwd()

detector = VideoObjectDetection()
detector.setModelTypeAsYOLOv3()
detector.setModelPath(os.path.join(
    execution_path, "weights/yolo.h5"))
detector.loadModel()

video_path = detector.detectObjectsFromVideo(input_file_path=os.path.join(execution_path, "yolo_video/video2-frames.mp4"), output_file_path=os.path.join(
    execution_path, "../static/interface/video/video2-yolo"), frames_per_second=30, log_progress=True)
print(video_path)
