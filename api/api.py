from fastapi import FastAPI

from api.endpoints.rates import router

app = FastAPI(title='Dynatrace internship task', description='Paweł Cichowski', docs_url='/')

app.include_router(router.router, prefix='/rates')
