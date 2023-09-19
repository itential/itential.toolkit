const axios = require('axios');
const util = require('util');
const fs = require('fs');
const cliProgress = require('cli-progress');
const prompt = require('password-prompt');
const Ajv = require("ajv");

let TARGETHOSTURL;
let TARGETUSERNAME;
let TARGETPASSWORD;

// create a new progress bar instance and use shades_classic theme
const bar1 = new cliProgress.SingleBar({}, cliProgress.Presets.shades_classic);

/**
 * Reads command line args and sets variables from them. Exits the
 * process if any are missing.
 */
async function getCmdArgs() {
  if (process.argv.length < 4) {
    console.error(`Missing script parameters!`);
    console.log(`Usage:\nnode validate-all-adapters.js <iap-host-port> <iap-username>`);
    console.log('Example:\nnode validate-all-adapters.js http://myiap.host.com:3000 admin@pronghorn');
    process.exit(1);
  }
  TARGETHOSTURL = process.argv[2];
  TARGETUSERNAME = process.argv[3];
  TARGETPASSWORD = await prompt('password: ', {'method':'hide'});
}

/**
 * Gets a session token from an IAP server.
 * @returns {string} - The IAP session token
 */
async function login() {
  let config = {
    method: 'POST',
    url: `${TARGETHOSTURL}/login`,
    headers: {
      'Content-Type': 'application/json'
    },
    data: {
      'user': {
        'username': TARGETUSERNAME,
        'password': TARGETPASSWORD
      }
    }
  };
  const token = await axios(config).then(function (response) {
    return response.data;
  }).catch(function (e) {
    console.error(`Can not get IAP session token: ${e}`);
    process.exit(1);
  });
  return token;
}

/**
 * This will use the IAP admin essentials API to get a list of adapters. The
 * API requires iterating over the pagination. The API call is restricting the
 * adapter fields that are returned to just the name and ID with the "include"
 * parameter. They are also sorted by name and ordered.
 * @param {string} token - The IAP session token
 * @param {integer} limit - The number of results to return in a page
 * @param {integer} skip - The number in the result set to start from
 * @returns {object} - The API response object
 */
async function getAdapters(token, limit, skip) {
  let config = {
    method: 'GET',
    url: `${TARGETHOSTURL}/adapters?limit=${limit}&skip=${skip}&order=1&sort=name&include=name&token=${token}`,
    headers: {
      'Content-Type': 'application/json',
      'Cookie': token
    }
  };
  const adapters = await axios(config).then(function (response) {
    return response;
  }).catch(function (e) {
    console.error(`Error searching for adapters list: ${util.inspect(e)}`);
    return false;
  });
  return adapters;
}

/**
 * This will use the IAP automation-studio API to get a single adapter by
 * name.
 * @param {string} token - The IAP session token
 * @param {string} adapterName - The adapter name
 * @returns {object} - The object representing the workflow
 */
async function getAdapter(token, adapterName) {
  let config = {
    method: 'GET',
    url: `${TARGETHOSTURL}/adapters/${encodeURIComponent(adapterName)}?token=${token}`,
    headers: {
      'Content-Type': 'application/json',
      'Cookie': token
    }
  };
  const adapter = await axios(config).then(function (response) {
    return response;
  }).catch(function (e) {
    console.error(`Error searching for adapter '${adapterName}': ${util.inspect(e)}`);
    return false;
  });
  return adapter.data.data;
}

/**
 * This will use the IAP admin essentials API to get a list of all adapter
 * names. First, it will make a call for a single adapter to discover the
 * total number of adapters. Using this total it will "crawl" to fetch all
 * the adapter names making multiple calls if needed.
 * @param {string} token - The IAP session token
 * @returns {array} - The array containing all the adapter names
 */
async function getAllAdapterNames(token) {
  const limit = 100;
  let skip = 0;
  let adapterNames = [];
  // Make a simple call to determine the total
  const totals = await getAdapters(token, 1, 0);
  const total = totals.data.total;
  const numCalls = Math.ceil(total / limit);
  // Iterate over all adapters
  for (let i = 0; i < numCalls; i++) {
    let adapters = await getAdapters(token, limit, skip);
    batchOfNames = adapters.data.results.map((adapter) => {
      return adapter.data.name;
    });
    adapterNames = adapterNames.concat(batchOfNames);
    skip = skip + limit;
  }
  return adapterNames;
}

/**
 * This function will get the JSON schema for an adapter instance.
 * @param {string} token - The IAP session token
 * @param {string} adapterName - The name of the adapter to get the schema for
 * @returns
 */
async function getAdapterSchema(token, adapterName) {
  let config = {
    method: 'GET',
    url: `${TARGETHOSTURL}/schema/adapters/${adapterName}?token=${token}`,
    headers: {
      'Content-Type': 'application/json',
      'Cookie': token
    }
  };
  const adapterSchema = await axios(config).then(function (response) {
    return response;
  }).catch(function (e) {
    console.error(`Error searching for adapter '${adapterName}': ${util.inspect(e)}`);
    return false;
  });
  return adapterSchema.data;
}

/**
 * Encapsulates all the logic.
 */
async function main() {
  let finalReport = {};
  let totalErrors = 0;
  let totalWarnings = 0;

  // Read all the cmd line args
  await getCmdArgs();

  // Get an IAP login token
  console.log('Getting session token...');
  const token = await login();

  // Get all the adapter names
  console.log("Getting all adapter names...");
  const adapterNames = await getAllAdapterNames(token);
  console.log(`Found ${adapterNames.length} adapters`);

  // Iterate over all adapter names, get the adapter, validate the adapter,
  // and capture validation output as the report
  console.log("Validating all adapters...");
  bar1.start(adapterNames.length, 0);
  for (let i = 0; i < adapterNames.length; i++) {
    let adapterName = adapterNames[i];
    let adapter = await getAdapter(token, adapterName);

    // Get adapter schema
    const adapterSchema = await getAdapterSchema(token, adapterName);
    if (adapter) {
      const ajv = new Ajv({strict:false});
      const valid = ajv.validate(adapterSchema, adapter);
      if (!valid) {
        finalReport[adapterName] = ajv.errors;
        totalErrors += ajv.errors.length;
      } else {
        finalReport[adapterName] = [];
      }
    }
    bar1.increment();

  }
  bar1.stop();

  // Write the final report to a file
  console.log("Writing adapter report file...");
  try {
    fs.writeFileSync('adapter-upgrade-report.json', JSON.stringify(finalReport, null, 2));
  } catch (e) {
    console.error(`Problem writing report file: ${util.inspect(e)}`);
  }

  console.log(`Total errors: ${totalErrors}`);
  console.log(`Total warnings: ${totalWarnings}`);
}

main();
