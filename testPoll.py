#!/usr/bin/env python
# pylint: disable=C0116
# This program is dedicated to the public domain under the CC0 license.

"""
Basic example for a bot that works with polls. Only 3 people are allowed to interact with each
poll/quiz the bot generates. The preview command generates a closed poll/quiz, exactly like the
one the user sends the bot
"""
import logging

from telegram import (
    Poll,
    ParseMode,
    KeyboardButton,
    KeyboardButtonPollType,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,

)
from telegram.ext import (
    Updater,
    CommandHandler,
    PollAnswerHandler,
    PollHandler,
    MessageHandler,
    Filters,
    CallbackContext,
    PicklePersistence,
    CallbackQueryHandler,
)

#added for deployment to heroku
import os
PORT = int(os.environ.get('PORT', 443))



logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = '1724307554:AAFAAOq5nkIM-XOPgfVnPB-KlYmYz7tKiIY'


keyboard = []
date = "___"

def start(update: Update, _: CallbackContext) -> None:
    """Inform user about what this bot can do"""
    update.message.reply_text(
        'To update flight members, enter in the following format: \n\n/update\nperson1\nperson2\n.\n.\n.\n\n/cawpaw <date> to begin recording parade state for the specified date'
    )

def updateMembers(update: Update, context: CallbackContext) -> None:

	members = update.message.text.split("\n")
	del members[0]
	context.chat_data["flightMembers"] = members

	index = 0
	keyboard.clear()
	for x in context.chat_data["flightMembers"]:
		keyboard.append(
		#name
		[InlineKeyboardButton(x, callback_data = 'none')]
		)
		keyboard.append(
		#options
		[
		InlineKeyboardButton("AM", callback_data=str(index)+',0,AM \u2714'),
		],
		)
		index += 1

# 		#options
# 		# [
		# InlineKeyboardButton("AM", callback_data=str(index+',0,AM \u2714') ),
		# InlineKeyboardButton("PM", callback_data=str(index+',1,PM \u2714') ),
		# InlineKeyboardButton("IN", callback_data=str(index+',2,IN \u2714') ),
		# InlineKeyboardButton("OFF", callback_data=str(index+',3,OFF \u2714') ),
		# InlineKeyboardButton("MC", callback_data=str(index+',4,MC \u2714') ),
		# InlineKeyboardButton("CSE", callback_data=str(index+',5,CSE \u2714') ),
		# InlineKeyboardButton("OS", callback_data=str(index+',6,OS \u2714') ),
# 		# ],
# 		)

#can remove after done
def members(update: Update, context: CallbackContext) -> None:
	
	update.message.reply_text(context.chat_data["flightMembers"])


def cawpaw(update: Update, context: CallbackContext) -> None:

	date = update.message.text[8:]
	
	reply_markup = InlineKeyboardMarkup(keyboard)
	update.message.reply_text('Parade state for *__'+date+'__*', reply_markup=reply_markup, parse_mode='MarkdownV2')



def addCheck(update: Update, _: CallbackContext) -> None:

	query = update.callback_query
	query.answer()

	target = query.data.split(',')




	keyboard[int(target[0])][int(target[1])] = InlineKeyboardButton(str(target[2]),callback_data='none')

	reply_markup = InlineKeyboardMarkup(keyboard)
	#query.edit_message_text(text= 'Parade state for *__'+date+'__*', reply_markup= reply_markup)
	#query.edit_message_text(text=target)
	query.edit_message_text(text= 'Parade state for *__'+date+'__*', reply_markup=reply_markup, parse_mode='MarkdownV2')





def main() -> None:
    # Create the Updater and pass it your bot's token.
    persistence = PicklePersistence(filename="CAWPAWBOT")
    updater = Updater(TOKEN, persistence = persistence)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.text &Filters.regex("^/update\n"), updateMembers))
    dispatcher.add_handler(MessageHandler(Filters.text &Filters.regex("^/cawpaw "), cawpaw))
    #make check appear
    dispatcher.add_handler(CallbackQueryHandler(addCheck))
    
    #dispatcher.add_handler(CommandHandler('cawpaw', cawpaw))

    #can remove when done
    dispatcher.add_handler(CommandHandler('members', members))

    #added to deploy to heroku
    updater.start_webhook(listen="0.0.0.0",port=int(PORT),url_path=TOKEN,webhook_url='https://cawpawbot.herokuapp.com/'+TOKEN)

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()