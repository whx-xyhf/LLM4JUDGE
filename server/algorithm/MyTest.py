# import os
# import json
# import ExtractData
# import MatchData
from algorithm.MatchData import *
from zhipuai import ZhipuAI
# client = ZhipuAI(api_key="dbf4f92f5d600f4f7df9929fe9fe2714.NRNX96VSSWOJdNFj") # 填写您自己的APIKey

# filePath = './server/data/chunks_volume_two.json'

# #测试当前的工作目录
# current_directory = os.getcwd()
# # print(f"\n当前工作目录是：{current_directory}\n")

# json_file_path = os.path.join(filePath)

# data = {}
# # 检查文件是否存在
# if os.path.exists(json_file_path):
#     with open(json_fsile_path, 'r', encoding='utf-8') as file:
#         data = json.load(file)
# else:
#     print(f"文件 {json_file_path} 不存在。")

# # # 访问 chunks 列表
# chunks = data.get('chunks', [])

# def GetChunks():
#     return data.get('chunks', [])
#这个方法的作用是提取新工厂的故障现象的名称
def ExtractName(strs):
    chunk = strs
    singleStrs = chunk.split('\n')
    flag = 1
    for i, inStr in enumerate(singleStrs):
        child_str1 = "a)"
        #判断单条列表中是否含有 "a)" 子串 若有->停止判断，进入下一个列表
        if child_str1 in singleStrs[i] :
            # print(f"index: {index+1}___故障设备现象：{singleStrs[i-1]}")
            val_fault = singleStrs[i-1]
            pos = val_fault.find(' ')
            val_fault = val_fault[pos+1:]
            return val_fault

#这个方法的作用是提取新工厂的故障现象
def ExtractNewFactory_Fault_phnm(strs):
    alphabet = ['a','b','c','d','e']
    #分割出完成的一条数据 形成一个列表
    singleStrs = strs.split('\n')

    #列表数据测试
    # for i, inStr in enumerate(singleStrs):
    #     print(f"str[{i}] == {inStr}")
    # print()

    #第一个for：查询有原因现象的那一条数据
    for i, inStr in enumerate(singleStrs):
        flag = 'a'
        #如果 字符"a"出现在当前的字符串 inStr 中 则开始裁剪字符串
        if flag in inStr:
            faults = []
            #第二个for：便利所有出现的字母 截取原因 现象
            for j in range(len(alphabet)-1):
                c1 = alphabet[j]
                c2 = alphabet[j+1]
                index1 = 0
                index2 = 0
                if c1 in inStr:
                    index1 = inStr.index(c1)
                else:
                    break

                if c2 in inStr:
                    index2 = inStr.index(c2)
                    faults.append(inStr[index1:index2-1])
                else:
                    faults.append(inStr[index1:len(inStr)])
                    break

            #故障 现象 原因 内容测试
            # for k, str in enumerate(faults):
            #     print(str)
            # print()
            for k, str in enumerate(faults):
                c1 = "现象"
                s = str[0: 6]
                if c1 in s:
                    return str
            return '空'
           

#这个方法的作用是提取新工厂的故障原因
def ExtractNewFactory_Fault_reason(strs):
    alphabet = ['a','b','c','d','e']
    #分割出完成的一条数据 形成一个列表
    singleStrs = strs.split('\n')

    #列表数据测试
    # for i, inStr in enumerate(singleStrs):
    #     print(f"str[{i}] == {inStr}")
    # print()

    #第一个for：查询有原因现象的那一条数据
    for i, inStr in enumerate(singleStrs):
        flag = 'a'
        #如果 字符"a"出现在当前的字符串 inStr 中 则开始裁剪字符串
        if flag in inStr:
            faults = []
            #第二个for：便利所有出现的字母 截取原因 现象
            for j in range(len(alphabet)-1):
                c1 = alphabet[j]
                c2 = alphabet[j+1]
                index1 = 0
                index2 = 0
                if c1 in inStr:
                    index1 = inStr.index(c1)
                else:
                    break

                if c2 in inStr:
                    index2 = inStr.index(c2)
                    faults.append(inStr[index1:index2-1])
                else:
                    faults.append(inStr[index1:len(inStr)])
                    break

            #故障 现象 原因 内容测试
            # for k, str in enumerate(faults):
            #     print(str)
            # print()

            for k, str in enumerate(faults):
                # print(str)
                c2 = "原因"
                s = str[0: 6]
                if c2 in s:
                    # print(f"原因:____{str}")
                    return str
            return '空'

