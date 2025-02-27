import requests
import asyncio
import json
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# 🔹 Replace with your actual Telegram bot token
TOKEN = "7932275637:AAGGTUkxBtr2NLHmdgOeM5lDBtoBdDHkFrs"

# 🔹 Replace with your exact location coordinates
LATITUDE = 16.488305
LONGITUDE = 80.501011

# 🔹 Initialize bot and dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)

# 🔹 JSON file to store subscriber chat IDs
SUBSCRIBERS_FILE = "subscribers.json"


# ✅ Function to load subscribers
def load_subscribers():
    try:
        with open(SUBSCRIBERS_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


# ✅ Function to save subscribers
def save_subscribers(subscribers):
    with open(SUBSCRIBERS_FILE, "w") as f:
        json.dump(subscribers, f)


# ✅ Function to fetch Iftar & Suhoor timings from API
def get_iftar_suhoor_times():
    url = f"https://api.sunrisesunset.io/json?lat={LATITUDE}&lng={LONGITUDE}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        iftar_time = data["results"]["sunset"]
        suhoor_time = data["results"]["first_light"]

        return iftar_time, suhoor_time
    except Exception as e:
        print(f"❌ Error fetching timings: {e}")
        return None, None


# ✅ Async function to send messages to all users
async def send_iftar_suhoor_times():
    subscribers = load_subscribers()
    iftar_time, suhoor_time = get_iftar_suhoor_times()

    if iftar_time and suhoor_time:
        message = (
            "السلام عليكم! 🌙\n\n"
            "🌟 *Ramadan Timings* 🌟\n\n"
            f"🌄 *Suhoor Time:* {suhoor_time}\n"
            f"🕌 *Iftar Time:* {iftar_time}\n\n"
            "🤲 May Allah accept your fasts! رمضان مبارك! 🌙"
        )

        # Send messages to all users
        for chat_id in subscribers:
            try:
                await bot.send_message(chat_id, message, parse_mode="Markdown")
                print(f"✅ Sent to {chat_id}")
            except Exception as e:
                print(f"❌ Error sending to {chat_id}: {e}")


# ✅ Function to subscribe users via /start command
@dp.message(Command("start"))
async def start(message: types.Message):
    chat_id = message.chat.id
    subscribers = load_subscribers()

    if chat_id not in subscribers:
        subscribers.append(chat_id)
        save_subscribers(subscribers)
        await message.answer("✅ Subscribed! You will receive daily Iftar & Suhoor updates.")
    else:
        await message.answer("⚡ You are already subscribed!")


# ✅ Run the bot
async def main():
    await dp.start_polling(bot)


# ✅ Call function to send daily messages (Runs when script is executed)
def send_iftar_suhoor_times_sync():
    asyncio.run(send_iftar_suhoor_times())


# ✅ Execution starts here
if __name__ == "__main__":
    send_iftar_suhoor_times_sync()
