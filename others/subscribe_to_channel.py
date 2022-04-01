import requests
import json
url = "https://www.googleapis.com/calendar/v3/calendars/jagatheeshthangaraj@gmail.com/events/watch"
access_token = "ya29.A0ARrdaM_ZJ78rMkT1oJg61S1M1nQNK0OI8SXPLTeRFtoh36-P2Wry3x8W0OvHRdGo7-x7WdD5f-4Vw6-BvRnFpj7wOZI697PfVu6c4MpwsYKuOmFiWeNuIeVsSbahwZmir8obdzY6albufVOyE945p-Q3ruCRbQ"
# access_token = "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"
data={"id": "test_channel",
        "type":"web_hook",
        "address":"https://925f-157-51-94-239.ngrok.io/gcal/"}
result = requests.post(url,
      headers={'Content-Type':'application/json',
               'Authorization': 'Bearer {}'.format(access_token)}, data=json.dumps(data))