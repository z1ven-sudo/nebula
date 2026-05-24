import os
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Nebula</title>

        <style>

        body{
            background:#0f172a;
            color:white;
            font-family:Arial;
            display:flex;
            justify-content:center;
            align-items:center;
            height:100vh;
            margin:0;
        }

        .box{
            width:300px;
            background:#1e293b;
            padding:20px;
            border-radius:15px;
            text-align:center;
        }

        button{
            padding:12px 20px;
            border:none;
            border-radius:10px;
            cursor:pointer;
            margin-top:10px;
        }

        </style>
    </head>

    <body>

        <div class="box">

            <h1>Nebula</h1>

            <p>Instagram Clone Backend Online</p>

            <button onclick="checkApi()">
                Check API
            </button>

            <p id="status"></p>

        </div>

        <script>

        async function checkApi(){

            const res = await fetch('/api')
            const data = await res.json()

            document.getElementById("status")
                .innerText = data.status
        }

        </script>

    </body>
    </html>
    """

@app.route("/api")
def api():
    return {
        "status":"Nebula online"
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
