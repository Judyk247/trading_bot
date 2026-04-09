import os
import asyncio
from starlette.applications import Starlette
from starlette.routing import Route, Mount
from starlette.responses import JSONResponse, Response
from starlette.requests import Request
import uvicorn
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    TypeHandler,
)
from telegram.request import HTTPXRequest
import trading_bot  # your bot's logic file

# --- Bot Setup ---
# Create the Application instance from your trading_bot module
bot_app = trading_bot.setup_bot()

async def health(request):
    return Response("OK", status_code=200)

async def webhook(request: Request):
    """Handle incoming Telegram updates."""
    req_data = await request.json()
    update = Update.de_json(req_data, bot_app.bot)
    # Use asyncio.create_task to handle the update without blocking the response
    asyncio.create_task(bot_app.process_update(update))
    return Response("OK", status_code=200)

# --- Starlette App Setup ---
async def lifespan(app):
    # Set up the webhook when the app starts
    webhook_url = f"{os.environ['RENDER_EXTERNAL_URL']}/webhook"
    await bot_app.bot.set_webhook(webhook_url)
    print(f"Webhook set to {webhook_url}")
    yield
    # Clean up webhook when the app shuts down
    await bot_app.bot.delete_webhook()

app = Starlette(
    debug=False,
    routes=[
        Route("/health", health, methods=["GET"]),
        Route("/webhook", webhook, methods=["POST"]),
    ],
    lifespan=lifespan,
)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
