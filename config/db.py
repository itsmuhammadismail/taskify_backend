from pymongo import MongoClient

MONGO_URI = "mongodb+srv://jaweria:admin12345@cluster0.r9ropnv.mongodb.net/?retryWrites=true&w=majority"

conn = MongoClient(MONGO_URI)

db = conn.taskify
