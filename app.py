from flask import Flask, render_template
from manager import InstaProfile, Database
import requests
import os

app = Flask(__name__)


targte_username = "hirushaadi"

# obj = InstaProfile()
# obj.setTARGET("hirushaadi")
# obj.login(username=Database.USERNAME, password=Database.PASSWORD)

# Main Account Info
print("[*] Please wait while target's profile information is being loaded")
# accinfo = obj.getProfileInfo()
print("[+] Loaded all basic target's profile information!")


@app.route("/")
def index():
    return render_template(
        "index.html",
        accinfo={
            'followers': 300,
            'followees': 1500,
            'mediacount': 1000,
            'full_name': "Hirusha Adikari",
            'username': 'hirushaadi',
            'profile_pic_url': "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8d/KDE_logo.svg/1200px-KDE_logo.svg.png",
            'sample': ''
        }
    )


def runWebServer():
    app.run(
        Database.HOST,
        port=int(Database.PORT),
        debug=bool(Database.DEBUG)
    )


if __name__ == "__main__":
    runWebServer()
