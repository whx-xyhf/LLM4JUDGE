# 每次用大模型生成limit条数据，默认10条
def get_glm_respones(filedata, total=0,limit=10):
    '''
    filedata: 上传的数据文件
    total: 已经梳理的总条数
    limit: 单次梳理的条数
    '''
    data = [{
    "id":1,
    "condition": "判据",
    "phenomenon": "故障名称",
    "rule": "规程",
    'parameter':'运行参数',
    "example1": "样例1",
    "example2": "样例2",
    "status": "未校准"
    }, {
    "id":2,
    "condition": "2016-05-02",
    "phenomenon": "王小虎",
    "rule": "上海市普陀区金沙江路 1518 弄",
    'parameter':'运行参数',
    "example1": "上海市普陀区金沙江路 1518 弄",
    "example2": "上海市普陀区金沙江路 1518 弄",
    "status": "已校准"
    }, {
        "id":3,
    "condition": "2016-05-04",
    "phenomenon": "王小虎",
    "rule": "上海市普陀区金沙江路 1518 弄",
    'parameter':'运行参数',
    "example1": "上海市普陀区金沙江路 1518 弄",
    "example2": "上海市普陀区金沙江路 1518 弄",
    "status": "已校准"
    }, {
        "id":4,
    "condition": "2016-05-01",
    "phenomenon": "王小虎",
    "rule": "上海市普陀区金沙江路 1518 弄",
    'parameter':'运行参数',
    "example1": "上海市普陀区金沙江路 1518 弄",
    "example2": "上海市普陀区金沙江路 1518 弄",
    "status": "未校准"
    }, {
        "id":5,
    "condition": "2016-05-08",
    "phenomenon": "王小虎",
    "rule": "上海市普陀区金沙江路 1518 弄",
    'parameter':'运行参数',
    "example1": "上海市普陀区金沙江路 1518 弄",
    "example2": "上海市普陀区金沙江路 1518 弄",
    "status": "未校准"
    }, {
        "id":6,
    "condition": "2016-05-06",
    "phenomenon": "王小虎",
    "rule": "上海市普陀区金沙江路 1518 弄",
    'parameter':'运行参数',
    "example1": "上海市普陀区金沙江路 1518 弄",
    "example2": "上海市普陀区金沙江路 1518 弄",
    "status": "未校准"
    }, {
    "id":7,
    "condition": "2016-05-07",
    "phenomenon": "王小虎",
    "rule": "上海市普陀区金沙江路 1518 弄",
    'parameter':'运行参数',
    "example1": "上海市普陀区金沙江路 1518 弄",
    "example2": "上海市普陀区金沙江路 1518 弄",
    "status": "已校准"
}]
    #判断有没有梳理完，应该去判断规程里的故障的长度和已梳理的长度
    #所以应该在获取数据之前判断，我这里因为模拟数据，就在之后判断了
    if total >= len(data):
        return None, True
    return data[total:total+limit], False
    