from imageai.Detection.Custom import CustomObjectDetection, CustomDetectionUtils
import cv2
import os
import json


class CustomVideoObjectDetection:

    """
    This is the object detection class for videos and camera live stream inputs using your custom trained detection models. It provides support for your custom YOLOv3 models.
    """

    def __init__(self):
        self.__model_type = ""
        self.__model_path = ""
        self.__model_labels = []
        self.__model_anchors = []
        self.__detection_config_json_path = ""
        self.__model_loaded = False
        self.__input_size = 416
        self.__object_threshold = 0.4
        self.__nms_threshold = 0.4
        self.__detector = []
        self.__detection_utils = CustomDetectionUtils(labels=[])

    def setModelTypeAsYOLOv3(self):
        """
        'setModelTypeAsYOLOv3' is used to set your custom detection model as YOLOv3
        :return:
        """

        self.__model_type = "yolov3"

    def setModelPath(self, detection_model_path):
        """
        'setModelPath' is used to specify the filepath to your custom detection model
        :param detection_model_path:
        :return:
        """
        self.__model_path = detection_model_path

    def setJsonPath(self, configuration_json):
        """
        'setJsonPath' is used to set the filepath to the configuration JSON file for your custom detection model
        :param configuration_json:
        :return:
        """
        self.__detection_config_json_path = configuration_json

    def loadModel(self):
        """
        'loadModel' is used to load the model into the CustomVideoObjectDetection class
        :return:
        """

        if (self.__model_loaded == False):
            if(self.__model_type == "yolov3"):
                detector = CustomObjectDetection()
                detector.setModelTypeAsYOLOv3()
                detector.setModelPath(self.__model_path)
                detector.setJsonPath(self.__detection_config_json_path)
                detector.loadModel()

                self.__detector = detector
                self.__model_loaded = True

    def detectObjectsFromVideo(self, input_file_path="", camera_input=None, output_file_path="", frames_per_second=20,
                               frame_detection_interval=1, minimum_percentage_probability=50, log_progress=False,
                               display_percentage_probability=True, display_object_name=True, save_detected_video=True,
                               per_frame_function=None, per_second_function=None, per_minute_function=None,
                               video_complete_function=None, return_detected_frame=False, detection_timeout=None):
        """
        'detectObjectsFromVideo()' function is used to detect objects observable in the given video path or a camera input:
            * input_file_path , which is the file path to the input video. It is required only if 'camera_input' is not set
            * camera_input , allows you to parse in camera input for live video detections
            * output_file_path , which is the path to the output video. It is required only if 'save_detected_video' is not set to False
            * frames_per_second , which is the number of frames to be used in the output video
            * frame_detection_interval (optional, 1 by default)  , which is the intervals of frames that will be detected.
            * minimum_percentage_probability (optional, 50 by default) , option to set the minimum percentage probability for nominating a detected object for output.
            * log_progress (optional) , which states if the progress of the frame processed is to be logged to console
            * display_percentage_probability (optional), can be used to hide or show probability scores on the detected video frames
            * display_object_name (optional), can be used to show or hide object names on the detected video frames
            * save_save_detected_video (optional, True by default), can be set to or not to save the detected video
            * per_frame_function (optional), this parameter allows you to parse in a function you will want to execute after each frame of the video is detected. If this parameter is set to a function, after every video  frame is detected, the function will be executed with the following values parsed into it:
                -- position number of the frame
                -- an array of dictinaries, with each dictinary corresponding to each object detected. Each dictionary contains 'name', 'percentage_probability' and 'box_points'
                -- a dictionary with with keys being the name of each unique objects and value are the number of instances of the object present
                -- If return_detected_frame is set to True, the numpy array of the detected frame will be parsed as the fourth value into the function
            * per_second_function (optional), this parameter allows you to parse in a function you will want to execute after each second of the video is detected. If this parameter is set to a function, after every second of a video is detected, the function will be executed with the following values parsed into it:
                -- position number of the second
                -- an array of dictionaries whose keys are position number of each frame present in the last second , and the value for each key is the array for each frame that contains the dictionaries for each object detected in the frame
                -- an array of dictionaries, with each dictionary corresponding to each frame in the past second, and the keys of each dictionary are the name of the number of unique objects detected in each frame, and the key values are the number of instances of the objects found in the frame
                -- a dictionary with its keys being the name of each unique object detected throughout the past second, and the key values are the average number of instances of the object found in all the frames contained in the past second
                -- If return_detected_frame is set to True, the numpy array of the detected frame will be parsed
                                                                    as the fifth value into the function
            * per_minute_function (optional), this parameter allows you to parse in a function you will want to execute after each minute of the video is detected. If this parameter is set to a function, after every minute of a video is detected, the function will be executed with the following values parsed into it:
                -- position number of the minute
                -- an array of dictionaries whose keys are position number of each frame present in the last minute , and the value for each key is the array for each frame that contains the dictionaries for each object detected in the frame
                -- an array of dictionaries, with each dictionary corresponding to each frame in the past minute, and the keys of each dictionary are the name of the number of unique objects detected in each frame, and the key values are the number of instances of the objects found in the frame
                -- a dictionary with its keys being the name of each unique object detected throughout the past minute, and the key values are the average number of instances of the object found in all the frames contained in the past minute
                -- If return_detected_frame is set to True, the numpy array of the detected frame will be parsed as the fifth value into the function
            * video_complete_function (optional), this parameter allows you to parse in a function you will want to execute after all of the video frames have been detected. If this parameter is set to a function, after all of frames of a video is detected, the function will be executed with the following values parsed into it:
                -- an array of dictionaries whose keys are position number of each frame present in the entire video , and the value for each key is the array for each frame that contains the dictionaries for each object detected in the frame
                -- an array of dictionaries, with each dictionary corresponding to each frame in the entire video, and the keys of each dictionary are the name of the number of unique objects detected in each frame, and the key values are the number of instances of the objects found in the frame
                -- a dictionary with its keys being the name of each unique object detected throughout the entire video, and the key values are the average number of instances of the object found in all the frames contained in the entire video
            * return_detected_frame (optionally, False by default), option to obtain the return the last detected video frame into the per_per_frame_function, per_per_second_function or per_per_minute_function
            * detection_timeout (optionally, None by default), option to state the number of seconds of a video that should be detected after which the detection function stop processing the video
        :param input_file_path:
        :param camera_input:
        :param output_file_path:
        :param frames_per_second:
        :param frame_detection_interval:
        :param minimum_percentage_probability:
        :param log_progress:
        :param display_percentage_probability:
        :param display_object_name:
        :param save_detected_video:
        :param per_frame_function:
        :param per_second_function:
        :param per_minute_function:
        :param video_complete_function:
        :param return_detected_frame:
        :param detection_timeout:
        :return output_video_filepath:
        :return counting:
        :return output_objects_array:
        :return output_objects_count:
        :return detected_copy:
        :return this_second_output_object_array:
        :return this_second_counting_array:
        :return this_second_counting:
        :return this_minute_output_object_array:
        :return this_minute_counting_array:
        :return this_minute_counting:
        :return this_video_output_object_array:
        :return this_video_counting_array:
        :return this_video_counting:
        """

        output_frames_dict = {}
        output_frames_count_dict = {}

        input_video = cv2.VideoCapture(input_file_path)
        if (camera_input != None):
            input_video = camera_input

        output_video_filepath = output_file_path + '.mp4'

        frame_width = int(input_video.get(3))
        frame_height = int(input_video.get(4))
        output_video = cv2.VideoWriter(output_video_filepath, cv2.VideoWriter_fourcc(*'H265'),
                                       frames_per_second,
                                       (frame_width, frame_height))

        counting = 0
        predicted_numbers = None
        scores = None
        detections = None

        detection_timeout_count = 0
        video_frames_count = 0

        if(self.__model_type == "yolov3"):

            while (input_video.isOpened()):
                ret, frame = input_video.read()

                if (ret == True):

                    detected_frame = frame.copy()

                    video_frames_count += 1
                    if (detection_timeout != None):
                        if ((video_frames_count % frames_per_second) == 0):
                            detection_timeout_count += 1

                        if (detection_timeout_count >= detection_timeout):
                            break

                    output_objects_array = []

                    counting += 1

                    if (log_progress == True):
                        print("Processing Frame : ", str(counting))

                    check_frame_interval = counting % frame_detection_interval

                    if (counting == 1 or check_frame_interval == 0):
                        try:
                            detected_frame, output_objects_array = self.__detector.detectObjectsFromImage(
                                input_image=frame, input_type="array", output_type="array",
                                minimum_percentage_probability=minimum_percentage_probability,
                                display_percentage_probability=display_percentage_probability,
                                display_object_name=display_object_name)
                        except:
                            None

                    output_frames_dict[counting] = output_objects_array

                    output_objects_count = {}
                    for eachItem in output_objects_array:
                        eachItemName = eachItem["name"]
                        try:
                            output_objects_count[eachItemName] = output_objects_count[eachItemName] + 1
                        except:
                            output_objects_count[eachItemName] = 1

                    output_frames_count_dict[counting] = output_objects_count

                    if (save_detected_video == True):
                        output_video.write(detected_frame)

                    if (counting == 1 or check_frame_interval == 0):
                        if (per_frame_function != None):
                            if (return_detected_frame == True):
                                per_frame_function(counting, output_objects_array, output_objects_count,
                                                   detected_frame)
                            elif (return_detected_frame == False):
                                per_frame_function(
                                    counting, output_objects_array, output_objects_count)

                    if (per_second_function != None):
                        if (counting != 1 and (counting % frames_per_second) == 0):

                            this_second_output_object_array = []
                            this_second_counting_array = []
                            this_second_counting = {}

                            for aa in range(counting):
                                if (aa >= (counting - frames_per_second)):
                                    this_second_output_object_array.append(
                                        output_frames_dict[aa + 1])
                                    this_second_counting_array.append(
                                        output_frames_count_dict[aa + 1])

                            for eachCountingDict in this_second_counting_array:
                                for eachItem in eachCountingDict:
                                    try:
                                        this_second_counting[eachItem] = this_second_counting[eachItem] + \
                                            eachCountingDict[eachItem]
                                    except:
                                        this_second_counting[eachItem] = eachCountingDict[eachItem]

                            for eachCountingItem in this_second_counting:
                                this_second_counting[eachCountingItem] = int(
                                    this_second_counting[eachCountingItem] / frames_per_second)

                            if (return_detected_frame == True):
                                per_second_function(int(counting / frames_per_second),
                                                    this_second_output_object_array, this_second_counting_array,
                                                    this_second_counting, detected_frame)

                            elif (return_detected_frame == False):
                                per_second_function(int(counting / frames_per_second),
                                                    this_second_output_object_array, this_second_counting_array,
                                                    this_second_counting)

                    if (per_minute_function != None):

                        if (counting != 1 and (counting % (frames_per_second * 60)) == 0):

                            this_minute_output_object_array = []
                            this_minute_counting_array = []
                            this_minute_counting = {}

                            for aa in range(counting):
                                if (aa >= (counting - (frames_per_second * 60))):
                                    this_minute_output_object_array.append(
                                        output_frames_dict[aa + 1])
                                    this_minute_counting_array.append(
                                        output_frames_count_dict[aa + 1])

                            for eachCountingDict in this_minute_counting_array:
                                for eachItem in eachCountingDict:
                                    try:
                                        this_minute_counting[eachItem] = this_minute_counting[eachItem] + \
                                            eachCountingDict[eachItem]
                                    except:
                                        this_minute_counting[eachItem] = eachCountingDict[eachItem]

                            for eachCountingItem in this_minute_counting:
                                this_minute_counting[eachCountingItem] = int(
                                    this_minute_counting[eachCountingItem] / (frames_per_second * 60))

                            if (return_detected_frame == True):
                                per_minute_function(int(counting / (frames_per_second * 60)),
                                                    this_minute_output_object_array, this_minute_counting_array,
                                                    this_minute_counting, detected_frame)

                            elif (return_detected_frame == False):
                                per_minute_function(int(counting / (frames_per_second * 60)),
                                                    this_minute_output_object_array, this_minute_counting_array,
                                                    this_minute_counting)

                else:
                    break

            if (video_complete_function != None):

                this_video_output_object_array = []
                this_video_counting_array = []
                this_video_counting = {}

                for aa in range(counting):
                    this_video_output_object_array.append(
                        output_frames_dict[aa + 1])
                    this_video_counting_array.append(
                        output_frames_count_dict[aa + 1])

                for eachCountingDict in this_video_counting_array:
                    for eachItem in eachCountingDict:
                        try:
                            this_video_counting[eachItem] = this_video_counting[eachItem] + \
                                eachCountingDict[eachItem]
                        except:
                            this_video_counting[eachItem] = eachCountingDict[eachItem]

                for eachCountingItem in this_video_counting:
                    this_video_counting[eachCountingItem] = this_video_counting[
                        eachCountingItem] / counting

                video_complete_function(this_video_output_object_array, this_video_counting_array,
                                        this_video_counting)

            input_video.release()
            output_video.release()

            if (save_detected_video == True):
                return output_video_filepath, output_frames_dict


