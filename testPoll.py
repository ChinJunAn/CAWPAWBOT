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


def start(update: Update, _: CallbackContext) -> None:
    """Inform user about what this bot can do"""
    update.message.reply_text(
        'To update flight members, enter in the following format: \n\n/update\nperson1\nperson2\n.\n.\n.\n\n/cawpaw <date> to begin recording parade state for the specified date'
    )

def updateMembers(update: Update, context: CallbackContext) -> None:

	members = update.message.text.split("\n")
	del members[0]
	context.chat_data["flightMembers"] = members

#can remove after done
def members(update: Update, context: CallbackContext) -> None:
	
	update.message.reply_text(context.chat_data["flightMembers"])

# #keyboard = []
# date = "___"
# def cawpaw(update: Update, context: CallbackContext) -> None:

# 	date = update.message.text[8:]
# 	index = 0
# 	for x in context.chat_data["flightMembers"]:
# 		keyboard.append(
# 		#name
# 		[InlineKeyboardButton(x, callback_data = 1)]
# 		)
# 		keyboard.append(
# 		InlineKeyboardButton("test option", callback_data=1),
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
# 		index += 1

# 	reply_markup = InlineKeyboardMarkup(keyboard)
# 	update.message.reply_text('Parade state for *__'+date+'__*', reply_markup=reply_markup, parse_mode='MarkdownV2')


		# InlineKeyboardButton("AM", callback_data='1'),
		# InlineKeyboardButton("PM", callback_data='1'),
		# InlineKeyboardButton("IN", callback_data='1'),
		# InlineKeyboardButton("OFF", callback_data='1'),
		# InlineKeyboardButton("LVE", callback_data='1'),
		# InlineKeyboardButton("MC", callback_data='1'),
		# InlineKeyboardButton("CSE", callback_data='1'),
		# InlineKeyboardButton("OS", callback_data='1'),

keyboard = []
date = "___"

def cawpaw(update: Update, context: CallbackContext) -> None:

	date = update.message.text[8:]
	index = 0
	for x in context.chat_data["flightMembers"]:
		keyboard.append(
		#name
		[InlineKeyboardButton(x, callback_data = 'none')]
		)
		keyboard.append(
		#options
		[
		InlineKeyboardButton('test option',callback_date = index+",0,test option \u2714")
		],
		)
		index += 1

	reply_markup = InlineKeyboardMarkup(keyboard)
	update.message.reply_text('Parade state for *__'+date+'__*', reply_markup=reply_markup, parse_mode='MarkdownV2')

#def button(update: Update, _: CallbackContext) -> None:

	query = update.callback_query
	query.answer()

	target = query.data.split(',')

	keyboard[target[0]][target[1]] = InlineKeyboardButton(target[2],callback_data=None)

	reply_markup = InlineKeyboardMarkup(keyboard)
	query.edit_message_text(text= 'Parade state for *__'+date+'__*', reply_markup= reply_markup)

def main() -> None:
    # Create the Updater and pass it your bot's token.
    persistence = PicklePersistence(filename="CAWPAWBOT")
    updater = Updater(TOKEN, persistence = persistence)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.text &Filters.regex("^/update\n"), updateMembers))
    dispatcher.add_handler(MessageHandler(Filters.text &Filters.regex("^/cawpaw "), cawpaw))
    #for button
    #dispatcher.add_handler(CallbackQueryHandler(button))
    
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