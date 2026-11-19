# 🧹 Telegram Account Auto Cleaner

Telegram hisobingizdagi shaxsiy xabarlar, havola (link)lar, lokatsiyalar va ma'lum guruhlardagi yuborilgan barcha fayllarni avtomatik qidirish va o'chirish uchun mo'ljallangan Python skriptlar to'plami.

Har bir skript **to'liq mustaqil** (standalone) ishlaydi va har bir faylning tepasida `api_id` hamda `api_hash` sozlamalari mavjud.

---

## 📌 Xususiyatlari

- 🔍 **Havola/Matn bo'yicha tozalash (`cleaner.py`)**: Barcha chatlar va kanallar ichidan faqat o'zingiz yuborgan va ma'lum bir kalit so'z/link (masalan `github.com`) tutgan xabarlarni topib o'chiradi.
- 📍 **Lokatsiyalarni tozalash (`geopoint.py`)**: Barcha chatlardan ilgari yuborgan aniq va jonli (live) lokatsiyalaringizni avtomatik tozalaydi.
- 👥 **Guruhni tozalash (`grup.py`)**: Aniq bir ko'rsatilgan guruhdagi barcha xabarlaringizni (matn, rasm, video, stiker, ovozli xabar) bittalab me'yorda o'chiradi.
- 🛡 **Xavfsizlik**: `.session` fayllari `.gitignore` orqali himoyalangan (ombor yopiq bo'lsa ham tasodifiy yuklanishning oldi olinadi).
- ⏳ **Rate Limit / FloodWait**: Telegram cheklovlariga tushib qolganda skript avtomatik kutiladi va to'xtab qolmaydi.

---

## 🔑 Telegram API (api_id va api_hash) olish yo'riqnomasi

Skriptlar ishlashi uchun Telegram'dan shaxsiy API kalitlarini olishingiz kerak:

1. Brauzerda [my.telegram.org](https://my.telegram.org) sahifasiga kiring.
2. Telegram akkauntingizga bog'langan **telefon raqamingizni** xalqaro formatda kiriting (masalan: `+998901234567`).
3. Telegram ilovangizga kelgan **tasdiqlash kodini** sahifaga yozib kiring.
4. Ochilgan menyudan **"API development tools"** bo'limiga o'ting.
5. Yangi ilova yaratish formasini to'ldiring:
   - **App title**: Istalgan nom (masalan: `MyCleanerApp`)
   - **Short name**: Qisqa nom (masalan: `mycleaner`)
6. **"Create application"** tugmasini bosing.
7. Hosil bo'lgan ekranda **`App api_id`** (raqam) va **`App api_hash`** (uzun harf-raqamli kod) paydo bo'ladi. Ularni nusxalab oling.

---

## 📁 Fayllar strukturasi va ularning vazifasi

| Fayl | Vazifasi |
| :--- | :--- |
| **`cleaner.py`** | Mustaqil skript. Barcha chatlarda o'zingiz yuborgan kalit so'zli/linkli xabarlarni qidiradi va o'chiradi. |
| **`geopoint.py`** | Mustaqil skript. Barcha chatlardagi siz yuborgan lokatsiya (geopoint) ma'lumotlarini o'chiradi. |
| **`grup.py`** | Mustaqil skript. Belgilangan bitta guruh ichidagi barcha yuborgan xabarlaringizni o'chirib chiqadi. |
| **`.gitignore`** | Sizning maxfiy `.session` faylingiz GitHub'ga chiqib ketmasligini ta'minlaydi. |
| **`requirements.txt`** | Skriptlar ishlashi uchun zarur bo'lgan Python kutubxonasi (`telethon`). |

---

## 🚀 O'rnatish va ishlatish

### 1. Kerakli kutubxonani o'rnatish
Terminalda quyidagi buyruqni bajaring:
```bash
pip install -r requirements.txt
```

### 2. Skriptlarda API kalitlarni sozlash
Har bir skript fayli (`cleaner.py`, `geopoint.py`, `grup.py`)ning yuqori qismidagi o'zgaruvchilarga o'zingizning `api_id` va `api_hash` qiymatlaringizni yozing:

```python
api_id = 12345678          # my.telegram.org dagi API ID
api_hash = 'YOUR_API_HASH' # my.telegram.org dagi API Hash
```

---

## ⚙️ Skriptlarni ishga tushirish

### 1. Kalit so'z yoki havolalarni o'chirish (`cleaner.py`)
`cleaner.py` faylida `TARGET_LINK = 'https://github.com/'` o'zgaruvchisiga o'chirmoqchi bo'lgan so'z yoki havolani kiriting va ishga tushiring:
```bash
python cleaner.py
```

### 2. Barcha lokatsiyalarni o'chirish (`geopoint.py`)
Chatlardagi barcha lokatsiyalarni avtomatik o'chirish uchun:
```bash
python geopoint.py
```

### 3. Aniq guruhdagi barcha xabarlaringizni o'chirish (`grup.py`)
`grup.py` faylida `TARGET_GROUP = -1001234567890` o'zgaruvchisiga guruh ID yoki username'ini kiriting va ishga tushiring:
```bash
python grup.py
```

> ℹ️ **Eslatma:** Birinchi marta ishga tushirganda Telethon sizdan telefon raqamingiz va Telegram'ga kelgan SMS/kodni kiritishingizni so'raydi. Shundan so'ng papkada `.session` fayli hosil bo'ladi va qayta login qilish talab etilmaydi.

---

## 📄 Litsenziya

MIT License
