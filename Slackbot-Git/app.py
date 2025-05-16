from flask import Flask
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler
import requests
import os
from dotenv import load_dotenv

load_dotenv()

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_SIGNING_SECRET = os.getenv("SLACK_SIGNING_SECRET")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO_OWNER = os.getenv("REPO_OWNER")
REPO_NAME = os.getenv("REPO_NAME")
WORKFLOW_FILE_NAME = os.getenv("WORKFLOW_FILE_NAME")

app = App(token=SLACK_BOT_TOKEN, signing_secret=SLACK_SIGNING_SECRET)
flask_app = Flask(__name__)
handler = SlackRequestHandler(app)

@app.command("/deploy")
def handle_deploy(ack, respond):
    ack()  # Acknowledge command
    respond("🚀 Starting deployment...")

    # GitHub API Call
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/actions/workflows/{WORKFLOW_FILE_NAME}/dispatches"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {
        "ref": "main"  # or your branch name
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 204:
        respond("✅ Deployment triggered!")
    else:
        respond(f"❌ Failed to deploy. GitHub response: {response.text}")

@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    return handler.handle(request)

if __name__ == "__main__":
    flask_app.run(port=3000)
