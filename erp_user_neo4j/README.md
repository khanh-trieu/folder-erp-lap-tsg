# Step by steps to setup develoyment environment

* Install `python=3.8+` on local machine
* Install `Neo4j enterprise` on local machine
* Run `cypher-cell` and login to shell
* On shell, run `USE erp CREATE CONSTRAINT company_constraint IF NOT EXISTS ON (n:Company) ASSERT n.tax_code IS UNIQUE`
* Set env vars: `NEO4J_URI`, `NEO4J_USER`, `NEO4J_PASS`, `NEO4J_DB`
* Run `pip install -r requirements.txt`
* Run `uvicorn src.main:app --reload` to start application