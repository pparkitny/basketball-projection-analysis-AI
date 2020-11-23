from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import random


def index(request):
    context = {
        'test': random.random(),
    }
    return render(request, 'interface/index.html', context)


def instruction(request):
    return render(request, 'interface/instruction.html', {})


def upload(request):
    return render(request, 'interface/upload.html', {})


def analysis(request):
    return render(request, 'interface/analysis.html', {})


def authors(request):
    return render(request, 'interface/authors.html', {})
