import os
import cv2
import json
import shutil


def tomanyjsons(path=None):

    if path:
        json_path = os.path.join(path, "video-frames-openpose.json")
        output_local_json = os.path.join(path, "openpose.json")
    else:
        json_path = '..\\static\\interface\\video\\video-frames-openpose.json'
        output_local_json = '..\\static\\interface\\video\\openpose.json'

    data = []
    frames = []

    filename = 'video-frames'

    json_files = [pos_json for pos_json in os.listdir(
        json_path) if pos_json.endswith('.json')]

    for filename in json_files:
        with open(os.path.join(json_path, filename), 'r') as f:
            data.append(json.load(f))

    for idx, frame in enumerate(data):
        persons = []
        for people in frame["people"]:
            body_parts = []
            keypoints = people["pose_keypoints_2d"]
            for index in range(0, len(keypoints), 3):
                body_parts.append(
                    [keypoints[index], keypoints[index+1], keypoints[index+2]])
            persons.append(body_parts)
        frames.append({
            "id": idx,
            "persons": persons,
        })

    with open(output_local_json, "w+") as f:
        json.dump(frames, f, indent=4)

    shutil.rmtree(json_path)


if __name__ == "__main__":
    tomanyjsons()
