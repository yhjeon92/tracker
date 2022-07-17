from flask import Flask, request, Response, redirect
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename
from parseGpx import GpxParser
import json, uuid, os, io


def parse_response(status: int, code: int, message: str, detail: str):
    return Response(response=json.dumps({'code': code, 'message': message, 'detail': detail}), status=status,
                    mimetype="application/json")


app = Flask(__name__,
            static_url_path='',
            static_folder='static')
parser = GpxParser()


@app.route('/upload', methods=["POST"])
def upload_gpx():
    file = request.files.get("file")
    if file is None:
        return parse_response(400, 400, "Bad Request", "Request must be a valid multipart/form-data with field named file")

    try:
        gpxText = file.stream.read()
        sessionId = uuid.uuid1()

        file_sub_path = secure_filename(f'static{os.linesep}{sessionId}.js')
        path = f'{os.path.join(os.getcwd(), file_sub_path)}'

        parser.parse(gpxText, path)

        return parse_response(200, 200, f'{sessionId}.js', "")
    except Exception as err:
        print('Internal Server Error: ', err)
        return parse_response(500, 500, "Internal Server Error", "Exception encountered while parsing given .gpx file")


@app.route('/', methods=["GET"])
def index_page():
    return redirect('/index.html')


if __name__ == "__main__":
    CORS(app)
    app.run(host='0.0.0.0', port=80)
