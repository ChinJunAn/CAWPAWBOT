#!/usr/bin/env python
# pylint: disable=C0116
# This program is dedicated to the public domain under the CC0 license.

"""
Basic example for a bot that works with polls. Only 3 people are allowed to interact with each
poll/quiz the bot generates. The preview command generates a closed poll/quiz, exactly like the
one the user sends the bot
"""
import logging
import telegram
import telegram.ext

# from telegram import (
#     Poll,
#     ParseMode,
#     KeyboardButton,
#     KeyboardButtonPollType,
#     ReplyKeyboardMarkup,
#     ReplyKeyboardRemove,
#     Update,
# )
# from telegram.ext import (
#     Updater,
#     CommandHandler,
#     PollAnswerHandler,
#     PollHandler,
#     MessageHandler,
#     Filters,
#     CallbackContext,
# )

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
        '/add <callsign> to add flight members \n/remove to remove flight members \n/members show flight members \n/cawpaw <date> to begin recording parade state for specified date'
    )

def add(update: Update, context: CallbackContext) -> None:
	
	def getCallsign(userinput):
		return userinput[4:]

	callsign = update.message.text
	update.message.reply_text("\""+getCallsign(callsign)+"\" was added")

	context.chat_data[callsign] = callsign

def members (update: Update, context: CallbackContext) -> None:
	
	update.message.reply_text(context.chat_data)



# def poll(update: Update, context: CallbackContext) -> None:
#     """Sends a predefined poll"""
#     questions = ["Good", "Really good", "Fantastic", "Great"]
#     message = context.bot.send_poll(
#         update.effective_chat.id,
#         "How are you?",
#         questions,
#         is_anonymous=False,
#         allows_multiple_answers=True,
#     )
#     # Save some info about the poll the bot_data for later use in receive_poll_answer
#     payload = {
#         message.poll.id: {
#             "questions": questions,
#             "message_id": message.message_id,
#             "chat_id": update.effective_chat.id,
#             "answers": 0,
#         }
#     }
#     context.bot_data.update(payload)


# def receive_poll_answer(update: Update, context: CallbackContext) -> None:
#     """Summarize a users poll vote"""
#     answer = update.poll_answer
#     poll_id = answer.poll_id
#     try:
#         questions = context.bot_data[poll_id]["questions"]
#     # this means this poll answer update is from an old poll, we can't do our answering then
#     except KeyError:
#         return
#     selected_options = answer.option_ids
#     answer_string = ""
#     for question_id in selected_options:
#         if question_id != selected_options[-1]:
#             answer_string += questions[question_id] + " and "
#         else:
#             answer_string += questions[question_id]
#     context.bot.send_message(
#         context.bot_data[poll_id]["chat_id"],
#         f"{update.effective_user.mention_html()} feels {answer_string}!",
#         parse_mode=ParseMode.HTML,
#     )
#     context.bot_data[poll_id]["answers"] += 1
#     # Close poll after three participants voted
#     if context.bot_data[poll_id]["answers"] == 3:
#         context.bot.stop_poll(
#             context.bot_data[poll_id]["chat_id"], context.bot_data[poll_id]["message_id"]
#         )


# def quiz(update: Update, context: CallbackContext) -> None:
#     """Send a predefined poll"""
#     questions = ["1", "2", "4", "20"]
#     message = update.effective_message.reply_poll(
#         "How many eggs do you need for a cake?", questions, type=Poll.QUIZ, correct_option_id=2
#     )
#     # Save some info about the poll the bot_data for later use in receive_quiz_answer
#     payload = {
#         message.poll.id: {"chat_id": update.effective_chat.id, "message_id": message.message_id}
#     }
#     context.bot_data.update(payload)


# def receive_quiz_answer(update: Update, context: CallbackContext) -> None:
#     """Close quiz after three participants took it"""
#     # the bot can receive closed poll updates we don't care about
#     if update.poll.is_closed:
#         return
#     if update.poll.total_voter_count == 3:
#         try:
#             quiz_data = context.bot_data[update.poll.id]
#         # this means this poll answer update is from an old poll, we can't stop it then
#         except KeyError:
#             return
#         context.bot.stop_poll(quiz_data["chat_id"], quiz_data["message_id"])


# def preview(update: Update, _: CallbackContext) -> None:
#     """Ask user to create a poll and display a preview of it"""
#     # using this without a type lets the user chooses what he wants (quiz or poll)
#     button = [[KeyboardButton("Press me!", request_poll=KeyboardButtonPollType())]]
#     message = "Press the button to let the bot generate a preview for your poll"
#     # using one_time_keyboard to hide the keyboard
#     update.effective_message.reply_text(
#         message, reply_markup=ReplyKeyboardMarkup(button, one_time_keyboard=True)
#     )


# def receive_poll(update: Update, _: CallbackContext) -> None:
#     """On receiving polls, reply to it by a closed poll copying the received poll"""
#     actual_poll = update.effective_message.poll
#     # Only need to set the question and options, since all other parameters don't matter for
#     # a closed poll
#     update.effective_message.reply_poll(
#         question=actual_poll.question,
#         options=[o.text for o in actual_poll.options],
#         # with is_closed true, the poll/quiz is immediately closed
#         is_closed=True,
#         reply_markup=ReplyKeyboardRemove(),
#     )


def help_handler(update: Update, _: CallbackContext) -> None:
    """Display a help message"""
    update.message.reply_text('/initialise to add update flight members \n /cawpaw <date> to begin recording parade state for specified date')


def main() -> None:
    # Create the Updater and pass it your bot's token.
    persistence = PicklePersistence(filename="CAWPAWBOT")
    updater = Updater(TOKEN, persistence = persistence)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.text,add))
    # dispatcher.add_handler(CommandHandler('add', add))


    # dispatcher.add_handler(PollAnswerHandler(receive_poll_answer))
    # dispatcher.add_handler(CommandHandler('quiz', quiz))
    # dispatcher.add_handler(PollHandler(receive_quiz_answer))
    # dispatcher.add_handler(CommandHandler('preview', preview))
    # dispatcher.add_handler(MessageHandler(Filters.poll, receive_poll))
    # dispatcher.add_handler(CommandHandler('help', help_handler))

    # Start the Bot
    #updater.start_polling()

    #added to deploy to heroku
    updater.start_webhook(listen="0.0.0.0",port=int(PORT),url_path=TOKEN,webhook_url='https://cawpawbot.herokuapp.com/'+TOKEN)
    #updater.bot.setWebhook(webhook_url='https://cawpawbot.herokuapp.com/'+TOKEN)

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()