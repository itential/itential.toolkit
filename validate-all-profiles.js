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
    console.log(`Usage:\nnode validate-all-profiles.js <iap-host-port> <iap-username>`);
    console.log('Example:\nnode validate-all-profiles.js http://myiap.host.com:3000 admin@pronghorn');
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
 * This will use the IAP admin essentials API to get a list of profiles. The
 * API requires iterating over the pagination. The API call is restricting the
 * profile fields that are returned to just the name and ID with the "include"
 * parameter. They are also sorted by name and ordered.
 * @param {string} token - The IAP session token
 * @param {integer} limit - The number of results to return in a page
 * @param {integer} skip - The number in the result set to start from
 * @returns {object} - The API response object
 */
async function getProfiles(token, limit, skip) {
  let config = {
    method: 'GET',
    url: `${TARGETHOSTURL}/profiles?limit=${limit}&skip=${skip}&order=1&sort=id&include=id&token=${token}`,
    headers: {
      'Content-Type': 'application/json',
      'Cookie': token
    }
  };
  const profiles = await axios(config).then(function (response) {
    return response;
  }).catch(function (e) {
    console.error(`Error searching for profiles list: ${util.inspect(e)}`);
    return false;
  });
  return profiles;
}

/**
 * This will use the IAP automation-studio API to get a single profile by
 * name.
 * @param {string} token - The IAP session token
 * @param {string} profileName - The profile name
 * @returns {object} - The object representing the workflow
 */
async function getProfile(token, profileName) {
  let config = {
    method: 'GET',
    url: `${TARGETHOSTURL}/profiles/${encodeURIComponent(profileName)}?token=${token}`,
    headers: {
      'Content-Type': 'application/json',
      'Cookie': token
    }
  };
  const profile = await axios(config).then(function (response) {
    return response;
  }).catch(function (e) {
    console.error(`Error searching for profile '${profileName}': ${util.inspect(e)}`);
    return false;
  });
  //console.log(util.inspect(profile.data.profile,{depth:null}))
  return profile.data.profile;
}

/**
 * This will use the IAP admin essentials API to get a list of all profile
 * names. First, it will make a call for a single profile to discover the
 * total number of profiles. Using this total it will "crawl" to fetch all
 * the profile names making multiple calls if needed.
 * @param {string} token - The IAP session token
 * @returns {array} - The array containing all the profile names
 */
async function getAllProfileNames(token) {
  const limit = 100;
  let skip = 0;
  let profileNames = [];
  // Make a simple call to determine the total
  const totals = await getProfiles(token, 1, 0);
  const total = totals.data.total;
  const numCalls = Math.ceil(total / limit);
  // Iterate over all profiles
  for (let i = 0; i < numCalls; i++) {
    let profiles = await getProfiles(token, limit, skip);
    batchOfNames = profiles.data.results.map((profile) => {
      return profile.profile.id;
    });
    profileNames = profileNames.concat(batchOfNames);
    skip = skip + limit;
  }
  return profileNames;
}

/**
 * This function will get the JSON schema for an profile instance.
 * @param {string} token - The IAP session token
 * @returns
 */
async function getProfileSchema(token) {
  let config = {
    method: 'GET',
    url: `${TARGETHOSTURL}/schema/profiles?token=${token}`,
    headers: {
      'Content-Type': 'application/json',
      'Cookie': token
    }
  };
  const profileSchema = await axios(config).then(function (response) {
    return response;
  }).catch(function (e) {
    console.error(`Error searching for profile schema: ${util.inspect(e)}`);
    return false;
  });
  return profileSchema.data;
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

  // Get all the profile names
  console.log("Getting all profile names...");
  const profileNames = await getAllProfileNames(token);
  console.log(`Found ${profileNames.length} profiles`);

  // Iterate over all profile names, get the profile, validate the profile,
  // and capture validation output as the report
  console.log("Validating all profiles...");
  bar1.start(profileNames.length, 0);
  for (let i = 0; i < profileNames.length; i++) {
    let profileName = profileNames[i];
    let profile = await getProfile(token, profileName);

    // Get profile schema
    const profileSchema = await getProfileSchema(token);
    if (profile) {
      const ajv = new Ajv({strict:false});
      const valid = ajv.validate(profileSchema, profile);
      if (!valid) {
        finalReport[profileName] = ajv.errors;
        totalErrors += ajv.errors.length;
      } else {
        finalReport[profileName] = [];
      }
    }
    bar1.increment();

  }
  bar1.stop();

  // Write the final report to a file
  console.log("Writing profile report file...");
  try {
    fs.writeFileSync('profile-upgrade-report.json', JSON.stringify(finalReport, null, 2));
  } catch (e) {
    console.error(`Problem writing report file: ${util.inspect(e)}`);
  }

  console.log(`Total errors: ${totalErrors}`);
  console.log(`Total warnings: ${totalWarnings}`);
}

main();
