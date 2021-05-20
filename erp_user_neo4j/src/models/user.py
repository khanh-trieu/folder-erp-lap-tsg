from typing import Optional, List

from neo4j.exceptions import ConstraintError
from pydantic import BaseModel
import neo4j
from utils import neo4j_conn
from utils.singleton import Singleton
from models.email import EmailModel, SvcEmail


class UserModel(BaseModel):
    user_name: str
    full_name: str


class SvcUser(metaclass=Singleton):
    def __init__(self):
        self.dbname = neo4j_conn.neo4j_db
        self.driver = neo4j_conn.driver

    def fn_create_an_user(self, email, **user_props):
        with self.driver.session(database=self.dbname) as session:
            tx = session.begin_transaction()
            record = self.fn_get_an_user_by_id_or_username(id_or_username=user_props['user_name'])
            if record:
                raise ConstraintError
            else:
                user_node_id = self._create_an_user_node(tx, **{'user_name': user_props['user_name'],
                                                                'full_name': user_props['full_name']})
                email_node_id = SvcEmail._create_an_email_node_ifnot_exists(tx,
                                                                            **{'email_address': email})
                self._create_rel_user_has_an_email(tx, user_node_id, email_node_id)
                tx.commit()
                tx.close()

    def fn_update_an_user(self, id_or_username, email, **user_props):
        with self.driver.session(database=self.dbname) as session:
            tx = session.begin_transaction()
            user_node_id = self._update_an_user(tx, id_or_username, **{'user_name': user_props['user_name'],
                                                     'email':email, 'full_name': user_props['full_name']})
            if email:
                email_node_id = SvcEmail._create_an_email_node_ifnot_exists(tx,
                                                                            **{'email_address': email})
                self._create_rel_user_has_an_email(tx, user_node_id, email_node_id)
            tx.commit()
            tx.close()

    @staticmethod
    def _create_an_user_node(tx, **kwargs):
        query = (
            "CREATE (n:User) "
            "SET n = $user_props, n.is_active = true, n.created_at = timestamp() "
            "RETURN id(n) AS user_id"
        )
        return tx.run(query, user_props=kwargs).single()["user_id"]

    @staticmethod
    def _create_rel_user_has_an_email(tx, user_id, email_id):
        query = (
            "MATCH (u:User), (e:Email) "
            "WHERE id(u) = $user_id AND id(e) = $email_id AND NOT EXISTS( (u)-[:HAS_EMAIL]-(e) )"
            "CREATE (u)-[r:HAS_EMAIL]->(e) "
            "SET r.is_active = true, r.created_at = timestamp()"
        )
        tx.run(query, user_id=user_id, email_id=email_id)

    @staticmethod
    def _update_an_user(tx, id_or_username, **kwargs):
        if kwargs['email']:
            query_email = ("MATCH (u:User) "
                           "WHERE (id(u) = toInteger($node_id) OR u.user_name = $node_id)"
                            "MATCH (u)-[r:HAS_EMAIL]-()"
                           "SET r.is_active = false")
            tx.run(query_email, node_id=id_or_username)
            kwargs.pop('email', [])
        else:
            kwargs.pop('email', [])
        query = (
            "MATCH (u:User) "
            "WHERE (id(u) = toInteger($node_id) OR u.user_name = $node_id)"
            "SET u += $user_props, u.updated_at = timestamp() "
            "RETURN id(u) as user_id"
        )
        return tx.run(query, node_id=id_or_username, user_props=kwargs).single()["user_id"]

    def fn_delete_an_user(self, id_or_username):
        with self.driver.session(database=self.dbname) as session:
            session.run(
                "MATCH (u:User)-[r]->(n) "
                "WHERE id(u) = toInteger($node_id) OR u.user_name = $node_id "
                "SET u.is_active = false, u.updated_at = timestamp(), "
                "r.is_active = false, r.updated_at = timestamp(), "
                "n.is_active = false, n.updated_at = timestamp()",
                node_id=id_or_username
            )

    def fn_get_an_user_by_id_or_username(self, id_or_username):
        with self.driver.session(database=self.dbname, default_access_mode=neo4j.READ_ACCESS) as session:
            record = session.run("MATCH (u:User) "
                                 "WHERE (id(u) = toInteger($node_id) OR u.user_name = $node_id) AND u.is_active = true "
                                 "RETURN u{ .user_name, .full_name, "
                                 "email: [(u)-[:HAS_EMAIL]->(e:Email) | e.email_address] } AS user ",
                                 node_id=id_or_username).single()
            return record
