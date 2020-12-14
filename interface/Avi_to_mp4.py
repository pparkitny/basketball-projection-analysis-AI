import cv2
import os


def avi_to_mp4(path=None):

    if path:
        video_input = os.path.join(path, "video-openpose.avi")
        video_out_name = os.path.join(path, "video-openpose-converted.mp4")
    else:
        video_input = '..\\static\\interface\\video\\video-openpose.avi'
        video_out_name = '..\\static\\interface\\video\\video-openpose-converted.mp4'


    cap = cv2.VideoCapture(video_input)

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

            # Write the frame into the file 'output.avi'
            out.write(frame)

        # Break the loop
        else:
            break

    # When everything done, release the video capture and video write objects
    cap.release()
    out.release()

    # Closes all the frames
    cv2.destroyAllWindows()
    os.remove(video_input)


if __name__ == "__main__":
    avi_to_mp4()
