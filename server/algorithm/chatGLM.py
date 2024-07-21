#coding=utf-8
from algorithm.MyTest import*
# # 每次用大模型生成limit条数据，默认10条

import re
def get_glm_respones(filedata, total, limit):
    
    '''
    global_data = {'guicheng':[],'dingzhiqingce':[], 'example':[]}
    filedata: 上传的数据文件
    total: 已经梳理的总条数
    limit: 单次梳理的条数
    '''
    chunks = []
    if not filedata['guicheng']:
        #region 测试是否有数据
        print("----------------------------")
        print("\n规程数据为空\n")
        print("----------------------------")
        #endregion 
    else:
        chunks = filedata['guicheng'][0]
        #region 测试是否有数据
        print("----------------------------")
        print("\n规程数据 已导入\n")
        print("----------------------------")
        #endregion 
    
    # print(f"chunks:\n{chunks}")

    ######
    if total >= len(chunks):
        return None, True
    ######

    RunParam = []
    if not filedata['dingzhiqingce']:
        #region 测试是否有数据
        print("----------------------------")
        print("\n运行参数为空\n")
        print("----------------------------")
        #endregion 
    else:
        RunParam = filedata['dingzhiqingce']
        #region 测试是否有数据
        print("----------------------------")
        print("\n运行参数 已导入\n")
        print("----------------------------")
        #endregion 测试
    
    examples = filedata['example']

    data = []
    limit = int(limit)
    for i in range(total,total+limit):
        # print(f"test{i}\n")
        
        id = i+1
        print("*******************************************************")
        print(f"id = {id}")

        condition = '空'
        phnm = '空'
        rule = '空'
        para = '空'
        example1 = '空'
        example2 = '空'

        if i<len(chunks):
            phnm = GetPhnmName(chunks[i])
            rule = Getrules(chunks[i])
            # 使用正则表达式匹配每个现象，并分隔开
            phenm_list = re.split(r'\d\) ', rule)[1:]  # 从第二个元素开始，因为第一个是空字符串

            # 移除每个现象后的多余符号 把现象组分割成零散的单条现象
            phenom_list = [phenm.strip('。') for phenm in phenm_list]

            
            example1 = GetExample(chunks[i],examples[0])

            example2 = GetExample(chunks[i],examples[1])
            
            if '空' in rule:
                print("现象 = null 无法判断")
                continue
            else:
                for j, strPhnm in enumerate(phenom_list):
                    phL = [strPhnm] 
                    para = GetParam(chunks[i],RunParam,phL)
                    if '空' in para:
                        print("运行参数 = null 无法判断")
                        continue 
                    condition = UseLModel(i,chunks,phnm,para,example1,example2)
                    # 提取JSON格式的字符串部分
                    if condition != '空':
                        # 定位JSON字符串的开始和结束位置
                        # Extracting the first occurrence of JSON content without the square brackets and removing newlines
                        start_index = condition.find("[") + 1
                        end_index = condition.find("]", start_index)
                        # Extracting the JSON substring without brackets and newlines
                        json_content = condition[start_index:end_index].strip().replace("\n", "")
                        condition = json_content
                        condition = condition.replace('"', '')
                        condition = condition.replace("'", '')
                        condition = condition.replace('”', '')
                        condition = condition.replace('“', '')
                        condition = condition.replace('‘', '')
                        condition = condition.replace('’', '')
                        condition = condition.replace(',', '，')
                        condition = condition.replace(' ', '')
                    s = {"id":id, "condition": condition,"phenomenon": phnm,"rule": strPhnm,'parameter':para,"example1": example1,"example2": example2,"status": "未校准"}
                    for key, value in s.items():
                        print(f"{key}: {value}")
                    data.append(s)

    #判断有没有梳理完，应该去判断规程里的故障的长度和已梳理的长度
    #所以应该在获取数据之前判断，我这里因为模拟数据，就在之后判断了
    return data[total:total+limit], False

# get_glm_respones(0, total=0,limit=10)
    