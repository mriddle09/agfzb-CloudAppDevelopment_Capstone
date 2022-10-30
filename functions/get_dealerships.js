

function main(params) {
    secret = {
        "COUCH_URL": "https://53620507-b58c-47eb-9890-6508a1c535b0-bluemix.cloudantnosqldb.appdomain.cloud",
        "IAM_API_KEY": "EXvmEXFIBCf3XkKUnh_bBuqJF52XlC5cj-n16I3PmN_Y",
        "COUCH_USERNAME": "EXvmEXFIBCf3XkKUnh_bBuqJF52XlC5cj-n16I3PmN_Y"
    };

    return new Promise(function (resolve, reject) {
        const cloudant = CloudantV1.newInstance({
            url: params.COUCH_URL,
            plugins: { iamauth: { iamApiKey: params.IAM_API_KEY } }
        });

        const dealship_db = cloudant.use('dealerships')

        if (params.state) {
            dealershi_db.find({"selector": {"state": {"$eq": params.state}}}, 
                function (err, result) {
                    if (err) {
                        reject(err)
                    }
                    let code = 200
                    if (result.docs.lenth == 0) {
                        code = 404
                    }
                    resolve({
                        statusCode: code,
                        headers: {'Content-Type':'Application/json'},
                        body: result
                    });

                }
            )
        }

        else {
            dealship_db.find(
                function (err, result) {
                    if (err) {
                        reject(err)
                    }
                    let code = 200
                    if (result.docs.lenth == 0) {
                        code = 404
                    }
                    resolve({
                        statusCode: code,
                        headers: {'Content-Type':'Application/json'},
                        body: result
                    });

                }
            )
        }
    }) 
        
}