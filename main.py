import uvicorn
from fastapi import FastAPI

from src.routes import contacts, auth, users

app = FastAPI()

app.include_router(contacts.router, prefix='/api')
app.include_router(auth.router, prefix='/auth')
app.include_router(users.router, prefix='/user')


# @app.on_event("startup")
# def startup():
#     pass


@app.get("/")
def read_root():
    return {"message": "Hello World"}


if __name__ == '__main__':
    uvicorn.run('main:app', port=8000, reload=True)