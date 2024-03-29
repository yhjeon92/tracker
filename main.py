from flask import Flask, request, Response, redirect
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename
from parseGpx import GpxParser
import json, uuid, os, io, sys, traceback


def parse_error(status: int, code: int, message: str, detail: str):
    return Response(response=json.dumps({'code': code, 'message': message, 'detail': detail}), status=status,
                    mimetype="application/json")

def parse_response(result: dict):
    return Response(response=json.dumps(result), status=200, mimetype="application/json")

app = Flask(__name__,
            static_url_path='',
            static_folder='static')
parser = GpxParser()


@app.route('/upload', methods=["POST"])
def upload_gpx():
    file = request.files.get("file")
    if file is None:
        return parse_error(400, 400, "Bad Request", "Request must be a valid multipart/form-data with field named file")

    try:
        gpxText = file.stream.read()
        sessionId = uuid.uuid1()

        file_name = secure_filename(f'{sessionId}.js')
        path = os.path.join(os.getcwd(), 'static', 'temp', file_name)

        result_dict = parser.parse(gpxText, path)
        
        return parse_response(result_dict)
    except Exception as err:
        print(traceback.format_exc())
        print('Internal Server Error: ', err, file=sys.stderr)
        return parse_error(500, 500, "Internal Server Error", "Exception encountered while parsing given .gpx file")


@app.route('/', methods=["GET"])
def index_page():
    return redirect('/index.html')


if __name__ == "__main__":
    CORS(app)
    app.run(host='127.0.0.1', port=8080, debug=True)
