from flask import Flask, render_template
from manager import InstaProfile, Database
app = Flask(__name__)


obj = InstaProfile()
obj.setTARGET("ac3.desu")
obj.login(username=Database.USERNAME, password=Database.PASSWORD)
obj.processProfile()
accinfo = obj.getProfileInfo()


@app.route("/")
def index():
    return render_template(
        "index.html",
        accinfo=accinfo
    )


@app.route("/followers")
def followers():
    obj.saveFollowers()
    return "Done"


@app.route("/followees")
def followees():
    obj.saveFollowees()
    return "Done"


@app.route("/posts")
def download_posts():
    obj.savePosts()
    return "Done!"


@app.route("/tagged")
def download_tagged_posts():
    obj.saveAllTaggedPosts()
    return "Done!"


@app.route("/igtv")
def download_igtv_posts():
    obj.saveAllIGTVPosts()
    return "Done!"


@app.route("/posts/all")
def download_all_posts():
    obj.saveAllPosts()
    return "Done!"


@app.route("/profile")
def download_profile_info():
    obj.saveProfileInfo()
    return "Done!"


@app.route("/all")
def download_all():
    obj.saveAll()
    return "Done!"


def runWebServer():
    app.run(
        Database.HOST,
        port=int(Database.PORT),
        debug=bool(Database.DEBUG)
    )


if __name__ == "__main__":
    runWebServer()
