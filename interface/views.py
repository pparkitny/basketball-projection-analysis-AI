from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.conf import settings
import random
import os
import time
import json
from .celery import app as celery
from interface.Analisys import analysis
from interface.Frames_count import frames_count
from interface.Openpose import openpose
from interface.ToManyJsons import tomanyjsons
from interface.CustomVideoDetection import customvideodetecion
from interface.Avi_to_mp4 import avi_to_mp4


def index(request):
    context = {
        'test': random.random(),
    }
    return render(request, 'interface/index.html', context)


def instruction(request):
    return render(request, 'interface/instruction.html', {})


def upload(request):
    upload_file = request.FILES['drive_file']
    ret = {}
    if upload_file:
        target_folder = os.path.join(
            settings.STATICFILES_DIRS[0], 'interface/video')
        if not os.path.exists(target_folder):
            os.mkdir(target_folder)
        rtime = str(int(time.time()))
        filename = "video.mp4"
        target = os.path.join(target_folder, filename)
        with open(target, 'wb+') as dest:
            for c in upload_file.chunks():
                dest.write(c)
        ret['file_remote_path'] = target
        basic_path = os.path.join(os.getcwd().replace("interface", "").replace("\\", "/"),
                                  'static/interface/video')
        task = video.apply_async((basic_path, ))
    else:
        return JsonResponse({"error": "Zły plik"})
    return JsonResponse({"task_id": task.id})

    # return render(request, 'interface/upload.html', {})


def authors(request):
    return render(request, 'interface/authors.html', {})


@celery.task(name='video.analysis', bind=True)
def video(self, path):
    self.update_state(state="PROGRESS", meta={"step": 1, "max": 6})
    print("Frames Count")
    frames_count(path)

    self.update_state(state="PROGRESS", meta={"step": 2, "max": 6})
    print("OPENPOSE")
    openpose(path)

    self.update_state(state="PROGRESS", meta={"step": 3, "max": 6})
    print("avi")
    avi_to_mp4(path)

    self.update_state(state="PROGRESS", meta={"step": 4, "max": 6})
    print("cvd")
    customvideodetecion(path)

    self.update_state(state="PROGRESS", meta={"step": 5, "max": 6})
    print("tommy")
    tomanyjsons(path)

    self.update_state(state="PROGRESS", meta={"step": 6, "max": 6})
    print("anal")
    analysis(path)

    return "Done"


def get_task_status(request, task_id):
    task = video.AsyncResult(task_id)

    if task.state == 'SUCCESS':
        response = {
            'state': task.state,
            'result': task.result,
        }
    elif task.state == 'PROGRESS':
        response = {
            'state': task.state,
            'step': task.info.get('step', 0),
            'max': task.info.get('max', 6),
        }
    else:
        response = {
            'state': task.state,
            'step': str(task.info),  # exception
        }

    return json.dumps(response)
