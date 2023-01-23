from neo4j import GraphDatabase

# Replace with your own Neo4j connection URL and credentials
uri = "bolt://localhost:7687"
user = "neo4j"
password = "neo4j"

# Create a driver to connect to the database
driver = GraphDatabase.driver(uri, auth=(user, password))

# Use the driver to create a session to interact with the database
with driver.session() as session:
    # Run a Cypher query to retrieve all nodes in the database
    result = session.run("MATCH (n) RETURN n")
    # Print the results
    for record in result:
        print(record)

# Close the driver when you're finished
driver.close()