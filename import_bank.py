"""Kendi/öğretmen yazdığınız soruları ekler: python import_bank.py sorular.json
Biçim: [{"ders","konu","soru","secenekler":[4],"dogru":0-3,"cozum"}]"""
import json,sys
from validate import validate
new=json.load(open(sys.argv[1],encoding="utf-8"));seed=json.load(open("data/seed.json",encoding="utf-8"));ok=0
for q in new:
    e=validate(q)
    if e: print("REDDEDİLDİ:",q.get("soru","")[:40],e)
    else: seed.append(q);ok+=1
json.dump(seed,open("data/seed.json","w",encoding="utf-8"),ensure_ascii=False,indent=1);print(ok,"soru eklendi")
