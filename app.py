import json
import logging
import os
import subprocess
import sys
import tkinter.font as font
import webbrowser
from threading import Thread
from tkinter import *

import texts
from manager import InstaProfile
from utils import Database


def pip_install(name: str):
    os.system(f'{"pip" if os.name == "nt" else "pip3"} install -U {name}')


try:
    import requests
except:
    pip_install("requests")
    import requests

try:
    from flask import Flask, redirect, render_template, send_file, url_for
except:
    pip_install("flask")
    from flask import Flask, redirect, render_template, send_file, url_for

# GUI - Starts Here
# -------------------------------------------------------------------------------------------------------
root = Tk()
root.title("ikman.lk Scrapper")
root.resizable(True, True)

font_15_bold = font.Font(size="15", weight="bold")
font_13_bold = font.Font(size="13", weight="bold")

# First Row ----------------
# Topic
l_title = Label(root, text="InstaStalker")
l_title.grid(row=2, column=2, columnspan=2, rowspan=1)
l_title['font'] = font_15_bold

# Second Row ----------------
# Target Info
l_target = Label(root, text="Target: ")
l_target.grid(row=4, column=2, columnspan=1, rowspan=1)
l_target['font'] = font_15_bold


root.mainloop()

app = Flask(__name__)
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

try:
    target_username = "hirushaadi"
    # target_username = sys.argv[1]
except IndexError:
    target_username = input("Enter target username> ")

print(texts.Loading)

ORIGINAL_DIR = os.getcwd()

# Instantiate and set target
print("Please wait while the object is being created!")
obj = InstaProfile()
obj.TARGET = target_username
print("Created the object successfully!")

# Login
print("Please wait while logging in!")
try:
    # obj.login(username=Database.USERNAME, password=Database.PASSWORD)
    pass
except Exception as e:
    print(e)
    login_username = input("Enter login username> ")
    login_password = input("Enter login password> ")
    try:
        obj.login(username=login_username, password=login_password)
    except Exception as e:
        print(e)
        continue_yn = input("[!!] Login Failed! Do you want to exit [y/n] >")
        if continue_yn.lower() in ("yes", "y", "yeah", "ye", "true", "t"):
            pass
        else:
            sys.exit("Quitting! Have a nice day!")
print("Logged in successfully!")


print("[*] Please wait while target's profile information is being loaded")

# Process Main Info in obj to prevent fucky errors
# obj._process_profile_data()

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
                'image_url_for_web_server': f'/static/data/{folder_name}/{folder_name}_profile_pic.png',
                'folder_path': current_history_folder
            }
        )
print("[+] Loaded history")

print("[*] Loading filenames to be used by the web server")
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
tagged_posts_folder_path = os.path.join(
    os.getcwd(),
    current_session_folder,
    "posts",
    "tagged"
)
igtv_posts_folder_path = os.path.join(
    os.getcwd(),
    current_session_folder,
    "posts",
    "igtv"
)
profile_followers_list_file_json = os.path.join(
    current_session_folder_absolute,
    "followers.json"
)
profile_followees_list_file_json = os.path.join(
    current_session_folder_absolute,
    "followees.json"
)
print("[+] Completed loading everything!")

texts.clear()


# Support Functions
def open_folder(folder_path):
    subprocess.Popen(
        ['explorer' if os.name == 'nt' else 'xdg-open', folder_path])
    print(
        f"[+] Ran: {'explorer' if os.name == 'nt' else 'xdg-open'} '{folder_path}'\n\tTo open the folder")


@app.route("/")
def index():
    print("[+] Returning `index.html` with required data")
    return render_template(
        "index.html",
        accinfo=accinfo,
        final_all_history_list=final_all_history_list,
    )


@app.route("/save/profile/piccture")
def save_profile_pic():
    print("[+] Returning profile picture of the current target")
    return send_file(profile_picture_filename)


@app.route("/save/profile/info")
def save_profile_info_txt():
    print(texts.PROFILE_INFORMATION)

    if not(os.path.isfile(information_filename_txt)):
        print("[*] Loading & Saving profile information!")
        obj.save_ProfileInfo(
            final_filename=information_filename_txt, file_format='txt')
        print("[+] Saved profile information as text file: `txt` !")
    print(f"[+] Returning {information_filename_txt} as attachment.")
    return send_file(information_filename_txt, as_attachment=True)


@app.route("/save/posts/uploaded")
def save_posts_uploaded():
    print(texts.UPLOADED_POSTS)

    if not(os.path.isdir(uploaded_posts_folder_path)):
        os.makedirs(uploaded_posts_folder_path)
        print(f"[+] Made directory {uploaded_posts_folder_path}")

    t3 = Thread(
        target=obj.save_PostsUploaded,
        args=(ORIGINAL_DIR, uploaded_posts_folder_path, True)
    )
    t3.start()
    print("[+] Started new thread for `save_PostsUploaded()`")

    t2 = Thread(target=open_folder, args=(uploaded_posts_folder_path,))
    t2.start()

    return redirect(url_for('index'))


