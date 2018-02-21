from __future__ import print_function
import json
import logging
import datetime
import os

from urllib2 import Request, urlopen, URLError, HTTPError

print('Loading function')
SLACK_HOOK = os.environ['SLACK_HOOK']
HOOK_URL = "https://hooks.slack.com/services/" + SLACK_HOOK

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info("Event: " + str(event))

    sns = event['Records'][0]['Sns']
    message = sns['Message']
    logger.info("Message: " + str(message))

    try:
        msg = json.loads(message)
    except ValueError, e:
        icon_url = msg.get('icon_url', 'https://slack-files2.s3-us-west-2.amazonaws.com/bot_icons/2015-12-12/16554689335_48.png')
        p  = {
             "username": sns['TopicArn'].split(':')[-1],
             "text": "`Invalid Message Format`\n```" + message + "```",
             "icon_url": icon_url,
             "channel": "#test"
             }
    else:
        username = msg.get('username', sns['TopicArn'].split(':')[-1])
        text = msg.get('text', 'no text...')
        icon_url = msg.get('icon_url', 'https://slack-files2.s3-us-west-2.amazonaws.com/bot_icons/2015-12-12/16554689335_48.png')
        p = {
            "username": username,
            "text": text,
            "icon_url": icon_url,
            "channel": "#test"
            }
        if 'channel' in msg:
            p['channel'] = msg['channel']

    req = Request(HOOK_URL, json.dumps(slack_message))
    try:
        response = urlopen(req)
        response.read()
        logger.info("Message posted to %s", slack_message['channel'])
    except HTTPError as e:
        logger.error("Request failed: %d %s", e.code, e.reason)
    except URLError as e:
        logger.error("Server connection failed: %s", e.reason)
