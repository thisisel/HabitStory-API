import uvicorn

from app import app

def run():
    uvicorn.run("run:app", host="0.0.0.0", port=8000, reload=True)

if __name__ == '__main__':
    run()

    