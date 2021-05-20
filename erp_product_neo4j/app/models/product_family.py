from typing import Optional
from pydantic import BaseModel

from config import label_node_family
from utils import neo4j_conn
from utils.singleton import Singleton


class ProFamilyModel(BaseModel):
    code: str
    name: str


class SvcProFamily(metaclass=Singleton):
    def __init__(self):
        self.dbname = neo4j_conn.neo4j_db
        self.driver = neo4j_conn.driver

    @staticmethod
    def create_a_node_profamily(tx, **kwargs):
        query = (
            "MERGE (n:"+label_node_family+" {code: $code}) "
            "ON CREATE SET n = $props, n.deleted = false, n.created_at = timestamp() "
            "RETURN id(n) AS pro_family_id"
        )
        return tx.run(query,code= kwargs['code'], props=kwargs).single()["pro_family_id"]
