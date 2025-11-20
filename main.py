import os
import io
import zipfile
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import StreamingResponse, JSONResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI Backend!"}

@app.get("/api/hello")
def hello():
    return {"message": "Hello from the backend API!"}

@app.get("/test")
def test_database():
    """Test endpoint to check if backend is running"""
    return {"backend": "✅ Running"}


SPLINE_URL = "https://prod.spline.design/pVLJXSVq3zyQq0OD/scene.splinecode"

# Base HTML head with fonts and shared meta
BASE_HEAD = """
<!DOCTYPE html>
<html lang=\"en\">
<head>
  <meta charset=\"UTF-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />
  <title>{eventTitle}</title>
  <link rel=\"preconnect\" href=\"https://fonts.googleapis.com\" />
  <link rel=\"preconnect\" href=\"https://fonts.gstatic.com\" crossorigin />
  <link href=\"https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Inter:wght@300;400;600;700;900&family=Great+Vibes&display=swap\" rel=\"stylesheet\"> 
  <script type=\"module\" src=\"https://unpkg.com/@splinetool/viewer@latest/build/spline-viewer.js\"></script>
  <style>
    :root{
      --bg: #0b0f19;
      --muted: #9aa4b2;
      --card: #0f1424;
      --ring: rgba(255,255,255,0.06);
    }
    *{box-sizing:border-box}
    html,body{margin:0;padding:0;background:var(--bg);color:#fff}
    .page{min-height:100vh;display:flex;flex-direction:column}
    .hero{position:relative;height:42vh;min-height:320px;overflow:hidden}
    .cover{position:absolute;inset:0}
    spline-viewer{width:100%;height:100%;display:block;pointer-events:none}
    .overlay-grad{position:absolute;inset:0;background:radial-gradient(1200px_600px at 50% 80%,rgba(255,255,255,.18),transparent),linear-gradient(to bottom,rgba(3,7,18,0.1),rgba(3,7,18,0.65) 55%,rgba(3,7,18,1));}
    .content{display:grid;gap:28px;max-width:1080px;margin:-80px auto 64px;padding:0 24px 64px}
    .card{border-radius:28px;background:linear-gradient(180deg,rgba(255,255,255,.08),rgba(255,255,255,.02));backdrop-filter:blur(12px);border:1px solid var(--ring);box-shadow:0 10px 30px rgba(0,0,0,0.35);overflow:hidden}
    .inner{padding:36px 36px 40px}
    .title{font:700 56px/1.05 'Playfair Display', serif;letter-spacing:.2px}
    .subtitle{font:600 18px/1.6 'Inter', system-ui}
    .grid{display:grid;grid-template-columns:repeat(12,1fr);gap:24px}
    .pill{display:inline-flex;gap:10px;align-items:center;padding:10px 14px;border:1px solid var(--ring);border-radius:999px;background:rgba(255,255,255,.04)}
    .row{display:flex;flex-wrap:wrap;gap:14px}
    .section-title{font:700 14px/1 'Inter';letter-spacing:.2em;text-transform:uppercase;color:var(--muted)}
    .big-script{font-family:'Great Vibes', cursive;font-size:48px;line-height:1.1;opacity:.9}
    .divider{height:1px;background:linear-gradient(90deg,transparent,rgba(255,255,255,.18),transparent);margin:10px 0 24px}
    .badge{position:absolute;right:24px;bottom:22px;height:44px;aspect-ratio:1;border-radius:14px;background:linear-gradient(135deg,#6ee7ff,#7c3aed);filter:blur(.0px);box-shadow:inset 0 0 0 6px rgba(255,255,255,.25),0 12px 28px rgba(124,58,237,.35)}
    @media (max-width: 780px){
      .title{font-size:38px}
      .hero{height:36vh}
      .inner{padding:26px}
    }
  </style>
</head>
"""

# Template builders: each returns a full HTML string using the shared head and unique body styles.

