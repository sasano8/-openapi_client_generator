def return_self(self):
    return self


def endpoint(**kwargs):
    return return_self


class MockAPI:
    async def __call__(self, scope, receive, send):
        raise NotImplementedError("fastapi is not installed.")

    def include_router(self, **kwargs):
        pass

    def __getattr__(self, name):
        return endpoint


FastAPI = MockAPI
APIRouter = MockAPI

try:
    from fastapi import APIRouter  # type: ignore
    from fastapi import FastAPI  # type: ignore

except:
    pass
