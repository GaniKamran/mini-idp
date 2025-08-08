from fastapi import HTTPException
from api.schemas import ItemCreate

class ItemHandler:
    def __init__(self):
        self.items = {1: "Item One", 2: "Item Two", 3: "Item Three"}

    async def root(self):
        return {"message": "Welcome to My API!"}

    async def get_item(self, item_id: int):
        item = self.items.get(item_id)
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        return {"item_id": item_id, "item_name": item}

    async def create_item(self, item: ItemCreate):
        return {"message": "Item created successfully!", "item": item}