#下面这个算法的作用是将chunks2每一条故障名字、现象、原因 做个分割
def SplitData(chunk) :
    text = chunk.split('\n')
    for i, s in enumerate(text):
        if s != '' and s[0]!='a':
            pos = s.find(' ')
            text[i] = s[pos+1:]
    return text

#返回总共整理的数目
def GetRows(chunks):
    return len(chunks)
#返回新电厂的故障名称
def GetPhnmName(chunk):
    return ExtractName(chunk)
#返回某设备的规程
def Getrules(chunk):
    rules = "现象:" + ExtractNewFactory_Fault_phnm(chunk) + "\n" + "原因：" + ExtractNewFactory_Fault_reason(chunk)
    return rules
#返回运行参数限额
def GetParam(index,chunk):
    listStr = SplitData(chunk)
    param = MatchParameter(listStr)
#返回其他工厂同样现象的样例
def GetExam1(chunk):
    listStr = SplitData(chunk)
    return MatchFactoryA(listStr) 
def GetExam2(chunk):
    listStr = SplitData(chunk)
    return MatchFactoryB(listStr) 
#大模型问答
def UseLModel(index, chunks):
    if index<len(chunks):
        chunk = chunks[index]
        listStr = SplitData(chunk)
        system = listStr[0]
        equipment  = ExtractName(chunk)
        param = MatchParameter(listStr)
        # phnm = listStr[3]
        # print(f"设备名字：{system}")
        # print(f"故障现象：{equipment}")
        # print(f"运行参数限额：{param}")
        phnm = ExtractNewFactory_Fault_phnm(chunk)
        reason = ExtractNewFactory_Fault_reason(chunk)
        
        fA_condition = MatchFactoryA(listStr) 
        
        fB_condition = MatchFactoryB(listStr) 
        question = f"当前我是一名电厂的工作人员，我需要根据两个电厂的历史故障判据和新电厂的规程文件由此梳理出新电厂的故障判据。\n\
新电厂c出故障的设备是{system}，该设备的现象是{equipment}\n\
c电厂规程文件中{equipment}现象如下：{phnm} \n\
c电厂规程文件中{equipment}原因如下： {reason}\n\
C电厂的规程文件中{equipment}参数限额如下： {param}\n\
A电厂出故障的设备是{system}，该设备的现象是{equipment}，该设备的判据条件是：{fA_condition} \n\
B电厂出故障的设备是{system}，该设备的现象是{equipment}，该设备的判据条件是：{fB_condition} \n\
请你参考A电厂的判据条件格式，若A电厂的判据条件是空，那么参考格式为：给煤量5分钟内变化量<3t/h ; 给煤机转速5分钟内变化量<30r/min ; 给煤机电流一分钟变化率>3A ; 磨煤机出口温度一分钟变化率>5℃ ; 磨煤机电流一分钟下降率>3A。\n\
然后参考B电厂的判据条件格式，若B电厂的判据条件是空，那么参考格式为：给煤量5分钟内变化量<3t/h ; 给煤机转速5分钟内变化量<30r/min ; 给煤机电流一分钟变化率>3A ; 磨煤机出口温度一分钟变化率>5℃ ; 磨煤机电流一分钟下降率>3A。\n\
有了A电厂和B电厂的判据参考，根据新电厂新电厂C的规程文件的现象和原因梳理出新电厂的判据条件， 最终的结果以json格式输出：['判据1', '判据2', '判据3']...，你的回答内容中只包含一条json格式且你的回答不包含任何其他内容\n"
        
        prompt = question
        # print(f"user:{prompt}")
        client = ZhipuAI(api_key="dbf4f92f5d600f4f7df9929fe9fe2714.NRNX96VSSWOJdNFj") # 填写您自己的APIKey
        response = client.chat.completions.create(
            model="glm-4",  # 填写需要调用的模型名称
            messages=[
                {"role": "user", "content": prompt}
            ],
        )
        answer = response.choices[0].message.content
    # print("ZhipuAI:",answer)
    

    # print(f"A工厂的判据：{fA_condition}")
    # print(f"B工厂的判据：{fB_condition}")
    # print("--------------------------------------")
        return answer
    return '空'
