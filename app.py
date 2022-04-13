from flask import Flask, render_template, redirect, url_for, send_file
from manager import InstaProfile, Database
import requests
import os
import json
from threading import Thread
import subprocess

app = Flask(__name__)


target_username = "maneshsamarathunga"

ORIGINAL_DIR = os.getcwd()

# Instantiate and set target
print("Please wait while the object is being created!")
obj = InstaProfile()
obj.TARGET = target_username
print("Created the object successfully!")

# Login
print("Please wait while logging in!")
obj.login(username=Database.USERNAME, password=Database.PASS)
print("Logged in successfully!")


print("[*] Please wait while target's profile information is being loaded")

# Process Main Info in obj to prevent fucky errors
obj._process_profile_data()

# Folder to store the user data in
current_session_folder_absolute = os.path.join(
    os.getcwd(),
    "static",
    "data",
    target_username
)
current_session_folder = os.path.join(
    "static",
    "data",
    target_username
)
if not(os.path.isdir(current_session_folder_absolute)):
    os.makedirs(current_session_folder_absolute)

# Main Profile Info
information_filename_json = os.path.join(
    current_session_folder_absolute,
    f"{target_username}.json"
)
information_filename_txt = os.path.join(
    current_session_folder_absolute,
    f"{target_username}.txt"
)
if not(os.path.isfile(information_filename_json)):
    obj.save_ProfileInfo(
        file_format="json",
        final_filename=information_filename_json
    )
    obj.save_ProfileInfo(
        file_format="txt",
        final_filename=information_filename_txt
    )
    accinfo = obj.profile_data
else:
    with open(information_filename_json, "r", encoding="utf8") as main_data_temp_file:
        accinfo = json.load(main_data_temp_file)

# Profile Picture
profile_picture_filename = os.path.join(
    current_session_folder_absolute,
    f"{target_username}_profile_pic.png"
)
if not(os.path.isfile(profile_picture_filename)):
    r = requests.get(accinfo['profile_pic_url'])
    if 300 > r.status_code >= 200:
        with open(profile_picture_filename, "wb") as image_file_write:
            image_file_write.write(r.content)

# Custom Profile Picture Location URL for the frontend;
#   Thanks to instagram for blocking: returning of the image when image url is not current location of window
accinfo['profile_picture_web_server_url'] = f'/static/data/{target_username}/{target_username}_profile_pic.png'

print(
    f"[+] Loaded all basic target's profile information and saved in ./static/data/{target_username}/{target_username}.json")
print(
    f"[+] Saved profile picture to ./static/data/{target_username}/{target_username}_profile_pic.png")

print("[*] Please wait while the history is being loaded!")
all_sessions_folder = os.path.join(
    os.getcwd(),
    "static",
    "data"
)
final_all_history_list = []
for folder_name in os.listdir(all_sessions_folder):
    if not(folder_name == target_username):
        current_history_folder = os.path.join(all_sessions_folder, folder_name)
        current_history_profile_info_filename = os.path.join(
            current_history_folder, f'{folder_name}.json')
        with open(current_history_profile_info_filename, "r", encoding="utf-8") as current_history_profile_info_file:
            history_current_profile_info = json.load(
                current_history_profile_info_file)
        final_all_history_list.append(
            {
                'username': f"@{folder_name}",
                'followers': history_current_profile_info['followers'],
                'full_name': history_current_profile_info['full_name'],
                'image_url_for_web_server': f'/static/data/{folder_name}/{folder_name}_profile_pic.png'
            }
        )
print("[+] Loaded history")

# Other Files and Folder Paths
information_filename_txt = os.path.join(
    current_session_folder_absolute,
    f"{target_username}.txt"
)
uploaded_posts_folder_path = os.path.join(
    os.getcwd(),
    current_session_folder,
    "posts",
    "uploaded"
)


# Support Functions
def open_folder(folder_path):
    subprocess.Popen(
        ['explorer' if os.name == 'nt' else 'xdg-open', folder_path])


@ app.route("/")
def index():
    return render_template(
        "index.html",
        accinfo=accinfo,
        final_all_history_list=final_all_history_list,
    )


@app.route("/save/profile/piccture")
def save_profile_pic():
    return send_file(profile_picture_filename)


@app.route("/save/profile/info")
def save_profile_info_txt():
    if not(os.path.isfile(information_filename_txt)):
        obj.save_ProfileInfo(
            final_filename=information_filename_txt, file_format='txt')
    return send_file(information_filename_txt, as_attachment=True)


@app.route("/save/posts/uploaded")
def save_posts_uploaded():
    if not(os.path.isdir(uploaded_posts_folder_path)):
        os.makedirs(uploaded_posts_folder_path)

    t2 = Thread(target=open_folder, args=(uploaded_posts_folder_path,))
    t2.start()

    t3 = Thread(
        target=obj.save_PostsUploaded,
        args=("uploaded", ORIGINAL_DIR, uploaded_posts_folder_path, True)
    )
    t3.start()

    return redirect(url_for('index'))


def runWebServer():
    app.run(
        Database.HOST,
        port=int(Database.PORT),
        debug=bool(Database.DEBUG)
    )


if __name__ == "__main__":
    runWebServer()
