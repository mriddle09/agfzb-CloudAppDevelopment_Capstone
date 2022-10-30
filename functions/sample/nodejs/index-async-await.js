/**
 * Get all dealerships
 */

const { CloudantV1 } = require('@ibm-cloud/cloudant');
const { IamAuthenticator } = require('ibm-cloud-sdk-core');

async function main(params) {
      const cloudant = CloudantV1.newInstance({
          url: params.COUCH_URL,
          plugins: { iamauth: { iamApiKey: params.IAM_API_KEY } }
      });
      
      try {
        let dbList = await cloudant.db.list();
        return { "dbs": dbList };
      } catch (error) {
          return { error: error.description };
      }
}

