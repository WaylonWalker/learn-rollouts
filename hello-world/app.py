from pathlib import Path

from flask import Flask, request

app = Flask(__name__)

LIVE = Path("livez")
LIVE.write_text("ok")


@app.route("/")
def hello_world():
    version = "v3"
    if "5000" in request.base_url:
        mode = "local"
        header_color = "#a0dfa0"
    elif "30001" in request.base_url:
        mode = "active"
        header_color = "#a0c0df"
    elif "30002" in request.base_url:
        mode = "preview"
        header_color = "#dfa0df"
    else:
        mode = "unknown"
        header_color = "#dfc0a0"
    import time

    LIVE.write_text("no")
    time.sleep(10)
    LIVE.write_text("ok")

    return f"""
<html>
<head>
    <title>{mode}: Hello, World!</title>
    <style>
      body {{
        width: 100vw;
        height: calc(100vh - 100px);
        background-color: #333;
        color: #eee;
        margin: 0 auto;
        font-family: Tahoma, Verdana, Arial, sans-serif;
      }}

      main {{
        width: 100%;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
      }}
      header {{
        width: 100%;
        height: 100px;
        background-color: {header_color};
        color: #333;
        display: flex;
        justify-content: center;
        align-items: center;
      }}
    </style>
</head>

  <body>
  <header>
    <h2>{mode}: Hello, World! {version}</h2>
  </header>
    <main>
        <h1>Hello, World!</h1>
        <p>Mode: {mode}</p>
        <p>Version: {version}</p>
    </main>
  </body>
</html>
"""


@app.route("/healthz")
def healthz():
    # return "failed", 500
    return "I'm still here.", 200


@app.route("/livez")
def livez():
    if LIVE.read_text() == "ok":
        return "All done working here."
    return "I'm working here!", 500
