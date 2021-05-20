import uvicorn
from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse
from neo4j.exceptions import ConstraintError

from models.products import *

app = FastAPI(
    title='ERP Products',
    description='This is a auto gen doc for Product object.'
)
obj = SvcProducts()


@app.on_event('shutdown')
async def shutdown_event():
    pass


@app.post("/products")
def create_a_note(request: RequestMultiModel):
    try:
        obj.fn_create_or_update_a_product(**request.dict())
        return JSONResponse(content={'message': "Created successfully."}, status_code=201)
    except ConstraintError:
        return JSONResponse(content={'message': "Already exists."})


@app.put("/products/{id_or_code_product}")
def update_by_code(id_or_code_product,request: RequestMultiModel):
    obj.fn_create_or_update_a_product(id_or_code_product,**request.dict())
    return JSONResponse(content={'message': "Updated successfully."})


@app.delete("/products/{id_or_code}")
def delete_an_product_by_id_or_code(id_or_code):
    obj.fn_delete_a_product(id_or_code)
    return JSONResponse(content={'message': "Deleted."})


@app.get("/products/{id_or_code}")
def get_detail_product_by_id_or_code(id_or_code):
    record = obj.fn_get_a_product_by_id(id_or_code)
    return JSONResponse(status_code=200, content={'result': record}) if record else JSONResponse(status_code=204)


@app.get("/products/search/{name_or_code}")
async def read_products_by_name_or_code(name_or_code,page:int=1,size:int=10):
    record = obj.fn_get_product_by_name_or_code(name_or_code,size,page-1)
    return JSONResponse(status_code=200, content={'result': record}) if record else JSONResponse(status_code=204)


@app.get("/products")
async def read_all_products(page:int=1,size:int=10):
    record = obj.fn_get_all_product(page-1,size)
    return JSONResponse(status_code=200, content={'result': record}) if record else JSONResponse(status_code=204)


@app.get("/products/{id_or_code_product}/price")
def get_price(id_or_code_product):
    record = obj.fn_get_node_price_of_product(id_or_code_product)
    return JSONResponse(status_code=200, content={'result': record}) if record else JSONResponse(status_code=204)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
