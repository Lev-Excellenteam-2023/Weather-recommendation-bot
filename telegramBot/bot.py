from typing import Final
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler

CHOOSING, DATE, GET_DATE, GET_CITY, GET_FREE_TEXT = range(5)

users_data = {}


# commands:
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Handle the /start command and initialize user-specific data.

    This function is triggered when the user starts a conversation with the bot using the /start command.
    It extracts the user's unique ID from the update, sends an introductory message to the user,
    and sets up a keyboard with options to choose from. It then initializes a user-specific dictionary
    to store information related to the conversation and adds it to the global users_data dictionary.

    :param update: The incoming update from Telegram.
    :type update: telegram.Update
    :param context: The context object for the conversation.
    :type context: telegram.ext.ContextTypes.DEFAULT_TYPE
    :return: The next conversation state, which is CHOOSING.
    :rtype: int
    """
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
    users_data[user_id] = {}
    return CHOOSING


async def create_user_dict():
    """
    Create a dictionary to store user-specific information.

    This dictionary stores information reported by the user during their interaction with the bot.
    It includes:
    - The date the user reports about (format: dd.mm.yyyy).
    - The city location of the user.
    - Free text provided by the user, expressing their feelings related to the weather.

    :return: A dictionary containing user-specific information with keys "date", "city", and "free_text".
    :rtype: dict
    """
    return {
        "date": None,
        "city": None,
        "free_text": None
    }


async def choosing(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Handle the user's choice between weather update and advice request.

    This function is triggered when the user is in the CHOOSING state of the conversation.
    It sends a message to the user with options to choose from: "update" or "advice".
    The user can either inform the bot about the weather conditions or request advice about what to wear.

    :param update: The incoming update from Telegram.
    :type update: telegram.Update
    :param context: The context object for the conversation.
    :type context: telegram.ext.ContextTypes.DEFAULT_TYPE
    :return: The next conversation state, which is CHOOSING.
    :rtype: int
    """
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


async def date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Request the user to enter a date in the format: dd.mm.yyyy.

    This function is triggered when the user is in the DATE state of the conversation.
    It sends a message to the user requesting them to enter a date in the specified format.
    The user is expected to respond with a valid date format (dd.mm.yyyy).

    :param update: The incoming update from Telegram.
    :type update: telegram.Update
    :param context: The context object for the conversation.
    :type context: telegram.ext.ContextTypes.DEFAULT_TYPE
    :return: The next conversation state, which is GET_DATE.
    :rtype: int
    """
    await update.message.reply_text('Please enter date (format: dd.mm.yyyy): ')
    return GET_DATE


async def get_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Store the user's provided date and prompt for the user's location (city).

    This function is triggered when the user responds with a date in the GET_DATE state of the conversation.
    It extracts the user's unique ID from the update, saves the provided date in the user-specific dictionary,
    and then prompts the user to insert their location (city).

    :param update: The incoming update from Telegram.
    :type update: telegram.Update
    :param context: The context object for the conversation.
    :type context: telegram.ext.ContextTypes.DEFAULT_TYPE
    :return: The next conversation state, which is GET_CITY.
    :rtype: int
    """
    # Extract the user's unique ID
    user_id = update.message.from_user.id
    # Save the user's answer in the user-specific dictionary
    users_data[user_id]["date"] = update.message.text
    await update.message.reply_text('Please insert your location (city): ')
    return GET_CITY


async def get_city(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Store the user's provided city location and prompt for free text input.

    This function is triggered when the user responds with their city location in the GET_CITY state of the conversation.
    It extracts the user's unique ID from the update, saves the provided city location in the global dictionary,
    and then prompts the user to enter free text about how they are feeling today.

    :param update: The incoming update from Telegram.
    :type update: telegram.Update
    :param context: The context object for the conversation.
    :type context: telegram.ext.ContextTypes.DEFAULT_TYPE
    :return: The next conversation state, which is GET_FREE_TEXT.
    :rtype: int
    """
    # Extract the user's unique ID
    user_id = update.message.from_user.id
    # Save the user's answer in the global dictionary
    users_data[user_id]["city"] = update.message.text.lower()
    await update.message.reply_text('Please enter in free style how you are feeling today: ')
    return GET_FREE_TEXT


async def get_free_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Store the user's provided free text and prompt for the next action.

    This function is triggered when the user responds with free text in the GET_FREE_TEXT state of the conversation.
    It extracts the user's unique ID from the update, saves the provided free text in the global dictionary,
    and then prompts the user to choose whether they want to inform about the weather conditions or get advice.

    :param update: The incoming update from Telegram.
    :type update: telegram.Update
    :param context: The context object for the conversation.
    :type context: telegram.ext.ContextTypes.DEFAULT_TYPE
    :return: The next conversation state, which is CHOOSING.
    :rtype: int
    """
    replay_options = ['update', 'advice']
    # Extract the user's unique ID
    user_id = update.message.from_user.id
    # Save the user's answer in the global dictionary
    users_data[user_id]["free_text"] = update.message.text
    await update.message.reply_text(
        'If you want to inform me about the weather conditions, insert: "update". '
        'If you want advice from me about what to wear, insert: "advice".',
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[replay_options], one_time_keyboard=True,
            input_field_placeholder="advice or update?",
            resize_keyboard=True
        ))
    return CHOOSING


async def advice_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Handle the user's choice to receive advice and provide a suggestion.

    This function is triggered when the user chooses to receive advice in the CHOOSING state of the conversation.
    It temporarily stores the user's choice in the context's user_data dictionary,
    then responds to the user with a suggestion about what to wear today.

    :param update: The incoming update from Telegram.
    :type update: telegram.Update
    :param context: The context object for the conversation.
    :type context: telegram.ext.ContextTypes.DEFAULT_TYPE
    :return: The next conversation state, which is CHOOSING.
    :rtype: int
    """
    # TODO: get answer from GPT
    text = update.message.text
    context.user_data["choice"] = text
    await update.message.reply_text('Here a suggestion of what to wear today')
    return CHOOSING


async def done(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
      Handle the end of the conversation and provide a farewell message.

      This function is triggered when the user decides to end the conversation.
      It clears any temporary user data related to the conversation and sends a farewell message to the user.

      :param update: The incoming update from Telegram.
      :type update: telegram.Update
      :param context: The context object for the conversation.
      :type context: telegram.ext.ContextTypes.DEFAULT_TYPE
      :return: The conversation end state.
      :rtype: int
      """
    user_data = context.user_data
    if "choice" in user_data:
        del user_data["choice"]
    await update.message.reply_text(
        "Until next time!",
        reply_markup=ReplyKeyboardRemove(),
    )
    return ConversationHandler.END


def run(token: str) -> None:
    """
    Initialize and run the Telegram bot application.

    This function sets up the bot's conversation handler, entry points, states, and fallbacks
    for handling user interactions. It creates an instance of the Application class with the provided bot token,
    adds the conversation handler to it, and starts polling for incoming updates from Telegram.

    :param token: The API token of the Telegram bot.
    :type token: str
    :return: None
    """
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(token).build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start_command)],
        states={
            CHOOSING: [MessageHandler(filters.Regex("^update$"), date),
                       MessageHandler(filters.Regex("^advice$"), advice_command), ],
            DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, date)],
            GET_DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_date)],
            GET_CITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_city)],
            GET_FREE_TEXT: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_free_text)],
        },
        fallbacks=[MessageHandler(filters.Regex("^Done$"), done)],
    )
    application.add_handler(conv_handler)
    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)
