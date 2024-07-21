from FlagEmbedding import FlagModel
import numpy as np
import json

def load_data(url):
    with open(url, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data


def triple2sentence(triples):
    sentences = []
    for items in triples:
        head = items['source']['name']
        relation = items['relationship']['type']
        tail = items['target']['name']
        sentences.append(head + "的" + relation + "是" + tail)
    return sentences

def embedding(sentences, model_path):
    model = FlagModel(model_path, query_instruction_for_retrieval="为这个句子生成表示用以检索相关文章：", use_fp16=True)
    return model.encode(sentences)

def save_embedding(embeddings, url):
    with open(url, 'w') as f:
        json.dump(embeddings.tolist(), f)
    print("save embedding successfully!")

def get_vector_db(url):
    with open(url, 'r') as f:
        data = json.load(f)
    return np.array(data)

# def get_context_data(data, vector, vectors, k):
#     distance = vector @ vectors.T
#     index = np.argsort(-distance)
#     context = []
#     for i in range(k):
#         context.append(data[index[0][i]])
#     return context
def get_context_data(vector, vectors, k):
    distance = vector @ vectors.T
    distance = distance[0]
    # for i,var in enumerate(distance):
    #     print(var)
    print(distance)
    # if len(distance) > 1:
    
    index = np.argsort(-distance)
    print(f"max = {distance[index[0]]}")
    print(index)
    return index
    context = []
    
if __name__ == "__main__":
    # url = '../data/graphData.json'
    # model = './bge-large-zh'
    model = r"E:\临时下载资源\文本相似度匹配\bge-large-zh"
    # embeddings_path = './data/embddings.json'
    # data = load_data(url)
    # sentences = triple2sentence(data)
    # embeddings = get_vector_db(embeddings_path)
    # embeddings = embedding(sentences, model)
    # save_embedding(embeddings, embeddings_path)
    qTest = ['汽泵前置泵出口或汽泵进口压力波动', '给水泵出口压力、给水流量急剧下降且大幅度晃动', '给水泵内有噪音及水击声，泵组振动增大']
    q1 = ["2.4.3.13 凝结水系统运行参数限额"]
    name = [
    "2.4.5 凝结水系统异常及事故处理"
]
    embeddings_ = embedding(q1, model)
    embeddings = embedding(name,model)
    index = get_context_data(embeddings_, embeddings, 10)


# if __name__ == "__main__":
#     url = '../data/graphData.json'
#     # model = './bge-large-zh'
#     model = r"E:\临时下载资源\文本相似度匹配\bge-large-zh\example.txt"
#     embeddings_path = './data/embddings.json'
#     data = load_data(url)
#     sentences = triple2sentence(data)
#     embeddings = get_vector_db(embeddings_path)
#     embeddings = embedding(sentences, model)
#     save_embedding(embeddings, embeddings_path)
#     q1 = ["项目对象为美国的项目有多少个？"]
#     embeddings_ = embedding(q1, model)
#     context_data = get_context_data(sentences, embeddings_, embeddings, 10)
#     print(context_data)