def tpl_kids_birthday():
    return BASE_HEAD + f"""
<body>
  <div class=\"page\">
    <header class=\"hero\">
      <div class=\"cover\">
        <spline-viewer url=\"{SPLINE_URL}\"></spline-viewer>
        <div class=\"overlay-grad\"></div>
      </div>
    </header>

    <main class=\"content\">
      <section class=\"card\" style=\"background:linear-gradient(180deg,rgba(99,102,241,.15),rgba(99,102,241,.05));position:relative;\">
        <div class=\"inner\">
          <div class=\"grid\">
            <div class=\"col\" style=\"grid-column:span 12;\">
              <div class=\"row\" style=\"gap:12px;\">
                <span class=\"pill\" style=\"background:rgba(59,130,246,.12)\">🎈</span>
                <span class=\"pill\" style=\"background:rgba(236,72,153,.12)\">🎂</span>
                <span class=\"pill\" style=\"background:rgba(234,179,8,.12)\">🎁</span>
              </div>
              <div style=\"height:10px\"></div>
              <div class=\"title\">{eventTitle}</div>
              <div class=\"divider\"></div>
            </div>

            <div class=\"col\" style=\"grid-column:span 7;\">
              <div class=\"subtitle\" style=\"font-size:20px\">{eventDescription}</div>
              <div style=\"height:18px\"></div>
              <div class=\"row\">
                <span class=\"pill\">📅 {eventDate}</span>
                <span class=\"pill\">📍 {decidedLocation}</span>
              </div>
              <div style=\"height:18px\"></div>
              <div class=\"row\">
                <span class=\"pill\">🍰 {decidedFood}</span>
                <span class=\"pill\">🎯 {decidedActivities}</span>
              </div>
            </div>

            <div class=\"col\" style=\"grid-column:span 5;position:relative\">
              <div style=\"position:relative;border-radius:22px;overflow:hidden;border:1px solid var(--ring);background:radial-gradient(120px 160px at 20% 20%,rgba(236,72,153,.35),transparent),radial-gradient(160px 220px at 80% 30%,rgba(59,130,246,.35),transparent),radial-gradient(140px 180px at 40% 80%,rgba(234,179,8,.4),transparent);min-height:220px\">
                <svg viewBox=\"0 0 400 240\" width=\"100%\" height=\"260\" preserveAspectRatio=\"none\">
                  <defs>
                    <linearGradient id=\"g1\" x1=\"0\" x2=\"1\"> <stop offset=\"0\" stop-color=\"#60a5fa\"/> <stop offset=\"1\" stop-color=\"#f472b6\"/></linearGradient>
                  </defs>
                  <g fill=\"none\" stroke=\"url(#g1)\" stroke-width=\"2\" opacity=\".85\">
                    <path d=\"M0,60 Q80,10 160,60 T320,60 T480,60\"/>
                    <path d=\"M0,120 Q80,70 160,120 T320,120 T480,120\" opacity=\".7\"/>
                    <path d=\"M0,180 Q80,130 160,180 T320,180 T480,180\" opacity=\".5\"/>
                  </g>
                </svg>
                <div class=\"badge\"></div>
              </div>
            </div>

            <div class=\"col\" style=\"grid-column:span 12\">
              <div class=\"divider\"></div>
              <div class=\"big-script\">{customText}</div>
            </div>
          </div>
        </div>
      </section>
    </main>
  </div>
</body>
</html>
"""


def tpl_wine_and_dine():
    return BASE_HEAD + f"""
<body>
  <div class=\"page\" style=\"background:radial-gradient(800px 600px at 20% -10%, rgba(255,255,255,.08), transparent),radial-gradient(900px 700px at 100% 10%, rgba(168,85,247,.10), transparent),#0a0a0a;\">
    <header class=\"hero\">
      <div class=\"cover\">
        <spline-viewer url=\"{SPLINE_URL}\"></spline-viewer>
        <div class=\"overlay-grad\" style=\"background:linear-gradient(to bottom, rgba(10,10,10,.15), rgba(10,10,10,.85) 60%, #0a0a0a)\"></div>
      </div>
    </header>

    <main class=\"content\">
      <section class=\"card\" style=\"background:linear-gradient(180deg,rgba(255,255,255,.06),rgba(255,255,255,.02));\">
        <div class=\"inner\">
          <div class=\"title\" style=\"font-family:'Playfair Display',serif;letter-spacing:.5px\">{eventTitle}</div>
          <div class=\"divider\"></div>
          <div class=\"grid\">
            <div style=\"grid-column:span 6\">
              <div class=\"subtitle\" style=\"font-size:18px;color:#e5e7eb\">{eventDescription}</div>
              <div style=\"height:24px\"></div>
              <div class=\"row\">
                <span class=\"pill\">🗓️ {eventDate}</span>
                <span class=\"pill\">📍 {decidedLocation}</span>
              </div>
              <div style=\"height:18px\"></div>
              <div class=\"row\">
                <span class=\"pill\">🍷 {decidedFood}</span>
                <span class=\"pill\">🎶 {decidedActivities}</span>
              </div>
            </div>
            <div style=\"grid-column:span 6\">
              <div style=\"position:relative;border:1px solid var(--ring);border-radius:22px;overflow:hidden;min-height:250px;background:conic-gradient(from 180deg at 50% 50%,#f5f5f5 0deg,#eab308 60deg,#a855f7 140deg,#ef4444 220deg,#14b8a6 300deg,#f5f5f5 360deg);filter:saturate(.7) brightness(.6)\"></div>
            </div>
            <div style=\"grid-column:span 12\">
              <div class=\"divider\"></div>
              <div class=\"big-script\" style=\"font-size:56px\">{customText}</div>
            </div>
          </div>
        </div>
      </section>
    </main>
  </div>
</body>
</html>
"""


