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
    new_review = database.create_document(dict["review"])

    if new_review.exists():
        result = {
            "headers": {"Content-Type": "application/json"},
            "body": {"message": "Review posted successfully"}
        }
        
        return result

    else:
        error = {
            "statusCode": 500,
            "message": "Could not post review due to server error"
        }

        return error