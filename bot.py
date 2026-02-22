"""
Crypto Meme Telegram Bot
========================
Generates random crypto memes and sends them to users.

Setup:
    pip install python-telegram-bot pillow requests

Usage:
    1. Get a bot token from @BotFather on Telegram
    2. Set your BOT_TOKEN in config.py or as an environment variable
    3. Run: python bot.py

Commands:
    /start   - Welcome message
    /meme    - Generate a random crypto meme
    /help    - Show help
    /coin    - Get a random coin-themed meme
    /moon    - Motivational moon meme
    /wen     - "Wen lambo" style meme
"""

import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)
from meme_generator import MemeGenerator

# ── Logging ──────────────────────────────────────────────────────────────────
logging.basicConfig(
    format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# ── Config ────────────────────────────────────────────────────────────────────
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8507056571:AAEbgrM4y9b12UzzR2dK0hinpjoSV4BAhaQ")

generator = MemeGenerator()


# ── Helpers ───────────────────────────────────────────────────────────────────
def meme_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🎲 Another one!", callback_data="random"),
            InlineKeyboardButton("🌙 Moon meme",   callback_data="moon"),
        ],
        [
            InlineKeyboardButton("🪙 Coin meme",   callback_data="coin"),
            InlineKeyboardButton("🏎️ Wen lambo",   callback_data="wen"),
        ],
    ])


async def send_meme(update: Update, context: ContextTypes.DEFAULT_TYPE, category: str = "random"):
    """Generate and send a meme image."""
    chat_id = update.effective_chat.id

    await context.bot.send_chat_action(chat_id=chat_id, action="upload_photo")

    img_bytes = generator.generate(category)

    caption = generator.get_caption(category)

    if update.callback_query:
        await update.callback_query.answer()
        await context.bot.send_photo(
            chat_id=chat_id,
            photo=img_bytes,
            caption=caption,
            reply_markup=meme_keyboard(),
        )
    else:
        await update.message.reply_photo(
            photo=img_bytes,
            caption=caption,
            reply_markup=meme_keyboard(),
        )


# ── Handlers ──────────────────────────────────────────────────────────────────
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "👋 *Welcome to the Crypto Meme Bot!*\n\n"
        "I generate dank crypto memes on demand. 🚀\n\n"
        "Commands:\n"
        "• /meme — Random meme\n"
        "• /moon — Moon-themed meme\n"
        "• /coin — Coin-themed meme\n"
        "• /wen  — Wen lambo meme\n"
        "• /help — Show this message\n\n"
        "_WAGMI 🙌_"
    )
    await update.message.reply_text(text, parse_mode="Markdown")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start(update, context)


async def meme_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_meme(update, context, "random")


async def moon_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_meme(update, context, "moon")


async def coin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_meme(update, context, "coin")


async def wen_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_meme(update, context, "wen")


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    category = update.callback_query.data
    await send_meme(update, context, category)


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        raise ValueError("❌ Set your BOT_TOKEN env variable before running!")

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help",  help_command))
    app.add_handler(CommandHandler("meme",  meme_command))
    app.add_handler(CommandHandler("moon",  moon_command))
    app.add_handler(CommandHandler("coin",  coin_command))
    app.add_handler(CommandHandler("wen",   wen_command))
    app.add_handler(CallbackQueryHandler(button_callback))

    logger.info("🤖 Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
