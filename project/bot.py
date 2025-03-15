import asyncio
import os
from aiogram import Bot, Dispatcher, types, Router
from aiogram.filters import Command
from aiogram.client.session.aiohttp import AiohttpSession
from config import BOT_TOKEN, ADMIN_ID, PROXY_URL
from database import init_db, add_user, add_file, get_file_by_code

# تنظیم پراکسی (اگر نیاز دارید، مقدار PROXY_URL را در config.py تنظیم کنید)
session = AiohttpSession(proxy=PROXY_URL) if PROXY_URL else None
bot = Bot(token=BOT_TOKEN, session=session)
dp = Dispatcher()
router = Router()
dp.include_router(router)

init_db()

# 📌 خواندن لیست کانال‌های اسپانسر از فایل
def get_sponsor_channels():
    if os.path.exists("sponsors.txt"):
        with open("sponsors.txt", "r", encoding="utf-8") as file:
            return [line.strip() for line in file.readlines()]
    return []

sponsors = get_sponsor_channels()

# 📌 بررسی عضویت در کانال‌های اسپانسر
async def check_user_membership(user_id):
    for channel in sponsors:
        try:
            chat_member = await bot.get_chat_member(channel, user_id)
            if chat_member.status not in ["member", "administrator", "creator"]:
                return False
        except:
            return False
    return True

# 📌 مدیریت `/start`
@router.message(Command("start"))
async def start(message: types.Message):
    user_id = message.from_user.id
    add_user(user_id)

    # بررسی عضویت در کانال‌های اسپانسر
    if sponsors:
        sponsor_text = "🔹 برای استفاده از ربات باید در کانال‌های زیر عضو شوید:\n\n"
        for ch in sponsors:
            sponsor_text += f"🔹 {ch}\n"
        sponsor_text += "\n✅ بعد از عضویت، /start را مجددا ارسال کنید."

        if not await check_user_membership(user_id):
            await message.answer(sponsor_text)
            return

    await message.answer("✅ خوش آمدید! لطفا کد فایل مورد نظر را وارد کنید.")

# 📌 دریافت کد فایل و ارسال فایل مرتبط
@router.message()
async def handle_code(message: types.Message):
    file_code = message.text.strip()
    file_id = get_file_by_code(file_code)

    if file_id:
        await bot.send_document(message.chat.id, file_id)
    else:
        await message.answer("❌ کد وارد شده معتبر نیست.")

# 📌 ذخیره فایل جدید (فقط برای ادمین)
@router.message(lambda message: message.document)
async def save_file(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return

    file_id = message.document.file_id
    file_code = str(abs(hash(file_id)))[:6]  # تولید کد ۶ رقمی برای هر فایل
    add_file(file_id, file_code)
    await message.answer(f"✅ فایل ذخیره شد!\n📌 کد فایل: `{file_code}`")

# 📌 اجرای ربات
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())