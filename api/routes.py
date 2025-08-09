from fastapi import HTTPException
from api.schemas import ItemCreate, DeployData
from kubernates_deployment.deployer import AppDeployer

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
    async def deploy_data(self, item: DeployData):
        # item dict olarak kullanmak için
        item_dict = item.dict()
        print(item_dict)
        namespace=item_dict['name']
        self.deploy_process= AppDeployer(item_dict,namespace)
     
        
        return {
            "message": "Item created successfully!",
            "item": item_dict
        }