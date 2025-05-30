# Slack Rephrase Bot (with Gemini)

A simple Slack bot that uses Google Gemini to rephrase your messages and suggest improvements, with Accept/Reject buttons.

## Features

- Mention the bot (e.g., `@Rephrase Bot your message`) to get a rephrased suggestion.
- Accept/Reject the suggestion with interactive buttons.
- Uses Google Gemini (Generative Language API) for rephrasing.

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/slack-gemini-rephrase-bot.git
cd slack-gemini-rephrase-bot
```

### 2. Create a Google Gemini API Key

- Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
- Generate an API key.

### 3. Create a Slack App

- Go to [Slack API: Your Apps](https://api.slack.com/apps)
- Create a new app (from scratch).
- Enable **Socket Mode** and generate an App-Level Token (`xapp-...`).
- Add the following **Bot Token Scopes**:
  - `app_mentions:read`
  - `chat:write`
  - `channels:history`
- Install the app to your workspace and get the **Bot User OAuth Token** (`xoxb-...`).
- Invite the bot to your channel with `/invite @YourBotName`.

### 4. Configure Environment Variables

- Copy `.env.example` to `.env` and fill in your keys:

```bash
cp .env.example .env
# Then edit .env and fill in your tokens/keys
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the Bot

```bash
python app.py
```

## Usage

- In Slack, mention the bot with your message:
  ```
  @Rephrase Bot Can you help me with this task?
  ```
- The bot will reply with a rephrased suggestion and Accept/Reject buttons.

## Notes

- The bot cannot edit human messages due to Slack limitations. When you accept, the rephrased message is posted as a new message.
- Never commit your `.env` file or share your API keys.

## License

MIT 