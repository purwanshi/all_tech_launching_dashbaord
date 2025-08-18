import os
from twilio.rest import Client# type: ignore
import yagmail# type: ignore
import pywhatkit# type: ignore
import psutil# type: ignore
import requests# type: ignore
from googlesearch import search # type: ignore
from instabot import Bot# type: ignore
import gradio as gr# type: ignore
import datetime
import cv2 # type: ignore
import numpy as np
import sys
from PIL import Image
import io
import sys
import gradio as gr
from openai import OpenAI
import threading
import cv2
import time
import pygame
import requests
import webbrowser
from cvzone.HandTrackingModule import HandDetector
from twilio.rest import Client
import boto3
import uuid
import gradio as gr
import paramiko
import subprocess


#sys.stdout.reconfigure(encoding='utf-8')

# Logging Decorator
def log_action(func):
    def wrapper(*args, **kwargs):
        action_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"\n[{action_time}] Running: {func.__name__}\n"
        with open("task_log.txt", "a") as f:
            f.write(log_entry)
        try:
            result = func(*args, **kwargs)
            with open("task_log.txt", "a") as f:
                f.write(f"[{action_time}] Success: {func.__name__}\n")
            return result
        except Exception as e:
            with open("task_log.txt", "a") as f:
                f.write(f"[{action_time}] Error in {func.__name__}: {e}\n")
            return f"Error: {e}"
    return wrapper

# Twilio Config
account_sid = ''
auth_token = 'f515950ed2be5be63d00727d595ed68d'
twilio_number = '+15013820385'
client = Client(account_sid, auth_token)

@log_action
def send_sms():
    message = client.messages.create(
        body="🚨 wanna meet up? A cup of coffee maybe ☕",
        from_=twilio_number,
        to='+919571797661'
    )
    return f"✅ SMS sent. SID: {message.sid}"

@log_action
def send_whatsapp(contact, message):
    pywhatkit.sendwhatmsg_instantly(contact, message)
    return f"✅ WhatsApp sent to {contact}"

@log_action
def send_email(to, subject, body, attachment):
    if attachment and not os.path.exists(attachment):
        return f"❌ Attachment not found: {attachment}"
    yag = yagmail.SMTP("your_email@gmail.com", "your_app_password")
    yag.send(to=to, subject=subject, contents=body, attachments=attachment if attachment else None)
    return f"✅ Email sent to {to}"

def google_search(query):
    results = []
    for j in search(query, tld="co.in", num=5, stop=5, pause=2):
        results.append(j)
    return "\n".join(results)

def download_webpage(url):
    response = requests.get(url)
    if response.status_code == 200:
        filename = "downloaded_page.html"
        with open(filename, "w", encoding="utf-8") as file:
            file.write(response.text)
        return f"✅ Page downloaded as {filename}"
    else:
        return f"❌ Failed with status: {response.status_code}"

def check_ram():
    memory_info = psutil.virtual_memory()
    return (
        f"💾 Total: {memory_info.total / (1024**3):.2f} GB\n"
        f"💾 Used: {memory_info.used / (1024**3):.2f} GB\n"
        f"💾 Available: {memory_info.available / (1024**3):.2f} GB\n"
        f"📊 Usage: {memory_info.percent}%"
    )

@log_action
def insta_bot_action():
    bot = Bot()
    bot.login(username="your_insta_username", password="your_password")
    bot.follow("shivangijoshi18")
    bot.unfollow_everyone()
    followers = bot.get_user_followers("shivangijoshi18")
    return f"✅ Insta bot done. Followers: {len(followers)}"

