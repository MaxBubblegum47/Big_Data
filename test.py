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
  # prova = mycol.find_one({"id":"0000"})
  # prova['ciao'] = '0001'
  # mycol.update_one({"id":"0000"},{"$set":{"sector":"prova"}}, upsert=False)
  pass

def query():
  pass


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


  

if __name__ == "__main__":
  main()