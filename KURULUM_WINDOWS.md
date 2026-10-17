# LGS MASTER – Windows Kurulum Rehberi
Gerekli: Python 3.10+ (python.org, kurarken "Add to PATH" işaretleyin).
1. ZIP'i açın, klasörde CMD açın.
2. `pip install -r requirements.txt`
3. `set ADMIN_PASSWORD=sifreniz` ve `set CRON_TOKEN=uzun-rastgele-metin`
4. İlk paket: `python gen.py`
5. Site: `python app.py` → http://localhost:5000
6. Test: `pip install pytest` → `python -m pytest tests`
7. Windows'ta her gün 06:00: Görev Zamanlayıcı → Temel Görev → günlük 06:00 → program `python`, argüman `gen.py`, "Başlangıç yeri" = proje klasörü. (PC o saatte açık olmalı; "kaçırılan görevi sonra çalıştır" işaretleyin.)

## İnternete yayın (Render.com örneği, hesabı siz açarsınız)
1. Klasörü GitHub'a yükleyin → Render'da "New Web Service" → Build: `pip install -r requirements.txt`, Start: `gunicorn app:app`.
2. Environment: ADMIN_PASSWORD, CRON_TOKEN, (isteğe bağlı) ANTHROPIC_API_KEY. Kalıcı disk ekleyin (lgs.db ve pdfs/ için, aksi halde yeniden başlatmada silinir).
3. Ücretsiz plan uyur → `.github_workflow_daily.yml` dosyasını GitHub Actions olarak kullanın (adresi güncelleyin) veya cron-job.org ile `/api/cron/<CRON_TOKEN>` adresini 06:00'da çağırın.
## Notlar
- Admin: /admin (kullanıcı adı serbest, şifre ADMIN_PASSWORD).
- Matematik soruları her gün kodla üretilir ve Python ile doğrulanır. Diğer 5 ders için ANTHROPIC_API_KEY tanımlanırsa model soru üretir, ikinci bir çağrıyla bağımsız çözdürülür; anahtar yoksa yalnızca 10 ders-içi seed soru döner (günlük yeni soru üretilmez).

## Siteyi nasıl açarım?
- **Kendi bilgisayarında (en hızlı):** `python app.py` → tarayıcıda http://localhost:5000 (yalnızca senin PC'nde açılır).
- **Aynı Wi-Fi'deki telefon:** `python -m flask --app app run --host 0.0.0.0` → telefonda http://BILGISAYAR_IP:5000
- **Herkese açık link:** Render/Railway/PythonAnywhere'e yükle; platform sana https://....onrender.com gibi bir adres verir.

## Diğer dersler için alternatifler (API anahtarsız)
1. Yerleşik şablon üreticiler (`extra.py`): Fen (basınç, özkütle, hız), İngilizce (karşılaştırma, fiil), Türkçe (yazım), İnkılap (tarih), Din (temel bilgi). Havuz sınırlı; birkaç gün sonra tükenir.
2. Öğretmen/kendi sorularını `python import_bank.py sorular.json` ile ekle (otomatik doğrulanır).
3. `ANTHROPIC_API_KEY` tanımla: model her gün yeni soru üretir, bağımsız çözümle doğrulanır.
4. Aylık toplu üretim: bir sohbette 100–200 soru istenip import edilir, yönetici gözden geçirir.
