from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

DB_PATH = "papara.db"  # GitHub'dan çekip Render klasörüne koyduğun .db

def normalize(text):
    """Büyük harfe çevir ve baş/son boşlukları kırp."""
    return text.upper().strip()

def query_db(query, params=()):
    """SQLite sorgusu çalıştır ve dict listesi döndür."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # dict gibi erişim
    cur = conn.cursor()
    cur.execute(query, params)
    rows = [dict(row) for row in cur.fetchall()]
    conn.close()
    return rows

@app.route("/")
def home():
    return {"status": "ok", "message": "Papara API aktif"}

# 1️⃣ Papara no ile sorgu
@app.route("/paparano")
def paparano_sorgu():
    paparano = request.args.get("paparano")
    if not paparano:
        return {"error": "paparano parametresi eksik"}
    sonuc = query_db("SELECT * FROM papara WHERE paparano = ?", (paparano,))
    return jsonify(sonuc)

# 2️⃣ Ad ile sorgu
@app.route("/ad")
def ad_sorgu():
    ad = request.args.get("ad")
    if not ad:
        return {"error": "ad parametresi eksik"}
    ad = normalize(ad)
    sonuc = query_db("SELECT * FROM papara")
    sonuc = [x for x in sonuc if ad in normalize(x["adsoyad"])]
    return jsonify(sonuc)

# 3️⃣ Soyad ile sorgu
@app.route("/soyad")
def soyad_sorgu():
    soyad = request.args.get("soyad")
    if not soyad:
        return {"error": "soyad parametresi eksik"}
    soyad = normalize(soyad)
    sonuc = query_db("SELECT * FROM papara")
    sonuc = [x for x in sonuc if soyad in normalize(x["adsoyad"])]
    return jsonify(sonuc)

# 4️⃣ Ad + Soyad ile sorgu
@app.route("/adsoyad")
def adsoyad_sorgu():
    ad = request.args.get("ad")
    soyad = request.args.get("soyad")
    if not ad or not soyad:
        return {"error": "ad ve soyad parametreleri gerekli"}
    ad = normalize(ad)
    soyad = normalize(soyad)
    sonuc = query_db("SELECT * FROM papara")
    sonuc = [x for x in sonuc if ad in normalize(x["adsoyad"]) and soyad in normalize(x["adsoyad"])]
    return jsonify(sonuc)

if __name__ == "__main__":
    # Render default port
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
