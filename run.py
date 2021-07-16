import os
import uvicorn

from app import app

def run():
    host = os.getenv('HOST', "0.0.0.0")
    port = os.getenv('PORT', 8000)
    uvicorn.run("run:app", host=host, port=port, reload=True)

if __name__ == '__main__':
    run()

    