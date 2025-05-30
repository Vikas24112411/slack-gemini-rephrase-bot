import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Initialize the Slack app
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

# Configure Gemini
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel("models/gemini-1.5-flash-latest")

print("App is starting and code is running.....")

# Listen for @rephrase mentions
def extract_message(text, bot_user_id):
    # Remove the mention and return the rest
    return text.replace(f"<@{bot_user_id}>", "").strip()

@app.event("app_mention")
def handle_app_mention_events(body, say, client, event):
    user = event["user"]
    channel = event["channel"]
    text = event["text"]
    ts = event["ts"]
    bot_user_id = body["authorizations"][0]["user_id"]

    # Extract the message after the mention
    original_message = extract_message(text, bot_user_id)
    if not original_message:
        say(text="Please provide a message to rephrase after mentioning me.", thread_ts=ts)
        return
    try:
        prompt = f"Rephrase this message to be more professional and clear while keeping the original meaning:\n\n{original_message}"
        response = model.generate_content(prompt)
        rephrased_message = response.text
        # Send the rephrased message with buttons
        say(
            blocks=[
                {"type": "section", "text": {"type": "mrkdwn", "text": f"*Rephrased suggestion:*\n{rephrased_message}"}},
                {"type": "actions", "elements": [
                    {"type": "button", "text": {"type": "plain_text", "text": "✅ Accept"}, "style": "primary", "action_id": "accept_rephrase", "value": f"{ts}|||{rephrased_message}"},
                    {"type": "button", "text": {"type": "plain_text", "text": "❌ Reject"}, "style": "danger", "action_id": "reject_rephrase", "value": ts}
                ]}
            ],
            thread_ts=ts
        )
    except Exception as e:
        say(text=f"Sorry, I encountered an error while rephrasing your message: {str(e)}", thread_ts=ts)

@app.action("accept_rephrase")
def handle_accept_rephrase(ack, body, client, action):
    ack()
    channel_id = body["channel"]["id"]
    value = action["value"]
    ts, rephrased_message = value.split("|||", 1)
    try:
        # Post the rephrased message in the thread
        client.chat_postMessage(
            channel=channel_id,
            thread_ts=ts,
            text=f"Here is your rephrased message:\n{rephrased_message}"
        )
    except Exception as e:
        client.chat_postMessage(
            channel=channel_id,
            thread_ts=ts,
            text=f"Failed to post rephrased message: {str(e)}"
        )

@app.action("reject_rephrase")
def handle_reject_rephrase(ack, body, client, action):
    ack()
    channel_id = body["channel"]["id"]
    ts = action["value"]
    client.chat_postMessage(
        channel=channel_id,
        thread_ts=ts,
        text="❌ Rephrased suggestion rejected."
    )

if __name__ == "__main__":
    handler = SocketModeHandler(app, os.environ.get("SLACK_APP_TOKEN"))
    handler.start() 