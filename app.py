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


def runWebServer():
    app.run(
        Database.HOST,
        port=int(Database.PORT),
        debug=bool(Database.DEBUG)
    )


if __name__ == "__main__":
    runWebServer()
