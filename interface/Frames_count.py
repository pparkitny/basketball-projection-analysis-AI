import cv2
import os


def frames_count(path=None):

    # Create a VideoCapture object
    if path:
        video_path = os.path.join(path, "video.mp4")
        video_out_name = os.path.join(path, "video-frames.mp4")
    else:
        video_path = '..\\static\\interface\\video\\video.mp4'
        video_out_name = '..\\static\\interface\\video\\video-frames.mp4'
    cap = cv2.VideoCapture(video_path)
    frame_counter = 0

    # Default resolutions of the frame are obtained.The default resolutions are system dependent.
    # We convert the resolutions from float to integer.
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))

    # Define the codec and create VideoWriter object.The output is stored in 'outpy.avi' file.
    out = cv2.VideoWriter(video_out_name, cv2.VideoWriter_fourcc(
        *'H264'), 30, (frame_width, frame_height))

    while(True):
        ret, frame = cap.read()
        if ret == True:

            # describe the type of font to be used.
            font = cv2.FONT_HERSHEY_SIMPLEX

            # Use putText() method for inserting text on video
            cv2.putText(frame,
                        str(frame_counter),
                        (75, 75),
                        font, 2,
                        (255, 255, 255),
                        4,
                        cv2.LINE_4)

            # Write the frame into the file 'output.avi'
            out.write(frame)
            # Increase frame counter
            frame_counter += 1

        # Break the loop
        else:
            break

    # When everything done, release the video capture and video write objects
    cap.release()
    out.release()

    # Closes all the frames
    cv2.destroyAllWindows()


if __name__ == "__main__":
    frames_count()
