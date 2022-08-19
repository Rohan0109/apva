from re import fullmatch
import flask
from flask import request, render_template,Response
import requests


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

def storeDatabaseNameType(fulfillment,parameters,session_name):
    print("\n\nCALLING =======> ", fulfillment)
    temp = parameters['api-database']
    res = temp.split('(')
    print("first split",res)
    name = res[0]
    name = name.strip()
    r1 = res[1]
    r2 = r1.split(' ')
    type = r2[0]
    jsonResponse = {
                "fulfillment_response":
                    {
                        "messages": [
                            {
                                "text": {
                                    "text": []
                                }
                            }
                        ]
                    },
                    "session_info": {
                        "session": session_name,
                        "parameters": {
                            "database-name": name,
                            "database-type": type
                        }
                    }
            }
    return jsonResponse


def deploy(fulfillment):
    url = 'https://services.apiplatform.io/v1/admin/shanthan/table-attributes?table=Persons&database=default&databaseType=sqlserver'
    r = requests.get(url=url, headers={"accept": "*/*", "pkey": '3fec0c58ff418f6a3fbd23bccc692338'}, )
    print("\n\nSchema definition")
    print(r.json())
    jsonResponse = {
                    "fulfillment_response":
                        {
                            "messages": [
                                {
                                    "text": {
                                        "text": []
                                    }
                                }
                            ]
                        }
            }
    return jsonResponse


def displayExistingTableCollection(fulfillment,parameters):
    print("\n\nCALLING =======> ", fulfillment)
    env = str(parameters['environment'])
    pkey = str(parameters['partner-key'])
    database_type = str(parameters['database-type'])
    database_name = str(parameters['database-name'])

    url = 'https://services.apiplatform.io/v1/admin/'+str(env)+'/database/'+str(database_type)+'/'+str(database_name)+'/get-database-tables'
    r = requests.get(url = url,headers={"accept": "*/*", "pkey": str(pkey)},)
    lists = r.json()
    jsonResponse =  {"fulfillment_response":{
            "messages":[
                {
                    "payload":{
                    "richContent": [
                                [
                                    {
                                        "options": [],
                                        "type": "chips"
                                    }
                                ]
                            ]
                        }
                    }
                ]
            }
        }
    temp = jsonResponse['fulfillment_response']['messages'][0]['payload']['richContent'][0][0]['options']

    for i in range(len(lists)):
        data = {}
        data['text'] = lists[i]
        temp.append(data)

    return jsonResponse


def displayDataTypes(fulfillment,parameters):
    if fulfillment == 'test5':
        print("\n\nCALLING =======> ", fulfillment)
        temp = parameters['api-database']
        res = temp.split('(')
        name = res[0]
        r1 = res[1]
        r2 = r1.split(' ')
        r = r2[0]
        print(name,r)
        data_type = []
        if r == 'mongodb':
            data_type = mongodb
        if r == 'sqlserver':
            data_type = sqlserver
        if r == 'mysql':
            data_type = mysql
        if r == 'dynamodb':
            data_type = dynamodb
        if r == 'postgresql':
            data_type = postgresql
        if r == 'cosmosdb':
            data_type = cosmosdb
        if r == 'aurora-postgresql':
            data_type = aurora_postgresql
        if r == 'aurora-mysql':
            data_type = aurora_mysql
        if r == 'snowflake':
            data_type = snowflake
        if r == 'csv':
            data_type = csv
        jsonResponse =  {"fulfillment_response":{
            "messages":[
                {
                    "payload":{
                    "richContent": [
                                [
                                    {
                                        "options": [],
                                        "type": "chips"
                                    }
                                ]
                            ]
                        }
                    }
                ]
            }
        }
        temp1 = jsonResponse['fulfillment_response']['messages'][0]['payload']['richContent'][0][0]['options']
        # print(databases)
        for i in range(len(data_type)):
            data = {}
            data['text'] = data_type[i]
            temp1.append(data)

    return jsonResponse
        

def displayGateways(fulfillment,parameters):
    print("\n\nCALLING =======> ", fulfillment)
    env = str(parameters['environment'])
    url = 'https://services.apiplatform.io/core/core/v1/partner-settings'
    r = requests.get(url=url, headers={"pkey": "3feee3f13ffecbc23fdcb845d0b9359a","API-PLATFORM-PARTNER" : str(env),"API-PLATFORM-ACCOUNT":str(env)},)

    res = r.json()
    gateways = []
    for i in range(len(res['apigateway'])):
        p = []
        p.append(res['apigateway'][i]['provider'])
        p.append(res['apigateway'][i]['name'])
        gateways.append(str(p[1]) + ' [' + str(p[0])+']')

    jsonResponse = {"fulfillment_response": {
        "messages": [
                    {
                        "payload": {
                            "richContent": [
                                [
                                    {
                                        "options": [],
                                        "type": "chips"
                                    }
                                ]
                            ]
                        }
                    }
                ]
            }   
        }
    temp = jsonResponse['fulfillment_response']['messages'][0]['payload']['richContent'][0][0]['options']
    # print(databases)
    for i in range(len(gateways)):
        data = {}
        data['text'] = gateways[i]
        temp.append(data)

    return jsonResponse


