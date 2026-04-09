import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# --- Your existing code for start, menu, button_handler remains exactly the same ---

# ---------- Simple menu handler ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Welcome to Trading Bot!\n\n"
        "Use /menu to see available commands."
    )

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("💰 Set Amount", callback_data="amount")],
        [InlineKeyboardButton("⏱ Set Timeframe", callback_data="timeframe")],
        [InlineKeyboardButton("📈 Scan Assets", callback_data="scan")],
        [InlineKeyboardButton("▶️ Start Trading", callback_data="start")],
        [InlineKeyboardButton("⏹ Stop Trading", callback_data="stop")],
    ]
    await update.message.reply_text(
        "⚙️ Main Menu",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "amount":
        await query.edit_message_text("Send amount, e.g.: 1000 NGN")
    elif data == "timeframe":
        await query.edit_message_text("Timeframe options: 1m, 2m, 5m")
    elif data == "scan":
        await query.edit_message_text("🔍 Scanning market... (demo)")
    elif data == "start":
        await query.edit_message_text("▶️ Trading started (demo mode)")
    elif data == "stop":
        await query.edit_message_text("⏹ Trading stopped")
    else:
        await query.edit_message_text("Unknown command")

# --- Bot setup function (called from app.py) ---
def setup_bot():
    TOKEN = os.environ.get("TELEGRAM_TOKEN")
    if not TOKEN:
        raise ValueError("No TELEGRAM_TOKEN environment variable set")

    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("menu", menu))
    app.add_handler(CallbackQueryHandler(button_handler))
    return app

# If run directly (for local testing)
if __name__ == "__main__":
    app = setup_bot()
    print("Bot is running locally... Press Ctrl+C to stop.")
    app.run_polling()
