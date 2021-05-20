# -*- coding: utf-8 -*-

from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from typing import Optional
from neo4j.exceptions import ConstraintError
from models import obj_company
from models.company import CompanyModel

app = FastAPI(
    title='ERP Accounts',
    description='This is a auto gen doc for Account object.'
)


@app.on_event('shutdown')
async def shutdown_event():
    pass


@app.post("/accounts")
async def create_a_new_account(account: CompanyModel, account_type: str = 'enterprise'):
    if account_type == 'enterprise':
        try:
            # TODO: check constraint tax_code is unique and isn't deleted yet
            obj_company.fn_create_or_update_a_company(**account.dict())
            return JSONResponse(content={'message': "Created successfully."}, status_code=201)
        except ConstraintError:
            return JSONResponse(content={'message': "Already exists."})
    else:
        # TODO: create a personal account
        pass


@app.put("/accounts/{id_or_taxcode}")
async def update_an_account(id_or_taxcode, account: CompanyModel, account_type: str = 'enterprise'):
    if account_type == 'enterprise':
        obj_company.fn_create_or_update_a_company(id_or_taxcode, **account.dict())
        return JSONResponse(content={'message': "Updated successfully."})
    else:
        # TODO: update a personal account
        pass


@app.delete("/accounts/{id_or_taxcode}")
async def delete_an_account(id_or_taxcode, account_type: str = 'enterprise'):
    # node_id may be node's id or node's tax_code
    if account_type == 'enterprise':
        obj_company.fn_delete_a_company(id_or_taxcode)
    else:
        # TODO: delete a personal account
        pass
    return JSONResponse(content={'message': "Deleted."})


@app.get("/accounts/search")
async def search_accounts(q: Optional[str] = Query(None, max_length=69), account_type: str = 'enterprise', limit: int = 10):
    if account_type == 'enterprise':
        records = obj_company.fn_fulltext_search_and_filter(query_string=q, limit=limit)
        return JSONResponse(content={'results': records})
    else:
        pass


@app.get("/accounts/{id_or_taxcode}")
async def read_an_account_by_id_or_taxcode(id_or_taxcode, account_type: str = 'enterprise'):
    if account_type == 'enterprise':
        record = obj_company.fn_get_a_company_by_id_or_taxcode(id_or_taxcode)
        return JSONResponse(status_code=200, content={'result': record['company']}) if record else JSONResponse(status_code=204)
    else:
        # TODO: read a personal account
        pass


@app.head("/accounts/{id_or_taxcode}/exists")
async def check_an_account_if_exists(id_or_taxcode, account_type: str = 'enterprise'):
    if account_type == 'enterprise':
        record = obj_company.fn_get_a_company_by_id_or_taxcode(id_or_taxcode)
        return JSONResponse(status_code=200) if record else JSONResponse(status_code=204)
    else:
        # TODO: check a personal account if exists
        pass
