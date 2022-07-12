const { CloudantV1 } = require('@ibm-cloud/cloudant');
const { IamAuthenticator } = require('ibm-cloud-sdk-core');


// getting all dealerships & dealerships by state 
function main(params) {

    const authenticator = new IamAuthenticator({ apikey: params.IAM_API_KEY })
    const cloudant = CloudantV1.newInstance({
      authenticator: authenticator
    });
    cloudant.setServiceUrl(params.COUCH_URL);

    let st = params.st;
    
    let dbListPromise;

    if(!st) {
        dbListPromise = getDealerships(cloudant);
    }
    else{
        dbListPromise = getDealershipsByState(cloudant, st);
    }

    return dbListPromise;
}

// original-version:
function getDbs(cloudant) {
     return new Promise((resolve, reject) => {
        cloudant.getAllDbs()
            .then(body => {
                resolve({ dbs: body.result });
            })
            .catch(err => {
                console.log(err);
                reject({ err: err });
            });
     });
}
 
 
// version-01 [https://github.com/IBM/cloudant-node-sdk/blob/master/examples/postAllDocs/example_request.js]:
function getDealerships(cloudant) {
    let databaseName = "dealerships";
     
    return new Promise((resolve, reject) => {
        cloudant.postAllDocs({
            db: databaseName,
            includeDocs: true,
            limit: 10
        })
        .then(response => {
            resolve({ docs: response.result.rows});
        })
        .catch(err => {
            console.log(err);
            reject({ err: err });
        });
     });
 }
 
// version-01 [https://github.com/IBM/cloudant-node-sdk/blob/master/examples/postAllDocs/example_request.js]:
function getDealershipsByState(cloudant, st) {
    let databaseName = "dealerships";
     
    return new Promise((resolve, reject) => {
        cloudant.postFind({
            db: databaseName,
            selector: {
                st: st
            }
        })
        .then(response => {
            resolve({ docs: response.result.docs});
        })
        .catch(err => {
            console.log(err);
            reject({ err: err });
        });
     });
}