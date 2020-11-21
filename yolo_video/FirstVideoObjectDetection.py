from imageai.Detection import VideoObjectDetection
import os

execution_path = os.getcwd()

detector = VideoObjectDetection()
detector.setModelTypeAsYOLOv3()
detector.setModelPath(os.path.join(
    execution_path, "weights/test.h5"))
detector.loadModel()

video_path = detector.detectObjectsFromVideo(input_file_path=os.path.join(execution_path, "media/video.mp4"), output_file_path=os.path.join(
    execution_path, "video2"), frames_per_second=30, log_progress=True)
print(video_path)
