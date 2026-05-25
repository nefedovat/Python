import os
import requests
from bs4 import BeautifulSoup
import time
from gtts import gTTS, gTTSError
import random
from deep_translator import GoogleTranslator

from telegram import (
    Update,
    ReplyKeyboardMarkup,
    KeyboardButton
)

from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)

# TOKEN БОТА


TOKEN = "8861533524:AAHwjx503rj8QosLuTEIKrVP_YCj0gucM9A"


# КНОПКИ


keyboard = [
    [KeyboardButton("🎤 Озвучить текст")],
    [KeyboardButton("📜 Случайная цитата")],
    [KeyboardButton("❓ Help")]
]

reply_markup = ReplyKeyboardMarkup(
    keyboard,
    resize_keyboard=True
)


# СОСТОЯНИЯ

WAITING_TEXT = {}


# /start

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_name = update.effective_user.first_name

    text = (
        f"Привет, {user_name}!\n\n"
        "Я бот для перевода текста в речь.\n"
        "Выберите действие:"
    )

    await update.message.reply_text(
        text,
        reply_markup=reply_markup
    )


# /help

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    help_text = (
        "📌 Возможности бота:\n\n"
        "• Озвучивание текста\n"
        "• Получение случайной цитаты с сайта\n"
        "• Отправка голосового сообщения\n\n"
        "Как пользоваться:\n"
        "1. Нажмите кнопку 'Озвучить текст'\n"
        "2. Отправьте текст\n"
        "3. Бот пришлет голосовое сообщение"
    )

    await update.message.reply_text(help_text)


# ПАРСИНГ САЙТА

def get_quote():

    url = "https://quotes.toscrape.com/"

    response = requests.get(url)

    soup = BeautifulSoup(response.text, "html.parser")

    quotes = soup.find_all("span", class_="text")

    # список всех цитат
    quote_list = [quote.text for quote in quotes]

    # случайная цитата
    random_quote = random.choice(quote_list)

    # перевод на русский
    translated = GoogleTranslator(
        source='auto',
        target='ru'
    ).translate(random_quote)

    return translated


# СОЗДАНИЕ ГОЛОСА

def text_to_speech(text, filename="voice.mp3"):

    tts = gTTS(
        text=text,
        lang="ru",
        tld='com'
    )

    tts.save(filename)


# ОБРАБОТКА СООБЩЕНИЙ

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id
    text = update.message.text


    # КНОПКА ОЗВУЧИТЬ ТЕКСТ

    if text == "🎤 Озвучить текст":

        WAITING_TEXT[user_id] = True

        await update.message.reply_text(
            "Введите текст для озвучивания:"
        )

        return


    # КНОПКА HELP

    if text == "❓ Help":

        await help_command(update, context)

        return


    # КНОПКА ЦИТАТА

    if text == "📜 Случайная цитата":

        quote = get_quote()

        text_to_speech(quote)

        with open("voice.mp3", "rb") as audio:

            await update.message.reply_voice(audio)

        os.remove("voice.mp3")

        return
    
    
    # ВВОД ТЕКСТА ПОЛЬЗОВАТЕЛЕМ

    if WAITING_TEXT.get(user_id):

        text_to_speech(text)

        with open("voice.mp3", "rb") as audio:

            await update.message.reply_voice(audio)

        os.remove("voice.mp3")

        WAITING_TEXT[user_id] = False



def main():

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_message
        )
    )

    print("Бот запущен!")

    app.run_polling()


if __name__ == "__main__":
    main()
