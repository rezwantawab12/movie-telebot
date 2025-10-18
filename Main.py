import telebot
import subprocess
import os
from api import api  # توکن ربات خودت

bot = telebot.TeleBot(api)

# ذخیره وضعیت کاربران
user_state = {}  # chat_id : {"stage": "waiting_name" / "waiting_movie_choice" / "waiting_quality", "movies": [], "qualities": [], "selected_movie": ""}
movie = {}

# /start
@bot.message_handler(commands=["start"])
def hello(message):
    bot.send_message(
        message.chat.id,
        "👋 Hello!\nUse /search to search for movies."
    )

# /search
@bot.message_handler(commands=["search"])
def search_start(message):
    chat_id = message.chat.id
    user_state[chat_id] = {"stage": "waiting_name"}
    bot.send_message(chat_id, "🎬 Enter your movie name:")

# دریافت پیام کاربر
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id
    text = message.text.strip()

    # مرحله وارد کردن نام فیلم
    if chat_id in user_state and user_state[chat_id]["stage"] == "waiting_name":
        file_name = text
        subprocess.call(["bash", "search.sh", file_name, str(chat_id)])

        if not os.path.exists(str(chat_id)):
            bot.send_message(chat_id, "❌ Error: search failed.")
            del user_state[chat_id]
            return

        with open(str(chat_id), "r") as f:
            movies = [line.strip() for line in f.readlines()[2:] if line.strip()]

        if not movies:
            bot.send_message(chat_id, "❌ No movies found.")
            del user_state[chat_id]
            return

        bot.send_message(chat_id, "📃 Select your movie:")
        for i, movie in enumerate(movies, start=1):
            bot.send_message(chat_id, f"{i}. {movie}")

        user_state[chat_id]["stage"] = "waiting_movie_choice"
        user_state[chat_id]["movies"] = movies
        return

    # مرحله انتخاب فیلم
    if chat_id in user_state and user_state[chat_id]["stage"] == "waiting_movie_choice":
        if not text.isdigit():
            bot.send_message(chat_id, "❌ Please send a number corresponding to the movie.")
            return

        choice = int(text)
        movies = user_state[chat_id]["movies"]

        if not (1 <= choice <= len(movies)):
            bot.send_message(chat_id, "❌ Invalid selection.")
            return

        selected_movie = movies[choice - 1]
        user_state[chat_id]["selected_movie"] = selected_movie
        chat_idd = "g" + str(chat_id)

        subprocess.call(["bash", "graphic.sh", selected_movie, chat_idd])

        if not os.path.exists(chat_idd):
            bot.send_message(chat_id, "❌ Error: could not fetch video qualities.")
            del user_state[chat_id]
            return

        with open(chat_idd, "r") as f:
            qualities = [line.strip() for line in f.readlines() if line.strip()]

        if not qualities:
            bot.send_message(chat_id, "❌ No qualities found.")
            del user_state[chat_id]
            return

        bot.send_message(chat_id, "🎥 Select video quality:")
        for i, q in enumerate(qualities, start=1):
            bot.send_message(chat_id, f"{i}. {q}")

        user_state[chat_id]["stage"] = "waiting_quality"
        user_state[chat_id]["qualities"] = qualities
        return

    # مرحله انتخاب کیفیت
    if chat_id in user_state and user_state[chat_id]["stage"] == "waiting_quality":
        if not text.isdigit():
            bot.send_message(chat_id, "❌ Please send a number corresponding to the quality.")
            return

        choice = int(text)
        qualities = user_state[chat_id]["qualities"]
        sel = user_state[chat_id]["selected_movie"]

        if not (1 <= choice <= len(qualities)):
            bot.send_message(chat_id, "❌ Invalid selection.")
            return
        id = "n" + str(chat_id)
        idd = "k" + str(chat_id)
        selected_quality = qualities[choice - 1]
        bot.message_handler(chat_id , "file is downloading")
        send = subprocess.call(["bash" , "download.sh" , f"{sel}" , f"{chat_id}" , f"{id}" , f"{selected_quality}" , f"{idd}"])


        # مرحله تمام شد، پاک کردن وضعیت کاربر
        del user_state[chat_id]
        return

    # اگر پیام غیرمنتظره بود
    bot.send_message(chat_id, "❌ Please start with /search to find a movie.")

# اجرای بات
bot.polling()