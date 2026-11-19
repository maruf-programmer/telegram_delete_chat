import asyncio
from telethon import TelegramClient, errors

# --- Telegram API Sozlamalari ---
api_id = 12345678  # O'z API ID raqamingizni yozing (masalan: 12345678)
api_hash = 'YOUR_API_HASH'  # O'z API Hash-ingizni yozing
session_name = 'my_telegram_session'

client = TelegramClient(session_name, api_id, api_hash)


async def main():
    print('🔍 Barcha chatlardan siz yuborgan lokatsiyalar qidirilmoqda...')
    found_count = 0
    deleted_count = 0

    await client.start()

    # Barcha chatlar va kanallarni tekshirish
    async for dialog in client.iter_dialogs():
        try:
            # Faqat o'zingiz yuborgan xabarlar orasidan lokatsiyalarni qidirish
            async for message in client.iter_messages(dialog.entity, from_user='me'):
                # Xabar lokatsiya (geo) yoki joylashuv (venue) ekanligini tekshirish
                if message.geo or message.venue:
                    found_count += 1
                    print(f'--- Topilgan lokatsiya #{found_count} ---')
                    print(f'📌 Chat/Guruh nomi : {dialog.name}')
                    print(f'💬 Xabar ID        : {message.id}')

                    try:
                        await client.delete_messages(dialog.entity, [message.id])
                        deleted_count += 1
                        print('🗑 Holati: Lokatsiya muvaffaqiyatli o‘chirildi!\n')
                    except errors.FloodWaitError as fwe:
                        print(f'⏳ Telegram cheklovi! {fwe.seconds} sekund kutilmoqda...')
                        await asyncio.sleep(fwe.seconds)
                        try:
                            await client.delete_messages(dialog.entity, [message.id])
                            deleted_count += 1
                            print('🗑 Holati: Lokatsiya muvaffaqiyatli o‘chirildi!\n')
                        except Exception as e:
                            print(f'⚠️ O‘chirib bo‘lmadi: {e}\n')
                    except Exception as del_err:
                        print(f'⚠️ O‘chirib bo‘lmadi: {del_err}\n')

        except errors.FloodWaitError as fwe:
            print(f'⏳ Telegram cheklovi! {fwe.seconds} sekund kutilmoqda...')
            await asyncio.sleep(fwe.seconds)
        except Exception:
            continue

    print(
        f'✅ Jarayon yakunlandi! Topildi: {found_count} ta | O‘chirildi: {deleted_count} ta lokatsiya.'
    )


if __name__ == '__main__':
    with client:
        client.loop.run_until_complete(main())