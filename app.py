# import library yang dibutuhkan
import os
from os.path import join, dirname
from dotenv import load_dotenv

from flask import Flask, render_template, request, jsonify
import certifi
ca = certifi.where()
from pymongo import MongoClient
from random import random

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# varibale untuk menampung link database mongoDB yang nantinya akan disimpan pada .env di glitch
MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME =  os.environ.get("DB_NAME")


client = MongoClient(MONGODB_URI, tlsCAFile=ca)
db = client[DB_NAME]

app = Flask(__name__)

# pada route ('/') atau home akan menampilkan file index.html yang terdapat pada folder templates
@app.route('/')
def home():
   return render_template('index.html')

@app.route("/bucket", methods=["POST"])
def bucket_post():
    # membuat variable untuk menampung input user yang sudah disimpan pada data bucket_give di sisi client
    bucket_receive = request.form['bucket_give']
    # variable untuk membuat data yang unik pada setiap datanya agar lebih presisi saat akan dipakai untuk parameter dalam menjalankan function di sisi client
    count = db.bucket.count_documents({})
    # variable num berisi panjang dari data pada database, ditambah angka random yang memiliki tipe data float yang digenerate function random()
    num = count + random()
    # menyusun data dalam bentuk dictionary python dengan key value pair untuk diinput ke dalam database
    doc = {
        'num': num,
        'bucket': bucket_receive,
        'done': 0
    }
    # menginput variable doc yang berisi data ke dalam database collection bucket
    db.bucket.insert_one(doc)
    return jsonify({'msg': 'data saved!'})

@app.route("/bucket/done", methods=["POST"])
def bucket_done():
    # membuat variable untuk mengambil data dari variable num_give yang terdapat pada sisi client(berisi angka unik yang menjadi parameter pada data list yang dipilih)
    num_receive = request.form['num_give']
    # memperbaharui data dengan key 'done' menjadi 1, pada data dalam database yang memiliki key 'num' = variable num_reveive
    db.bucket.update_one(
        {'num': float(num_receive)},
        {'$set': {'done': 1 }}
    )
    return jsonify({'msg': 'Update done!'})

@app.route("/delete", methods=["POST"])
def bucket_delete():
    num_receive = request.form['num_give']
    # menghapus data dengan key 'num' = variable num_reveive pada data dalam database
    db.bucket.delete_one({'num' : float(num_receive)})
    return jsonify({'msg': 'Delete done!'})

@app.route("/bucket", methods=["GET"])
def bucket_get():
    # variable untuk menampung semua data list pada database, keculai yang memiliki key _id. dan memasukannya ke dalam Object 'buckets' json
    buckets_list = list(db.bucket.find({},{'_id': False}))
    return jsonify({'buckets': buckets_list})

if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)
