from fastapi import FastAPI

app = FastAPI(title="Ultimate Tic-Tac-Toe")


@app.get("/")
def read_root():
    return {"message": "Ultimate Tic-Tac-Toe API is running!"}
