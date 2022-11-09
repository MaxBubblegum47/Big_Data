import pymongo
import datetime

# MongoDB Server and Database Data
server = "mongodb://localhost:27017/"
database = "City"
collection = "City_Inspections_DB"
index_name = "date_index"

def connect():
  myclient = pymongo.MongoClient(server)
  mydb = myclient[database]
  mycol = mydb[collection]
  return mycol


def insert(mycol):
  
  inspection = {"id" : "00000-0000-ENFO", "certificate_number" : "17041999", "business_name" : "Videogames Center",
  "date" : "1999-4-17", "result" : "Fail", "sector" : "Videogames", "address" : {"city" : "Georgia",
  "zip" : "41030", "street" : "Rue de Baptiste", "number" : "19"}}  
  
  check = mycol.find({"id":str(inspection.get("id"))}).distinct("id")
  
  if not check:
    mycol.insert_one(inspection)
  else:
    print("There is already this object")
    
  

def update(mycol):
  query = {"id":"00000-0000-ENFO"}
  new_values = {"$set":{"Inspector Name":"Lorenzo Stigliano"}}

  check = mycol.find(query).distinct("id")
  if not check:
    print("There is document with the right id to be updated")
  else:
    mycol.update_one(query, new_values, upsert = True)


def index(mycol):
  mycol.create_index([('date', pymongo.ASCENDING )], name = index_name)

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
      {"$group" : {"_id": "$id", "inspected_business": {"$addToSet": "$business_name"}}},
      {"$unwind" : "$inspected_business"},
      {"$sort": {"inspected_business": 1}}
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
    # query on all object with 11234 zip code, that have Cigarette Retail Dealer as sector between the 2016-1-4 and the 2016-4-30
    # then create a group with the object id and the street of all the company inspected and make a count about how many company per street
    # have been inspected. Finally sort the result by the count yet done
    
    query = [
      {"$match" : {"address.zip" : 11234, "sector" : "Cigarette Retail Dealer - 127", "date" : {"$gte":"2016-1-1", "$lte":"2016-4-30"}}},
      {"$group" : { "_id" : "$id", "street_inspected" : {"$addToSet" : "$address.street"}}},
      {"$unwind" : "$street_inspected"},                
      {"$group": {"_id": "$street_inspected", "count": { "$sum": 1}}},
      {"$sort": {"count": 1}}
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
    # Inspect in 3 differents part of New York, between the 2015-1-1 and the 2016-12-31, which is the most sector that have more result like:
    # - Fail
    # - Violation Issued

    query = [
      {"$match" : {"address.zip" : {"$in" : [10475, 11234, 11427]}, "result" : {"$in" : ["Fail", "Violation Issued"]}, "date" : {"$gte":"2015-1-1", "$lte":"2016-12-31"}}},
      {"$group" : { "_id" : "$certificate_number", "sector_inspected" : {"$addToSet" : '$sector'}}},
      {"$unwind" : "$sector_inspected"},                
      {"$group": {"_id": "$sector_inspected", "count": { "$sum": 1}}},
      {'$sort': {'count': -1}},
      {"$group": { "_id": "$sector_inspected", "maxval": { "$first": '$$ROOT'}}},
      {"$replaceWith": "$maxval"} 
    ]

    result = mycol.aggregate(query)

    print("Fourth Query:\n")

    for x in result:
      print(x)
    
    print("\n------------------------------------------------------------------\n")
        


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
  
  # indexing
  print("Indexing the collection: " + str(collection) + " with an index on " + index_name)
  index(mycol)
  print("OK\n")

  # query
  print("Queries on collection: " + str(collection))
  query(mycol)

  

if __name__ == "__main__":
  main()
