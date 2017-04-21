
from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import datetime

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Steven Quick'


def get_credentials():
    credential_path = os.path.join('',
                                   'temp.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def main():
    credentials = get_credentials()
    print(type(credentials))
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    eventsResult = service.events().list(
        calendarId='primary', timeMin=now, maxResults=10, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        print(event)
        if event['status'] != "confirmed":
            continue
        for when in event.when:
            try:
                start_time = datetime.datetime.strptime(when.start_time.split(".")[0], "%Y-%m-%dT%H:%M:%S")
                end_time = datetime.datetime.strptime(when.end_time.split(".")[0], "%Y-%m-%dT%H:%M:%S")
            except ValueError:
                # ValueError happens on parsing error. Parsing errors
                # usually happen for "all day" events since they have
                # not time, but we do not care about this events.
                continue
            now = datetime.datetime.now()
            if end_time > now:
                for reminder in when.reminder:
                    # We handle only reminders with method "alert"
                    # and whose start time minus the reminder delay has passed
                    if reminder.method == "alert" \
                            and start_time - datetime.timedelta(0, 60 * int(reminder.minutes)) < now:
                        # Build the notification
                        print('%s: %s' % (event.title.text,event.content.text))


if __name__ == '__main__':
    main()
