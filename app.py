import os
from flask import Flask, request, render_template, send_file, jsonify

from werkzeug.exceptions import RequestEntityTooLarge

from datetime import datetime
from extensions import JinkelaFlask

app: Flask = JinkelaFlask(import_name=__name__)

app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024  # 10M


# @app.errorhandler(Exception)
# def handle_exception(e):
#     if isinstance(e, RequestEntityTooLarge):
#         return jsonify({"test": "文件过大"})

#     return e


@app.post("/upload")
def upload() -> str:
    file = request.files["file"]
    filename = file.filename
    file.save(os.path.join("./uploads", filename))
    return dict(
        test_datetime=datetime.now(),
        test=f"文件 {filename} 上传成功",
    )


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


if __name__ == "__main__":
    app.run(debug=False)
