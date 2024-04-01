import os
from flask import Flask, request, render_template, send_file

app: Flask = Flask(__name__)


@app.post("/upload")
def upload() -> str:
    file = request.files["file"]
    filename = file.filename
    file.save(os.path.join("./uploads", filename))
    return f"文件 {filename} 上传成功"


@app.get("/image")
def image_url():
    filename = request.args.get("name")
    return send_file(
        path_or_file=f"./uploads/{filename}",
        download_name=filename,
        as_attachment=True,
    )


@app.get("/")
def upload_html() -> str:
    return render_template("index.html")
