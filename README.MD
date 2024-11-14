# 设想

1. 使用fastapi 搭建一个api服务
2. cursor中将openai的base_url 设置为 本地fastapi服务
3. cursor的llm请求拦截，添加自定义参数，例如添加search参数，调用大模型自身提供的更多功能

## 现象

![alt text](image.png)
![alt text](20241114114703.png)

