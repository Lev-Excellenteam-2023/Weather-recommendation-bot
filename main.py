from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN: Final = '6594358995:AAGhbzwS5ERkx5RYEPdWkq1EYPFleiMk1IU'
BOT_USERNAME: Final = '@weather_edvider_bot'


# commands:
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello! I will help you to decide what to wear today')


async def update_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Please insert date')


async def advice_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Here a suggestion of what to wear today')


def update_handler() -> str:
    pass


def advice_handler() -> str:
    pass


# responses
def handle_response(text: str) -> str:
    if 'advice' in text:
        return advice_handler()
    elif 'update' in text:
        return update_handler()
    else:
        return 'try again'


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type  # indicate if it group or private chat
    text: str = update.message.text  # incoming message

    print(f'user ({update.message.chat.id}) in {message_type}: "{text}"')

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
    else:
        response = handle_response(text)

    print('Bot:', response)
    await update.message.reply_text(response)


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')


if __name__ == '__main__':
    print('Bot is app and running!')
    app = Application.builder().token(TOKEN).build()

    # commands:
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('update', update_command))
    app.add_handler(CommandHandler('advice', advice_command))

    # messages:
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # errors:
    app.add_error_handler(error)

    # check for new messages:
    print('polling...')
    app.run_polling(poll_interval=3)

