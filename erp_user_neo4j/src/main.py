from typing import Optional

import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from neo4j.exceptions import ConstraintError
from models import obj_user
from models.user import UserModel


app = FastAPI(
    title='ERP Users',
    description='This is a auto gen doc for User object.'
)


@app.on_event('shutdown')
async def shutdown_event():
    pass


@app.post("/users")
def create_a_new_user(user: UserModel, email: str):
    # TODO: create a personal user
    try:
        obj_user.fn_create_an_user(email, **user.dict())
        return JSONResponse(content={'message': "Created successfully."}, status_code=201)
    except ConstraintError as error:
        return JSONResponse(content={'message': "Already exists."})


@app.put("/users/{id_or_username}")
def update_an_user(id_or_username: str,  user: UserModel, email: Optional[str] = ''):
    obj_user.fn_update_an_user(id_or_username, email, **user.dict())
    return dict(message="Updated successfully.")


@app.delete("/users/{id_or_username}")
def delete_an_account(id_or_username):
    # node_id may be node's id or node's tax_code
    obj_user.fn_delete_an_user(id_or_username)
    return JSONResponse(content={'message': "Deleted."})


@app.get("/users/{id}")
def read_an_user_by_user_name(id_or_username):
    record = obj_user.fn_get_an_user_by_id_or_username(id_or_username)
    return JSONResponse(status_code=200, content={'result': record['user']}) if record else JSONResponse(
        status_code=204)


@app.head("/accounts/{id_or_username}/exists")
def check_an_user_if_exists(id_or_username):
    record = obj_user.fn_get_an_user_by_id_or_username(id_or_username)
    return JSONResponse(status_code=200) if record else JSONResponse(status_code=204)


@app.get("/users")
def search_and_filter_users():
    pass


if __name__ == '__main__':
    uvicorn.run("main:app", host='0.0.0.0', port=8000, reload=True)


