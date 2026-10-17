# Vercel notları
- Vercel'de disk kalıcı değil: site her istekte günün paketini TARİHE GÖRE aynı şekilde (deterministik) üretir; veritabanı yok. Arşiv son 7 gün.
- Bu modda: model/API ile soru üretimi kapalı, günlük cron gereksiz (paket ilk ziyarette oluşur), admin kayıtları kalıcı değil.
- Ortam değişkeni: ADMIN_PASSWORD (Settings > Environment Variables). Sonra Redeploy.
- Hata görürsen: Vercel > Deployments > projen > Logs (Runtime Logs) kısmındaki kırmızı satırı bana gönder.
- Kalıcı veri/yönetici/gerçek günlük görev için Render + kalıcı disk veya Supabase gerekir.