@app.route("/save/posts/tagged")
def save_posts_tagged():
    print(texts.TAGGED_POSTS)

    if not(os.path.isdir(tagged_posts_folder_path)):
        os.makedirs(tagged_posts_folder_path)
        print(f"[+] Made directory {uploaded_posts_folder_path}")

    t5 = Thread(
        target=obj.save_PostsTagged,
        args=(ORIGINAL_DIR, tagged_posts_folder_path, True)
    )
    t5.start()
    print("[+] Started new thread for `save_PostsTagged()`")

    t4 = Thread(target=open_folder, args=(tagged_posts_folder_path,))
    t4.start()

    return redirect(url_for('index'))


@app.route("/save/posts/igtv")
def save_posts_igtv():
    print(texts.IGTV_POSTS)

    if not(os.path.isdir(igtv_posts_folder_path)):
        os.makedirs(igtv_posts_folder_path)
        print(f"[+] Made directory {igtv_posts_folder_path}")

    t7 = Thread(
        target=obj.save_PostsIGTV,
        args=(ORIGINAL_DIR, igtv_posts_folder_path, True)
    )
    t7.start()
    print("[+] Started new thread for `save_PostsIGTV()`")

    t6 = Thread(target=open_folder, args=(igtv_posts_folder_path,))
    t6.start()

    return redirect(url_for('index'))


@app.route("/save/profile/followers")
def save_profile_followers():
    print(texts.FOLLOWERS)

    if not(profile_followers_list_file_json):
        t8 = Thread(
            target=obj.save_FollowersFollowees,
            args=(
                "followers",
                profile_followers_list_file_json,
                "all",
                "json"
            )
        )
        t8.start()
        print("[+] Started new thread for `save_FollowersFollowees()` for `followers`")

    t9 = Thread(target=open_folder, args=(
        current_session_folder_absolute,))
    t9.start()

    return redirect(url_for('index'))


@app.route("/save/profile/followees")
def save_profile_followees():
    print(texts.FOLLOWEES)

    if not(os.path.isfile(profile_followees_list_file_json)):
        t10 = Thread(
            target=obj.save_FollowersFollowees,
            args=(
                "followees",
                profile_followees_list_file_json,
                "all",
                "json"
            )
        )
        t10.start()
        print("[+] Started new thread for `save_FollowersFollowees()` for `followees`")

    t11 = Thread(target=open_folder, args=(
        current_session_folder_absolute,))
    t11.start()

    return redirect(url_for('index'))


@app.route("/save/posts/all")
def save_all_posts():
    def save_info_and_every_post():
        print(texts.SAVE__ALL)

        os.chdir(ORIGINAL_DIR)

        if not(os.path.isfile(information_filename_txt)):
            # Base Profile Info - txt
            # No need for json because its being made by default
            obj.save_ProfileInfo(
                final_filename=information_filename_txt, file_format='txt')
            texts.clear()
            print("[+] Saved profile information")

        # All Posts
        obj.save_PostsUploaded(ORIGINAL_DIR, uploaded_posts_folder_path, True)
        texts.clear()
        obj.save_PostsTagged(ORIGINAL_DIR, tagged_posts_folder_path, True)
        texts.clear()
        obj.save_PostsIGTV(ORIGINAL_DIR, igtv_posts_folder_path, True)
        texts.clear()
        print("[+] Saved Posts")

        # Followers and Followee info if not files already exist
        if not(profile_followers_list_file_json):
            obj.save_FollowersFollowees(
                "followers", profile_followers_list_file_json, "all", "json")
            texts.clear()
            print("[+] Saved Followers")
        if not(os.path.isfile(profile_followees_list_file_json)):
            obj.save_FollowersFollowees(
                "followers", profile_followees_list_file_json, "all", "json")
            texts.clear()
            print("[+] Saved Posts")

        os.chdir(ORIGINAL_DIR)

        print(texts.COMPLETED)
        print("[+] Saved all account information and posts")

    t12 = Thread(target=save_info_and_every_post)
    t12.start()

    t11 = Thread(target=open_folder, args=(
        current_session_folder_absolute,))
    t11.start()

    return redirect(url_for('index'))


@app.route("/open/current")
def open_target_folder():
    t12 = Thread(target=open_folder, args=(current_session_folder_absolute,))
    t12.start()
    print("[+] Opened current target's folder")
    return redirect(url_for('index'))


@app.route("/open/<history>")
def open_history_folder(history):
    for item in final_all_history_list:
        if item['username'] == history:
            t13 = Thread(target=open_folder, args=(item['folder_path'],))
            t13.start()
    print(f"[+] Opened {history} 's history folder")
    return redirect(url_for('index'))


def runWebServer():
    texts.clear()
    print(texts.InstaStalker_Web)
    print(
        f"Opening http://{Database.HOST}:{Database.PORT}/ in your default browser\nIf this did not happen, please open this URL in your browser manually!\n\n")

    t14 = Thread(target=webbrowser.open, args=(
        f"http://localhost:{Database.PORT}/", ))
    t14.start()

    app.run(
        Database.HOST,
        port=int(Database.PORT),
        debug=bool(Database.DEBUG)
    )


if __name__ == "__main__":
    runWebServer()
