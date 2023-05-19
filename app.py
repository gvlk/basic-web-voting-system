from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def main() -> str:
    if request.method == "POST":
        return render_template("")
    else:
        return render_template("index.html")


if __name__ == '__main__':
    app.run()
