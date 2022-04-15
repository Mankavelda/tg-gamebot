import logging
import platform

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram.update import Update

from constants import BOT_API_KEY
# function to greet the user
from data.quiz import test_poll


# function to handle the /start command
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Hi\nTo start a game, select game type.")


def about(update: Update, context: CallbackContext):
    update.message.reply_text(f'This is a bot for the {platform.system()} platform')


# show available games
def games(update, context):
    update.message.reply_text("Games are not implemented yet")


# Display leaderboard
def leaderboard(update, context):
    update.message.reply_text("Leaderboard is not implemented yet")


# stop ongoing game
def stop(update, context):
    update.message.reply_text("Stopping game")
    test_poll.stop()


# schedule a game
def schedule(update, context):
    update.message.reply_text("Scheduling games")


# pause game
def pause(update, context):
    test_poll.pause()


# resume game
def resume(update, context):
    test_poll.resume()


def menu(update, context):
    buttons = [[InlineKeyboardButton(text='Start', callback_data="/start"),
                InlineKeyboardButton(text='Stop', callback_data="/stop"),
                InlineKeyboardButton(text='Pause', callback_data="/pause"),
                InlineKeyboardButton(text='Resume', callback_data="/resume")],
               [InlineKeyboardButton(text='About', callback_data="/about"),
                InlineKeyboardButton(text='Help', callback_data="/help"),
                InlineKeyboardButton(text='Games', callback_data="/games"),
                InlineKeyboardButton(text='Leaderboard', callback_data="/leaderboard")]]
    # create a keyboard
    reply_markup = InlineKeyboardMarkup(buttons)
    # send message with keyboard
    update.message.reply_text('Please select an option:', reply_markup=reply_markup)
    # handle the buttons clicked


def send_keyboard(update, context):
    keyboard_layout = [
        [
            KeyboardButton(text='Start 🏁', callback_data='/start'),
            KeyboardButton(text='Stop 🛑', callback_data='/stop'),
            KeyboardButton(text='Pause ⏸️', callback_data='/pause'),
        ],
        [
            KeyboardButton(text='Resume 🎬', callback_data='/resume'),
            KeyboardButton(text='Games 🎮', callback_data='/games'),
            KeyboardButton(text='Leaderboard 🏆', callback_data='/leaderboard'),
        ],
        [
            KeyboardButton(text='About 🆘️', callback_data='/about'),
            KeyboardButton(text='Help ℹ', callback_data='/help'),
        ]
    ]

    reply_markup = ReplyKeyboardMarkup(keyboard_layout, one_time_keyboard=True)
    update.message.reply_text('Select Menu', reply_markup=reply_markup)


# function to handle the /help command
def help_cmd(update: Update, context: CallbackContext):
    commands = {
        'about': 'Displays information about the bot',
        'help': 'displays help comands',
        'games': 'displays a list of available games',
        'leaderboard': 'displays the leaderboard',
        'stop': 'stops game',
        'start': 'Start a game',
        'schedule': 'schedules games',
        'pause': 'pauses ongoing game',
        'resume': 'resumes paused game',
    }
    reply = 'The following commands are available:\n'
    for option in commands:
        reply += f'/{option} : {commands[option]}\n\n'
    update.message.reply_text(reply)


# function to handle errors occurred in dispatcher
def error(update: Update, context: CallbackContext):
    """Log Errors caused by Updates."""
    logging.warning('Update "%s" caused error "%s"', update, context.error)


def text(update: Update, context: CallbackContext):
    text_received = update.message.text
    update.message.reply_text(f'You said: {text_received}')


def handler():
    updater = Updater(BOT_API_KEY, use_context=True)
    dispatcher = updater.dispatcher
    # create handlers for all functions above
    dispatcher.add_handler(CommandHandler('menu', menu))
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('help', help_cmd))
    dispatcher.add_handler(CommandHandler('about', about))
    dispatcher.add_handler(CommandHandler('games', games))
    dispatcher.add_handler(CommandHandler('leaderboard', leaderboard))
    dispatcher.add_handler(CommandHandler('stop', stop))
    dispatcher.add_handler(CommandHandler('schedule', schedule))
    dispatcher.add_handler(CommandHandler('pause', pause))
    dispatcher.add_handler(CommandHandler('resume', resume))
    dispatcher.add_handler(CommandHandler('send_keyboard', send_keyboard))
    dispatcher.add_handler(MessageHandler(Filters.text, text))
    dispatcher.add_error_handler(error)
    # run til infinity
    updater.start_polling()

    updater.idle()
