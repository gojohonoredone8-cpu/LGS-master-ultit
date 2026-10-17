import json,random,os,sqlite3,datetime,hashlib,math
from validate import validate,similar
BASE=os.path.dirname(os.path.abspath(__file__));os.chdir(BASE)
VERCEL=bool(os.environ.get("VERCEL"))  # sunucusuz: kalıcı disk yok -> her gün tarihe göre deterministik üretim
DB=os.environ.get("LGS_DB","/tmp/lgs.db" if VERCEL else "lgs.db")
def db():
    c=sqlite3.connect(DB);c.row_factory=sqlite3.Row
    c.executescript("""CREATE TABLE IF NOT EXISTS packages(date TEXT PRIMARY KEY,status TEXT,data TEXT,created TEXT);
    CREATE TABLE IF NOT EXISTS logs(id INTEGER PRIMARY KEY,ts TEXT,msg TEXT);
    CREATE TABLE IF NOT EXISTS review(qid TEXT PRIMARY KEY,status TEXT);""");return c
def log(c,m): c.execute("INSERT INTO logs(ts,msg) VALUES(?,?)",(datetime.datetime.now().isoformat(),m));c.commit()
def mk(r,text,ans,kon,sol,fmt=str,dist=None):
    d=dist or [ans+k for k in (-2,-1,1,2,3,-3)]
    opts=[ans]+[x for x in dict.fromkeys(d) if x!=ans][:3];r.shuffle(opts)
    return {"ders":"Matematik","konu":kon,"soru":text,"secenekler":[fmt(x) for x in opts],"dogru":opts.index(ans),"cozum":sol,"dogru_deger":fmt(ans),"zorluk":"orta"}
