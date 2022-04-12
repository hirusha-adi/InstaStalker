from flask import Flask, render_template
from manager import InstaProfile, Database
import requests
import os
import json

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


@ app.route("/")
def index():
    return render_template(
        "index.html",
        accinfo=accinfo,
    )


def runWebServer():
    app.run(
        Database.HOST,
        port=int(Database.PORT),
        debug=bool(Database.DEBUG)
    )


if __name__ == "__main__":
    runWebServer()
