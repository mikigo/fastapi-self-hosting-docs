import uvicorn

from fastapi_self_hosting_docs import FastAPI

app = FastAPI()

uvicorn.run(app)
