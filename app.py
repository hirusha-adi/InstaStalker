from flask import Flask, render_template
from manager import Manager
app = Flask(__name__)


@app.route("/")
def index():
    obj = Manager("")
    obj.login()
    obj.processProfile()
    accinfo = obj.getProfileInfo()

    return render_template(
        "index.html",
        accinfo=accinfo
    )


app.run("0.0.0.0", port=8080, debug=True)
