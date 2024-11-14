import fastapi

from fastapi.middleware.cors import CORSMiddleware

app = fastapi.FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 假设你有一个环境变量或配置文件来存储你的 OpenAI API 密钥
OPENAI_API_KEY = "你的key"
OPENAI_API_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"


@app.middleware("http")
async def add_process_time_header(request: fastapi.Request, call_next):
    import time
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    print(f"Processed {request.method} {request.url} in {process_time:.4f} seconds")
    return response

from openai import OpenAI
client = OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_API_URL)

@app.post("/chat/completions")
async def chat_completions(request: fastapi.Request):
    request_data = await request.json()
    print("completions", request_data)
    response = client.chat.completions.create(**request_data)
    return response.model_dump_json()


@app.get("/models")
async def get_models():
    response = client.models.list()
    return response.model_dump_json()

# 使用 uvicorn 启动服务
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