def tpl_goolparty():
    return BASE_HEAD + f"""
<body>
  <div class=\"page\" style=\"background:linear-gradient(180deg,#021526 0%, #03192e 40%, #02101c 100%);\">
    <header class=\"hero\">
      <div class=\"cover\">
        <spline-viewer url=\"{SPLINE_URL}\"></spline-viewer>
        <div class=\"overlay-grad\" style=\"background:linear-gradient(to bottom, rgba(2,15,26,.2), rgba(2,15,26,.85) 60%, #021526)\"></div>
      </div>
    </header>
    <main class=\"content\">
      <section class=\"card\" style=\"background:linear-gradient(180deg,rgba(20,184,166,.14),rgba(2,6,23,.3));\">
        <div class=\"inner\">
          <div class=\"title\" style=\"letter-spacing:.4px\">{eventTitle}</div>
          <div class=\"divider\"></div>
          <div class=\"grid\">
            <div style=\"grid-column:span 8\">
              <div class=\"subtitle\">{eventDescription}</div>
              <div style=\"height:14px\"></div>
              <div class=\"row\">
                <span class=\"pill\">📅 {eventDate}</span>
                <span class=\"pill\">📍 {decidedLocation}</span>
                <span class=\"pill\">🍹 {decidedFood}</span>
                <span class=\"pill\">⚽ {decidedActivities}</span>
              </div>
            </div>
            <div style=\"grid-column:span 4\">
              <div style=\"position:relative;border-radius:22px;border:1px solid var(--ring);overflow:hidden;min-height:220px;background:radial-gradient(150px 90px at 60% 30%, rgba(34,197,94,.45), transparent),radial-gradient(160px 120px at 20% 60%, rgba(59,130,246,.45), transparent),radial-gradient(120px 80px at 80% 70%, rgba(244,63,94,.45), transparent)\"></div>
            </div>
            <div style=\"grid-column:span 12\">
              <div class=\"divider\"></div>
              <div class=\"big-script\">{customText}</div>
            </div>
          </div>
        </div>
      </section>
    </main>
  </div>
</body>
</html>
"""


def tpl_gardenparty():
    return BASE_HEAD + f"""
<body>
  <div class=\"page\" style=\"background:linear-gradient(180deg,#07130b,#0a1a10);\">
    <header class=\"hero\">
      <div class=\"cover\">
        <spline-viewer url=\"{SPLINE_URL}\"></spline-viewer>
        <div class=\"overlay-grad\" style=\"background:linear-gradient(to bottom, rgba(7,19,11,.2), rgba(7,19,11,.9) 60%, #07130b)\"></div>
      </div>
    </header>

    <main class=\"content\">
      <section class=\"card\" style=\"background:linear-gradient(180deg,rgba(34,197,94,.15),rgba(34,197,94,.05));\">
        <div class=\"inner\">
          <div class=\"grid\">
            <div style=\"grid-column:span 7\">
              <div class=\"title\" style=\"font-family:'Playfair Display',serif\">{eventTitle}</div>
              <div class=\"divider\"></div>
              <div class=\"subtitle\">{eventDescription}</div>
              <div style=\"height:18px\"></div>
              <div class=\"row\">
                <span class=\"pill\">📅 {eventDate}</span>
                <span class=\"pill\">📍 {decidedLocation}</span>
              </div>
              <div style=\"height:12px\"></div>
              <div class=\"row\">
                <span class=\"pill\">🥗 {decidedFood}</span>
                <span class=\"pill\">🪴 {decidedActivities}</span>
              </div>
            </div>
            <div style=\"grid-column:span 5\">
              <div style=\"position:relative;border:1px solid var(--ring);border-radius:22px;overflow:hidden;min-height:240px;background:linear-gradient(135deg, rgba(34,197,94,.3), rgba(16,185,129,.25)), url('data:image/svg+xml;utf8,<svg xmlns=\\'http://www.w3.org/2000/svg\\' width=\\'600\\' height=\\'400\\'><defs><pattern id=\\'l\\' width=\\'40\\' height=\\'40\\' patternUnits=\\'userSpaceOnUse\\'><path d=\\'M20 0v40M0 20h40\\' stroke=\\'%23ffffff22\\' stroke-width=\\'1\\'/></pattern></defs><rect fill=\\'%2300000000\\' width=\\'600\\' height=\\'400\\'/><rect fill=\\'url(%23l)\\' width=\\'600\\' height=\\'400\\'/></svg>') center/cover no-repeat\"></div>
            </div>
            <div style=\"grid-column:span 12\">
              <div class=\"divider\"></div>
              <div class=\"big-script\">{customText}</div>
            </div>
          </div>
        </div>
      </section>
    </main>
  </div>
</body>
</html>
"""


