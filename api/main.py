from fastapi import FastAPI
from api.routers.carteira_router import router as carteiras_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="Carteira Digital API",
        version="1.0.0",
        description="API de carteira digital com SQL puro e FastAPI.",
    )

    app.include_router(carteiras_router)

    return app


app = create_app()

@app.get("/") 
def read_root():
    return {"mensagem": "API rodando com sucesso!"}