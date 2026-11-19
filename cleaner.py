import asyncio
from telethon import TelegramClient, errors

# --- Telegram API Sozlamalari ---
api_id = 12345678  # O'z API ID raqamingizni yozing (masalan: 12345678)
api_hash = 'YOUR_API_HASH'  # O'z API Hash-ingizni yozing
session_name = 'my_telegram_session'

# Qidirilayotgan so'z yoki havola (link)
TARGET_LINK = 'https://github.com/'

client = TelegramClient(session_name, api_id, api_hash)


async def main():
    print('🔍 Barcha chatlarda yuborilgan xabarlaringiz skanerlanmoqda...')
    print(f'📌 Qidiruv kalit soʻzi / link: "{TARGET_LINK}"\n')
    found_count = 0
    deleted_count = 0

    await client.start()

    async for dialog in client.iter_dialogs():
        try:
            # Faqat o'zingiz yuborgan (from_user='me') va kalit so'z bor xabarlarni qidirish
            async for message in client.iter_messages(
                dialog.entity, search=TARGET_LINK, from_user='me'
            ):
                if message:
                    found_count += 1
                    print(f'--- Topilgan xabar #{found_count} ---')
                    print(f'📌 Chat/Guruh nomi : {dialog.name}')
                    print(f'🆔 Chat ID          : {dialog.id}')
                    print(f'💬 Xabar ID         : {message.id}')
                    print(f'📝 Matn             : {message.text[:50] if message.text else ""}')

                    try:
                        await client.delete_messages(dialog.entity, [message.id])
                        deleted_count += 1
                        print('🗑 Holati: Muvaffaqiyatli o\'chirildi!\n')
                    except errors.FloodWaitError as fwe:
                        print(f'⏳ Telegram cheklovi! {fwe.seconds} sekund kutilmoqda...')
                        await asyncio.sleep(fwe.seconds)
                        try:
                            await client.delete_messages(dialog.entity, [message.id])
                            deleted_count += 1
                            print('🗑 Holati: Muvaffaqiyatli o\'chirildi!\n')
                        except Exception as e:
                            print(f'⚠️ O\'chirib bo\'lmadi: {e}\n')
                    except Exception as del_err:
                        print(f'⚠️ O\'chirib bo\'lmadi: {del_err}\n')

        except errors.FloodWaitError as fwe:
            print(f'⏳ Telegram cheklovi! {fwe.seconds} sekund kutilmoqda...')
            await asyncio.sleep(fwe.seconds)
        except Exception:
            # Cheklangan yoki ruxsat yo'q chatlarni o'tkazib yuborish
            continue

    print(f'✅ Qidiruv yakunlandi!')
    print(f'📊 Topildi: {found_count} ta | O\'chirildi: {deleted_count} ta')


if __name__ == '__main__':
    with client:
        client.loop.run_until_complete(main())