from neo4j import GraphDatabase
import logging
from neo4j.exceptions import ServiceUnavailable

class App:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        # Don't forget to close the driver connection when you are finished with it
        self.driver.close()


    def create_node(self, name, location, lat, lon, type):
        with self.driver.session(database="neo4j") as session:
            # Write transactions allow the driver to handle retries and transient errors
            result = session.execute_write(
                self._create_node, name, location, lat, lon, type)
            print("Created Node\n")

    def _create_node(tx, name, location, lat, lon, type):
        # To learn more about the Cypher syntax, see https://neo4j.com/docs/cypher-manual/current/
        # The Reference Card is also a good resource for keywords https://neo4j.com/docs/cypher-refcard/current/
        query = (
                "CREATE (n:PointOfInterest {lat: '43', location: 'point({srid:4327, x:-75, y:43})', lon: '-75', name: 'FIM', type: 'statue'})"
        )
        result = tx.run(query, name=name, location=location, lat=lat, lon=lon, type=type)
        try:
            return [{"n": row["n"]["name"]}
                    for row in result]
        # Capture any errors along with the query and data for traceability
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise

    def find_node(self, name):
        with self.driver.session(database="neo4j") as session:
            result = session.execute_read(self._find_node, name)
            for row in result:
                print("Found node: {row}".format(row=row))

    @staticmethod
    def _find_node(tx, name):
        query = (
            "MATCH (p:PointOfInterest) "
            "WHERE p.name = 'FIM' "
            "RETURN p"
        )
        result = tx.run(query, name=name)
        return [row["name"] for row in result]


if __name__ == "__main__":
    # Aura queries use an encrypted connection using the "neo4j+s" URI scheme
    uri = "neo4j+s://90b42d62.databases.neo4j.io"
    user = "<Username for Neo4j Aura instance>"
    password = "<Password for Neo4j Aura instance>"
    app = App(uri, user, password)

    # Informazioni riguardo il nome che si intende aggiungere
    location = ""
    name = ""
    lat = ""
    lon = ""
    type = ""

    app.create_node(name, location, lat, lon, type)

    # Ricerca del nodo appena creato
    app.find_node(name)

    # Creazione della relazione tra nodo appena creato ed un altro
    name2 = ""
    app.create_relationship()

    # Creazione indice sui nomi dei punti di interesse
    app.create_index()

    # Interrogazione avanzata
    app.make_query()

    # Modifica nodo creato
    app.edit_node()

    app.close()