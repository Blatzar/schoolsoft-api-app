#!/usr/bin/env python3
import requests
import json
import time
import datetime
import os

def write_json(file, data):
    with open(file,'w') as f:
        json.dump(data, f, indent=4)


"""
Checks the responses from the server and throws errors accordingly.
"""
def check_response(response):
    if response.status_code == 401:
        raise ValueError("Old or incorrect token used, ensure you've got a working one with get_updated_token()")
    if response.status_code == 404:
        raise ValueError("Incorrect parameters passed to the API")
    if response.status_code == 500:
        # This might because no deviceid
        raise ValueError("Unknown error with request")


"""
App key is the first step in authentication, it gets a key used to generate the token.
"""
def get_app_key(name, password, write_file_path='app_key.json'):
    # It actually sends the password plaintext to the server.
    app_key_json = requests.post("https://sms.schoolsoft.se/nacka/rest/app/login",
        data={'identification':name,
            'verification':password,
            'logintype':'4',
            'usertype':'1',
            }).json()

    if write_file_path:
        write_json(write_file_path, app_key_json)

    return app_key_json

"""
Gets the token used for authentication from the app_key.
Note that the token has an expiry date.
This function shouldn't be used directly. 
Use get_updated_token() to prevent spamming the servers for new tokens.
"""
def get_token(app_key_json={}, app_key_path=None, write_file_path='token.json'):
    key = None
    if 'appKey' in app_key_json and not app_key_path:
        key = app_key_json['appKey']
    elif app_key_path:
        with open(app_key_path) as app_key_json:
            key = json.load(app_key_json).get('appKey')

    # If no key is obtained from app_key_path or app_key_json raises an error.
    if not key:
        raise InputError('No valid value for app_key. An app key is needed to generate the token')

    token_response = requests.get('https://sms.schoolsoft.se/nacka/rest/app/token', headers={
        "appversion": "2.3.2",
        "appos": "android",
        "appkey": key,
        "deviceid":""
      })

    check_response(token_response)
    token_json = token_response.json()

    if write_file_path:
        write_json(write_file_path, token_json)

    return token_json


"""
Gets the lessons based on token and schoolname.
School is found in the url like this:
"https://sms13.schoolsoft.se/   school   /jsp/student/right_student_startpage.jsp"
"""
def get_lessons(token, school, write_file_path='lessons.json'):
    # student/28, 28 is same the orgId from get_app_key. Investigate.
    lesson_response = requests.get(f'https://sms.schoolsoft.se/{school}/api/lessons/student/28', headers= {
    "appversion": "2.3.2",
    "appos": "android",
    "token": token})

    check_response(lesson_response)
    lesson_json = lesson_response.json()

    if write_file_path:
        write_json(write_file_path, lesson_json)

    return lesson_json


"""
Gets the calendar for the student based on unix timestamps (1597246367)
The API uses milliseconds based timestamps, but the function takes second based ones and converts them.
By default with no parameters it will use the current time as start and a month from that as end.
"""
def get_calendar(token, school, unix_time_start=None, unix_time_end=None, write_file_path='calendar.json'):
    unix_time_start = time.time()*1000 if not unix_time_start else unix_time_start*1000
    unix_time_end = (time.time() + 2592000)*1000 if not unix_time_end else unix_time_end*1000
    # No decimals can get passed to the api without errors.
    unix_time_start = round(unix_time_start)
    unix_time_end = round(unix_time_end)

    calendar_response = requests.get(f'https://sms.schoolsoft.se/{school}/api/notices/student/28/{unix_time_start}/{unix_time_end}/calendar,schoolcalendar,privatecalendar', 
        headers={
        "appversion": "2.3.2",
        "appos": "android",
        "token": token})

    check_response(calendar_response)
    calendar_json = calendar_response.json()

    if write_file_path:
        write_json(write_file_path, calendar_json)

    return calendar_json


"""
Gets the lunch :)
"""
def get_lunch(token, school, write_file_path='lunch.json'):
    lunch_response = requests.get(f'https://sms.schoolsoft.se/{school}/api/lunchmenus/student/28', 
        headers={
        "appversion": "2.3.2",
        "appos": "android",
        "token": token})

    check_response(lunch_response)
    lunch_json = lunch_response.json()

    if write_file_path:
        write_json(write_file_path, lunch_json)

    return lunch_json


"""
Basically get_token(), but looks at the previous tokens expiry date and determines if a new token should
be issued or use the old one. This function should be used when making applications.
"""
def get_updated_token(app_key_json={}, app_key_path=None, token_json={}, token_path=None, write_file_path='token.json'):
    if 'expiryDate' not in token_json and token_path:
        if os.path.isfile(token_path):
            with open(token_path) as f:
                token_json = json.load(f)

    if not token_json:
        # If no token passed to the function it generates a new one.
        token_json = get_token(app_key_json, app_key_path, write_file_path)
        return token_json

    # Cuts off milliseconds.
    expiry_date = token_json['expiryDate'][:-4]
    # Assumes the date is formatted like "2020-08-12 17:48:22".
    unix_time = time.mktime(datetime.datetime.strptime(expiry_date, "%Y-%m-%d %H:%M:%S").timetuple())
    # Extra 5 minutes for good measure
    # The token seems to last 3 hours.
    if time.time() + 5*60 > unix_time:
        token_json = get_token(app_key_json, app_key_path, write_file_path)
    else:
        write_json(write_file_path, token_json)
    return token_json
