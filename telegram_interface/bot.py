import os
from datetime import datetime

from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler

from DataBase.database_interface import FirebaseHandler
from WeatherData.weather_interface import get_date_weather
from ai_interface.feeling_classifier import FeelingClassifier
from ai_interface.recommendation_generator import RecommendationGenerator

CHOOSING, DATE, GET_DATE, GET_CITY, GET_FREE_TEXT = range(5)

users_data = {}
is_update = True


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
    users_data[user_id] = {}
    return CHOOSING


async def create_user_dict():
    return {
        "date": None,
        "city": None,
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


async def date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global is_update
    is_update = update.message.text == "update"
    await update.message.reply_text('Please enter date (format: y-m-d): ')
    return GET_DATE


async def get_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Extract the user's unique ID
    user_id = update.message.from_user.id
    # Save the user's answer in the user-specific dictionary
    users_data[user_id]["date"] = update.message.text
    await update.message.reply_text('Please insert your location (city): ')
    return GET_CITY


async def get_city(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global is_update
    # Extract the user's unique ID
    user_id = update.message.from_user.id
    # Save the user's answer in the global dictionary
    users_data[user_id]["city"] = update.message.text.lower()
    if is_update:
        await update.message.reply_text('Please enter in free style how you are feeling today: ')
        return GET_FREE_TEXT
    else:
        await advice_command(update,context)
        is_update = True
        return CHOOSING


async def get_free_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    fdb = FirebaseHandler()
    openai_fc = FeelingClassifier(os.getenv('OPENAI_API_KEY'))
    replay_options = ['update', 'advice']
    # Extract the user's unique ID
    user_id = update.message.from_user.id
    # Save the user's answer in the global dictionary
    users_data[user_id]["free_text"] = openai_fc.get_answer(update.message.text)
    await update.message.reply_text(
        'If you want to inform me about the weather conditions, insert: "update". '
        'If you want advice from me about what to wear, insert: "advice".',
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[replay_options], one_time_keyboard=True,
            input_field_placeholder="advice or update?",
            resize_keyboard=True
        ))
    user_ind = get_date_weather(users_data[user_id]['date'], users_data[user_id]['city'])
    user_ind['feeling'] = users_data[user_id]["free_text"]
    fdb.add_user_indication(str(user_id), users_data[user_id]["date"], user_ind)
    return CHOOSING


async def advice_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global is_update
    is_update = False
    user_id = update.message.from_user.id
    fdb = FirebaseHandler()
    open_ai_rec = RecommendationGenerator(os.getenv('OPENAI_API_KEY'))
    text = update.message.text
    context.user_data["choice"] = text
    await update.message.reply_text('Here a suggestion of what to wear today')
    await update.message.reply_text(open_ai_rec.get_answer(f"history: {fdb.get_user(str(update.message.from_user.id))}."
                                                           , f"Forecast: {get_date_weather(users_data[user_id]['date'], users_data[user_id]['city'])}"))
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


def run(token: str) -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(token).build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start_command)],
        states={
            CHOOSING: [MessageHandler(filters.Regex("^update$"), date),
                       MessageHandler(filters.Regex("^advice$"), date), ],
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
