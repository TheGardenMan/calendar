from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.http import JsonResponse

from datetime import date, datetime, timedelta
import os.path
import json


from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def get_week_start_end_dates():
    today = date.today()

    start = today - timedelta(days=today.weekday())
    end = start + timedelta(days=6)
    start_time_of_a_day = datetime.min.time()
    end_time_of_a_day = datetime.max.time()
    start_of_current_week = datetime.combine(start, start_time_of_a_day)
    end_of_current_week = datetime.combine(start, end_time_of_a_day)

def get_week_range(date):
    # weekdays mon-0, sun-6
    start_date = date + timedelta(-date.weekday(), weeks=-1) # we go back one week ( weeks = -1).now we are at same day but last week.and then we go back the gap between "last week ,same day" and "last, week monday". "-0" is fine with python. It's taken as 0
    end_date = date + timedelta(-date.weekday() - 1) #we need go back to the end of previous week. so we go back weekday+1 days ( Since weekdays start from 0, we need to go back one more day) 
    return start_date, end_date
# get_week_range(date.today())

def get_start_end_time_of_nth_month(n):
    today = date.today()
    for i in range(n):
        today = today.replace(day=1) - timedelta(days=1)
    start_time_of_a_day = datetime.min.time()
    end_time_of_a_day = datetime.max.time()
    # date to datetime
    start_date = datetime.combine(today.replace(day=1), start_time_of_a_day)
    end_date = datetime.combine(today, end_time_of_a_day)
    return timezone.make_aware(start_date).isoformat(), timezone.make_aware(end_date).isoformat()

def get_metrics():
    # return HttpResponse(status=200)
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    module_dir = os.path.dirname(__file__)
    creds_path = os.path.join(module_dir, 'credentials.json')
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                creds_path, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    try:
        service = build('calendar', 'v3', credentials=creds)
        metrics = {}
        meeting_times = []
        for i in range(0,3):
            month_data = {}
            total_meeting_time = 0
            total_interview_time = 0
            meeting_count = 0
            # print('for month ', i)
            start_time, end_time = get_start_end_time_of_nth_month(i+1)
            events_result = service.events().list(calendarId='primary', timeMin=start_time,timeMax = end_time,
                                                singleEvents=True,
                                                orderBy='startTime').execute()
            events = events_result.get('items', [])
            
            if not events:
                print('No upcoming events found.')
            else:
                meeting_count = len(events)
                for event in events:
                    import arrow
                    meeting_seconds = (arrow.get(event['end'].get('dateTime')).datetime - arrow.get(event['start'].get('dateTime')).datetime).total_seconds()
                    total_meeting_time = total_meeting_time + meeting_seconds
                    event_summary = (event.get('summary') or '').lower()
                    if 'interview' in event_summary or 'screening' in event_summary:
                        total_interview_time = total_interview_time + meeting_seconds
            month_data['total_meeting_time'] = str(timedelta(seconds=total_meeting_time))
            month_data['total_interview_time'] = str(timedelta(seconds=total_interview_time))
            month_data['meetings_count'] = meeting_count
            month_data['month_name'] = arrow.get(event['end'].get('dateTime')).datetime.strftime("%B")
            print(month_data['month_name'],meeting_count)
            metrics[i] = month_data
            meeting_times.insert(i,meeting_count)
        metrics['highest_meetings_month'] = metrics[meeting_times.index(max(meeting_times))]['month_name']
        metrics['lowest_meetings_month'] = metrics[meeting_times.index(min(meeting_times))]['month_name']
        return metrics
    except HttpError as error:
        print('An error occurred: %s' % error)
        return {"error":"Error occurred in server"}


def refresh_metrics():
    metrics = get_metrics()
    with open("metrics.json", "w") as outfile:
        json.dump(metrics, outfile)

@csrf_exempt
def api(request):
    try:
        f = open('metrics.json')
        data = json.load(f)
        f.close()
        return JsonResponse(data)
    except FileNotFoundError as e:
        refresh_metrics()
        f = open('metrics.json')
        data = json.load(f)
        f.close()
        return JsonResponse(data)        

@csrf_exempt
def main(request):
    # push notifications requests only indicate that a resource has changed and have a url for that resource in the header. These requests don't contain any body
    refresh_metrics()
    return HttpResponse(status=200)