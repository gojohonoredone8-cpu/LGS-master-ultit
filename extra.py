"""API anahtarı olmadan 5 ders için günlük farklı soru üretimi: parametrik (Fen, İngilizce, Türkçe yazım) + olgu tabloları (İnkılap, Din)."""
import random
def Q(r,ders,konu,soru,ans,dist,cozum):
    ans=str(ans);dist=[str(x) for x in dist]
    o=[ans]+[d for d in dict.fromkeys(dist) if d!=ans][:3];r.shuffle(o)
    return {"ders":ders,"konu":konu,"soru":soru,"secenekler":o,"dogru":o.index(ans),"cozum":cozum,"kaynak":"sablon"} if len(o)==4 else None
TARIH=[("Samsun'a çıkış","19 Mayıs 1919"),("Amasya Genelgesi'nin yayımlanması","22 Haziran 1919"),("Erzurum Kongresi'nin toplanması","23 Temmuz 1919"),("Sivas Kongresi'nin toplanması","4 Eylül 1919"),("Misak-ı Millî'nin kabulü","28 Ocak 1920"),("TBMM'nin açılması","23 Nisan 1920"),("Mudanya Ateşkesi'nin imzalanması","11 Ekim 1922"),("Lozan Antlaşması'nın imzalanması","24 Temmuz 1923"),("Cumhuriyet'in ilanı","29 Ekim 1923"),("Halifeliğin kaldırılması","3 Mart 1924"),("Medeni Kanun'un kabulü","17 Şubat 1926"),("Harf İnkılabı'nın kabulü","1 Kasım 1928"),("Soyadı Kanunu'nun kabulü","21 Haziran 1934"),("Kadınlara milletvekili seçme ve seçilme hakkının verilmesi","5 Aralık 1934"),("Büyük Taarruz'un başlaması","26 Ağustos 1922")]
DIN=[("Kur'an-ı Kerim kaç sûreden oluşur?","114"),("İslam'ın şartları kaç tanedir?","5"),("Günde kaç vakit farz namaz kılınır?","5"),("Peygamberimize inen ilk âyetler hangi sûrededir?","Alak"),("Hz. Muhammed'in doğduğu şehir neresidir?","Mekke"),("Hicret hangi şehre yapılmıştır?","Medine"),("Hz. Muhammed'in güvenilirliği nedeniyle verilen lakap hangisidir?","el-Emin"),("Zekât hangi ibadet türüne girer?","Malî ibadet"),("Fıtır sadakası hangi bayramdan önce verilir?","Ramazan Bayramı"),("Hacda Arafat'ta bulunmaya ne denir?","Vakfe")]
DIN_Y=["Hacc","Umre","Sa'y","Mekke","Tevekkül","Bedenî ibadet","Kurban Bayramı","Küfe","7","3","30","99"]
ADJ=[("tall","taller","tallest"),("big","bigger","biggest"),("happy","happier","happiest"),("good","better","best"),("bad","worse","worst"),("hot","hotter","hottest"),("easy","easier","easiest"),("far","farther","farthest"),("expensive","more expensive","most expensive"),("interesting","more interesting","most interesting")]
VERB=[("go","went"),("see","saw"),("eat","ate"),("take","took"),("buy","bought"),("write","wrote"),("come","came"),("give","gave"),("run","ran"),("drink","drank"),("teach","taught"),("bring","brought")]
YAZIM=[("yanlış","yalnış"),("herkes","herkez"),("şoför","şöför"),("yalnız","yanlız"),("birçok","bir çok"),("hiçbir","hiç bir"),("kırgın","kırğın"),("orijinal","orjinal"),("egzoz","egzos"),("mağaza","mağza"),("sürpriz","sürpiz"),("meşgul","meşkul"),("istatistik","istatik"),("pazartesi","pazar tesi")]
def make(ders,r,n):
    out=[]
    for _ in range(n*3):
        q=None
        if ders=="İnkılap Tarihi":
            o,t=r.choice(TARIH);q=Q(r,ders,"Milli Mücadele ve Cumhuriyet",f"{o} hangi tarihte gerçekleşmiştir?",t,[x[1] for x in r.sample(TARIH,5)],f"Kronolojiye göre {o}: {t}.")
        elif ders=="Din Kültürü":
            s,a=r.choice(DIN);q=Q(r,ders,"Temel Dinî Bilgiler",s,a,[x[1] for x in r.sample(DIN,5)]+DIN_Y,f"Doğru cevap: {a}.")
        elif ders=="Fen Bilimleri":
            t=r.randrange(3)
            if t==0:
                A=r.choice([2,4,5,10]);F=r.choice([20,40,50,100,200]);p=F//A
                q=Q(r,ders,"Basınç",f"Yüzey alanı {A} m² olan zemine {F} N'luk kuvvet dik olarak etki ediyor. Basınç kaç Pa'dır?",p,[p*A,p+A,p*2,F*A,p//2 or 1],f"P = F/A = {F}/{A} = {p} Pa.")
            elif t==1:
                v=r.choice([2,4,5,8]);V=r.choice([5,10,20,25]);m=v*V
                q=Q(r,ders,"Madde ve Endüstri",f"Kütlesi {m} g, hacmi {V} cm³ olan maddenin özkütlesi kaç g/cm³'tür?",v,[V,m,v+1,v*2,max(v-1,1)],f"d = m/V = {m}/{V} = {v} g/cm³.")
            else:
                s=r.choice([5,10,20,30]);tm=r.choice([2,4,6]);x=s*tm
                q=Q(r,ders,"Enerji Dönüşümleri",f"Sabit hızla {x} m yolu {tm} s'de alan cismin hızı kaç m/s'dir?",s,[x,tm,s+tm,s*2,max(s-5,1)],f"v = x/t = {x}/{tm} = {s} m/s.")
        elif ders=="İngilizce":
            if r.random()<.5:
                a,c,s=r.choice(ADJ);k=r.choice([1,2])
                txt=f'Complete: "This is the ___ {"one" if k else "thing"} I have seen." ({a})' if k==1 else f'Complete: "My brother is ___ than me." ({a})'
                ans=s if k==1 else c;q=Q(r,ders,"Friendship",txt,ans,[a,c,s,"more "+a,"most "+a],f"'than' -> comparative ({c}); 'the ... I have seen' -> superlative ({s}).")
            else:
                v,p=r.choice(VERB);q=Q(r,ders,"Teen Life",f'Complete: "Yesterday, she ___ to school early." ({v})' if v=="go" else f'Choose the past form of "{v}".',p,[v,v+"ed",v+"s",v+"ing"],f"'{v}' fiilinin ikinci hâli '{p}'.")
        elif ders=="Türkçe":
            d,y=r.choice(YAZIM);q=Q(r,ders,"Yazım ve Noktalama","Aşağıdakilerden hangisi doğru yazılmıştır?",d,[z[1] for z in r.sample(YAZIM,5)],f"Doğru yazım: {d}.")
            if q: q["secenekler"]=q["secenekler"]
        if q: out.append(q)
    return out
