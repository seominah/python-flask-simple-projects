from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.lifequotes


@app.route('/')
def home():
    return render_template('index.html')


@app.route("/homework", methods=["POST"])
def homework_post():
    nickname_receive = request.form['nickname_give']
    comment_receive = request.form['comment_give']
    doc = {
        'nickname': nickname_receive,
        'comment': comment_receive
    }
    db.lifequotes.insert_one(doc)
    return jsonify({'msg': '등록 완료!'})


@app.route("/homework", methods=["GET"])
def homework_get():
    life_quotes_list = list(db.lifequotes.find({}, {'_id': False}))
    return jsonify({'life_quotes': life_quotes_list})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)
