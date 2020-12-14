import os
import cv2
import json
import shutil
import subprocess
from os.path import exists, join, basename, splitext


def openpose(path=None):

    print(os.getcwd())
    if path:
        video_path = os.path.join(path, "video-frames.mp4")
        video_output = os.path.join(path, "video-openpose.avi")
        op_path = os.path.join(os.getcwd(), "bin/OpenPoseDemo.exe")
    else:
        video_path = os.path.join(
            os.getcwd().replace("openpose1", ""), '..\\static\\interface\\video\\video-frames.mp4')
        video_output = os.path.join(
            os.getcwd().replace("openpose1", ""), '..\\static\\interface\\video\\video-openpose.avi')

    openpose_json_path = video_path.replace(
        '.mp4', '') + '-openpose.json'

    # subprocess.run(
    # "{op_path} --video {video_path} --display 0 --write_video {video_output} --write_json {openpose_json_path}’", shell=True)
    # "bin/OpenPoseDemo.exe --video {video_path} --display 0 --write_video {video_output} --write_json {openpose_json_path}", shell=True
    os.system(
        # f"cmd /k bin\\OpenPoseDemo.exe --video {video_path} --display 0 --write_video {video_output} --write_json {openpose_json_path}")
        f"bin\\OpenPoseDemo.exe --video {video_path} --display 0 --write_video {video_output} --write_json {openpose_json_path}")


if __name__ == "__main__":
    openpose()
