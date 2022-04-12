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
        # accinfo=accinfo,
        # profile_image="file://" + os.path.join(os.getcwd(), "profilepic")
    )


def runWebServer():
    app.run(
        Database.HOST,
        port=int(Database.PORT),
        debug=bool(Database.DEBUG)
    )


if __name__ == "__main__":
    runWebServer()
