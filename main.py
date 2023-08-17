from typing import Final
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler

TOKEN: Final = None 
BOT_USERNAME: Final = '@weather_edvider_bot'
BOT = 'weatherEdviserBot'

CHOOSING, MOISTURE, RAINING, FREE_TEXT, ADVICE = range(5)

users_data = {}


# commands:
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # Extract the user's unique ID
    user_id = update.message.from_user.id

    replay_options = ['update', 'advice']
    await update.message.reply_text(
        'Hello! I will help you to decide what to wear today. '
        'If you want to inform me about the weather conditions, insert: "update". '
        'If you want advice from me about what to wear, insert: "advice".',
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[replay_options], one_time_keyboard=True,
            input_field_placeholder="advice or update?",
            resize_keyboard=True
        ),
    )
    # Create a user-specific dictionary and add it to users_data
    users_data[user_id] = await create_user_dict()

    return CHOOSING


async def create_user_dict():
    return {
        "temperature": None,
        "moisture": None,
        "raining": None,
        "free_text": None
    }


async def choosing(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    replay_options = ['update', 'advice']

    await update.message.reply_text(
        'If you want to inform me about the weather conditions, insert: "update". '
        'If you want advice from me about what to wear, insert: "advice".',
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[replay_options], one_time_keyboard=True,
            input_field_placeholder="advice or update?",
            resize_keyboard=True
        ),
    )
    return CHOOSING


async def update_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Extract the user's unique ID
    user_id = update.message.from_user.id

    await update.message.reply_text('Please insert temperature value: ')

    # Save the user's answer in the user-specific dictionary
    users_data[user_id]["temperature"] = update.message.text

    return MOISTURE


async def moisture(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Extract the user's unique ID
    user_id = update.message.from_user.id

    await update.message.reply_text('Please insert moisture rate: ')

    # Save the user's answer in the global dictionary
    users_data[user_id]["moisture"] = update.message.text

    return RAINING


async def raining(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Extract the user's unique ID
    user_id = update.message.from_user.id

    reply_keyboard = [["yes", "no"]]
    await update.message.reply_text('Is raining today? ',
                                    reply_markup=ReplyKeyboardMarkup(reply_keyboard,
                                                                     one_time_keyboard=True,
                                                                     input_field_placeholder="Yes or No?",
                                                                     resize_keyboard=True)
                                    )
    # Save the user's answer in the global dictionary
    users_data[user_id]["raining"] = update.message.text.lower() == "yes"

    return FREE_TEXT


async def free_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Extract the user's unique ID
    user_id = update.message.from_user.id

    await update.message.reply_text('Please enter in free style how you are feeling today: ')

    # Save the user's answer in the global dictionary
    users_data[user_id]["free_text"] = update.message.text

    return CHOOSING


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


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start_command)],
        states={
            CHOOSING: [MessageHandler(filters.Regex("^update$"), update_command),
                       MessageHandler(filters.Regex("^advice$"), advice_command),
                       ],
            MOISTURE: [MessageHandler(filters.TEXT & ~filters.COMMAND, moisture)],
            RAINING: [MessageHandler(filters.TEXT & ~filters.COMMAND, raining)],
            FREE_TEXT: [MessageHandler(filters.TEXT & ~filters.COMMAND, free_text)],
            ADVICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, choosing)],
        },
        fallbacks=[MessageHandler(filters.Regex("^Done$"), done)],
    )

    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    print('Bot is app and running!')
    main()

# def update_handler() -> str:
#     pass
#
#
# def advice_handler() -> str:
#     pass
#
#
# # responses
# def handle_response(text: str) -> str:
#     if 'advice' in text:
#         return advice_handler()
#     elif 'update' in text:
#         return update_handler()
#     else:
#         return 'try again'
#
#
# async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     message_type: str = update.message.chat.type  # indicate if it group or private chat
#     text: str = update.message.text  # incoming message
#
#     print(f'user ({update.message.chat.id}) in {message_type}: "{text}"')
#
#     if message_type == 'group':
#         if BOT_USERNAME in text:
#             new_text: str = text.replace(BOT_USERNAME, '').strip()
#             response: str = handle_response(new_text)
#     else:
#         response = handle_response(text)
#
#     print('Bot:', response)
#     await update.message.reply_text(response)
#
#
# async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     print(f'Update {update} caused error {context.error}')


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
