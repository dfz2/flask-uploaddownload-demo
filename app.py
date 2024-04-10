import os
from flask import Flask, request, render_template, send_file, jsonify

from werkzeug.exceptions import RequestEntityTooLarge

from datetime import datetime
from extensions import JinkelaFlask

from dataclasses import dataclass
from enum import Enum, StrEnum


# 'primary' | 'success' | 'info' | 'warning' | 'danger'


class EColor(StrEnum):
    PRIMARY = "primary"
    SUCCESS = "success"
    INFO = "info"
    WARNING = "warning"
    DANGER = "danger"


@dataclass
class StatusMixin:
    label: str
    status_code: int
    color: EColor


class BaseEnum(Enum):

    @classmethod
    def parse(cls, status_code):
        for item in cls.__dict__.values():
            if isinstance(item, cls) and item.status_code == status_code:
                return item
        raise ValueError(f"No enum item with value {status_code}")


class EOrderStatus(StatusMixin, BaseEnum):
    DELETE = "删除", 10, EColor.PRIMARY


app: Flask = JinkelaFlask(import_name=__name__)

app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024  # 10M


# @app.errorhandler(Exception)
# def handle_exception(e):
#     if isinstance(e, RequestEntityTooLarge):
#         return jsonify({"test": "文件过大"})

#     return e


@app.get("/test")
def get_test_enum():
    print(EOrderStatus.parse(10))
    return dict(
        order_status=EOrderStatus.DELETE,
        order_status2=EOrderStatus.parse(10),
    )


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
