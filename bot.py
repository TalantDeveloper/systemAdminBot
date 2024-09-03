import logging

TOKEN = "1881218661:AAFcllZI3Kf4ivPKlpmUFtC6Zfo88_GbBGc"

from telegram import ForceReply, Update, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler
from telegram import InlineKeyboardButton
import requests

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""

    await update.message.reply_text("Assalomu alaykum. MIT texnik bo'limga xush kelibsiz.\n"
                                    "Ism, Familyangiz va bo'limingizni yozivoring Iltimos:",
                                    )


base_url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    await query.answer()

    parameters = {'chat_id': '-4583772583', 'text': query.data}
    response = requests.get(base_url, data=parameters)
    await query.edit_message_text(text=f"Sizdagi muammo: {query.data}. Xodimlar siz bilan bog'lanishadi.")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    user_id = update.message.from_user.id
    full_name = update.message.from_user.full_name

    await context.bot.send_message(556841744, text=f"Hi {full_name}! yordam so'radi")

    await update.message.reply_text(f"Qanday yordam kerak {full_name} - {user_id}")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""

    user_data = {
        'user_id': update.message.from_user.id,
        'user_full_name_department': update.message.text,
    }

    parameters = {'chat_id': '-4583772583',
                  'text': f"User ID: {user_data['user_id']}\nF.I.O.- {user_data['user_full_name_department']}"}
    response = requests.get(base_url, data=parameters)

    keyboard = [

        [InlineKeyboardButton("IP telephone problem", callback_data="IP telephone problem")],
        [InlineKeyboardButton("Internet problem", callback_data="Internet problem")],
        [InlineKeyboardButton("Printer problem", callback_data="Printer problem")],
        [InlineKeyboardButton("PC problem", callback_data="PC problem")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Sizda qanday muammo bor:", reply_markup=reply_markup)


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))

    application.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    application.add_handler(CallbackQueryHandler(button))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
