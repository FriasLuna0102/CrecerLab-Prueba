from app import create_app
from app.db.base import Base
from app.db.session import engine

Base.metadata.create_all(bind=engine)

app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)