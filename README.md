# sns-slack
consumes Amazon SNS json and posts to Slack

## post message to SNS

```python
payload = {
    "channel": "#test",
    "username": "bot",
    "text": "hi!"
}
self.sns.publish(
    TopicArn=SNS_ARN,
    Message=json.dumps({"default": json.dumps(self.payload)}),
    MessageStructure='json'
)
```