def face_swap(img1_pil, img2_pil):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    img1 = cv2.cvtColor(np.array(img1_pil), cv2.COLOR_RGB2BGR)
    img2 = cv2.cvtColor(np.array(img2_pil), cv2.COLOR_RGB2BGR)

    faces1 = face_cascade.detectMultiScale(cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY), 1.3, 5)
    faces2 = face_cascade.detectMultiScale(cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY), 1.3, 5)

    if len(faces1) == 0 or len(faces2) == 0:
        return "Face not detected", None, None

    (x1, y1, w1, h1) = faces1[0]
    (x2, y2, w2, h2) = faces2[0]

    face1 = img1[y1:y1+h1, x1:x1+w1]
    face2 = img2[y2:y2+h2, x2:x2+w2]

    face1_resized = cv2.resize(face1, (w2, h2))
    face2_resized = cv2.resize(face2, (w1, h1))

    img1[y1:y1+h1, x1:x1+w1] = face2_resized
    img2[y2:y2+h2, x2:x2+w2] = face1_resized

    img1_pil_out = Image.fromarray(cv2.cvtColor(img1, cv2.COLOR_BGR2RGB))
    img2_pil_out = Image.fromarray(cv2.cvtColor(img2, cv2.COLOR_BGR2RGB))

    return (" Faces Swapped!", img1_pil_out, img2_pil_out)

def list_files_ui(directory):
    try:
        if not os.path.exists(directory):
            return "❌ Directory not found."
        files = os.listdir(directory)
        return "\n".join(files) if files else "📂 No files found."
    except Exception as e:
        return f"❌ Error: {str(e)}"

def rename_file_ui(directory, old_name, new_name):
    try:
        old_path = os.path.join(directory, old_name)
        new_path = os.path.join(directory, new_name)
        os.rename(old_path, new_path)
        return "✅ File renamed successfully."
    except Exception as e:
        return f"❌ Rename failed: {e}"

def delete_path_ui(directory, name):
    try:
        path = os.path.join(directory, name)
        if os.path.isfile(path):
            os.remove(path)
            return "🗑️ File deleted."
        elif os.path.isdir(path):
            shutil.rmtree(path)
            return "🧹 Directory deleted."
        else:
            return "❌ Path does not exist."
    except Exception as e:
        return f"❌ Delete failed: {e}"

def create_dir_ui(directory, folder_name):
    try:
        os.makedirs(os.path.join(directory, folder_name), exist_ok=True)
        return "📁 Folder created successfully."
    except Exception as e:
        return f"❌ Folder creation failed: {e}"

def create_file_ui(directory, folder_name, file_name):
    try:
        folder_path = os.path.join(directory, folder_name)
        if not os.path.exists(folder_path):
            return "❌ Folder does not exist."
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, "w") as f:
            f.write("")
        return f"📄 File '{file_name}' created inside '{folder_name}'."
    except Exception as e:
        return f"❌ File creation failed: {e}"

def context_gemini_chat(api_key, prompt):
    try:
        gemini_llm_model = OpenAI(
            api_key=api_key,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        )
        msg = [
            {"role": "system", "content": "You are an AI assistant"},
            {"role": "user", "content": prompt}
        ]
        response = gemini_llm_model.chat.completions.create(
            messages=msg, model="gemini-1.5-flash", stream=True
        )
        result = ""
        for chunk in response:
            if hasattr(chunk.choices[0].delta, "content"):
                result += chunk.choices[0].delta.content
        return result
    except Exception as e:
        return f"❌ Error: {e}"

def get_fashion_images(occasion, gender):
    from bs4 import BeautifulSoup
    import requests
    headers = {"User-Agent": "Mozilla/5.0"}
    url = f"https://www.google.com/search?tbm=isch&q={gender}+outfit+for+{occasion}".replace(" ", "+")
    soup = BeautifulSoup(requests.get(url, headers=headers).text, "html.parser")
    return [img["src"] for img in soup.find_all("img") if "src" in img.attrs][1:7]

def get_fashion_tip(occasion, gender):
    tips = {
        "wedding": {"Male": "Sherwani or blazer with shoes", "Female": "Lehenga, saree or gown"},
        "party": {"Male": "Casual shirt + jeans", "Female": "Cocktail dress or jumpsuit"},
        "office": {"Male": "Shirt and trousers", "Female": "Formal blouse + skirt"},
        "casual": {"Male": "T-shirt and jeans", "Female": "Floral dress or top + denim"}
    }
    return tips.get(occasion.lower(), {}).get(gender, "Wear what feels comfy!")

def fashion_chatbot(img, occasion, gender):
    return get_fashion_tip(occasion, gender), get_fashion_images(occasion, gender)

