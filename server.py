from pymongo import MongoClient

client = MongoClient('localhost', 27017)  # substitua localhost e a porta pela sua configuração
db = client['mydatabase']
collection = db['mycollection']

results = []
for item in collection.find():
    results.append({
        'produto': item['produto'],
        'preco': item['preco']
    })
