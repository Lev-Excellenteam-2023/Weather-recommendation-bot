from typing import Final
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler

TOKEN: Final = '6594358995:AAGhbzwS5ERkx5RYEPdWkq1EYPFleiMk1IU'
BOT_USERNAME: Final = '@weather_edvider_bot'
BOT = 'weatherEdviserBot'

CHOOSING, MOISTURE, RAINING, FREE_TEXT = range(4)


# commands:
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    replay_options = ['update', 'advice']
    await update.message.reply_text(
        'Hello! I will help you to decide what to wear today'
        'If you want to inform me about the weather conditions insert: "update".'
        'If you want an advice from me about what to wear insert: "advice".',
        reply_markup=ReplyKeyboardMarkup(
            replay_options, one_time_keyboard=True, input_field_placeholder="advice or update?"
        ), )
    return CHOOSING


async def update_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Please insert temperature value: ')
    # TODO: save answer
    return MOISTURE


async def moisture(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Please insert moisture rate: ')
    # TODO: save answer
    return RAINING


async def raining(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_keyboard = [["yes", "no"]]
    await update.message.reply_text('Is reining today? ',
                                    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True,
                                                                     input_field_placeholder="Yes or No?")
                                    )
    # TODO: save answer
    return RAINING


async def free_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Please enter in free style how are feeling today: ')
    # TODO: save answer
    return ConversationHandler.END


async def advice_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # TODO: get answer from GPT
    text = update.message.text
    context.user_data["choice"] = text
    await update.message.reply_text('Here a suggestion of what to wear today')

    return CHOOSING


async def done(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_data = context.user_data
    if "choice" in user_data:
        del user_data["choice"]

    await update.message.reply_text(
        "Until next time!",
        reply_markup=ReplyKeyboardRemove(),
    )
    return ConversationHandler.END


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


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("TOKEN").build()

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start_command)],
        states={
            CHOOSING: [MessageHandler(filters.Regex("^update$"), update_command),
                       MessageHandler(filters.Regex("^advice$"), advice_command),
                       ],
            # TYPING_CHOICE: [
            #     MessageHandler(filters.TEXT & ~(filters.COMMAND | filters.Regex("^Done$")), regular_choice)
            #             ],
            # TYPING_REPLY: [
            #     MessageHandler(
            #         filters.TEXT & ~(filters.COMMAND | filters.Regex("^Done$")), received_information,)
            #
            MOISTURE: [MessageHandler(filters.TEXT & ~filters.COMMAND, moisture)],
            RAINING: [MessageHandler(filters.TEXT & ~filters.COMMAND, raining)],
            FREE_TEXT: [MessageHandler(filters.TEXT & ~filters.COMMAND, free_text)],
        },
        fallbacks=[MessageHandler(filters.Regex("^Done$"), done)],
    )

    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    print('Bot is app and running!')
    main()

# if __name__ == '__main__':
#
#     # commands:
#     app.add_handler(CommandHandler('start', start_command))
#     app.add_handler(CommandHandler('update', update_command))
#     app.add_handler(CommandHandler('advice', advice_command))
#
#     # messages:
#     app.add_handler(MessageHandler(filters.TEXT, handle_message))
#
#     # errors:
#     app.add_error_handler(error)
#
#     # check for new messages:
#     print('polling...')
#     app.run_polling(poll_interval=3)
#
