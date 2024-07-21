
from zhipuai import ZhipuAI
client = ZhipuAI(api_key="dbf4f92f5d600f4f7df9929fe9fe2714.NRNX96VSSWOJdNFj") # 填写您自己的APIKey

    
while True:
    prompt = input("user:")
    response = client.chat.completions.create(
        model="glm-4",  # 填写需要调用的模型名称
        messages=[
            {"role": "user", "content": prompt}
        ],
        stream=True,
    ) 
    
    answer = response.choices[0].message.content
    print("ZhipuAI:",answer)
