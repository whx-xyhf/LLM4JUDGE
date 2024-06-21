from flask import Flask, request, jsonify, make_response, render_template

# from flask_compress import Compress

app = Flask(__name__)
# app.config['COMPRESS_ALGORITHM'] = 'gzip'
app.config['JSON_AS_ASCII'] = False

# compress = Compress()
# compress.init_app(app)


@app.after_request
def cors(environ):
    environ.headers['Access-Control-Allow-Origin'] = '*'
    environ.headers['Access-Control-Allow-Method'] = '*'
    environ.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return environ


@app.route("/upload_file", methods=['POST'])
def upload_file():
    file = request.files.get('file')
    res = make_response(jsonify({'code': 200, 'data': ''}))
    return res

@app.route("/test", methods=['POST'])
def test():
    data = request.get_json()['message']
    if data == "hello":
        res = make_response(jsonify({'code': 200, 'data': "后端连接成功！"}))
    else:
        res = make_response(jsonify({'code': 200, 'data': "后端连接失败！"}))
    return res


@app.route('/', methods=['get'])
def root():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)

