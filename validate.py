import re
def validate(q):
    err=[]
    o=q.get("secenekler",[])
    if len(o)!=4: err.append("4 secenek olmali")
    if len(set(map(str,o)))!=len(o): err.append("tekrarlayan secenek")
    if q.get("dogru") not in (0,1,2,3): err.append("dogru indeks gecersiz")
    if len(q.get("soru",""))<15: err.append("soru kisa")
    if not q.get("cozum"): err.append("cozum yok")
    if "verify" in q and q["verify"]() != q.get("dogru_deger"): err.append("matematik dogrulama basarisiz")
    return err
def norm(t): return set(re.findall(r"\w+",t.lower()))
def similar(a,b,th=0.8):
    A,B=norm(a),norm(b)
    return bool(A and B) and len(A&B)/len(A|B)>=th
