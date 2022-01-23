import io
import csv
import logging
import requests
from rest_framework import status
from .models import TestLog
import json
from django.core.mail import EmailMultiAlternatives
from django.utils import timezone
from django.conf import settings
import pandas as pd
import smtplib
from email.message import EmailMessage
from pretty_html_table import build_table
import itertools

logger = logging.getLogger('__name__')


def send_test_csv_report(test_results, recipients):
    filename = "test_csv_report.csv"
    string = io.StringIO()
    csv_writer = csv.writer(
        string,
        delimiter=',',
        quotechar='"',
        quoting=csv.QUOTE_MINIMAL
    )

    csv_writer.writerow([
        'S.No',
        'Test Name',
        'Test Result',
        'Test Description'
    ])

    for result_index, result in enumerate(test_results):
        csv_writer.writerow([
            result_index + 1,
            result['test_name'],
            result['result'],
            result['test_description']
        ])

    email = EmailMultiAlternatives(
        subject=str(timezone.now().strftime("%d-%m-%Y")) + ' ' + 'Test Results' + " CSV report",
        from_email=settings.EMAIL_HOST_USER,
        to=recipients
    )

    email.attach(
        filename=filename,
        mimetype="text/csv",
        content=string.getvalue()
    )
    email.send()
    # print("mail sent", test_results)
    print("Email Sent Successfully")
    logger.info('Email Sent Successfully!!')


def send_mail(test_results):
    df = pd.DataFrame([test_results])
    df.dropna(inplace=True)
    msg = EmailMessage()

    html_table = build_table(df
                             , 'blue_light'
                             , font_size='medium'
                             , font_family='Courier New'
                             , text_align='left'
                             , width='auto'
                             , index=False
                             , even_color='black'
                             , even_bg_color='white'
                             )

    body = """
    <!DOCTYPE html>
    <html>
    <head>
    </head>

    <body>
    <h1>Category Insights API Test Logs</h1>
            {0}
    </body>

    </html>
    """.format(df.to_html(), html_table)

    msg.set_content(body, subtype='html')

    email_from = settings.EMAIL_HOST_USER
    email_to = settings.EMAIL_SEND_TO
    password = settings.EMAIL_HOST_PASSWORD

    msg['Subject'] = 'Category Insights Test Logs'
    msg['From'] = email_from
    msg['To'] = email_to

    # Send the message via our own SMTP server.
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(email_from, password)
    server.send_message(msg)
    server.quit()
    # print(df)
    print(f"Email Sent Successfully to : {email_to}")


def store_test_logs(logs):
    url = "http://127.0.0.1:8000/store_logs/"

    payload = json.dumps(logs)
    headers = {
        'Content-Type': 'application/json'
    }
    # print(payload)
    response = requests.request("POST", url, headers=headers, data=payload)

    # print(response.json())


def flatten(t):
    return [item for sublist in t for item in sublist]


def diff(list1, list2):
    c = set(list1).union(set(list2))  # or c = set(list1) | set(list2)
    d = set(list1).intersection(set(list2))  # or d = set(list1) & set(list2)
    return list(c - d)


def get_user_token(email, password):
    url = 'https://category-insights.ongil.io/api/v1/user/login/'

    payload = {
        'email': email,
        'password': password
    }

    try:
        response = requests.post(url, data=payload)
        if response.status_code == status.HTTP_200_OK:
            return response.json().get("token")
        else:
            return None
    except:
        return None


def get_data_listing(URL=None, HEADER=None, PROFILE=None):
    if PROFILE:
        profile = PROFILE
    else:
        profile = requests.get(URL, headers=HEADER).json()

    # List of clients
    CLIENTS = list(profile["profileData"]["clients"].keys())

    # List of Countries
    COUNTRIES = flatten(
        [list(profile["profileData"]["country_retailer_access"][x]["countries_access"].keys()) for x in CLIENTS])

    # List Of Retailers
    RETAILERS = []
    for cli in CLIENTS:
        country = profile["profileData"]["country_retailer_access"][cli]["retailer_access"].keys()
        for ctry in country:
            RETAILERS += profile["profileData"]["country_retailer_access"][cli]["retailer_access"][ctry]

    a = [CLIENTS, COUNTRIES, RETAILERS]
    combinations = list(itertools.product(*a))

    # print(profile)
    # print(a)
    # print(combinations)
    result = {
        "clients":CLIENTS,
        "countries":COUNTRIES,
        "retailers":RETAILERS,
        "combinations":combinations
    }

    return result
