from flask import Flask, render_template
from manager import Manager, Database
app = Flask(__name__)


obj = Manager()
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


@app.route("/download/posts")
def download_posts():
    obj.savePosts()
    return "Done!"


@app.route("/download/tagged")
def download_tagged_posts():
    obj.saveAllTaggedPosts()
    return "Done!"


@app.route("/download/igtv")
def download_igtv_posts():
    obj.saveAllIGTVPosts()
    return "Done!"


@app.route("/download/posts/all")
def download_all_posts():
    obj.saveAllPosts()
    return "Done!"


@app.route("/download/profile")
def download_profile_info():
    obj.saveProfileInfo()
    return "Done!"


@app.route("/download/all")
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
