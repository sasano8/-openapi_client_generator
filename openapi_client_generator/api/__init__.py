"""fastapi用"""

from fastapi import FastAPI

app = FastAPI()


from . import generator, scaffolder

app.include_router(generator.router, prefix="/generator")
app.include_router(scaffolder.router, prefix="/scaffolder")
