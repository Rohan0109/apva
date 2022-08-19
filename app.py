import flask
from flask import request, render_template
import requests
from webhooks import validatePartnerDetails,validateNameAndVersion,displayDatabases,displayGateways,displayDataTypes,storeDatabaseNameType,displayExistingTableCollection,deploy

app = flask.Flask(__name__)

url = 'https://services.apiplatform.io/v1/data/commons/commons/data-types'
r = requests.get(url = url,headers={"accept": "*/*","pkey": "3fe18f9884ea832e3fede1e661740c4a"},)

res = r.json()

allDatabases = []
for i in range(len(res)):
    if res[i]['database_type'] not in allDatabases:
        allDatabases.append(res[i]['database_type'])
mongodb = []
sqlserver = []
mysql = []
dynamodb = []
postgresql = []
cosmosdb = []
aurora_postgresql = []
aurora_mysql = []
snowflake = []
csv = [] 
for i in range(len(res)):
    if res[i]['database_type'] == 'mongodb':
        mongodb.append(res[i]['data_types'][0]['type'])
    if res[i]['database_type'] == 'sqlserver':
        sqlserver.append(res[i]['data_types'][0]['type'])
    if res[i]['database_type'] == 'mysql':
        mysql.append(res[i]['data_types'][0]['type'])
    if res[i]['database_type'] == 'dynamodb':
        dynamodb.append(res[i]['data_types'][0]['type'])
    if res[i]['database_type'] == 'postgresql':
        postgresql.append(res[i]['data_types'][0]['type'])
    if res[i]['database_type'] == 'cosmosdb':
        cosmosdb.append(res[i]['data_types'][0]['type'])
    if res[i]['database_type'] == 'aurora-postgresql':
        aurora_postgresql.append(res[i]['data_types'][0]['type'])
    if res[i]['database_type'] == 'aurora-mysql':
        aurora_mysql.append(res[i]['data_types'][0]['type'])
    if res[i]['database_type'] == 'snowflake':
        snowflake.append(res[i]['data_types'][0]['type'])
    if res[i]['database_type'] == 'csv':
        csv.append(res[i]['data_types'][0]['type'])

@app.route('/')
@app.route('/home')
def home():
    return render_template("index.html")


@app.route('/webhook', methods=['POST'])
def webhook():
    body = request.get_json(silent=True)

    # fetching tag
    fulfillment = body['fulfillmentInfo']['tag']
    parameters = {}
    print("\n\nDisplaying Body ======> {}".format(fulfillment))
    print(body)
    session_name = body.get('sessionInfo').get('session')

    #fetching parameters
    for key, value in body['sessionInfo']['parameters'].items():
        parameters.update({key:value})

    #function calls
    if fulfillment == "test1":
        res1 = validatePartnerDetails(fulfillment,  parameters, session_name)
        return res1
    if fulfillment == "test2":
        res2 = validateNameAndVersion(fulfillment,parameters,session_name)
        return res2   
    if fulfillment == 'test3':
        res3 = displayDatabases(fulfillment,parameters)
        return res3
    if fulfillment == 'test4':
        res4 = displayGateways(fulfillment,parameters)
        return res4
    if fulfillment == 'test5':
        res5 = displayDataTypes(fulfillment,parameters)
        return res5
    if fulfillment == 'test6':
        res6 = displayExistingTableCollection(fulfillment,parameters)
        return res6
    if fulfillment == 'test8':
        res8 = storeDatabaseNameType(fulfillment,parameters,session_name)
        return res8
    res7 = deploy(fulfillment)
    return res7

if __name__ == "__main__":
    app.secret_key = 'ItIsASecret2'
    app.debug = True
    app.run()


# dev-jeeva2714 - 3fde6ff25d215cfe3feafdca79bad17f
# shanthan -  3fec0c58ff418f6a3fbd23bccc692338
#Shanthan@1477

#https://services.apiplatform.io/v1/data/commons/commons/data-types - for all datatypes corresponding databases

#https://services.apiplatform.io/v1/admin/shanthan/table-attributes?table=Persons&database=default&databaseType=sqlserver

#For having schema of existing table
#'https://services.apiplatform.io/v1/admin/shanthan/table-attributes?table=Persons&database=default&databaseType=sqlserver'
# r2 = requests.get(url=url2, headers={"accept": "*/*", "pkey": '3fec0c58ff418f6a3fbd23bccc692338'}, )