def get_therapy_response(api_key, lover, hobbies, fav_food, indoor_outdoor, emotion, fav_flower):
    model = OpenAI(api_key=api_key, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
    prompt = f"""
    The user is a {lover} lover who enjoys {hobbies}, loves {fav_food}, prefers {indoor_outdoor} environments, feels {emotion}, and likes {fav_flower}.
    Suggest 5 cozy, uplifting tips based on their mood and personality.
    """
    messages = [
        {"role": "system", "content": "You are a warm, therapeutic AI offering cozy and scientifically-backed advice."},
        {"role": "user", "content": prompt}
    ]
    response = model.chat.completions.create(messages=messages, model="gemini-1.5-flash")
    return response.choices[0].message.content

def handle_first_click(api_key, lover, hobbies, fav_food, indoor_outdoor, emotion, fav_flower):
    result = get_therapy_response(api_key, lover, hobbies, fav_food, indoor_outdoor, emotion, fav_flower)
    return result, [api_key, lover, hobbies, fav_food, indoor_outdoor, emotion, fav_flower]

def handle_reload(inputs):
    if not inputs or len(inputs) != 7:
        return "Please submit preferences first.", inputs
    return get_therapy_response(*inputs), inputs

import gradio as gr
from cvzone.HandTrackingModule import HandDetector
import cv2
import os
import threading

# Global variable to control webcam loop
running = False

def run_hand_gesture():
    global running
    cap = cv2.VideoCapture(0)
    detector = HandDetector(detectionCon=0.8, maxHands=1)

    while running:
        success, img = cap.read()
        if not success:
            continue

        # Detect hands
        hands, img = detector.findHands(img)

        if hands:
            hand = hands[0]
            fingers = detector.fingersUp(hand)
            print("Detected fingers:", fingers)

            if fingers == [1, 1, 1, 1, 1]:
                print("📝 Opening MS Word...")
                os.system("start winword")  # "start msword" replaced with correct Windows command
                running = False
                break
            elif fingers == [1, 0, 0, 0, 0]:
                print("🌐 Opening Chrome...")
                os.system("start chrome")
                running = False
                break
            else:
                print("❌ No recognized gesture")

        cv2.imshow("Hand Gesture", img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


def start_gesture_tool():
    """Starts the hand gesture recognition in a separate thread."""
    global running
    if not running:
        running = True
        thread = threading.Thread(target=run_hand_gesture)
        thread.start()
        return "Hand gesture recognition started."
    return "Already running."


def stop_gesture_tool():
    """Stops the hand gesture recognition."""
    global running
    running = False
    return "Hand gesture recognition stopped."

# ===================== GLOBALS =====================
running_shell = False
running_emergency = False
alarm_triggered = False
sms_sent = False
call_made = False
last_trigger_time = 0
cooldown_time = 5  # seconds

# ===================== COMMON HAND DETECTOR =====================
hd = HandDetector(detectionCon=0.8, maxHands=1)

# ===================== SHELL TOOL =====================
def gesture_shell():
    global running_shell
    cap = cv2.VideoCapture(0)

    while running_shell:
        success, img = cap.read()
        if not success:
            continue

        hands, img = hd.findHands(img)
        if hands:
            fingers = hd.fingersUp(hands[0])
            if fingers == [1, 1, 1, 1, 1]:
                os.system("start winword")
                return "📄 Opened MS Word"
            elif fingers == [1, 0, 0, 0, 0]:
                os.system("start chrome")
                return "🌐 Opened Chrome"

        cv2.imshow("Shell Tool", img)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    return "🛑 Shell tool stopped."

def start_shell():
    global running_shell
    if not running_shell:
        running_shell = True
        threading.Thread(target=gesture_shell, daemon=True).start()
        return "🚀 Shell tool started."
    return "⚠ Already running."

def stop_shell():
    global running_shell
    running_shell = False
    return "🛑 Shell tool stopped."

# ===================== EMERGENCY SYSTEM =====================
pygame.mixer.init()
def play_alarm():
    alarm = pygame.mixer.Sound("alarm.mp3")
    alarm.play()

def get_location():
    try:
        response = requests.get("https://ipinfo.io/json")
        data = response.json()
        if "loc" in data:
            loc = data["loc"].split(",")
            return [float(loc[0]), float(loc[1])]
        return None
    except:
        return None

def send_emergency_sms(location=None):
    phone_numbers = ["+918209452791"]
    for number in phone_numbers:
        message_body = "🚨 Emergency detected! Please respond immediately."
        if location:
            message_body += f" Location: https://www.google.com/maps?q={location[0]},{location[1]}"
        try:
            message = client.messages.create(body=message_body, from_=twilio_number, to=number)
            print(f"SMS sent to {number}: {message.sid}")
        except Exception as e:
            print(f"SMS failed: {e}")

def make_emergency_call():
    call_numbers = ["+919571797661"]
    for number in call_numbers:
        try:
            call = client.calls.create(
                twiml="<Response><Say>Emergency detected. Please check immediately!</Say></Response>",
                from_=twilio_number,
                to=number
            )
            print(f"Call made to {number}: {call.sid}")
        except Exception as e:
            print(f"Call failed: {e}")

def open_location_in_browser(location):
    webbrowser.open(f"https://www.google.com/maps?q={location[0]},{location[1]}")

def run_emergency_system():
    global running_emergency, alarm_triggered, sms_sent, call_made, last_trigger_time
    cap = cv2.VideoCapture(0)

    while running_emergency:
        status, photo = cap.read()
        if not status:
            continue

        hands, img = hd.findHands(photo)
        current_time = time.time()

        if current_time - last_trigger_time > cooldown_time:
            alarm_triggered = sms_sent = call_made = False

        if hands:
            fingerup = hd.fingersUp(hands[0])

            if fingerup == [1, 1, 1, 1, 1] and not alarm_triggered:
                threading.Thread(target=play_alarm, daemon=True).start()
                loc = get_location()
                if loc:
                    send_emergency_sms(loc)
                    open_location_in_browser(loc)
                alarm_triggered = True
                last_trigger_time = current_time

            elif fingerup == [0, 1, 0, 0, 0] and not sms_sent:
                send_emergency_sms()
                sms_sent = True
                last_trigger_time = current_time

            elif fingerup == [1, 0, 0, 0, 1] and not call_made:
                make_emergency_call()
                call_made = True
                last_trigger_time = current_time

        cv2.imshow("Emergency System", photo)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

def start_emergency():
    global running_emergency
    if not running_emergency:
        running_emergency = True
        threading.Thread(target=run_emergency_system, daemon=True).start()
        return "🚀 Emergency system started."
    return "⚠ Already running."

def stop_emergency():
    global running_emergency
    running_emergency = False
    return "🛑 Emergency system stopped."

# ---------- AWS FUNCTIONS ----------
ec2 = boto3.client('ec2', region_name='ap-south-1')
s3 = boto3.client('s3', region_name='ap-south-1')
dynamodb = boto3.client('dynamodb', region_name='ap-south-1')

# ---------- Functions ----------
def launch_service(option):
    try:
        if option == "1":
            ec2_response = ec2.run_instances(
                ImageId='ami-0c123456789example',  # Replace with a valid AMI ID
                InstanceType='t2.micro',
                KeyName='your-key-pair-name',  # Replace with your key pair name
                MinCount=1,
                MaxCount=1,
                SecurityGroupIds=['sg-0abc12345example'],  # Replace with your security group ID
                SubnetId='subnet-0abc12345example',        # Replace with your subnet ID
                TagSpecifications=[
                    {
                        'ResourceType': 'instance',
                        'Tags': [{'Key': 'Name', 'Value': 'MyPythonEC2Instance'}]
                    }
                ]
            )
            instance_id = ec2_response['Instances'][0]['InstanceId']
            return f"✅ Launched EC2 Instance with ID: {instance_id}"

        elif option == "2":
            bucket_name = f"my-python-bucket-{uuid.uuid4().hex}"
            s3.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={'LocationConstraint': 'ap-south-1'}
            )
            return f"✅ Created S3 Bucket: {bucket_name}"

        elif option == "3":
            table_name = "MyPythonTable"
            dynamodb.create_table(
                TableName=table_name,
                KeySchema=[
                    {'AttributeName': 'ID', 'KeyType': 'HASH'}
                ],
                AttributeDefinitions=[
                    {'AttributeName': 'ID', 'AttributeType': 'S'}
                ],
                ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
            )
            return f"✅ Created DynamoDB Table: {table_name}"

        else:
            return "❌ Invalid option. Please select 1, 2, or 3."

    except Exception as e:
        return f"⚠ Error: {str(e)}"


# ---------- AWS function ----------
def aws_launcher_ui():
    with gr.Accordion("☁ AWS Service Launcher", open=True):
        gr.Markdown("### Select an AWS service to launch:")
        option = gr.Dropdown(
            choices=["1", "2", "3"],
            label="Choose an option",
            info="1 = EC2, 2 = S3, 3 = DynamoDB"
        )
        launch_btn = gr.Button("🚀 Launch Service")
        output_box = gr.Textbox(label="Status", interactive=False)

        launch_btn.click(fn=launch_service, inputs=option, outputs=output_box)
    
# ---------------- LINUX SSH EXECUTION FUNCTION ----------------
commands = {
    "1": "ls -l",           # List files in long format
    "2": "pwd",             # Print current working directory
    "3": "df -h",           # Show disk usage in human-readable format
    "4": "free -m",         # Show memory usage in MB
    "5": "uptime"           # Show system uptime
}
def run_linux_command(option):
    try:
        if option in commands:
            result = subprocess.check_output(commands[option], shell=True, text=True)
            return f"✅ Command: {commands[option]}\n\n{result}"
        else:
            return "❌ Invalid option. Please select a valid number."
    except Exception as e:
        return f"⚠ Error: {str(e)}"

#-----------------docker shell-----------------
docker_commands = {
    "1": "docker ps",                     # Running containers
    "2": "docker ps -a",                  # All containers
    "3": "docker images",                 # List images
    "4": "docker stats --no-stream",      # Container stats
    "5": "docker system df"               # Docker disk usage
}

def run_docker_command(option):
    try:
        if option in docker_commands:
            result = subprocess.check_output(docker_commands[option], shell=True, text=True)
            return f"🐳 Command: {docker_commands[option]}\n\n{result}"
        else:
            return "❌ Invalid option. Please select a valid number."
    except Exception as e:
        return f"⚠ Error: {str(e)}"

# =====================
# MAIN BLOCK STARTS
# =====================
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("## 💼 Central Dashboard")

    # 📱 Automated Panel
    with gr.Accordion("📱 Python Tasks Automation Panel", open=True):
       with gr.Tab("📑 All Task Titles"):
        gr.Markdown("""
        ### 🔖 Available Automation Tasks
        1. **Send SMS**  
        2. **Send WhatsApp**  
        3. **Check RAM Usage**  
        4. **Instagram Bot**  
        5. **Google Search**  
        6. **Send Email**  
        7. **Download Webpage**  
        8. **Swap Face Utility**
        """)

       with gr.Tab("live demo"):
    
        gr.Markdown("### 📨 Send SMS")
        gr.Button("Send SMS").click(send_sms, outputs=gr.Textbox(label="SMS Status"))
    
        gr.Markdown("### 💬 WhatsApp Message")
        contact = gr.Textbox(label="Contact No (+91...)")
        msg = gr.Textbox(label="Message")
        gr.Button("Send WhatsApp").click(send_whatsapp, inputs=[contact, msg], outputs=gr.Textbox(label="WhatsApp Status"))
    
        gr.Markdown("### 💾 Check RAM")
        gr.Button("Check RAM").click(check_ram, outputs=gr.Textbox(label="RAM Usage"))
    
        gr.Markdown("### 🤖 Insta Bot")
        gr.Button("Run Insta Bot").click(insta_bot_action, outputs=gr.Textbox(label="Bot Result"))
    
        gr.Markdown("### 🔍 Google Search")
        query = gr.Textbox(label="Search Query")
        gr.Button("Search").click(google_search, inputs=query, outputs=gr.Textbox(label="Search Results"))
    
        gr.Markdown("### 📨 Email Service")
        to = gr.Textbox(label="To Email")
        subject = gr.Textbox(label="Subject")
        body = gr.Textbox(label="Body")
        attachment = gr.Textbox(label="Attachment Path (optional)")
        gr.Button("Send Email").click(
            send_email, 
            inputs=[to, subject, body, attachment], 
            outputs=gr.Textbox(label="Email Status")
        )
    
        gr.Markdown("### 🌐 Webpage Downloader")
        url = gr.Textbox(label="Web Page URL")
        gr.Button("Download Page").click(download_webpage, inputs=url, outputs=gr.Textbox(label="Download Status"))
    
        gr.Markdown("### 🔁 Face Swap Utility")
        img1 = gr.Image(label="Upload Face 1")
        img2 = gr.Image(label="Upload Face 2")
        result = gr.Textbox(label="Status")
        out_img1 = gr.Image(label="Image 1 (After Swap)")
        out_img2 = gr.Image(label="Image 2 (After Swap)")
        gr.Button("🔄 Swap Faces").click(
            face_swap, 
            inputs=[img1, img2], 
            outputs=[result, out_img1, out_img2]
        )

    # 🗂️ File Manager
    with gr.Accordion("🗂️ File Management Menu", open=False):
        gr.Markdown("### 📁 Directory Settings")
        base_dir = gr.Textbox(label="Working Directory", placeholder="Enter folder path...")

        gr.Markdown("### 📋 List Files")
        gr.Button("List Files").click(list_files_ui, inputs=[base_dir], outputs=gr.Textbox(label="Files"))

        gr.Markdown("### ✏️ Rename File")
        old = gr.Textbox(label="Old File Name")
        new = gr.Textbox(label="New File Name")
        gr.Button("Rename File").click(rename_file_ui, inputs=[base_dir, old, new], outputs=gr.Textbox(label="Rename Status"))

        gr.Markdown("### 🗑️ Delete File or Folder")
        delete_name = gr.Textbox(label="File/Folder Name to Delete")
        gr.Button("Delete").click(delete_path_ui, inputs=[base_dir, delete_name], outputs=gr.Textbox(label="Delete Status"))

        gr.Markdown("### 📁 Create New Folder")
        folder_name = gr.Textbox(label="Folder Name")
        gr.Button("Create Folder").click(create_dir_ui, inputs=[base_dir, folder_name], outputs=gr.Textbox(label="Folder Status"))

        gr.Markdown("### 📃 Create File in Folder")
        folder = gr.Textbox(label="Existing Folder Name")
        file = gr.Textbox(label="File Name")
        gr.Button("Create File").click(create_file_ui, inputs=[base_dir, folder, file], outputs=gr.Textbox(label="File Status"))

    # 🤖 AI Projects
    with gr.Accordion("🤖 AI Projects", open=False):
        gr.Markdown("## 🧠 Unified AI Projects")

        # Shared API key
        gemini_api_input = gr.Textbox(label="🔐 Enter your Gemini API Key once", type="password", placeholder="Paste your Gemini API key here")

        # Project 1
        gr.Markdown("### 🧠 AI ChatGPT + Context Rememberance")
        context_prompt_input = gr.Textbox(label="🗣️ Your Message")
        context_output = gr.Textbox(label="🧠 Response")
        gr.Button("💬 Chat with Context").click(context_gemini_chat, inputs=[gemini_api_input, context_prompt_input], outputs=context_output)

        # Project 2
        gr.Markdown("### 👗 Fashion Genie: Your Style Assistant")
        with gr.Tab("Get Suggestions"):
            with gr.Row():
                with gr.Column():
                    photo_input = gr.Image(label="Upload Photo", type="filepath")
                    occasion_input = gr.Textbox(label="Occasion (e.g., wedding, office)")
                    gender_input = gr.Radio(choices=["Male", "Female"], label="Gender", value="Female")
                    suggest_btn = gr.Button("🔮 Recommend")
                with gr.Column():
                    fashion_tip = gr.Textbox(label="🎀 Style Tip", lines=2)
                    gallery = gr.Gallery(label="🌂 Outfit Suggestions", columns=3)
            suggest_btn.click(fashion_chatbot, inputs=[photo_input, occasion_input, gender_input], outputs=[fashion_tip, gallery])
        with gr.Tab("About Fashion Genie"):
            gr.Markdown("Fashion Genie gives style recommendations based on occasion and gender. It scrapes Google Images for outfit examples and offers expert tips.")

        # Project 3
        gr.Markdown("### 🌸 Gemini Pocket Therapist")
        with gr.Row():
            lover = gr.Textbox(label="💖 Nature/Music/Pet lover?")
            hobbies = gr.Textbox(label="🎨 Hobbies?")
        with gr.Row():
            fav_food = gr.Textbox(label="🍜 Favorite Food?")
            indoor_outdoor = gr.Textbox(label="🏡 Indoor/Outdoor?")
        with gr.Row():
            emotion = gr.Textbox(label="💭 How are you feeling?")
            fav_flower = gr.Textbox(label="🌷 Favorite Flower or Plant?")
        output = gr.Textbox(label="🧠 Cozy Suggestions", lines=12)
        get_btn = gr.Button("✨ Get Suggestions")
        reload_btn = gr.Button("🔄 Reload")
        state_inputs = gr.State([])
        get_btn.click(handle_first_click, inputs=[gemini_api_input, lover, hobbies, fav_food, indoor_outdoor, emotion, fav_flower], outputs=[output, state_inputs])
        reload_btn.click(handle_reload, inputs=[state_inputs], outputs=[output, state_inputs])

    # CV ZONE PROJECTS
    with gr.Accordion("👀🖐CV ZONE PROJECTS", open=False):
        with gr.Tab("Hand Gesture Shell Tool"):
            gr.Markdown("## ✋ Open Software Applications with Hand Gestures")
            gr.Markdown("🖐 = MS Word | ☝ = Chrome")
            with gr.Row():
                start_btn_shell = gr.Button("▶ Start")
                stop_btn_shell = gr.Button("⏹ Stop")
            status_shell = gr.Textbox(label="Shell Tool Status", interactive=False)
            start_btn_shell.click(start_shell, outputs=status_shell)
            stop_btn_shell.click(stop_shell, outputs=status_shell)

        with gr.Tab("Emergency Detection System"):
            gr.Markdown("## 🚨 Hand Gesture Emergency Detection System")
            gr.Markdown("🖐 = Alarm + SMS + Location | ☝ = SMS | ✌ = Call")
            with gr.Row():
                start_btn_em = gr.Button("▶ Start Detection")
                stop_btn_em = gr.Button("⏹ Stop Detection")
            status_em = gr.Textbox(label="Emergency System Status", interactive=False)
            start_btn_em.click(start_emergency, outputs=status_em)
            stop_btn_em.click(stop_emergency, outputs=status_em)
    #cloud 
    with gr.Accordion("☁ Cloud & AWS Tools", open=True):
        aws_launcher_ui()

    #LINUX PROJECT
    with gr.Accordion("💻LINUX Shell", open=True):
        gr.Markdown("### Available Commands")
        gr.Markdown("""
        1️⃣ **1 = ls -l**  → List files in current directory  
        2️⃣ **2 = pwd**  → Show current directory  
        3️⃣ **3 = df -h**  → Disk usage  
        4️⃣ **4 = free -m**  → Memory usage  
        5️⃣ **5 = uptime**  → System uptime  
        """)
        
        option = gr.Textbox(
            label="Enter Option Number",
            placeholder="Type 1, 2, 3, 4, or 5"
        )
        run_btn = gr.Button("▶ Run Command")
        output_box = gr.Textbox(label="Command Output", interactive=False, lines=15)

        run_btn.click(fn=run_linux_command, inputs=option, outputs=output_box)
#dockerp
    with gr.Accordion("🐳 Docker Command Menu", open=True):
        gr.Markdown("### Available Docker Commands")
        gr.Markdown("""
        1️⃣ **1 = docker ps** → Show running containers  
        2️⃣ **2 = docker ps -a** → Show all containers  
        3️⃣ **3 = docker images** → List Docker images  
        4️⃣ **4 = docker stats --no-stream** → Show container stats  
        5️⃣ **5 = docker system df** → Show Docker disk usage  
        """)
        
        option_docker = gr.Textbox(
            label="Enter Docker Option Number",
            placeholder="Type 1, 2, 3, 4, or 5"
        )
        run_btn_docker = gr.Button("▶ Run Docker Command")
        output_docker = gr.Textbox(label="Docker Output", interactive=False, lines=15)

        run_btn_docker.click(fn=run_docker_command, inputs=option_docker, outputs=output_docker)




# Launch app
demo.launch()

