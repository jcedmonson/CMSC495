
// const https = require('https')
const express = require("express");
// const fs = require('fs');
const history = require('connect-history-api-fallback');

const port = 4000

// const options = {
//   key: fs.readFileSync('certs/key.pem'),
//   cert: fs.readFileSync('certs/cert.pem'),
// }

const app = express();

const staticFileMiddleware = express.static('dist');
app.use(staticFileMiddleware);
app.use(history({
  disableDotRule: true,
  verbose: true
}));

app.use(staticFileMiddleware);

// const server = https.createServer(options, app).listen(port, () => {
//   console.log(`Express server is listening on port ${port}`);
// })

app.listen(port, () => {
  console.log(`APP IS READY ON PORT ${port}`)
});