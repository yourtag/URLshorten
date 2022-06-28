from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import requests
import json
import re
from gplink_tokens import tokens
from os import environ
import aiohttp



BOT_TOKEN = environ.get('BOT_TOKEN')
def start(update, context):
    keyboard = [
       [
            InlineKeyboardButton("Sign up", url='https://tiny.one/GPlinks'),
       ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(f'Hi! {update.message.from_user.first_name},\n\nIm GPlink bot. Just send me valid link and get short link\n\nGet /help ', reply_markup=reply_markup)


def help_command(update, context):
    keyboard = [
       [
            InlineKeyboardButton("How to use me", url='https://telegra.ph/How-to-use-me-10-29'),
       ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    
    update.message.reply_text('Hello, \n\nFollow these steps:\n\n🎈 First you have to sign up at tiny.one/GPlinks\n\n🎈 After that copy that link from GPlinks TOOLS API\n\n🎈 Then use /auth and sent copied link to me\n\n🎈 Now you are done! just sent any valid link to me', reply_markup=reply_markup)
    
def auth(update, context): 
    keyboard = [
        [
            InlineKeyboardButton("Log in", url='https://tiny.one/GPlinks'), InlineKeyboardButton("Authorize me ", url='https://gplinks.in/member/tools/api'),
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Get /help before autherizing.\n\n🔑 Please login to your gplink account by pressing the button below and copy paste the API url here\n\n', reply_markup=reply_markup)
    

def echo(update, context):

    if 'https://gplinks.in/api?api=' in str(update.message.text):
        chat = str(update.message.chat_id)
        url = update.message.text.replace("https://gplinks.in/api?api=", "")
        token = re.sub("&.*", "", url)
        tokens[chat] = str(token)
        with open('gplink_tokens.py', 'w') as file:
            file.write('tokens = ' + str(tokens))
            update.message.reply_text(f'🎉 Congratulations {update.message.from_user.first_name},\n\nYou are registered with API TOKEN : {token}\n\nIf you sent me a different API url I will reassign your GPlinks API TOKEN')
    elif 'https://gplinks.in/api?api=' not in str(update.message.text) and (re.search('^http://.*', str(update.message.text)) or re.search('^https://.*', str(update.message.text))):
        try:
            chat = str(update.message.chat_id)
            gptoken = tokens[chat]
            url_convert = update.message.text
        except:
            update.message.reply_text("Your api token is missing please autherise me by /auth for using me 🤪")

        req = requests.get(f'https://gplinks.in/api?api={gptoken}&url={url_convert}')
        r = json.loads(req.content)

        if r['status'] == 'success' :
            update.message.reply_text(' Status : ' + r['status'] + ' 👍')
            update.message.reply_text(' Shortened Url : ' + `r['shortenedUrl']`)
        if r['status'] == 'error':
            update.message.reply_text(' Error : ' + r['message'] + ' 👎')
            
            
def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Please dont spam here")

unknown_handler = MessageHandler(Filters.command, unknown)          


def main():
    updater = Updater(
        BOT_TOKEN, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("auth", auth))
    dp.add_handler(unknown_handler)  

    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
