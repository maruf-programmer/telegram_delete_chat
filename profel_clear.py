import asyncio
from telethon import TelegramClient
import time

# --- SOZLAMALAR ---
# my.telegram.org dan olgan malumotlaringizni yozing
api_id =  # o'zingnikini yoz
api_hash = '  '  # o'zingnikini yoz

# Qayerni tozalamoqchisiz?
# 1. O'z profilingiz (Saved Messages) uchun: 'me' deb qoldiring
# 2. Kanal uchun: '@kanalingiz_nomi' yoki kanal linkini yozing
CHAT_TO_CLEAN = 'me' 

client = TelegramClient('telegram_cleaner_session', api_id, api_hash)

async def main():
    await client.start()
    print(f"Ulandi! {CHAT_TO_CLEAN} dagi musiqalar qidirilmoqda...")

    to_delete = []
    count = 0

    async for message in client.iter_messages(CHAT_TO_CLEAN):
        # Faqat musiqa / audio / mp3 bo'lsa
        is_music = False
        if message.audio: # to'g'ridan to'g'ri musiqa
            is_music = True
        elif message.document:
            mime = message.document.mime_type
            # mp3, ogg, flac va hokazo
            if mime and ('audio' in mime or 'mpeg' in mime or 'ogg' in mime):
                is_music = True
        elif message.voice: # ovozli xabarlar ham kerak bo'lsa, qoldiring
            # is_music = True
            pass

        if is_music:
            to_delete.append(message.id)
            count += 1
            print(f"Topildi: {count} - ID {message.id}")

            # Telegram 100 tadan ko'p o'chirsa ban berishi mumkin, shuning uchun 100 tada tozalaymiz
            if len(to_delete) >= 100:
                await client.delete_messages(CHAT_TO_CLEAN, to_delete)
                print(f">>> {len(to_delete)} ta musiqa o'chirildi!")
                to_delete = []
                time.sleep(2) # 2 sekund kutish - FloodWait yemaslik uchun

    # Qolganlari
    if to_delete:
        await client.delete_messages(CHAT_TO_CLEAN, to_delete)
        print(f">>> Yana {len(to_delete)} ta musiqa o'chirildi!")

    print(f"TAYYOR! Jami {count} ta musiqa o'chirildi.")

with client:
    client.loop.run_until_complete(main())
