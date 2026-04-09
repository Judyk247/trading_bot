import os
import asyncio
from starlette.applications import Starlette
from starlette.routing import Route
from starlette.responses import Response
from starlette.requests import Request
import uvicorn
from telegram import Update
import trading_bot

# Create the bot application
bot_app = trading_bot.setup_bot()

# ---------- Webhook handler ----------
async def health(request):
    return Response("OK", status_code=200)

async def webhook(request: Request):
    """Receive updates from Telegram via webhook."""
    try:
        req_data = await request.json()
        update = Update.de_json(req_data, bot_app.bot)
        # Process update without blocking the response
        asyncio.create_task(bot_app.process_update(update))
        return Response("OK", status_code=200)
    except Exception as e:
        print(f"Webhook error: {e}")
        return Response("Error", status_code=500)

# ---------- Lifespan events (startup/shutdown) ----------
async def lifespan(app):
    # Startup: set webhook
    render_url = os.environ.get("RENDER_EXTERNAL_URL")
    if not render_url:
        print("WARNING: RENDER_EXTERNAL_URL not set. Webhook may not work.")
        yield
        return
    
    webhook_url = f"{render_url}/webhook"
    await bot_app.bot.set_webhook(webhook_url)
    print(f"✅ Webhook set to {webhook_url}")
    
    yield  # The app runs here
    
    # Shutdown: delete webhook
    await bot_app.bot.delete_webhook()
    print("✅ Webhook deleted")

# ---------- Starlette app ----------
app = Starlette(
    routes=[
        Route("/health", health, methods=["GET"]),
        Route("/webhook", webhook, methods=["POST"]),
    ],
    lifespan=lifespan,
)

# ---------- Run locally (optional) ----------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
