from instagrapi import Client
import time
import random
import os

def send_bulk_messages():
    USERNAME = "uf_sohil____01"
    PASSWORD = "SOHEL@#@#786"
    
    cl = Client()
    
    print("⏳ Instagram me login ho raha hai...")
    try:
        # Puraana session dhoondhne ki koshish karega taaki IG block na kare
        if os.path.exists("session.json"):
            cl.load_settings("session.json")
            cl.login(USERNAME, PASSWORD)
            print("✅ Puraane session se Login Successful!")
        else:
            cl.login(USERNAME, PASSWORD)
            cl.dump_settings("session.json") # Naya session save kar lega
            print("✅ Naya Login Successful aur session save ho gaya!")
            
    except Exception as e:
        print(f"❌ Login me problem aayi: {e}")
        return

    target_users = ["manishgurjar01m"] # Sirf ek user par test karein
    message_text = "Bhai ye second test hai, bata agar aaya ho toh!"

    for user in target_users:
        try:
            print(f"🔍 {user} ko dhoondh rahe hain...")
            user_id = cl.user_id_from_username(user)
            
            # Instagram ko bot hone ka shaq na ho isliye profile dekhne ki acting
            time.sleep(2) 
            
            print(f"✉️ Message bhej rahe hain...")
            cl.direct_send(message_text, user_ids=[user_id])
            print(f"✅ Code ke hisaab se {user} ko message chala gaya!")
            
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    send_bulk_messages()