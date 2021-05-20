# -*- coding: utf-8 -*-

from typing import Optional, List
from pydantic import BaseModel
import neo4j
from utils import neo4j_conn
from utils.singleton import Singleton
from models.email import EmailModel, SvcEmail
from models.phone import PhoneModel, SvcPhone


class CompanyModel(BaseModel):
    tax_code: str
    company_name: Optional[str]
    company_description: Optional[str]
    emails: Optional[List[EmailModel]]
    phones: Optional[List[PhoneModel]]


class SvcCompany(metaclass=Singleton):
    def __init__(self):
        self.dbname = neo4j_conn.neo4j_db
        self.driver = neo4j_conn.driver

    def fn_create_or_update_a_company(self, id_or_taxcode=None, **company_props):
        company_props_null_filtered = {k: v for k, v in company_props.items() if v}
        emails = company_props_null_filtered.pop('emails', [])
        phones = company_props_null_filtered.pop('phones', [])
        with self.driver.session(database=self.dbname) as session:
            tx = session.begin_transaction()
            if not id_or_taxcode:  # create
                company_node_id = self._create_a_company_node(tx, **company_props_null_filtered)
            else:  # update
                company_props_null_filtered.pop("tax_code")
                company_node_id = self._update_a_company_node(tx, id_or_taxcode, **company_props_null_filtered)
            for email in emails:
                email_node_id = SvcEmail._create_an_email_node_ifnot_exists(tx, **email)
                self._create_rel_company_has_an_email(tx, company_node_id, email_node_id)
            for phone in phones:
                phone_node_id = SvcPhone._create_a_phone_node_ifnot_exists(tx, **phone)
                self._create_rel_company_has_a_phone(tx, company_node_id, phone_node_id)
            tx.commit()
            tx.close()

    def fn_delete_a_company(self, id_or_taxcode):
        with self.driver.session(database=self.dbname) as session:
            session.run(
                "MATCH (c:Company)-[r]->(n) "
                "WHERE id(c) = toInteger($node_id) OR c.tax_code = $node_id "
                "SET c.deleted = true, c.updated_at = timestamp(), "
                "r.deleted = true, r.updated_at = timestamp(), "
                "n.deleted = true, n.updated_at = timestamp()",
                node_id=id_or_taxcode
            )

    def fn_get_a_company_by_id_or_taxcode(self, id_or_taxcode):
        with self.driver.session(database=self.dbname, default_access_mode=neo4j.READ_ACCESS) as session:
            record = session.run("MATCH (c:Company) "
                                 "WHERE (id(c) = toInteger($node_id) OR c.tax_code = $node_id) AND c.deleted = false "
                                 "RETURN c{.company_name, .tax_code, "
                                 "emails: [(c)-[:HAS_EMAIL]->(e:Email) | e{.email_address}], "
                                 "phones: [(c)-[:HAS_PHONE]->(p:Phone) | p{.phone_number}]} AS company",
                                 node_id=id_or_taxcode).single()
            return record

    def fn_fulltext_search_and_filter(self, query_string, limit):
        with self.driver.session(database=self.dbname, default_access_mode=neo4j.READ_ACCESS) as session:
            query = (
                "CALL db.index.fulltext.queryNodes('companyName', $query_string) YIELD node, score "
                "WHERE node.deleted = false "
                "RETURN id(node) AS id, node.company_name AS company_name, node.tax_code AS tax_code, score "
                "LIMIT $limit"
            )
            results = session.run(query, query_string=query_string, limit=limit)
            return [dict(r) for r in results]
    

    @staticmethod
    def _create_a_company_node(tx, **kwargs):
        query = (
            "CREATE (n:Company) "
            "SET n = $company_props, n.deleted = false, n.created_at = timestamp() "
            "RETURN id(n) AS company_id"
        )
        return tx.run(query, company_props=kwargs).single()["company_id"]

    @staticmethod
    def _update_a_company_node(tx, id_or_taxcode, **kwargs):
        query = (
            "MATCH (c:Company) "
            "WHERE (id(c) = toInteger($node_id) OR c.tax_code = $node_id) AND c.deleted = false "
            "SET c += $company_props, c.updated_at = timestamp() "
            "RETURN id(c) as company_id"
        )
        return tx.run(query, node_id=id_or_taxcode, company_props=kwargs)

    @staticmethod
    def _create_rel_company_has_an_email(tx, company_id, email_id):
        query = (
            "MATCH (c:Company), (e:Email) "
            "WHERE id(c) = $company_id AND id(e) = $email_id "
            "CREATE (c)-[r:HAS_EMAIL]->(e) "
            "SET r.deleted = false, r.created_at = timestamp()"
        )
        tx.run(query, company_id=company_id, email_id=email_id)

    @staticmethod
    def _create_rel_company_has_a_phone(tx, company_id, phone_id):
        query = (
            "MATCH (c:Company), (p:Phone) "
            "WHERE id(c) = $company_id AND id(p) = $phone_id "
            "CREATE (c)-[r:HAS_PHONE]->(p) "
            "SET r.deleted = false, r.created_at = timestamp()"
        )
        tx.run(query, company_id=company_id, phone_id=phone_id)
