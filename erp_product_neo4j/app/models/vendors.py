from typing import Optional
from pydantic import BaseModel
from utils import neo4j_conn
from utils.singleton import Singleton


class VendorsModel(BaseModel):
    code: str
    name: Optional[str]


class SvcVendors(metaclass=Singleton):
    def __init__(self):
        self.dbname = neo4j_conn.neo4j_db
        self.driver = neo4j_conn.driver

    @staticmethod
    def create_a_node_vendor(tx, **kwargs):
        query = (
            "MERGE (n:Vendor {code: $code}) "
            "ON CREATE SET n = $props, n.deleted = false, n.created_at = timestamp() "
            "RETURN id(n) AS vendor_node_id"
        )
        return tx.run(query, code=kwargs['code'], props=kwargs).single()["vendor_node_id"]