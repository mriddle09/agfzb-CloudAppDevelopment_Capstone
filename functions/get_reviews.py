from cloudant.client import cloudant
from cloudant.error import cloudantException

def main(dict):

    secret = {
        "COUCH_URL": "https://53620507-b58c-47eb-9890-6508a1c535b0-bluemix.cloudantnosqldb.appdomain.cloud",
        "IAM_API_KEY": "EXvmEXFIBCf3XkKUnh_bBuqJF52XlC5cj-n16I3PmN_Y",
        "COUCH_USERNAME": "EXvmEXFIBCf3XkKUnh_bBuqJF52XlC5cj-n16I3PmN_Y",
    }

    client = cloudant.iam(
        account_name = secret['COUCH_USERNAME'],
        api_key = secret['IAM_API_KEY'],
        url = secret['COUCH_USERNAME'],
        connect = True
    )

    database = client['reviews']
    print(database)

    try:
        selector = {'dealership' : {'$eq': int(dict["dealerId"])}}
        result_filter = database.get_query_result(
            selector, raw_result=true
        )

        result = {
            "headers": {'Content-type': 'application/json'}
            "body": {'data': result_filter} 
        }

        return result

    except:

        return {
            'statusCode' : 404,
            'message' : 'something went wrong'

        }
