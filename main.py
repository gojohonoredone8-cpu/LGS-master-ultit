import json,os,datetime,hmac
from flask import Flask,jsonify,request,send_file,render_template,abort,Response
import gen,re
PDFS=os.environ.get('LGS_PDFS') or ('/tmp/pdfs' if os.environ.get('VERCEL') else 'pdfs')
app=Flask(__name__)
def today_tr(): return (datetime.datetime.utcnow()+datetime.timedelta(hours=3)).date().isoformat()
def pkg(date=None):
    if not date: date=today_tr()
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}",date) or date>today_tr(): return None,None
    gen.build(date)  # varsa "mevcut" döner; yoksa üretir (Vercel'de ilk istekte)
    c=gen.db()
    row=c.execute("SELECT * FROM packages WHERE date=?",(date,)).fetchone() if date else c.execute("SELECT * FROM packages WHERE status='ok' ORDER BY date DESC").fetchone()
    return (row["date"],json.loads(row["data"])) if row else (None,None)
def admin_ok():
    a=request.authorization;pw=os.environ.get("ADMIN_PASSWORD")
    return bool(pw and a and hmac.compare_digest(a.password,pw))
@app.route("/")
def home(): return render_template("index.html")
@app.route("/api/package")
def api_package():
    d,p=pkg(request.args.get("date"))
    if not p: return jsonify(error="paket yok"),404
    qs=[{k:q[k] for k in("id","ders","konu","soru","secenekler","zorluk")} for q in p["sorular"]]  # cevap yok
    return jsonify(date=d,sayi=p["sayi"],sorular=qs,mufredat=json.load(open("data/curriculum.json",encoding="utf-8"))["dersler"],arsiv=[(datetime.date.fromisoformat(d)-datetime.timedelta(days=i)).isoformat() for i in range(7)])
@app.route("/api/check",methods=["POST"])
def check():
    j=request.get_json(silent=True) or {};d,p=pkg(j.get("date"))
    if not p or not isinstance(j.get("cevaplar"),dict): abort(400)
    out=[]
    for q in p["sorular"]:
        a=j["cevaplar"].get(q["id"]);out.append({"id":q["id"],"ders":q["ders"],"soru":q["soru"],"secenekler":q["secenekler"],"verilen":a if a in(0,1,2,3) else None,"dogru":q["dogru"],"cozum":q["cozum"]})
    return jsonify(out)
@app.route("/pdf/<date>/<kind>")
def pdf(date,kind):
    if kind not in("soru_kitapcigi","cevap_anahtari") or not all(ch.isdigit() or ch=="-" for ch in date): abort(404)
    pkg(date);f=f"{PDFS}/{date}/{kind}.pdf"
    return send_file(f,mimetype="application/pdf") if os.path.exists(f) else abort(404)
@app.route("/api/cron/<token>")
def cron(token):  # harici zamanlayıcı (cron-job.org vb.) için; ayrıca TR saati
    if not hmac.compare_digest(token,os.environ.get("CRON_TOKEN","x!")): abort(403)
    today=(datetime.datetime.utcnow()+datetime.timedelta(hours=3)).date().isoformat()
    return jsonify(sonuc=gen.build(today))
@app.route("/admin")
def admin():
    if not admin_ok(): return Response("Yetki gerekli",401,{"WWW-Authenticate":'Basic realm="admin"'})
    c=gen.db();last=c.execute("SELECT date,created FROM packages ORDER BY date DESC LIMIT 1").fetchone()
    logs=[dict(r) for r in c.execute("SELECT ts,msg FROM logs ORDER BY id DESC LIMIT 30")]
    return jsonify(son_basarili=dict(last) if last else None,sonraki_gorev="her gün 06:00 Europe/Istanbul",loglar=logs)
if __name__=="__main__": app.run(debug=False,port=5000)