def displayDatabases(fulfillment,parameters):
    print("\n\nCALLING =======> ", fulfillment)
    env = str(parameters['environment'])
    pkey = str(parameters['partner-key'])

    url = 'https://services.apiplatform.io/v1/admin/'+str(env)+'/databases?encrypt=true'
    #partner-management-resource -> getPartnerDatabase
    r = requests.get(url = url,headers={"accept": "*/*", "pkey": str(pkey)},)
    res = r.json()
    databases = []        
    for i in range(len(res)):
        p = []
        p.append(res[i]['database_name'])
        p.append(res[i]['database_type'])
        databases.append(str(p[0]) + ' (' + str(p[1])+' - us-east-1)')

        jsonResponse =  {"fulfillment_response":{
            "messages":[
                {
                    "payload":{
                    "richContent": [
                                [
                                    {
                                        "options": [],
                                        "type": "chips"
                                    }
                                ]
                            ]
                        }
                    }
                ]
            }
        }
        temp = jsonResponse['fulfillment_response']['messages'][0]['payload']['richContent'][0][0]['options']
        # print(databases)
        for i in range(len(databases)):
            data = {}
            data['text'] = databases[i]
            temp.append(data)

    return jsonResponse

    
def validateNameAndVersion(fulfillment,parameters,session_name):
    print("\n\nCALLING =======> ", fulfillment)
    api_name = str(parameters['api-name'])
    version = str(parameters['api-version'])
    env = str(parameters['environment'])
    pkey = str(parameters['partner-key'])

    url1 = 'https://services.apiplatform.io/v1/admin/' + \
        str(env)+'/'+str(env)+'/'+str(api_name)+'/'+str(version)
    url2 = 'https://services.apiplatform.io/v1/api/' + \
        str(env)+'/'+str(env)+'/'+str(api_name) + \
            '/'+str(version)+'/executor'

    #api-management-resource --> getPartnerAccountEntityById
    r1 = requests.get(url=url1, headers={
                        "accept": "*/*", "pkey": str(pkey)},)

    #try and except block to handle exception
    if r1.status_code == 200:
        num = 1
    elif r1.status_code == 404:
        #api-executor-management-resource --> getApiExecutorByPartnerAccountByNameAndVersion
        r2 = requests.get(url=url2, headers={
                            "accept": "*/*", "pkey": str(pkey)},)
        print("r2 status code", r2.status_code)
        if r2.status_code == 200:
            try:
                print(r2.json())
                num = 1
            except:
                num = 2
        else:
            num = 3
    else:
        num = 3

    #return condition
    if num == 1:
        jsonResponse = {
                "fulfillment_response":
                    {
                        "messages": [
                            {
                                "text": {
                                    "text": ["Entered Name and versiona already exists. Please enter different name and version"]
                                }
                            }
                        ]
                    },
                    "session_info": {
                        "session": "projects/aiva-359005/locations/us-east1/agents/caca77f3-466f-490a-8efd-8c6b0ff17047/sessions/e9126f-422-bad-14e-25b4b34dd",
                        "parameters": {
                            "validate-name": "exist"
                        }
                    }
            }
    elif num == 2:
        jsonResponse = {
        "fulfillment_response":
            {
                "messages": [
                    {
                        "text": {
                                    "text": ["The entered $session.params.api-name and $session.params.api-version is available"]
                                }
                        }
                ]
            },
            "session_info": {
                        "session": session_name,
                        "parameters": {
                            "validate-name": "proceed"
                        }
                    }
        }
    elif num == 3:
        jsonResponse = {
        "fulfillment_response":
            {
                "messages": [
                    {
                        "text": {
                                    "text": ["Internal Error. Please try again later"]
                                }
                        }
                ]
            },
    }

    return jsonResponse
                

def validatePartnerDetails(fulfillment,  parameters, session_name):
    print("\n\nCALLING =======> ", fulfillment)
    email_id = str(parameters['email-id'])
    env = str(parameters['environment'])
    pkey = str(parameters['partner-key'])

    url = 'https://services.apiplatform.io/v1/admin/'+str(env)+'/authorize'

    r = requests.get(url=url, headers={"accept": "*/*", "pkey": str(pkey)}, )

    if r.status_code == 200:
        msg = "Valid user"
    else:
        msg = "Invalid user"

    if msg == "Valid user":
        jsonResponse = {
            "fulfillment_response":
                {
                    "messages": [
                        {
                            "text": {
                                        "text": ["Partner details validated"]
                                    }
                            }
                    ]
                },
                "session_info": {
                        "session": session_name,
                        # "projects/aiva-359005/locations/us-east1/agents/caca77f3-466f-490a-8efd-8c6b0ff17047/sessions/20c323-ac2-3f7-fa3-08ec76e3b",
                        "parameters": {
                            "validate-user": "valid user"
                        }
                }
        }
    elif msg == "Invalid user":
        jsonResponse = {
                "fulfillment_response":
                    {
                        "messages": [
                            {
                                "text": {
                                    "text": ["Invalid user"]
                                }
                            }
                        ]
                    },
                    "session_info": {
                        "session": session_name,
                        # "projects/aiva-359005/locations/us-east1/agents/caca77f3-466f-490a-8efd-8c6b0ff17047/sessions/20c323-ac2-3f7-fa3-08ec76e3b",
                        "parameters": {
                            "validate-user": "invalid user"
                        }
                    }
        }
        print("End")
    return jsonResponse


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
