from typing import Optional
from pydantic import BaseModel
from utils import neo4j_conn
from utils.singleton import Singleton


class PricesModel(BaseModel):
    effective_at: Optional[int]
    expire_at: Optional[int]
    price: Optional[float]
    import_price: Optional[float]
    description: Optional[str]


class SvcPrices(metaclass=Singleton):
    def __init__(self):
        self.dbname = neo4j_conn.neo4j_db
        self.driver = neo4j_conn.driver

    @staticmethod
    def create_a_node_price(tx, **kwargs):
        query = (
            "CREATE (n:Price) "
            "SET n = $props, n.deleted = false, n.created_at = timestamp(), n.updated_at = timestamp() "
            "RETURN id(n) AS price_id"
        )
        return tx.run(query, props=kwargs).single()["price_id"]

    @staticmethod

    @staticmethod
    def delete_a_node_price(tx, price_node_id):
        query = (
            "MATCH (pe:Price)<-[r]->(n) "
            "WHERE id(pe) = toInteger($price_node_id)  "
            "SET pe.deleted = true, pe.updated_at = timestamp() "
        )
        return tx.run(query, price_node_id=price_node_id).single()["price_id"]

