import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import simpleSplit
PDFS=os.environ.get("LGS_PDFS") or ("/tmp/pdfs" if os.environ.get("VERCEL") else "pdfs")
F=os.path.join(os.path.dirname(__file__),"fonts")
def _font():
    for d in (F,"/usr/share/fonts/truetype/dejavu","/usr/share/fonts/dejavu"):
        a,b=os.path.join(d,"DejaVuSans.ttf"),os.path.join(d,"DejaVuSans-Bold.ttf")
        if os.path.exists(a) and os.path.exists(b):
            pdfmetrics.registerFont(TTFont("D",a));pdfmetrics.registerFont(TTFont("DB",b));return
    raise RuntimeError("DejaVuSans.ttf bulunamadi (fonts/ klasoru yuklenmemis)")
_font()
def _doc(path,title,items):
    c=canvas.Canvas(path,pagesize=A4);W,H=A4;y=H-60
    def head():
        c.setFont("DB",14);c.drawString(50,H-40,title);c.setFont("D",9)
    head()
    for blk in items:
        lines=[l for t in blk for l in simpleSplit(t,"D",10,W-100)]
        if y-len(lines)*14<60: c.setFont("D",8);c.drawString(W/2-20,30,f"Sayfa {c.getPageNumber()}");c.showPage();head();y=H-60
        c.setFont("D",10)
        for l in lines: c.drawString(50,y,l);y-=14
        y-=8
    c.setFont("D",8);c.drawString(W/2-20,30,f"Sayfa {c.getPageNumber()}");c.save()
def make(date,qs):
    os.makedirs(f"{PDFS}/{date}",exist_ok=True);L="ABCD"
    a=[[f"{i}. [{q['ders']} · {q['konu']}] {q['soru']}"]+[f"   {L[j]}) {o}" for j,o in enumerate(q["secenekler"])] for i,q in enumerate(qs,1)]
    b=[[f"{i}. Cevap: {L[q['dogru']]}",f"   Çözüm: {q['cozum']}"] for i,q in enumerate(qs,1)]
    p1,p2=f"{PDFS}/{date}/soru_kitapcigi.pdf",f"{PDFS}/{date}/cevap_anahtari.pdf"
    _doc(p1,f"LGS MASTER · {date} · Soru Kitapçığı",a);_doc(p2,f"LGS MASTER · {date} · Cevap Anahtarı ve Çözümler",b);return [p1,p2]
def verify(files,qs):
    from pypdf import PdfReader
    t=[]
    for f in files:
        r=PdfReader(f);assert len(r.pages)>=1 and os.path.getsize(f)>1000
        t.append("".join(p.extract_text() for p in r.pages))
        assert all(p.extract_text().strip() for p in r.pages),"bos sayfa"
    flat=lambda s:"".join(s.split())
    assert all(flat(q["secenekler"][0])[:15] in flat(t[0]) for q in qs),"soru metni eslesmiyor"
    assert all(f"{i}.Cevap:{'ABCD'[q['dogru']]}" in flat(t[1]) for i,q in enumerate(qs,1)),"cevap anahtari eslesmiyor"
