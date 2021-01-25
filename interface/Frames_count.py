import cv2
import os


def frames_count(path=None):

    if path:
        video_path = os.path.join(path, "video.mp4")
        video_out_name = os.path.join(path, "video-frames.mp4")
    else:
        video_path = '..\\static\\interface\\video\\video.mp4'
        video_out_name = '..\\static\\interface\\video\\video-frames.mp4'
    cap = cv2.VideoCapture(video_path)
    frame_counter = 0

    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))

    out = cv2.VideoWriter(video_out_name, cv2.VideoWriter_fourcc(
        *'H264'), 30, (frame_width, frame_height))

    while(True):
        ret, frame = cap.read()
        if ret == True:

            font = cv2.FONT_HERSHEY_SIMPLEX

            cv2.putText(frame,
                        str(frame_counter),
                        (75, 75),
                        font, 2,
                        (255, 255, 255),
                        4,
                        cv2.LINE_4)

            out.write(frame)

            frame_counter += 1

        else:
            break

    cap.release()
    out.release()

    cv2.destroyAllWindows()


if __name__ == "__main__":
    frames_count()
