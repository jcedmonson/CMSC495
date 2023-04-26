
const https = require('https')
const express = require("express");
const fs = require('fs');

const port = 4000

const options = {
  key: fs.readFileSync('certs/key.pem'),
  cert: fs.readFileSync('certs/cert.pem'),
}

const app = express();

app.use(express.static("dist"));

const server = https.createServer(options, app).listen(port, () => {
  console.log(`Express server is listening on port ${port}`);
})