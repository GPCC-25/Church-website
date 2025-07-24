from fastapi import FastAPI
from app.routes import announcement_route, auth_route


app = FastAPI()


# routes
app.include_router(announcement_route.router)
app.include_router(auth_route.router)
