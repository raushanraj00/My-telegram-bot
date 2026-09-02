import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import threading
from flask import Flask

# Your specific Bot Token
BOT_TOKEN = '8975252286:AAFZ3my-cRD5fSMsTuxyxX4ufpAxWQF1-9k'
bot = telebot.TeleBot(BOT_TOKEN)

# Your correct Telegram Video file_ids
TUTORIAL_VIDEOS = [
    "BAACAgUAAxkBAAMGapfONyoeKrzcpgABSHkbDn842c7aAAK3HwACq5fBVB77wBnHXV8PPQQ",
    "BAACAgUAAxkBAAMHapfONyq5A0u0i6z1kSwbMwrbauIAArgfAAKrl8FUoHlp7AP1vds9BA",
    "BAACAgUAAxkBAAMIapfONx64C-977GOs4ByrCcQJa5EAArkfAAKrl8FUx48-eH1yO5U9BA",
    "BAACAgUAAxkBAAMJapfON0if1TKdc6Q4m4DC8eOjEfIAArofAAKrl8FUk_0iovCEzuk9BA",
    "BAACAgUAAxkBAAMKapfONyMlzSJ4DwjpxfEswcAi0N0AArsfAAKrl8FUZFao2Rms7nw9BA",
    "BAACAgUAAxkBAAMLapfONwG-EPCKp3u18XHjteF24UkAArwfAAKrl8FUH2C5T54IvBU9BA",
    "BAACAgUAAxkBAAMMapfON0QwOIR5B5Mhsl4-ydjB_FMAAr4fAAKrl8FU51BfvVQ6E289BA",
    "BAACAgUAAxkBAAMNapfON2OAF7rPISIv7ntPjJLWzmIAAr0fAAKrl8FUoovbEkZfYoA9BA",
    "BAACAgUAAxkBAAMPapfONwfmPUMQru_3J71ceEVyd_4AAsAfAAKrl8FUmp1R0sRHYg09BA",
    "BAACAgUAAxkBAAMQapfON_zDkiffujgcebR6Ja-a1I4AAsEfAAKrl8FUUWkesdtcKpE9BA"
]

def delete_videos(chat_id, message_ids):
    """This runs 1 minute after the videos are sent to delete them."""
    for msg_id in message_ids:
        try:
            bot.delete_message(chat_id, msg_id)
        except Exception as e:
            print(f"Could not delete message {msg_id}: {e}")

def send_message_sequence(chat_id):
    """Handles sending videos, the warning, the card, and starts the deletion timer."""
    try:
        messages_to_delete = []
        
        for video_id in TUTORIAL_VIDEOS:
            try:
                msg = bot.send_video(
                    chat_id=chat_id,
                    video=video_id,
                    protect_content=True
                )
                messages_to_delete.append(msg.message_id)
            except Exception as e:
                print(f"Error sending a video: {e}")
        
        warning_msg = bot.send_message(
            chat_id, 
            "⚠️ <b>URGENT:</b> These videos will be permanently deleted in exactly 1 minute. Please watch them immediately!",
            parse_mode="HTML"
        )
        messages_to_delete.append(warning_msg.message_id)

        card_text = (
            "<blockquote>"
            "🔴 For getting Full access to these videos.\n\n"
            "🧾 1 Month Pass : <code> Rs. 120 </code>\n"
            "🧾 2 Month Pass : <code> Rs. 199 </code>\n"
            "🧾 3 Month Pass : <code> Rs. 259 </code>\n"
            "🎁 Category: VIP MEMEBER CHANNEL VIDEOS\n"
            "⏰ Expires After: <code> YOUR PLAN VALIDITY </code>\n"
            "</blockquote>"
        )
        
        markup = InlineKeyboardMarkup()
        dm_url = "https://t.me/raushanii00?text=I%20want%20to%20buy%20the%201%20month%20pass"
        btn = InlineKeyboardButton("MESSAGE HERE :- for exclusive offers", url=dm_url)
        markup.add(btn)
        
        bot.send_message(chat_id, card_text, reply_markup=markup, parse_mode="HTML")
        
        delete_timer = threading.Timer(60, delete_videos, args=[chat_id, messages_to_delete])
        delete_timer.start()
        
    except Exception as e:
        print(f"Failed to execute sequence for {chat_id}: {e}")

@bot.message_handler(commands=['start'])
def welcome_user(message):
    chat_id = message.chat.id
    bot.send_message(
        chat_id, 
        "Welcome! 🎓\n\nYour exclusive content is arriving now. Please watch immediately, as the videos will be deleted in 60 seconds."
    )
    threading.Thread(target=send_message_sequence, args=(chat_id,)).start()

# --- FLASK WEB SERVER FOR RENDER ---
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive and running!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
# -----------------------------------

if __name__ == "__main__":
    # Start the dummy web server in a separate thread
    threading.Thread(target=run_web).start()
    
    print("Bot is running! Waiting for /start commands...")
    bot.infinity_polling()
