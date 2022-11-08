import pymongo

# MongoDB Server and Database Data
server = "mongodb://localhost:27017/"
database = "City"
collection = "City_Inspections"

def connect():
  myclient = pymongo.MongoClient(server)
  mydb = myclient[database]
  mycol = mydb[collection]
  return mycol


def insert(mycol):
  inspection = {"id" : "0000", "certificate_number" : "0000", "business_name" : "maxbubblegum",
  "date" : "April", "result" : "dumped", "sector" : "0000", "address" : {"city" : "0000",
  "zip" : "0000", "street" : "0000", "number" : "0000"}}  
  mycol.insert_one(inspection)
  

def update(mycol):
  inpsection = mycol.find_one({"id":"0000"})
  inspection['Inspector Name'] = 'Lorenzo Stigliano'
  mycol.update_one({"id":"0000"},{"$set":{"Inspector Name":"inspection"}}, upsert=False)
  pass


def query(mycol):
    # prima query : tutte le ispezioni di tipo warning ( = result) fatte tra Feb 20 2015 e Jun 9 2015 fatti nella s
    # tessa via (tal dei tali)

    # seconda query: tutte le ispezioni su aziende con lo stesso settore (Electronic Store - 001) 
    # con zip code compreso tra due valori x e y
    # e con la via che contenga la parola "ST"
    # ordina in ordine crescente sullo zip code
  
    # terza query: tutte le ispezioni con city BROOKLYN e tutte qulle di NEW YORK
    # prendo il settore Cicarette Retail Dealer - 127
    # prendo tutti quelli che abbiamo AVE nel street
    # ordine in base address.number

    # quarta query: fai una creazione di un set in cui abbiamo
    # settore - city - street - result
    # poi faccio un unwind 
    # poi conto tutti i settori di tipo X per la citta' di New York con result Warning di una stessa via

    # quinta query: conto le citta' che sono presenti nel json per un determinato tipo di settore
    


def main():
  # connect
  print("Trying to connect to: " + str(server))
  mycol = connect()
  print("OK\n")

  # insert
  print("Inserting new object inside: " + str(collection))
  insert(mycol)
  print("OK\n")
  
  # update
  print("Updating the collection: " + str(collection))
  update(mycol)
  print("OK\n")
  
  # query
  print("Query 1 on collection: " + str(collection))
  query(mycol)

  

if __name__ == "__main__":
  main()
