from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import time
from .tasks import sendEmail
import requests
from django.core.cache import cache

def send_email(request):
    sendEmail.delay()
    return HttpResponse("<h1>Done Sending</h1>")

def test(request):
    if cache.get("test_delay_api") is None:
        response = requests.get('https://6b84698a-56f8-48db-88f3-cf1cf5a20948.mock.pstmn.io/test/delay/5')
        cache.set("test_delay_api", response.json())
    return JsonResponse(cache.get("test_delay_api"))
