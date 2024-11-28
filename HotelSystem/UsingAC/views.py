from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("请求路径:{}" .format(request.path))
# Create your views here.
