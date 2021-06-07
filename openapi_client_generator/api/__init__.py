# type: ignore
from ..apimock import FastAPI

app = FastAPI()


from . import generator
from . import scaffolder


app.include_router(generator.router, prefix="/generator")
app.include_router(scaffolder.router, prefix="/scaffolder")