# print(chunks[1])
# UseLModel(2, chunks)
# print(GetPhnmName(chunks[2]))
# 数据匹配
# for index, chunk in enumerate(chunks) :
#     listStr = SplitData(chunk)
    
#     system = listStr[0]
#     equipment  = ExtractName(chunk)
#     param = MatchParameter(listStr)
#     # phnm = listStr[3]
#     # print(f"设备名字：{system}")
#     # print(f"故障现象：{equipment}")
#     # print(f"运行参数限额：{param}")
#     phnm = ExtractNewFactory_Fault_phnm(chunk)
#     reason = ExtractNewFactory_Fault_reason(chunk)
#     fA_condition = MatchFactoryA(listStr) 
#     fB_condition = MatchFactoryB(listStr) 
#     question = f"当前我是一名电厂的工作人员，我需要根据两个电厂的历史故障判据和新电厂的规程文件由此梳理出新电厂的故障判据。\n\
# 新电厂c出故障的设备是{system}，该设备的现象是{equipment}\n\
# c电厂规程文件中{equipment}现象如下：{phnm} \n\
# c电厂规程文件中{equipment}原因如下： {reason}\n\
# C电厂的规程文件中{equipment}参数限额如下： {param}\n\
# A电厂出故障的设备是{system}，该设备的现象是{equipment}，该设备的判据条件是：{fA_condition} \n\
# B电厂出故障的设备是{system}，该设备的现象是{equipment}，该设备的判据条件是：{fA_condition} \n\
# 请你参考A电厂的判据条件格式，若A电厂的判据条件是空，那么参考格式为：给煤量5分钟内变化量<3t/h ; 给煤机转速5分钟内变化量<30r/min ; 给煤机电流一分钟变化率>3A ; 磨煤机出口温度一分钟变化率>5℃ ; 磨煤机电流一分钟下降率>3A。\n\
# 然后参考B电厂的判据条件格式，若B电厂的判据条件是空，那么参考格式为：给煤量5分钟内变化量<3t/h ; 给煤机转速5分钟内变化量<30r/min ; 给煤机电流一分钟变化率>3A ; 磨煤机出口温度一分钟变化率>5℃ ; 磨煤机电流一分钟下降率>3A。\n\
# 有了A电厂和B电厂的判据参考，根据新电厂新电厂C的规程文件的现象和原因梳理出新电厂的判据条件，最终的结果以json格式输出：['判据1', '判据2', '判据3']...\n"
    
#     prompt = question
#     print(f"user:{prompt}")
#     response = client.chat.completions.create(
#         model="glm-4",  # 填写需要调用的模型名称
#         messages=[
#             {"role": "user", "content": prompt}
#         ],
#     )
#     answer = response.choices[0].message.content
#     print("ZhipuAI:",answer)
    

#     # print(f"A工厂的判据：{fA_condition}")
#     # print(f"B工厂的判据：{fB_condition}")
#     print("--------------------------------------")
    