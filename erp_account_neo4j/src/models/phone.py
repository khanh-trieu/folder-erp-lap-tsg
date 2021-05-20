# -*- coding: utf-8 -*-

from pydantic import BaseModel
from utils.singleton import Singleton
from utils import neo4j_conn


class PhoneModel(BaseModel):
    phone_number: str


class SvcPhone(metaclass=Singleton):
    def __init__(self):
        self.dbname = neo4j_conn.neo4j_db
        self.driver = neo4j_conn.driver

    @staticmethod
    def _create_a_phone_node_ifnot_exists(tx, **kwargs):
        query = (
            "MERGE (n:Phone {phone_number: $phone_number}) "
            "ON CREATE SET n = $phone_props, n.deleted = false, n.created_at = timestamp() "
            "RETURN id(n) AS phone_node_id"
        )
        return tx.run(query, phone_number=kwargs['phone_number'], phone_props=kwargs).single()["phone_node_id"]
