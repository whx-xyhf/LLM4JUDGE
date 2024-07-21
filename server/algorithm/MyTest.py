from algorithm.MatchData import *
from zhipuai import ZhipuAI
from FlagEmbedding import FlagModel
import numpy as np

#这个方法的作用是提取新工厂的故障现象的名称
def ExtractName(strs):
    singleStrs = strs.split('\n')
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
    # rules = "现象:" + ExtractNewFactory_Fault_phnm(chunk)
    rules = ExtractNewFactory_Fault_phnm(chunk)
    return rules


##############################
#返回运行参数限额
def embedding(sentences, model_path):
    model = FlagModel(model_path, query_instruction_for_retrieval="为这个句子生成表示用以检索相关文章：", use_fp16=True)
    return model.encode(sentences)
def get_context_data(vector, vectors):
    distance = vector @ vectors.T   #得到点击后的 "相似度" （个人理解）mul(A[1*1],B[1*n]) = C[1*n]
    # print(distance) 
    
    distance = distance[0]
    # index = np.argsort(-distance) #降序排序
    return distance

def GetParam(chunk, RunParam, listPhnm):
    #相似度模型路径
    model = r"E:\临时下载资源\文本相似度匹配\bge-large-zh"

    listStr = chunk.split('\n')

    # 获取dingzhiqingce下的所有键
    dingzhiqingce_keys = [inner_dict.keys() for inner_dict in RunParam]
    # 将dingzhiqingce_keys转换为包含所有单个键的列表
    all_keys = [key for keys in dingzhiqingce_keys for key in keys] 
    # print(all_keys)   #测试
    index = -1
    #先匹配设备名 找到运行参数
    for i,name in enumerate(listStr):
        for j,targetName in enumerate(all_keys):
            if GetSimilarity(name, targetName) > 0.5: ######---->>>>此处有待修改
                index = j
                break
        if index!=-1:
            break
    if index==-1:
        return '空'
    else:
        out = []
        
        targert_runP = RunParam[index]
        key_name = list(RunParam[index].keys())[0]
        
        array2_runP = targert_runP[key_name]    #得到某个设备具体的参数限额表格

        cnt = 1 #cnt 的作用是 使得现象呈现为1···, 2···, 3···,···
        param = ''
        flag = [0 for r,row in enumerate(array2_runP) if r > 0]
        # print(f"\narray2:\n{array2_runP}\n")    #测试
        for i,s in enumerate(listPhnm):
            #相似度计算
            #实验组
            org = [s] 
            #对照组
            compare = [row[0] for r,row in enumerate(array2_runP) if r > 0]
            model = r"E:\临时下载资源\文本相似度匹配\bge-large-zh"
            A = embedding(org, model)
            B = embedding(compare,model)
            #拿实验组和对照组进行点积
            var = get_context_data(A, B)
            seq =np.argsort(-var)   #降序排序得到下标

            print(f"\norigional = {org}\ncompare = {compare}\nsimilarity = {var}\n")#数据测试
           
            #设置阈值
            threshold = 0.8
            
            #遍历循环相似列表
            if var[seq[0]] >= threshold:    #第一次阈值比较(说名当前的相似度高 优先选取)
                for t,id in enumerate(seq):
                    outStr = ""
                    simil = var[id]
                    #如果当前得到的 "相似度" > 阈值 and 当前的值未参与过比较 则得到相似的单元
                    if flag[id]==0 and simil >= threshold:
                        flag[id] = 1
                        #获取与现象相似的运行参数
                        for k,col in enumerate(array2_runP[id+1]): #id+1 是因为表格的第一行是没在compare里的
                            if col != '': 
                                col = col.replace('\n', '')
                                array2_runP[0][k] = array2_runP[0][k].replace('\n', '')
                                if k==0:
                                    outStr = str(cnt) + ')' + array2_runP[0][k] + ':' + col
                                else:
                                    outStr = outStr + ',' + array2_runP[0][k] + ':' + col
                        outStr += '。'
                        cnt+=1
                        param+=outStr
                        
            elif var[seq[0]] >=0.7  and var[seq[0]] < threshold:
                    threshold = 0.7
                    for t,id in enumerate(seq):
                        outStr = ""
                        simil = var[id]
                        #如果当前得到的 "相似度" > 阈值 and 当前的值未参与过比较 则得到相似的单元
                        if flag[id]==0 and simil >= threshold:
                            flag[id] = 1
                            #获取与现象相似的运行参数
                            for k,col in enumerate(array2_runP[id+1]): #id+1 是因为表格的第一行是没在compare里的
                                if col != '': 
                                    col = col.replace('\n', '')
                                    array2_runP[0][k] = array2_runP[0][k].replace('\n', '')
                                    if k==0:
                                        outStr = str(cnt) + ')' + array2_runP[0][k] + ':' + col
                                    else:
                                        outStr = outStr + ',' + array2_runP[0][k] + ':' + col
                            outStr += '。'
                            cnt+=1
                            param+=outStr
            elif var[seq[0]] >= 0.65555555  and var[seq[0]] < 0.7:
                    threshold = 0.65555555
                    for t,id in enumerate(seq):
                        outStr = ""
                        simil = var[id]
                        #如果当前得到的 "相似度" > 阈值 and 当前的值未参与过比较 则得到相似的单元
                        if flag[id]==0 and simil >= threshold:
                            flag[id] = 1
                            #获取与现象相似的运行参数
                            for k,col in enumerate(array2_runP[id+1]): #id+1 是因为表格的第一行是没在compare里的
                                if col != '': 
                                    col = col.replace('\n', '')
                                    array2_runP[0][k] = array2_runP[0][k].replace('\n', '')
                                    if k==0:
                                        outStr = str(cnt) + ')' + array2_runP[0][k] + ':' + col
                                    else:
                                        outStr = outStr + ',' + array2_runP[0][k] + ':' + col
                            outStr += '。'
                            cnt+=1
                            param+=outStr         
                       
        if param != '':  
            return param  
        else:
            return '空'                 
            

        # for i,s in enumerate(listPhnm):
        #     for j,row in enumerate(array2_runP):
        #         if GetSimilarity(s, row[0]) > 0.12: #匹配现象与参数限额具体参数是否相似
        #             outStr = ""
        #             for k,col in enumerate(row):
        #                 if col != '': 
        #                     col = col.replace('\n', '')
        #                     array2_runP[0][k] = array2_runP[0][k].replace('\n', '')
        #                     if k==0:
        #                         outStr = str(cnt) + ')' + array2_runP[0][k] + ':' + col
        #                     else:
        #                         outStr = outStr + ',' + array2_runP[0][k] + ':' + col
        #             # out.append(outStr)
        #             cnt+=1
        #             param+=outStr
        # return param
            

    

