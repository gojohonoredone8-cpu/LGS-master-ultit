# Vercel girişi: başlangıçta çökerse hatayı sayfada gösterir
try:
    from main import app
except Exception:
    import traceback
    tb=traceback.format_exc()
    from flask import Flask
    app=Flask(__name__)
    @app.route("/",defaults={"p":""})
    @app.route("/<path:p>")
    def _err(p): return "<h3>Baslangic hatasi</h3><pre>"+tb.replace("<","&lt;")+"</pre>",500