def customvideodetecion(path=None):

    if path:
        video_path = os.path.join(path, "video-frames.mp4")
        output_path_yolo_local = os.path.join(path, "video-yolo")
        json_in = os.path.join(path, "yolo.json")
        model_path = os.path.join(path.replace(
            "static/interface/video", ""), "weights/detection.h5")
        json_path = os.path.join(path.replace(
            "static/interface/video", ""), "weights/detection.json")
    else:
        video_path = '..\\static\\interface\\video\\video-frames.mp4'
        output_path_yolo_local = '..\\static\\interface\\video\\video-yolo'
        json_in = '..\\static\\interface\\video\\yolo.json'
        model_path = 'weights\\detection.h5'
        json_path = 'weights\\detection.json'

    execution_path = os.getcwd()

    detector = CustomVideoObjectDetection()
    detector.setModelTypeAsYOLOv3()
    detector.setModelPath(os.path.join(
        execution_path, model_path))
    detector.setJsonPath(json_path)
    detector.loadModel()

    video, output_frames = detector.detectObjectsFromVideo(
        input_file_path=video_path,
        output_file_path=output_path_yolo_local,
        frames_per_second=30,
        log_progress=True)

    with open(json_in, "w+") as f:
        json.dump(list(output_frames.values()), f, indent=4)


if __name__ == "__main__":
    customvideodetecion()
