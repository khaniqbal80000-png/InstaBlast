from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from instagrapi import Client
import time, random, os

app = Flask(__name__)
CORS(app)

cl = Client()
current_logged_in_user = None

def login_insta(username, password):
    global current_logged_in_user
    if current_logged_in_user == username:
        return True
    try:
        print(f"⏳ {username} ke account me login ho raha hai...")
        if os.path.exists("session.json"):
            cl.load_settings("session.json")
        cl.login(username, password)
        cl.dump_settings("session.json")
        current_logged_in_user = username
        print("✅ Login Successful!")
        return True
    except Exception as e:
        print("❌ Login me problem aayi:", e)
        if os.path.exists("session.json"):
            os.remove("session.json")
        return False

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_followers', methods=['POST'])
def get_followers():
    data = request.json
    ig_user = data.get('ig_username')
    ig_pass = data.get('ig_password')
    # NAYA: Website se number lena (default 50 agar khali chhod diya to)
    amount = data.get('amount', 50) 
    
    try:
        amount = int(amount)
    except ValueError:
        amount = 50

    if not ig_user or not ig_pass:
        return jsonify({"status": "error", "message": "Username aur Password zaroori hai!"})

    if not login_insta(ig_user, ig_pass):
        return jsonify({"status": "error", "message": "Login fail ho gaya. Details check karein."})
    
    try:
        print(f"⏳ {amount} Followers nikal rahe hain...")
        user_id = cl.user_id
        followers = cl.user_followers(user_id, amount=amount) 
        
        usernames = [user_info.username for uid, user_info in followers.items()]
        print(f"✅ {len(usernames)} followers mil gaye!")
        return jsonify({"status": "success", "followers": usernames})
    except Exception as e:
        print("❌ Error:", e)
        return jsonify({"status": "error", "message": str(e)})

@app.route('/send_messages', methods=['POST'])
def send_messages():
    data = request.json
    ig_user = data.get('ig_username')
    ig_pass = data.get('ig_password')
    target_users = data.get('usernames', [])
    message_text = data.get('message', '')

    if not ig_user or not ig_pass:
        return jsonify({"status": "error", "log": "Username aur Password zaroori hai!"})

    if not login_insta(ig_user, ig_pass):
        return jsonify({"status": "error", "log": "Login fail ho gaya."})

    logs = []
    for user in target_users:
        user = user.strip()
        if not user: continue
        try:
            print(f"🔍 {user} ko bhej rahe hain...")
            user_id = cl.user_id_from_username(user)
            time.sleep(2)
            
            cl.direct_send(message_text, user_ids=[user_id])
            success_msg = f"✅ {user} ko message chala gaya!"
            print(success_msg)
            logs.append(success_msg)
            
            time.sleep(random.randint(15, 30)) 
        except Exception as e:
            error_msg = f"❌ {user} fail hua: {str(e)}"
            print(error_msg)
            logs.append(error_msg)

    return jsonify({"status": "completed", "logs": logs})

if __name__ == '__main__':
    app.run(port=5000, debug=True)