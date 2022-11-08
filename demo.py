import pymongo
import datetime

# MongoDB Server and Database Data
server = "mongodb://localhost:27017/"
database = "City"
collection = "City_Inspections_DB"

def connect():
  myclient = pymongo.MongoClient(server)
  mydb = myclient[database]
  mycol = mydb[collection]
  return mycol


def insert(mycol):
  inspection = {"id" : "00000-0000-ENFO", "certificate_number" : "17041999", "business_name" : "Videogames Center",
  "date" : "1999-4-17", "result" : "Fail", "sector" : "Videogames", "address" : {"city" : "Georgia",
  "zip" : "41030", "street" : "Rue de Baptiste", "number" : "19"}}  
  mycol.insert_one(inspection)
  

def update(mycol):
  mycol.update_one({"id":"00000-0000-ENFO"},{"$set":{"Inspector Name":"Lorenzo Stigliano"}}, upsert=False)
  


def query(mycol):
    #   ___ _        _      ___                    
    #  | __(_)_ _ __| |_   / _ \ _  _ ___ _ _ _  _ 
    #  | _|| | '_(_-|  _| | (_) | || / -_| '_| || |
    #  |_| |_|_| /__/\__|  \__\_\\_,_\___|_|  \_, |
    #                                         |__/ 
    # Every inspections within 2015-1-1 and 2015-6-30, that have this two type of result: Fail or Violation Issued
    # that are done in NEW YORK city at FREDERICK DOUGLASS BLVD. The result are sorted by business_name and only this field is displayed

    print("First Query:\n")
    result = mycol.find({"date" : {"$gte":"2015-1-1", "$lte":"2015-6-30"}, "result" : {"$in" : ["Fail", "Violation Issued"]}, 
                        "$and" : [{"address.city" : "NEW YORK"}, {"address.street" : "FREDERICK DOUGLASS BLVD"}]}).sort("business_name").distinct("business_name")

    for x in result:
      print(x)  

    print("\n------------------------------------------------------------------\n")

    #   ___                              _      ___                            
    #  / __|  ___   __   ___   _ _    __| |    / _ \   _  _   ___   _ _   _  _ 
    #  \__ \ / -_) / _| / _ \ | ' \  / _` |   | (_) | | || | / -_) | '_| | || |
    #  |___/ \___| \__| \___/ |_||_| \__,_|    \__\_\  \_,_| \___| |_|    \_, |
    #                                                                     |__/ 
    # Every inspections with address.zip 10030 and 11373, that have Mobile Food Vendor - 881 as sector, grouped  by id and business_name
    # and sorted by business_name
    query = [
      {"$match" : {"address.zip" : {"$in" : [10030, 11373]}}},
      {"$match" : {"sector" : "Mobile Food Vendor - 881"}},
      {"$group" : {'_id': '$id', 'inspected_business': {'$addToSet': '$business_name'}}},
      {"$unwind" : "$inspected_business"},
      {'$sort': {'inspected_business': 1}}
    ]

    print("Second Query:\n")

    result = mycol.aggregate(query)

    for x in result:
      print(x)
    
    print("\n------------------------------------------------------------------\n")

    #   _____ _    _        _    ___                    
    #  |_   _| |_ (_)_ _ __| |  / _ \ _  _ ___ _ _ _  _ 
    #    | | | ' \| | '_/ _` | | (_) | || / -_| '_| || |
    #    |_| |_||_|_|_| \__,_|  \__\_\\_,_\___|_|  \_, |
    #                                              |__/     
    # terza query: tutte le ispezioni con city BROOKLYN e tutte qulle di NEW YORK
    # prendo il settore Cicarette Retail Dealer - 127
    # ordine in base address.number
    query = [
      {"$match" : {"address.zip" : 11234, "sector" : "Cigarette Retail Dealer - 127", "date" : {"$gte":"2016-1-1", "$lte":"2016-4-30"}}},
      # {"$match" : {"sector" : "Cigarette Retail Dealer - 127"}},
      # {"$match" : {"date" : {"$gte":"2016-1-1", "$lte":"2016-4-30"}}},
      {"$group" : { "_id" : "$id", "street_inspected" : {"$addToSet" : '$address.street'}}},
      {"$unwind" : "$street_inspected"},                
      {'$group': {'_id': '$street_inspected', 'count': { '$sum': 1}}},
      {'$sort': {'count': 1}}
    ]

    result = mycol.aggregate(query)

    print("Third Query:\n")

    for x in result:
      print(x)
    
    print("\n------------------------------------------------------------------\n")

    #   ___             _   _       ___                    
    #  | _____ _  _ _ _| |_| |_    / _ \ _  _ ___ _ _ _  _ 
    #  | _/ _ | || | '_|  _| ' \  | (_) | || / -_| '_| || |
    #  |_|\___/\_,_|_|  \__|_||_|  \__\_\\_,_\___|_|  \_, |
    #                                                 |__/     
    # quarta query: fai una creazione di un set in cui abbiamo
    # settore - city - street - result
    # poi faccio un unwind 
    # poi conto tutti i settori di tipo X per la citta' di New York con result Warning di una stessa via
    
    #   ___ _  __ _   _       ___                    
    #  | __(_)/ _| |_| |_    / _ \ _  _ ___ _ _ _  _ 
    #  | _|| |  _|  _| ' \  | (_) | || / -_| '_| || |
    #  |_| |_|_|  \__|_||_|  \__\_\\_,_\___|_|  \_, |
    #                                           |__/ 
    # quinta query: conto le citta' che sono presenti nel json per un determinato tipo di settore
    


def main():
  # connect
  print("Trying to connect to: " + str(server))
  mycol = connect()
  print("OK\n")

  # # insert
  # print("Inserting new object inside: " + str(collection))
  # insert(mycol)
  # print("OK\n")
  
  # # update
  # print("Updating the collection: " + str(collection))
  # update(mycol)
  # print("OK\n")
  
  # query
  print("Queries on collection: " + str(collection))
  query(mycol)

  

if __name__ == "__main__":
  main()
