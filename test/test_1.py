import uvicorn
from fastapi import FastAPI
import fastapi_self_hosting_docs

app = FastAPI(
    docs_url=None,
    redoc_url=None
)

fastapi_self_hosting_docs.mount(app)

uvicorn.run(app)
