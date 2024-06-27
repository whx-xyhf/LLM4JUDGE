from flask import Flask, request, jsonify, make_response, render_template
import json
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

@app.route("/getResult", methods=['POST'])
def getResult():
    # data = request.get_json()['message']
    # 此处数据应该是大模型跑出来的结果，暂时用其他数据代替
    data = [{
    "id":1,
    "condition": "2016-05-03",
    "phenomenon": "王小虎",
    "rule": "上海市普陀区金沙江路 1518 弄",
    "example1": "上海市普陀区金沙江路 1518 弄",
    "example2": "上海市普陀区金沙江路 1518 弄",
    "status": "未校准"
    }, {
    "id":2,
    "condition": "2016-05-02",
    "phenomenon": "王小虎",
    "rule": "上海市普陀区金沙江路 1518 弄",
    "example1": "上海市普陀区金沙江路 1518 弄",
    "example2": "上海市普陀区金沙江路 1518 弄",
    "status": "已校准"
    }, {
        "id":3,
    "condition": "2016-05-04",
    "phenomenon": "王小虎",
    "rule": "上海市普陀区金沙江路 1518 弄",
    "example1": "上海市普陀区金沙江路 1518 弄",
    "example2": "上海市普陀区金沙江路 1518 弄",
    "status": "已校准"
    }, {
        "id":4,
    "condition": "2016-05-01",
    "phenomenon": "王小虎",
    "rule": "上海市普陀区金沙江路 1518 弄",
    "example1": "上海市普陀区金沙江路 1518 弄",
    "example2": "上海市普陀区金沙江路 1518 弄",
    "status": "未校准"
    }, {
        "id":5,
    "condition": "2016-05-08",
    "phenomenon": "王小虎",
    "rule": "上海市普陀区金沙江路 1518 弄",
    "example1": "上海市普陀区金沙江路 1518 弄",
    "example2": "上海市普陀区金沙江路 1518 弄",
    "status": "未校准"
    }, {
        "id":6,
    "condition": "2016-05-06",
    "phenomenon": "王小虎",
    "rule": "上海市普陀区金沙江路 1518 弄",
    "example1": "上海市普陀区金沙江路 1518 弄",
    "example2": "上海市普陀区金沙江路 1518 弄",
    "status": "未校准"
    }, {
    "id":7,
    "condition": "2016-05-07",
    "phenomenon": "王小虎",
    "rule": "上海市普陀区金沙江路 1518 弄",
    "example1": "上海市普陀区金沙江路 1518 弄",
    "example2": "上海市普陀区金沙江路 1518 弄",
    "status": "已校准"
}]
    # with open('./static/data.json', 'r', encoding='utf-8') as f:
    #     data = json.load(f)
    res = make_response(jsonify({'code': 200, 'data': data}))
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

