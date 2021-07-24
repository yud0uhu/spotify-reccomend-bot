import json
import urllib.request
import os
import boto3
import analyze
from dotenv import load_dotenv

load_dotenv()

events = boto3.client("events")

def lambda_handler(event, context):
    try:
        event_json = json.loads(event["body"])
        type = event_json["events"][0]["type"]
    except TypeError:
        print("typeError occured")
        type = ""
    except KeyError:
        print("keyError occured")
        type = ""

    print("request type is [%s]." % type)
    if (type == "message"):
        reply_token = event_json["events"][0]["replyToken"]
        recv_msg = event_json["events"][0]["message"]["text"]
        track_id = analyze.getTrackId(recv_msg)
        msg = analyze.getRecommendTracks(track_id)
        linemessage_reply(reply_token, msg)
        # print("message content is [%s]." % recv_msg)

    else:
        reply_token = event_json["events"][0]["replyToken"]
        msg = "にゃーん"
        linemessage_reply(reply_token, msg)

    return {
        "statusCode": 200,
        "body": json.dumps("hello lambda.")
    }

def linemessage_reply(reply_token, msg):
    url = 'https://api.line.me/v2/bot/message/reply'
    access_token = os.getenv('YOUR_CHANNEL_ACCESS_TOKEN')
    method = "POST"
    headers = {
        "Authorization": "Bearer " + access_token,
        "Content-Type": "application/json"
    }
    payload = {
        "replyToken": reply_token,
        "messages": [
            {
                "type": "text",
                "text": msg
            }
        ]
    }
    request = urllib.request.Request(url, json.dumps(payload).encode("utf-8"), method=method, headers=headers)
    try:
        response = urllib.request.urlopen(request, timeout=10)
    except (urllib.error.HTTPError, urllib.error.URLError) as error:
        print("[warn]LINE Message data not retrieved because %s\n[warn]URL: %s" % (error, url))
        status_code = error.code
    else:
        print("[line-access-success] %s" % response.geturl())
        status_code = response.getcode()

    if (status_code != 200):
        print("[error]An error occurred while sending the LINE message.")
        print("[error]LINE Messaging API’s status-code: %d" % status_code)
        return

    return