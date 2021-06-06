def return_self(self):
    return self


def endpoint(**kwargs):
    return return_self


class MockAPI:
    async def __call__(self, scope, receive, send):
        raise NotImplementedError("fastapi is not installed.")

    def __getattr__(self, name):
        return endpoint


app = MockAPI()

try:
    from fastapi import FastAPI

    app = FastAPI()  # type: ignore
except:
    pass