#返回其他工厂同样现象的样例
def GetExample(chunk,example):
    sys = 1         #系统(设备)名称列
    phnm = 4        #故障现象列
    condition = 13  #判据条件列
    L = SplitData(chunk)
    for u,cell in enumerate(L):
        # for i,example in enumerate(examples):
        for j,singleData in enumerate(example):
            #是否能和出故障的节点做出匹配
            # print(f"my core test: sys = {singleData[sys]} phnm={singleData[phnm]}")
            if GetSimilarity(cell, singleData[sys]) > 0.8:
                for v,cell in enumerate(L):
                    if GetSimilarity(cell, singleData[phnm]) > 0.6:
                        return singleData[condition]
    return '空'


#大模型问答
def UseLModel(index, chunks,phnm,param,example1,example2):
    if index<len(chunks):
        chunk = chunks[index]
        listStr = SplitData(chunk)
        system = listStr[0]
        equipment  = ExtractName(chunk)

        fA_condition = example1 
        fB_condition = example2 
        #region备份

        question = f"当前我是一名电厂的工作人员，我需要根据两个电厂的历史故障判据和新电厂的规程文件由此梳理出新电厂的故障判据。\n\
新电厂出故障的设备是{system}，该设备的现象是{equipment}\n\
新电厂规程文件中{equipment}现象如下：{phnm} \n\
新电厂的规程文件中{equipment}运行参数如下： {param}\n\
A电厂出故障的设备是{system}，该设备的现象是{equipment}，该设备的判据条件是：{fA_condition} \n\
B电厂出故障的设备是{system}，该设备的现象是{equipment}，该设备的判据条件是：{fB_condition} \n\
请你参考A电厂的判据条件格式，若A电厂的判据条件是空，那么参考格式为：给煤量5分钟内变化量<3t/h ; 给煤机转速5分钟内变化量<30r/min ; 给煤机电流一分钟变化率>3A ; 磨煤机出口温度一分钟变化率>5℃ ; 磨煤机电流一分钟下降率>3A。\n\
然后参考B电厂的判据条件格式，若B电厂的判据条件是空，那么参考格式为：给煤量5分钟内变化量<3t/h ; 给煤机转速5分钟内变化量<30r/min ; 给煤机电流一分钟变化率>3A ; 磨煤机出口温度一分钟变化率>5℃ ; 磨煤机电流一分钟下降率>3A。\n\
有了A电厂和B电厂的判据参考，根据新电厂的设备现象去匹配规程文件中密切相关的运行参数，\
规程文件中的运行参数并不是所有都是与现象完全一致的，请你仔细核对，由此梳理出新电厂的\
判据条件， 最终的结果以json格式输出：['判据1', '判据2', '判据3']...，你的回答内容\
中仅仅只能包含一条json格式并且你的回答除了一条json格式外不包含任何其他内容"
        #endregion备份
        
