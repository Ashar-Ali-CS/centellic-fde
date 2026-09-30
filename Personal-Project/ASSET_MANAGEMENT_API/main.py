
from fastapi import FastAPI

from routers import funds, portfolios

app = FastAPI( title ="Asset Management API ")




app.include_router(funds.router)

app.include_router(portfolios.router)


# curl http://127.0.0.1:8000/health

@app.get("/health")
def health():
    return {"status": "ok"}





