from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

token: Final = 'token_provided_by_telegram'
bot_username: Final = 'your_bot_name'

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! Thanks for chatting with me! I am a bot:)")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("I am a bot! Please type something so that I can reply to you!!")

async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("This is a custom command")

def handle_response(text: str) -> str:
    processed: str = text.lower()
    if 'hello' in processed:
        return 'Hey there!'
    if 'how are you' in processed:
        return 'I am fine. Thanks for asking.'
    return 'I do not understand what you wrote!!'

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User({update.message.chat.id}) in {message_type}:"{text}"')

    if message_type == 'group':
        if bot_username in text:
            text = text.replace(bot_username, '').strip()
            response: str = handle_response(text)
        else:
            return
    else:
        response: str = handle_response(text)

    print('Bot:', response)
    await update.message.reply_text(response)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

if __name__ == '__main__':
    print('Starting bot...')
    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('custom', custom_command))

    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    app.add_error_handler(error)

    print('Pooling...')
    app.run_polling(poll_interval=3)
