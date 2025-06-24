import os
import telebot
from dotenv import load_dotenv
from telebot import apihelper
from generator import buat_resume

# Load token dari file .env
load_dotenv("resumebot.env")
TOKEN = os.getenv("TOKEN")

if not TOKEN:
    print("❌ TOKEN tidak ditemukan di file .env")
    exit(1)

# Inisialisasi bot
bot = telebot.TeleBot(TOKEN)
user_data = {}

@bot.message_handler(commands=['start'])
def handle_start(message):
    uid = message.chat.id
    user_data[uid] = {}
    bot.send_message(uid, "📄 Halo! Saya akan bantu buatkan resume kamu.\n\n📸 Kirim foto profil terlebih dahulu:")

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    uid = message.chat.id
    if uid not in user_data:
        bot.send_message(uid, "Ketik /start dulu ya 😊")
        return
    file_info = bot.get_file(message.photo[-1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    file_path = f"foto_{uid}.jpg"
    with open(file_path, 'wb') as f:
        f.write(downloaded_file)
    user_data[uid]['foto_path'] = file_path
    bot.send_message(uid, "✅ Foto diterima!\n\n✍️ Ketik nama lengkap kamu:")

@bot.message_handler(func=lambda m: m.chat.id in user_data and 'nama' not in user_data[m.chat.id])
def handle_nama(message):
    user_data[message.chat.id]['nama'] = message.text
    bot.send_message(message.chat.id, "📧 Masukkan email kamu:")

@bot.message_handler(func=lambda m: m.chat.id in user_data and 'email' not in user_data[m.chat.id])
def handle_email(message):
    user_data[message.chat.id]['email'] = message.text
    bot.send_message(message.chat.id, "📱 Nomor telepon kamu:")

@bot.message_handler(func=lambda m: m.chat.id in user_data and 'telepon' not in user_data[m.chat.id])
def handle_telepon(message):
    user_data[message.chat.id]['telepon'] = message.text
    bot.send_message(message.chat.id, "📍 Alamat domisili kamu:")

@bot.message_handler(func=lambda m: m.chat.id in user_data and 'alamat' not in user_data[m.chat.id])
def handle_alamat(message):
    user_data[message.chat.id]['alamat'] = message.text
    bot.send_message(message.chat.id, "🧾 Ringkasan singkat tentang kamu (opsional):")

@bot.message_handler(func=lambda m: m.chat.id in user_data and 'ringkasan' not in user_data[m.chat.id])
def handle_ringkasan(message):
    user_data[message.chat.id]['ringkasan'] = message.text
    bot.send_message(message.chat.id, "💼 Pengalaman kerja (pisahkan dengan titik koma ';'):")

@bot.message_handler(func=lambda m: m.chat.id in user_data and 'pengalaman' not in user_data[m.chat.id])
def handle_pengalaman(message):
    user_data[message.chat.id]['pengalaman'] = message.text.split(";")
    bot.send_message(message.chat.id, "🎓 Riwayat pendidikan (pisahkan dengan titik koma ';'):")

@bot.message_handler(func=lambda m: m.chat.id in user_data and 'pendidikan' not in user_data[m.chat.id])
def handle_pendidikan(message):
    user_data[message.chat.id]['pendidikan'] = message.text.split(";")
    bot.send_message(message.chat.id, "🧠 Keahlian kamu (pisahkan dengan koma):")

@bot.message_handler(func=lambda m: m.chat.id in user_data and 'skill' not in user_data[m.chat.id])
def handle_skill(message):
    user_data[message.chat.id]['skill'] = message.text.split(",")
    bot.send_message(message.chat.id, "🌐 Akun media sosial kamu (LinkedIn, IG, dll):")

@bot.message_handler(func=lambda m: m.chat.id in user_data and 'sosial' not in user_data[m.chat.id])
def handle_sosial(message):
    uid = message.chat.id
    user_data[uid]['sosial'] = message.text

    # Buat PDF resume
    pdf_path = f"resume_{uid}.pdf"
    try:
        buat_resume(user_data[uid], pdf_path)
        with open(pdf_path, 'rb') as f:
            bot.send_document(uid, f)
        bot.send_message(uid, "✅ Resume kamu sudah jadi! Terima kasih 🙏")
    except Exception as e:
        bot.send_message(uid, f"❌ Gagal membuat resume: {e}")
        print(f"[ERROR] Gagal membuat PDF: {e}")

    # Bersihkan data user
    if uid in user_data:
        del user_data[uid]

@bot.message_handler(func=lambda m: m.chat.id not in user_data)
def fallback(message):
    bot.send_message(message.chat.id, "Ketik /start dulu ya untuk mulai buat resume kamu 😊")

# Jalankan bot
bot.infinity_polling()
