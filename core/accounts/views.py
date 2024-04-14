from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import time
from .tasks import sendEmail
import requests

def send_email(request):
    sendEmail.delay()
    return HttpResponse("<h1>Done Sending</h1>")

def test(request):
    response = requests.get('https://6b84698a-56f8-48db-88f3-cf1cf5a20948.mock.pstmn.io/test/delay/5')
    return JsonResponse(response.json())
