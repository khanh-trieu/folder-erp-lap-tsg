from typing import Optional, List
import neo4j
from pydantic import BaseModel
from config import *
from models.prices import PricesModel, SvcPrices
from models.product_family import SvcProFamily, ProFamilyModel
from models.vendors import VendorsModel, SvcVendors
from utils import neo4j_conn
from utils.singleton import Singleton


class ProductsModel(BaseModel):
    sku: Optional[str]
    code: str
    name: str
    is_hard_ware: Optional[bool]
    is_antivirus: Optional[bool]
    unit: Optional[str]
    is_effective: Optional[bool]


class RequestMultiModel(BaseModel):
    product: Optional[ProductsModel]
    vendor: Optional[VendorsModel]
    prices: Optional[List[PricesModel]]
    product_family: Optional[ProFamilyModel]


class SvcProducts(metaclass=Singleton):
    def __init__(self):
        self.dbname = neo4j_conn.neo4j_db
        self.driver = neo4j_conn.driver

    def fn_create_or_update_a_product(self, id_or_code_product=None, **props):
        with self.driver.session(database=self.dbname) as session:
            tx = session.begin_transaction()
            props_null_filtered = {k: v for k, v in props.items() if v}
            prices = props_null_filtered.pop('prices', [])
            if not id_or_code_product:  # create
                product_node_id = self._create_a_node_product(tx, **props['product'])
            else:  # update
                product_node_id = self._update_a_node_product(tx, id_or_code_product, **props['product'])
            if 'product_family' in props_null_filtered:
                product_family_node_id = SvcProFamily.create_a_node_profamily(tx, **props['product_family'])
                self._create_rel_product_has_family(tx, product_node_id, product_family_node_id)
            if 'vendor' in props_null_filtered:
                vendor_node_id = SvcVendors.create_a_node_vendor(tx, **props['vendor'])
                self._create_rel_family_of_vendor(tx, vendor_node_id, product_family_node_id)
            for price in prices:
                price_node_id = SvcPrices.create_a_node_price(tx, **price)
                self._create_rel_product_has_an_price(tx, product_node_id, price_node_id)
            tx.commit()
            tx.close()

    def fn_update(self, code, **props):
        if 'code' in props.keys():
            del props['code']
        props_null_filtered = {k: v for k, v in props.items() if v}
        with self.driver.session(database=self.dbname) as session:
            session.write_transaction(self._update_a_node, code, **props_null_filtered)

    def fn_delete_a_product(self, id_or_code):
        with self.driver.session(database=self.dbname) as session:
            session.write_transaction(self._delete_a_product_node, id_or_code)

    def fn_get_product_by_name_or_code(self, code_or_name, size, page):
        with self.driver.session(database=self.dbname, default_access_mode=neo4j.READ_ACCESS) as session:
            query = """
                   MATCH (p:Product)
                   WHERE (p.name STARTS WITH $code_or_name OR p.code STARTS WITH $code_or_name) AND p.deleted = false
                   WITH  count(p) as total
                   MATCH (p:Product)
                   WHERE (p.name STARTS WITH $code_or_name OR p.code STARTS WITH $code_or_name) AND p.deleted = false
                   WITH  p ,total
                   ORDER BY -p.updated_at
                   SKIP $page*$size LIMIT $size
                   WITH COLLECT(p{.*,id:id(p)}) as products, total as total
                   RETURN {total:total,list: products}
                """
            record = session.run(
                # """ MATCH (p:Product) WHERE (p.name STARTS WITH $code_or_name OR p.code STARTS WITH $code_or_name) AND p.deleted = false
                #  RETURN p{.*,id:id(p)} AS product order by -p.updated_at
                #  SKIP $page*$size LIMIT $size
                query, code_or_name=code_or_name, size=size, page=page
            ).single()
            # result = [dict(item['product']) for item in record]
            return record

    def fn_get_a_product_by_id(self, id_or_code):
        with self.driver.session(database=self.dbname, default_access_mode=neo4j.READ_ACCESS) as session:
            record = session.run(
                """ 
                    MATCH (p:Product),(p)-[r:HAS_PRICE]->(n),(p)-[rf:HAS_FAMILY]->(pf:ProductFamily),
                    (pf)-[rv:OF_VENDOR]-> (v:Vendor)
                    WHERE (id(p) = toInteger($id_or_code) OR p.code = $id_or_code) AND p.deleted = false 
                    and r.deleted = false AND pf.deleted = false AND rv.deleted = false
                    RETURN p{.*,id:id(p),prices:collect(n{.*,id:id(n)}),family:pf{.*,id:id(pf)},vendor:v{.*,id:id(v)}}
                    AS product 
                """,
                id_or_code=id_or_code
            ).single()
            return record

    def fn_get_all_product(self, page, size):
        with self.driver.session(database=self.dbname, default_access_mode=neo4j.READ_ACCESS) as session:
            result = session.run(
                # "MATCH (p:Product),(p)-[r:" + rel_product_has_an_price + "]->(pe:Price) "
                #                                                          "WHERE p.deleted = false and r.deleted = false "
                #                                                          "RETURN p{.*,id:id(p), price:collect(pe{.*,id :id(pe)})} ORDER BY -p.updated_at "
                #                                                          "SKIP $page*$size LIMIT $size",
                "MATCH (p:Product),(p)-[r:" + rel_product_has_an_price + "]->(pe:Price) "
                "WHERE p.deleted = false and r.deleted = false "
                "WITH  count(p) as total "
                "MATCH (p:Product),(p)-[r:" + rel_product_has_an_price + "]->(pe:Price) "
                "WHERE p.deleted = false and r.deleted = false "
                "WITH  p ,total  "
                "ORDER BY -p.updated_at "
                "SKIP $page*$size LIMIT $size "
                "WITH COLLECT(p{id:id(p),.*}) as products, total as total "
                "RETURN {total:total,list: products}",
                page=page, size=size
            ).single()
            # records = [dict(item['p']) for item in result]
            return result

    def fn_get_node_price_of_product(self, id_or_code_product):
        with self.driver.session(database=self.dbname) as session:
            result = session.run(
                "MATCH (p:Product) -[r:" + rel_product_has_an_price + "]-> (pe:Price) "
                "where r.deleted = false AND (id(p) = toInteger($id_or_code_product) OR p.code = $id_or_code_product) "
                "RETURN pe{.*,id :id(pe)}",
                id_or_code_product=id_or_code_product
            )
            records = [dict(item['pe']) for item in result]
            return records

    @staticmethod
    def _create_a_node_product(tx, **kwargs):
        query = (
            "CREATE (p:Product) "
            "SET p = $props, p.deleted = false, p.created_at = timestamp(), p.updated_at = timestamp() "
            "RETURN id(p) AS product_id"
        )
        return tx.run(query, props=kwargs).single()["product_id"]

    @staticmethod
    def _update_a_node_product(tx, id_or_code_product, **props):
        query = (
            """ MATCH (p:Product) 
            WHERE (id(p) = toInteger($id_or_code_product) OR p.code = $id_or_code_product) AND p.deleted = false 
            SET p += $props, p.updated_at = timestamp() 
            RETURN id(p) AS product_id """
        )
        return tx.run(query, id_or_code_product=id_or_code_product, props=props).single()["product_id"]

    @staticmethod
    def _delete_a_product_node(tx, id_or_code):
        query = (
            "MATCH (p:Product)-[r]->(n) "
            "WHERE id(p) = toInteger($id_or_code) OR p.code = $id_or_code "
            "SET p.deleted = true, c.updated_at = timestamp(), "
            "r.deleted = true, r.updated_at = timestamp() "
        )
        tx.run(query, id_or_code=id_or_code)

    @staticmethod
    def _get_all_product_node(self):
        with self.driver.session(database=self.dbname, default_access_mode=neo4j.READ_ACCESS) as session:
            record = session.run("MATCH (c:Product) RETURN c AS company").single()
            return record

    @staticmethod
    def _create_rel_product_has_an_vendor(tx, product_id, vendor_id):
        query = (
                "MATCH (p:Product), (v:vendor)  "
                "WHERE id(p)=$product_id AND id(v)=$vendor_id  "
                "MERGE ((p) -[r:" + rel_vendor_has_an_product + "]-> (v) ) "
                "ON CREATE "
                "SET r.deleted = false, r.updated_at=timestamp() , r.created_at=timestamp() "
                "ON MATCH "
                "SET  r.created_at = timestamp() "
        )
        tx.run(query, product_id=product_id, vendor_id=vendor_id)

    @staticmethod
    def _create_rel_product_has_an_price(tx, product_id, price_id):
        query = (
                "MATCH (p:Product), (pe:Price) "
                "WHERE id(p) = $product_id AND id(pe) = $price_id "
                "MERGE (p)-[r:" + rel_product_has_an_price + "]->(pe) "
                "ON CREATE "
                "   SET r.deleted = false, r.updated_at=timestamp() , r.created_at=timestamp()"
                "ON MATCH "
                "   SET  r.created_at = timestamp() "
        )
        tx.run(query, product_id=product_id, price_id=price_id)

    @staticmethod
    def _create_rel_product_has_family(tx, product_id, product_family_node_id):
        query = (
                "MATCH (p:Product), (pf:" + label_node_family + ") "
                "WHERE id(p) = $product_id AND id(pf) = $product_family_node_id "
                "MERGE (p)-[r:" + rel_product_has_an_family + "]->(pf) "
                "ON CREATE "
                "   SET r.deleted = false, r.updated_at=timestamp() , r.created_at=timestamp()"
                "ON MATCH "
                "   SET r.deleted = false, r.created_at = timestamp() "
        )
        tx.run(query, product_id=product_id, product_family_node_id=product_family_node_id)

    @staticmethod
    def _create_rel_family_of_vendor(tx, vendor_node_id, product_family_node_id):
        query = (
                "MATCH (v:Vendor), (pf:" + label_node_family + ") "
                "WHERE id(v) = $vendor_node_id AND id(pf) = $product_family_node_id "
                "MERGE (pf)-[r:" + rel_family_of_vendor + "]->(v) "
                "ON CREATE "
                "   SET r.deleted = false, r.updated_at=timestamp() , r.created_at=timestamp() "
                "ON MATCH "
                "   SET r.deleted = false, r.created_at = timestamp() "
        )
        tx.run(query, vendor_node_id=vendor_node_id, product_family_node_id=product_family_node_id)

    @staticmethod
    def _delete_all_rel_product_has_family(tx, product_id):
        query = (
                "MATCH (p:Product)-[r:" + rel_product_has_an_family + "]-> (pf:" + label_node_family + ") "
                "where id(p)= $product_id  "
                "SET r.deleted = false "
        )
        tx.run(query, product_id=product_id)
