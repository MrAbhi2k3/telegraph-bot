import os
import requests
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ChatAction, InputFile

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the Hotstar downloader function
def download_hotstar(update, context):
    # Check if a Hotstar URL is provided
    if len(context.args) == 0:
        update.message.reply_text('Please provide a Hotstar URL')
        return
    
    # Get the Hotstar URL
    url = context.args[0]
    
    # Set chat action to upload document
    context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.UPLOAD_DOCUMENT)
    
    # Download the video
    file_name = 'hotstar_video.mp4'
    r = requests.get(url, stream=True)
    with open(file_name, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    
    # Send the video to the user
    context.bot.send_document(chat_id=update.message.chat_id, document=InputFile(file_name))
    
    # Delete the video file
    os.remove(file_name)

# Define the main function to start the bot
def main():
    # Set up the Telegram bot
    token = 'YOUR_BOT_TOKEN_HERE'
    updater = Updater(token=token, use_context=True)
    dispatcher = updater.dispatcher
    
    # Define the command handlers
    dispatcher.add_handler(CommandHandler('download', download_hotstar))
    
    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
