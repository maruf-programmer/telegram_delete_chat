import asyncio
from telethon import TelegramClient, errors

# --- Telegram API Sozlamalari ---
api_id = 12345678  # O'z API ID raqamingizni yozing (masalan: 12345678)
api_hash = 'YOUR_API_HASH'  # O'z API Hash-ingizni yozing
session_name = 'my_telegram_session'

# O'chirilishi kerak bo'lgan guruh ID si yoki username (masalan: -1001234567890 yoki 'guruh_username')
TARGET_GROUP = -1001234567890

client = TelegramClient(session_name, api_id, api_hash)


async def main():
    print('🔍 Ko‘rsatilgan guruhdagi xabarlaringiz tekshirilmoqda...')
    deleted_count = 0

    await client.start()

    try:
        # Guruh obyektini olish
        group_entity = await client.get_entity(TARGET_GROUP)
        group_title = getattr(group_entity, 'title', str(TARGET_GROUP))
        print(f'📌 Guruh topildi: {group_title}\n')

        # Guruhdagi barcha xabarlarni aylanib chiqish (from_user="me" - faqat o'zingiz yuborganlar)
        async for message in client.iter_messages(group_entity, from_user='me'):
            try:
                # Xabar turini aniqlash
                m_type = 'Matn'
                if message.photo:
                    m_type = 'Rasm 📷'
                elif message.video:
                    m_type = 'Video 🎥'
                elif message.document:
                    m_type = 'Fayl/Hujjat 📁'
                elif message.sticker:
                    m_type = 'Stiker 🧸'
                elif message.audio or message.voice:
                    m_type = 'Audio/Ovozli xabar 🎤'

                # Xabarni o'chirish
                await client.delete_messages(group_entity, [message.id])
                deleted_count += 1
                msg_preview = message.text[:30] if message.text else "(media)"
                print(f'🗑 O‘chirildi [{m_type}] | ID: {message.id} | Matn: "{msg_preview}"')

            except errors.FloodWaitError as fwe:
                print(f'⏳ Telegram cheklovi! {fwe.seconds} sekund kutilmoqda...')
                await asyncio.sleep(fwe.seconds)
                try:
                    await client.delete_messages(group_entity, [message.id])
                    deleted_count += 1
                    print(f'🗑 O‘chirildi [{m_type}] | ID: {message.id}')
                except Exception as e:
                    print(f'⚠️ Xabar ID {message.id} ni o‘chirishda xatolik: {e}')
            except Exception as del_err:
                print(f'⚠️ Xabar ID {message.id} ni o‘chirishda xatolik: {del_err}')

    except Exception as e:
        print(f'❌ Xatolik yuz berdi (Guruh topilmadi yoki huquq yo‘q): {e}')

    print(f'\n✅ Jarayon yakunlandi! Guruhdan jami {deleted_count} ta xabaringiz o‘chirildi.')


if __name__ == '__main__':
    with client:
        client.loop.run_until_complete(main())