import os
import threading

import telebot
from flask import Flask, jsonify

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("BOT_TOKEN is not configured")

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)


@app.get("/")
def home():
    return """
<!doctype html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>NOVA-HOST</title>
</head>
<body>
<h1>NOVA-HOST</h1>
<p>خدمة الاستضافة تعمل.</p>
</body>
</html>
"""


@app.get("/health")
def health():
    return jsonify(status="ok", service="NOVA-HOST")


@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(message, "NOVA-HOST يعمل.")


@bot.message_handler(commands=["ping"])
def ping(message):
    bot.reply_to(message, "PONG")


def run_web():
    port = int(os.getenv("PORT", "8080"))
    app.run(
        host="0.0.0.0",
        port=port,
        threaded=True,
        use_reloader=False,
    )


if __name__ == "__main__":
    web_thread = threading.Thread(target=run_web, daemon=True)
    web_thread.start()

    print("NOVA-HOST host bridge is running...")
    bot.infinity_polling(skip_pending=True)
