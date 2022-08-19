import requests

url = 'https://services.apiplatform.io/v1/admin/shanthan/database/mongodb/mongodbshanthan/get-database-tables'
r = requests.get(url = url,headers={"accept": "*/*", "pkey": '3fec0c58ff418f6a3fbd23bccc692338'},)
print(type(r.json()))