from pydantic import BaseModel,Extra 

class DeployData(BaseModel):

    name: str  
    image: str
    port: int
    replicas:int
    env:dict
    
    class Config:
        extra = Extra.allow  

# class ItemCreate(BaseModel):
#     name: str
    
    
# {
#   "name": "my-app",
#   "image": "nginx:latest",
#   "replicas":1,
#   "port": 80,
#   "env": {
#     "DATABASE_URL": "postgresql://user:pass@host/db",
#     "REDIS_HOST": "redis-service",
#     "LOG_LEVEL": "debug"
#   }
# }