# import MyTest
from algorithm.MyTest import*
import os
import json

from difflib import SequenceMatcher
filePath = 'data/chunks_volume_two.json'
# print(f"\n当前工作目录是：{filePath}\n")

# 当前的工作目录
current_directory = os.getcwd()
# print(f"\ncurrent={current_directory}\n")

json_file_path = os.path.join(filePath)

# print(f"\n当前工作目录是：{json_file_path}\n")

datas = {}
# 检查文件是否存在
if os.path.exists(json_file_path):
    with open(json_file_path, 'r', encoding='utf-8') as file:
        datas = json.load(file)
else:
    print(f"文件 {json_file_path} 不存在。")
# print(data)
# 访问 chunks 列表
chunks = datas.get('chunks', [])


# # 每次用大模型生成limit条数据，默认10条

def get_glm_respones(filedata, total, limit):
    
    '''
    global_data = {'guicheng':[],'dingzhiqingce':[], 'example':[]}
    filedata: 上传的数据文件
    total: 已经梳理的总条数
    limit: 单次梳理的条数
    '''
   
    # guicheng= filedata['guicheng']
    # chunks = guicheng[0]['chunks']
     # print(len(chunks))
    # print(f"\nlen = {chunks}")  #测试一下

    data = []
    limit = int(limit)
    for i in range(total,total+limit):
        print(f"test{i}\n")
        
        id = i+1
        print(f"id = {id}")

        condition = '空'
        phnm = '空'
        rule = '空'
        para = '空'
        example1 = '空'
        example2 = '空'

        if i<len(chunks):
            condition = UseLModel(i,chunks)
            phnm = GetPhnmName(chunks[i])
            rule = Getrules(chunks[i])
            para = GetParam(id,chunks[i])
            example1 = GetExam1(chunks[i])
            example2 = GetExam2(chunks[i])
        s = {"id":id, "condition": condition,"phenomenon": phnm,"rule": rule,'parameter':para,"example1": example1,"example2": example2,"status": "未校准"}
        print(s)    #数据测试
        data.append(s)

    #判断有没有梳理完，应该去判断规程里的故障的长度和已梳理的长度
    #所以应该在获取数据之前判断，我这里因为模拟数据，就在之后判断了
    if total >= 10:
        return None, True
    return data[total:total+limit], False

# get_glm_respones(0, total=0,limit=10)
    