#         question = f"当前我是一名电厂的工作人员，我需要根据两个电厂的历史故障判据和新电厂的规程文件由此梳理出新电厂的故障判据。\n\
# 新电厂出故障的设备是{system}，该设备的现象是{equipment}\n\
# 新电厂规程文件中{equipment}现象如下：{phnm} \n\
# 新电厂的规程文件中{equipment}运行参数如下： {param}\n\
# A电厂出故障的设备是{system}，该设备的现象是{equipment}，该设备的判据条件是：{fA_condition} \n\
# B电厂出故障的设备是{system}，该设备的现象是{equipment}，该设备的判据条件是：{fB_condition} \n\
# 请你参考A电厂的判据条件格式，若A电厂的判据条件是空，那么参考格式为：给煤量5分钟内变化量<3t/h ; 给煤机转速5分钟内变化量<30r/min ; 给煤机电流一分钟变化率>3A ; 磨煤机出口温度一分钟变化率>5℃ ; 磨煤机电流一分钟下降率>3A。\n\
# 然后参考B电厂的判据条件格式，若B电厂的判据条件是空，那么参考格式为：给煤量5分钟内变化量<3t/h ; 给煤机转速5分钟内变化量<30r/min ; 给煤机电流一分钟变化率>3A ; 磨煤机出口温度一分钟变化率>5℃ ; 磨煤机电流一分钟下降率>3A。\n\
# 有了A电厂和B电厂的判据参考，根据新电厂的设备现象去匹配规程文件中密切相关的运行参数，\
# 规程文件中的运行参数并不是所有都是与现象完全一致的，请你仔细核对，由此梳理出新电厂的\
# 判据条件。你的回答内容中要包括以下内容：\
# 1.以json格式输出：['判据1', '判据2', '判据3']...，。\
# 2.对你输出的判据找到对应规程文件中运行参数的序号，规程文件中{equipment}运行参数如下： {param}。结果以json格式输出,例如['1)','4)']"
        
        prompt = question
        # print(f"user:{prompt}")
        client = ZhipuAI(api_key="5a85128e04ee0faff3db9af4f43f4b23.RaLoQhra97kAFXv8") # 填写您自己的APIKey
        response = client.chat.completions.create(
            model="glm-4",  # 填写需要调用的模型名称
            messages=[
                {"role": "user", "content": prompt}
            ],
        )
        answer = response.choices[0].message.content
        print(f"\nZhipuAI:{answer}\n")

        return answer
    return '空'



    