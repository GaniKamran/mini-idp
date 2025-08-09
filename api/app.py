from fastapi import FastAPI
import uvicorn
from api.routes import ItemHandler

class MyAPI:
    def __init__(self):
        self.app = FastAPI()
        handler = ItemHandler()

        # self.app.add_api_route("/", handler.root, methods=["GET"])
        # self.app.add_api_route("/items/{item_id}", handler.get_item, methods=["GET"])
        self.app.add_api_route("/deploy/", handler.deploy_data, methods=["POST"])
        
    def run(self):
        uvicorn.run(self.app, host="127.0.0.1", port=8000)