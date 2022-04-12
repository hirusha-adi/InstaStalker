from flask import Flask, render_template, redirect, url_for, send_file
from manager import InstaProfile, Database
import requests
import os
import json
from threading import Thread
import subprocess

app = Flask(__name__)


target_username = "hirushaadi"

# Instantiate and set target
print("Please wait while the object is being created!")
obj = InstaProfile()
obj.setTARGET(target_username)
print("Created the object successfully!")

# Login
print("Please wait while logging in!")
# obj.login(username=Database.USERNAME, password=Database.PASSWORD)
print("Logged in successfully!")


print("[*] Please wait while target's profile information is being loaded")

# Folder to store the user data in
current_session_folder = os.path.join(
    os.getcwd(),
    "static",
    "data",
    target_username
)
if not(os.path.isdir(current_session_folder)):
    os.makedirs(current_session_folder)

# Main Profile Info
information_filename = os.path.join(
    current_session_folder,
    f"{target_username}.json"
)
if not(os.path.isfile(information_filename)):
    accinfo = obj.getProfileInfo()
    with open(information_filename, "w", encoding="utf8") as main_data_temp_file:
        json.dump(accinfo, main_data_temp_file)
else:
    with open(information_filename, "r", encoding="utf8") as main_data_temp_file:
        accinfo = json.load(main_data_temp_file)
        obj.setProfileInfo(accinfo)

# Profile Picture
profile_picture_filename = os.path.join(
    current_session_folder,
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
        # current_history_profile_picture = os.path.join(
        #     current_history_folder, f'{folder_name}_profile_pic.png')
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

# Other Files and Folder Paths
information_filename_txt = os.path.join(
    current_session_folder,
    f"{target_username}.txt"
)


@ app.route("/")
def index():
    return render_template(
        "index.html",
        accinfo=accinfo,
        final_all_history_list=final_all_history_list,
    )


@app.route("/save/profile_pic")
def save_profile_pic():

    # Will decide about this in the future
    # def open_folder_profile_pic():
    # if os.name == 'nt':
    # subprocess.Popen(['explorer', current_session_folder])
    # else:
    # subprocess.Popen(['xdg-open', current_session_folder])
    #
    # t1 = Thread(target=open_folder_profile_pic)
    # t1.start()

    return send_file(profile_picture_filename)


@app.route("/save/profile_info")
def save_profile_info_txt():
    if not(os.path.isfile(information_filename_txt)):
        try:
            with open(information_filename_txt, "w", encoding="utf-8") as file:
                file.write(obj.createProfileTXTFileContent(data=accinfo))
        except:
            obj.saveProfileInfo(
                filename=information_filename_txt, file_format='txt')

    return send_file(information_filename_txt, as_attachment=True)


def runWebServer():
    app.run(
        Database.HOST,
        port=int(Database.PORT),
        debug=bool(Database.DEBUG)
    )


if __name__ == "__main__":
    runWebServer()