def tpl_familygathering():
    return BASE_HEAD + f"""
<body>
  <div class=\"page\" style=\"background:radial-gradient(900px 700px at -10% 0%, rgba(59,130,246,.10), transparent), #0b0f19;\">
    <header class=\"hero\">
      <div class=\"cover\">
        <spline-viewer url=\"{SPLINE_URL}\"></spline-viewer>
        <div class=\"overlay-grad\"></div>
      </div>
    </header>

    <main class=\"content\">
      <section class=\"card\" style=\"background:linear-gradient(180deg,rgba(255,255,255,.05),rgba(255,255,255,.02));\">
        <div class=\"inner\">
          <div class=\"title\" style=\"letter-spacing:.3px\">{eventTitle}</div>
          <div class=\"divider\"></div>
          <div class=\"grid\">
            <div style=\"grid-column:span 6\">
              <div class=\"subtitle\">{eventDescription}</div>
              <div style=\"height:16px\"></div>
              <div class=\"row\">
                <span class=\"pill\">📅 {eventDate}</span>
                <span class=\"pill\">📍 {decidedLocation}</span>
              </div>
              <div style=\"height:12px\"></div>
              <div class=\"row\">
                <span class=\"pill\">🍲 {decidedFood}</span>
                <span class=\"pill\">🎲 {decidedActivities}</span>
              </div>
            </div>
            <div style=\"grid-column:span 6\">
              <div style=\"position:relative;border-radius:22px;border:1px solid var(--ring);overflow:hidden;min-height:250px;background:linear-gradient(160deg, rgba(99,102,241,.25), rgba(56,189,248,.25), rgba(34,197,94,.25));\"></div>
            </div>
            <div style=\"grid-column:span 12\">
              <div class=\"divider\"></div>
              <div class=\"big-script\">{customText}</div>
            </div>
          </div>
        </div>
      </section>
    </main>
  </div>
</body>
</html>
"""


def tpl_outdoor():
    return BASE_HEAD + f"""
<body>
  <div class=\"page\" style=\"background:linear-gradient(180deg,#050816,#030b12 50%,#02070d);\">
    <header class=\"hero\">
      <div class=\"cover\">
        <spline-viewer url=\"{SPLINE_URL}\"></spline-viewer>
        <div class=\"overlay-grad\" style=\"background:linear-gradient(to bottom, rgba(5,8,22,.1), rgba(5,8,22,.8) 60%, #050816)\"></div>
      </div>
    </header>

    <main class=\"content\">
      <section class=\"card\" style=\"background:linear-gradient(180deg,rgba(56,189,248,.18),rgba(56,189,248,.06));\">
        <div class=\"inner\">
          <div class=\"grid\">
            <div style=\"grid-column:span 8\">
              <div class=\"title\" style=\"font-family:'Playfair Display',serif\">{eventTitle}</div>
              <div class=\"divider\"></div>
              <div class=\"subtitle\">{eventDescription}</div>
              <div style=\"height:16px\"></div>
              <div class=\"row\">
                <span class=\"pill\">📅 {eventDate}</span>
                <span class=\"pill\">📍 {decidedLocation}</span>
                <span class=\"pill\">🧺 {decidedFood}</span>
                <span class=\"pill\">⛰️ {decidedActivities}</span>
              </div>
            </div>
            <div style=\"grid-column:span 4\">
              <div style=\"position:relative;border:1px solid var(--ring);border-radius:22px;overflow:hidden;min-height:220px;background:radial-gradient(200px 140px at 50% 0%, rgba(56,189,248,.4), transparent),radial-gradient(220px 200px at 120% 80%, rgba(34,197,94,.35), transparent),radial-gradient(180px 180px at -20% 80%, rgba(99,102,241,.35), transparent)\"></div>
            </div>
            <div style=\"grid-column:span 12\">
              <div class=\"divider\"></div>
              <div class=\"big-script\">{customText}</div>
            </div>
          </div>
        </div>
      </section>
    </main>
  </div>
</body>
</html>
"""


def build_zip_bytes() -> bytes:
    files = {
        "kids-birthday.html": tpl_kids_birthday(),
        "wine-and-dine.html": tpl_wine_and_dine(),
        "goolparty.html": tpl_goolparty(),
        "gardenparty.html": tpl_gardenparty(),
        "familygathering.html": tpl_familygathering(),
        "outdoor.html": tpl_outdoor(),
    }
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
        for name, content in files.items():
            zf.writestr(name, content)
    buf.seek(0)
    return buf.read()


@app.get("/api/invitations.zip")
async def get_invitations_zip():
    try:
        data = build_zip_bytes()
        return StreamingResponse(io.BytesIO(data), media_type="application/zip", headers={
            "Content-Disposition": "attachment; filename=invitation-templates.zip"
        })
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
