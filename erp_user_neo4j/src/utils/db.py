import os
from neo4j import GraphDatabase
from utils.singleton import Singleton


class Neo4jDB(metaclass=Singleton):
    def __init__(self):
        self._load_neo4j_config_from_env()
        self.driver = GraphDatabase.driver(self.neo4j_uri, auth=(self.neo4j_user, self.neo4j_pass))

    def _load_neo4j_config_from_env(self):
        self.neo4j_uri = os.getenv("NEO4J_URI", "neo4j://localhost:7687")
        self.neo4j_user = os.getenv("NEO4J_USER", "neo4j")
        self.neo4j_pass = os.getenv("NEO4J_PASS", "neo4j")
        self.neo4j_db = os.getenv("NEO4J_DB", "neo4j")

    def close(self):
        self.driver.close()
