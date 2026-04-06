import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.utils.keyboard import InlineKeyboardBuilder
from config import TOKEN, ADMIN_ID
from image_gen import generate_countdown_image
from database import init_db, add_user, get_all_users_data, get_users_by_platform

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()

init_db()

# تسجيل المستخدم عند أول تفاعل
@dp.message(F.any())
async def register_user(message: types.Message):
    await add_user(message.from_user.id, platform="Android")

# إرسال عرض رسمي لمنصة معينة
async def send_official_deal(platform, game_name, discount, promo, end_hours, img_url):
    time_str = f"{end_hours:02d}:00:00"
    try:
        photo_bio = generate_countdown_image(img_url, time_str)
    except Exception as e:
        print(f"خطأ في توليد الصورة: {e}")
        return

    users = await get_users_by_platform(platform)
    count = 0
    for u_id in users:
        try:
            kb = InlineKeyboardBuilder()
            if platform=="PS":
                kb.button(text=f"🛒 فتح متجر PlayStation", url="https://store.playstation.com/")
            elif platform=="PC":
                kb.button(text=f"🛒 فتح Steam", url="https://store.steampowered.com/")
            else:
                kb.button(text=f"🛒 فتح متجر Android", url="https://play.google.com/store")

            share_text = f"وجدي! شوف عرض {game_name} بخصم {discount} على {platform}! 🔥\nكود: {promo}"
            kb.button(text="📤 شارك العرض", switch_inline_query=share_text)
            kb.adjust(1)

            caption = (
                f"🌙 **عروض رمضان - منصة {platform}** 🌙\n\n"
                f"🎮 اللعبة: **{game_name}**\n"
                f"💰 الخصم: **{discount}**\n"
                f"🏷️ الكود: `{promo}`\n\n"
                f"⚠️ **تنبيه:** العد التنازلي على الصورة. الحق قبل ما ينتهي! ⏳"
            )

            await bot.send_photo(
                chat_id=u_id,
                photo=types.BufferedInputFile(photo_bio.read(), filename="deal.png"),
                caption=caption,
                parse_mode="Markdown",
                reply_markup=kb.as_markup()
            )
            count += 1
            await asyncio.sleep(0.05)
        except Exception as e:
            print(f"خطأ في الإرسال لـ {u_id}: {e}")
    print(f"✅ تم إرسال عرض {game_name} لـ {count} مستخدم على {platform}.")

# الحملة الكبرى 48 ساعة
async def start_48h_campaign():
    print("🚀 بدء حملة الـ 48 ساعة الكبرى...")
    await send_official_deal(
        platform="Android",
        game_name="PUBG Mobile - شدات",
        discount="40%",
        promo="LY_PUBG26",
        end_hours=24,
        img_url="https://w0.peakpx.com/wallpaper/594/436/HD-wallpaper-pubg-mobile-2021-games-pubg.jpg"
    )
    await send_official_deal(
        platform="PS",
        game_name="EA SPORTS FC 26",
        discount="60%",
        promo="RAMADAN26",
        end_hours=6,
        img_url="https://media.rawg.io/media/games/fc26_header_placeholder.jpg"
    )
    await send_official_deal(
        platform="PC",
        game_name="GTA V / Elden Ring",
        discount="75%",
        promo="PC_SOHOR",
        end_hours=12,
        img_url="https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/271590/header.jpg"
    )

# أمر للأدمن لإطلاق الحملة
@dp.message(F.text == "/launch_all", F.from_user.id == ADMIN_ID)
async def admin_launch(message: types.Message):
    await message.answer("🚀 بدأت الحملة الكبرى...")
    await start_48h_campaign()

# أمر لتجربة العد التنازلي
@dp.message(F.text == "/test_timer")
async def test_timer(message: types.Message):
    await message.answer("⏳ جاري توليد صورة العد التنازلي...")
    await send_official_deal("Android", "PUBG Mobile Test", "10%", "TESTCODE", 1, "https://w0.peakpx.com/wallpaper/594/436/HD-wallpaper-pubg-mobile-2021-games-pubg.jpg")

# تشغيل البوت
async def main():
    print("🚀 Ultimate Monster Bot v3.3.9 جاهز!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
