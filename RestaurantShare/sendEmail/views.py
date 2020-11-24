import os
import environ

from django.shortcuts import render
from django.http import (
    HttpResponse,
    HttpResponseRedirect
)
from django.urls import reverse
from shareRes.models import *
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

env = environ.Env()
environ.Env.read_env()

GMAIL = env('GMAIL')
PW = env('GMAIL_PW')

# Create your views here.
def sendEmail(request):
    checked_res_list = request.POST.getlist('checks')
    inputReceiver = request.POST['inputReceiver']
    inputTitle = request.POST['inputTitle']
    inputContent = request.POST['inputContent']
    
    print(checked_res_list)

    mail_html = f"""<html><body>
    <h1>Restaurant share</h1>
    <p>{inputContent}<br>There are restaurants to share.</p>
    """
    for checked_res_id in checked_res_list:
        restaurant = Restaurant.objects.get(id = checked_res_id)
        mail_html += f"""<h2>{restaurant.restaurant_name}</h2>
        <h4>Link</h4><p>{restaurant.restaurant_link}</p><br>
        <h4>Content</h4><p>{restaurant.restaurant_content}</p><br>
        <h4>Key Word</h4><p>{restaurant.restaurant_keyword}</p><br>
        <br>
        """
    mail_html += "</body></html>"
    print(mail_html)
    server = smtplib.SMTP_SSL('smtp.gmail.com',465)
    server.login(GMAIL, PW)

    msg = MIMEMultipart('alternative')
    msg['Subject'] = inputTitle
    msg['From'] = GMAIL
    msg['To'] = inputReceiver
    mail_html = MIMEText(mail_html, 'html')
    msg.attach(mail_html)
    server.sendmail(msg['From'],msg['To'].split(','),msg.as_string())
    server.quit()
    return HttpResponseRedirect(reverse('index'))