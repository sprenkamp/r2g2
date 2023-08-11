import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from langchain_agent.chat import chat

TOKEN = os.environ.get('telegram_OnePieceNavigator_bot')
BOT_NAME = "@OnePieceNavigator_bot" 

async def start_command(update: Update, context: ContextTypes):
    """Send a message when the command /start is issued."""
    await update.message.reply_text('Hi! I am a chatbot that can answer your questions about refugees in Switzerland. Ask me anything!')

async def help_command(update: Update, context: ContextTypes):
    """Send a message when the command /help is issued."""
    await update.message.reply_text('Please question about aslum or migration in Switzerland. I will try my best answer it.')

async def custom_command(update: Update, context: ContextTypes):
    """Send a message when the command /custom is issued."""
    await update.message.reply_text('This is a custom command, you can add whatever text you want here.')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type = update.message.chat.type
    text = update.message.text

    if message_type == 'group':
        if BOT_NAME in text:
            new_text = text.replace(BOT_NAME, "").strip()
            response = chat(new_text)
        else:
            return
        
    else:
        response = chat(text)
    
    print("Bot:", response)
    await update.message.reply_text(response)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

if __name__ == '__main__':
    print("Starting bot...")
    app = Application.builder().token(TOKEN).build()
    
    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('custom', custom_command))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Errors
    app.add_error_handler(error)

    print("polling...")
    # Polls the telegram server for updates
    app.run_polling(poll_interval=0.5)

