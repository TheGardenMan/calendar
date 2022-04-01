#  read the below to understand what params to pass
# https://developers.google.com/calendar/api/v3/reference/events/list
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

        #  read the below to understand what params to pass
        # https://developers.google.com/calendar/api/v3/reference/events/list
        # https://developers.google.com/calendar/api/v3/reference/events/get

For Google APIs, request bodyshould be "data" not "json"


https://developers.google.com/calendar/api/guides/push - Just send your URL and "channel id" (UUID gen by you and passed to Google while creating a "channel" ) to this endpoint and you'll get what you want