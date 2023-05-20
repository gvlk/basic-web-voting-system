# Guilherme Azambuja
# https://github.com/gvlk/basic-web-voting-system

from csv import reader, writer

from flask import Flask, render_template, request

app = Flask(__name__)

CSV_FILENAME = "votes.csv"


@app.route("/")
def main() -> str:
    return render_template("index.html")


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

    with open('votes.csv', 'w', newline='') as csvfile:
        csv_writer = writer(csvfile)
        csv_writer.writerows(data)

    return render_template("results.html", data=data[1:])


if __name__ == '__main__':
    app.run()