def math_q(r):
    t=r.randrange(6)
    if t==0:
        x=r.randint(2,15);a=r.randint(2,9);b=r.randint(1,20)
        return mk(r,f"{a}x + {b} = {a*x+b} denklemini sağlayan x değeri kaçtır?",x,"Doğrusal Denklemler",f"{a}x = {a*x+b}-{b} = {a*x}, x = {x}.")
    if t==1:
        a=r.randint(2,5);n=r.randint(2,4);m=r.randint(2,4)
        return mk(r,f"{a}^{n} · {a}^{m} işleminin sonucu kaçtır?",a**(n+m),"Üslü İfadeler",f"Taban aynı, üsler toplanır: {a}^{n+m} = {a**(n+m)}.",dist=[a**(n*m),a**(n+m)+a,a**(n+m)-a,a**(n+m)*2])
    if t==2:
        k=r.randint(2,9);a=r.randint(2,6)
        return mk(r,f"√{k*k*a} ifadesi k√{a} biçiminde yazılırsa k kaçtır?",k,"Kareköklü İfadeler",f"√{k*k*a} = √{k*k}·√{a} = {k}√{a}.")
    if t==3:
        p=r.choice([10,20,25,40,50]);n=r.choice([40,60,80,120,200])
        return mk(r,f"{n} sayısının %{p}'si kaçtır?",n*p//100,"Veri Analizi",f"{n}·{p}/100 = {n*p//100}.") if n*p%100==0 else math_q(r)
    if t==4:
        a=r.randint(3,12);b=r.randint(3,12);c=math.isqrt(a*a+b*b)
        return math_q(r) if c*c!=a*a+b*b else mk(r,f"Dik kenar uzunlukları {a} cm ve {b} cm olan dik üçgenin hipotenüsü kaç cm'dir?",c,"Üçgenler",f"{a}²+{b}²={c*c}, hipotenüs={c}.")
    x=r.randint(2,9);y=r.randint(2,9)
    return mk(r,f"x + y = {x+y} ve x - y = {x-y} ise x·y kaçtır?",x*y,"Cebirsel İfadeler ve Özdeşlikler",f"x={x}, y={y}; x·y={x*y}.")
def llm_questions(ders,konu,n):
    key=os.environ.get("ANTHROPIC_API_KEY")
    if not key: return []
    import urllib.request
    def call(p):
        rq=urllib.request.Request("https://api.anthropic.com/v1/messages",json.dumps({"model":os.environ.get("LGS_MODEL","claude-sonnet-4-6"),"max_tokens":3000,"messages":[{"role":"user","content":p}]}).encode(),{"x-api-key":key,"anthropic-version":"2023-06-01","content-type":"application/json"})
        return json.load(urllib.request.urlopen(rq,timeout=90))["content"][0]["text"]
    try:
        t=call(f"8. sınıf LGS {ders} / {konu}: {n} ÖZGÜN yeni nesil çoktan seçmeli soru. SADECE JSON dizi: [{{\"soru\",\"secenekler\"(4),\"dogru\"(0-3 indeks),\"cozum\"}}]")
        out=[]
        for q in json.loads(t[t.index("["):t.rindex("]")+1]):
            # Bağımsız doğrulama: cevabı vermeden yeniden çöz
            v=call("Soruyu çöz, SADECE doğru seçenek indeksini (0-3) yaz.\n"+q["soru"]+"\n"+"\n".join(f"{i}: {s}" for i,s in enumerate(q["secenekler"])))
            if v.strip()[:1]==str(q["dogru"]): q.update(ders=ders,konu=konu,zorluk="orta",kaynak="llm-dogrulandi");out.append(q)
        return out
    except Exception as e: return []
def build(date=None,per_subject=10):
    date=date or datetime.date.today().isoformat();c=db()
    if c.execute("SELECT 1 FROM packages WHERE date=?",(date,)).fetchone(): return "mevcut"
    r=random.Random(int(hashlib.md5(date.encode()).hexdigest(),16))
    cur=json.load(open("data/curriculum.json",encoding="utf-8"))["dersler"];seed=json.load(open("data/seed.json",encoding="utf-8"))
    past=[] if VERCEL else [q["soru"]+" "+" ".join(q["secenekler"]) for row in c.execute("SELECT data FROM packages WHERE status='ok'") for q in json.loads(row["data"])["sorular"]]
    qs=[]
    for ders in cur:
        got=[];tries=0
        pool=[] if ders=="Matematik" or VERCEL else llm_questions(ders,r.choice(cur[ders]),per_subject)
        import extra
        if ders!="Matematik": pool+=extra.make(ders,r,per_subject*2)
        pool+=[dict(s,kaynak="seed") for s in seed if s["ders"]==ders]
        while len(got)<per_subject and tries<400:
            tries+=1
            q=math_q(r) if ders=="Matematik" else (pool.pop(0) if pool else None)
            if q is None: break
            if validate(q) or any(similar(q["soru"]+" "+" ".join(q["secenekler"]),p) for p in past+[g["soru"]+" "+" ".join(g["secenekler"]) for g in got]): continue
            q.pop("verify",None);q.setdefault("zorluk","orta");q["id"]=hashlib.md5((date+q["soru"]+"|".join(q["secenekler"])).encode()).hexdigest()[:10];q["kontrol"]="otomatik";got.append(q)
        qs+=got
    if not qs: log(c,"HATA: soru yok");return "hata"
    try:
        import pdfgen;files=pdfgen.make(date,qs)
        pdfgen.verify(files,qs)
    except Exception as e:
        log(c,f"PDF HATA {e}")
        if not VERCEL: return "hata"   # yerelde bozuk paket yayımlanmaz
        files=[]                       # Vercel'de sorular yine de yayımlanır, PDF yok
    sayi={d:sum(q["ders"]==d for q in qs) for d in cur}
    c.execute("INSERT INTO packages VALUES(?,?,?,?)",(date,"ok",json.dumps({"sorular":qs,"sayi":sayi,"pdf":files},ensure_ascii=False),datetime.datetime.now().isoformat()));c.commit()
    log(c,f"{date}: {len(qs)} soru, {len(files)} pdf yayimlandi");return "ok"
if __name__=="__main__": print(build())
