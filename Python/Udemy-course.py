import pymysql
from flask import Flask, jsonify, request, make_response

app = Flask(__name__)

my_db = pymysql.connect(
    host="localhost",
    user="root",
    password="",
    database="db_sekolah"
)

@app.route("/")
def index():
    return "<h1>belajar flask python dasar</h1>"

@app.route("/ambil_data_siswa", methods=["GET"])
def abmil_data_siswa():
    query = "SELECT * FROM table_siswa WHERE 1=1"
    value = ()

    nis = request.args.get("nis")
    nama = request.args.get("nama")
    umur = request.args.get("umur")
    alamat = request.args.get("alamat")

    if nis:
        query += " AND nis = %s"
        value += (nis,)
    if nama:
        query += " AND nama = %s"
        value += ("%"+nama+"%",)
    if umur:
        query += " AND umur = %s"
        value += (umur,)
    if alamat:
        query += " AND alamat = %s"
        value += (alamat,)

    cursor = my_db.cursor()
    cursor.execute(query, value)
    hasil = cursor.fetchall()
    
    row_header = [x[0] for x in cursor.description]
    json_data = []
    for result in hasil:
        json_data.append(dict(zip(row_header, result)))

    return make_response(jsonify(json_data), 200)


@app.route("/masukkan_data_siswa", methods=["POST"])
def masukkan_data_siswa():
    hasil = {"status": "gagal masukkan data siswa"}

    try:
        data = request.json
        query = "INSERT INTO table_siswa(nis, nama, umur, alamat) VALUE(%s, %s, %s, %s)"
        cursor = my_db.cursor()
        cursor.execute(query, (data["nis"], data["nama"], data["umur"], data["alamat"]))
        my_db.commit()
        hasil["status"] = "berhasil masukkan data siswa"
    
    except Exception as e:
        print(e)

    return jsonify(hasil)

@app.route("/ubah_data_siswa", methods=["PUT"])
def ubah_data_siswa():
    hasil = {"status": "gagal ubah data siswa"}

    try:
        data = request.json
        query = "UPDATE table_siswa SET nis = %s, nama = %s, umur = %s, alamat = %s WHERE id = %s"
        cursor = my_db.cursor()
        cursor.execute(query, (data["nis"], data["nama"], data["umur"], data["alamat"], data["id"]))
        my_db.commit()
        hasil["status"] = "berhasil ubah data siswa"
    
    except Exception as e:
        print(e)

    return jsonify(hasil)

@app.route("/hapus_data_siswa", methods=["DELETE"])
def hapus_data_siswa():
    hasil = {"status": "gagal hapus data siswa"}

    try:
        data = request.json
        query = "DELETE FROM table_siswa WHERE id = %s"
        cursor = my_db.cursor()
        cursor.execute(query, (data["id"],))
        my_db.commit()
        hasil["status"] = "berhasil hapus data siswa"
    
    except Exception as e:
        print(e)

    return jsonify(hasil)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=5000)