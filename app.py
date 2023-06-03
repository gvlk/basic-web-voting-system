# Guilherme Azambuja
# https://github.com/gvlk/basic-web-voting-system

from csv import reader, writer

from flask import Flask, render_template, request, make_response, Response, redirect

app = Flask(__name__)

CSV_FILENAME = "votes.csv"


@app.route("/")
def main() -> str:
    username = request.cookies.get("username")
    if username is None:
        return render_template("index.html")
    else:
        userpic = request.cookies.get("userpic")
        if userpic == "monster1":
            userpic_path = "../static/images/monster1.png"
        elif userpic == "monster2":
            userpic_path = "../static/images/monster2.png"
        else:
            userpic_path = "../static/images/monster3.png"
        userclrm = request.cookies.get("userclrm")
        return render_template("voting.html", username=username, userpic_path=userpic_path, userclrm=userclrm)


@app.route("/login", methods=['POST'])
def save_login() -> Response:
    name = request.form['name']
    password = request.form['password']
    response = make_response(render_template("user_cfg.html", username=name))
    response.set_cookie("username", name)
    response.set_cookie("userpswd", password)
    return response


@app.route("/logout")
def delete_cookie() -> Response:
    response = make_response(redirect("/"))
    response.set_cookie("username", "", expires=0)
    response.set_cookie("userpswd", "", expires=0)
    response.set_cookie("userclrm", "", expires=0)
    response.set_cookie("userpic", "", expires=0)
    return response


@app.route("/save_user_cfg", methods=['POST'])
def vote_page() -> Response:
    username = request.form['name']
    userpic = request.form['profile_pic']
    userclrm = request.form['color_mode']
    response = make_response(redirect("/"))
    response.set_cookie("username", username)
    response.set_cookie("userpic", userpic)
    response.set_cookie("userclrm", userclrm)
    return response


@app.route("/vote", methods=['POST'])
def vote() -> str:
    data = list()
    with open(CSV_FILENAME, "r") as file:
        csv_reader = reader(file)
        for i, row in enumerate(csv_reader):
            if i == 0:
                data.append(row)
                continue
            data.append([row[0], int(row[1])])

    option = int(request.form['option'][-1])
    data[option][1] += 1

    with open(CSV_FILENAME, 'w', newline='') as csvfile:
        csv_writer = writer(csvfile)
        csv_writer.writerows(data)

    return render_template("results.html", data=data[1:])


if __name__ == '__main__':
    app.run()
