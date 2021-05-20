# -*- coding: utf-8 -*-

from pydantic import BaseModel, EmailStr
from utils.singleton import Singleton
from utils import neo4j_conn


class EmailModel(BaseModel):
    email_address: EmailStr


class SvcEmail(metaclass=Singleton):
    def __init__(self):
        self.dbname = neo4j_conn.neo4j_db
        self.driver = neo4j_conn.driver

    @staticmethod
    def _create_an_email_node_ifnot_exists(tx, **kwargs):
        query = (
            "MERGE (n:Email {email_address: $email_address}) "
            "ON CREATE SET n = $email_props, n.deleted = false, n.created_at = timestamp() "
            "RETURN id(n) AS email_node_id"
        )
        return tx.run(query, email_address=kwargs['email_address'], email_props=kwargs).single()["email_node_id"]
