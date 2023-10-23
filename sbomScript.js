const {axios} = require('axios');
const {exec} = require('node:child_process');
 
const createRepoSBOM =  async (repoLink) => {
    const result = await axios.get("www.google.com");
    console.log(result);
    console.log("hello")
}

createRepoSBOM();