# Step by steps to setup develoyment environment

* Install `python=3.8+` on local machine
* Install `Neo4j enterprise` on local machine
* Run `cypher-cell` and login to shell
* On shell, run 
```cypher
USE erp CREATE CONSTRAINT company_constraint IF NOT EXISTS ON (n:Company) ASSERT n.tax_code IS UNIQUE;
USE erp CREATE CONSTRAINT company_taxcode IF NOT EXISTS ON (n:Company) ASSERT EXISTS (n.tax_code);
CALL db.index.fulltext.createNodeIndex("companyName", ["Company"], ["company_name"]);
USE erp CREATE CONSTRAINT email_constraint IF NOT EXISTS ON (n:Email) ASSERT n.email_address IS UNIQUE;
USE erp CREATE CONSTRAINT company_email IF NOT EXISTS ON (n:Email) ASSERT EXISTS (n.email_address);
USE erp CREATE CONSTRAINT phone_constraint IF NOT EXISTS ON (n:Phone) ASSERT n.phone_number IS UNIQUE;
USE erp CREATE CONSTRAINT company_phone IF NOT EXISTS ON (n:Phone) ASSERT EXISTS (n.phone_number);
```
* Set env vars: `NEO4J_URI`, `NEO4J_USER`, `NEO4J_PASS`, `NEO4J_DB`
* Run `pip install -r requirements.txt`
* Enter working directory `cd /<path_to_project_directory>/src`
* Run `uvicorn main:app --reload` to start application

# Visual studio code's lauch configuration

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: FastAPI",
            "type": "python",
            "request": "launch",
            "module": "uvicorn",
            "cwd": "${workspaceFolder}/src",
            "env": {
                "NEO4J_URI": "neo4j://localhost:7687",
                "NEO4J_USER": "<user>",
                "NEO4J_PASS": "<pass>",
                "NEO4J_DB": "<database>"
            },
            "args": [
                "main:app",
                "--reload"
            ],
            "jinja": false
        }
    ]
}
```