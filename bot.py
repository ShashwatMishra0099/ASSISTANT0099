import logging
from telegram import Update, ChatAction
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the global variables
message_counter = {}

# Define the bot token and group ID
BOT_TOKEN = "6969264808:AAHcEsoYcJYfHfgCUYr-XTF4RRzTXwFrpGg"
GROUP_ID = "-1002076123692"

# Function to handle start command
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Bot is running!')

# Function to handle messages
def message_handler(update: Update, context: CallbackContext) -> None:
    message = update.message
    user_id = message.from_user.id
    chat_id = message.chat_id

  # Define filtered words
    filtered_words = ["FUCK YOU", "MADARCHOD", "BSDK"]  # Add your filtered words here
  
    # Check if message is from the group and increment message count
    if chat_id == GROUP_ID:
        if user_id not in message_counter:
            message_counter[user_id] = 1
        else:
            message_counter[user_id] += 1
        
        # Check if the message contains filtered content
        if "filter" in message.text.lower():
            # Delete the message
            message.delete()
            # Inform the user
            message.reply_text("Your message has been deleted due to filtered content.")

            # If the user has sent filtered messages more than 3 times, ban the user
            if message_counter[user_id] >= 3:
                context.bot.kick_chat_member(chat_id, user_id)
                message.reply_text("You have been banned for sending filtered messages repeatedly.")
                del message_counter[user_id]  # Reset message counter for the banned user
    else:
        pass  # Ignore messages from other chats

# Function to handle errors
def error(update: Update, context: CallbackContext) -> None:
    logger.error(f'Update {update} caused error {context.error}')
    # Check if the update object has 'from_user' attribute before accessing it
    if hasattr(update, 'from_user'):
        user_id = update.from_user.id
        logger.error(f'Error occurred for user {user_id}')

def main() -> None:
    # Create the Updater and pass the bot token
    updater = Updater(BOT_TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Register command handlers
    dispatcher.add_handler(CommandHandler("start", start))

    # Register message handler
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, message_handler))

    # Register error handler
    dispatcher.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C
    updater.idle()

if __name__ == '__main__':
    main()
