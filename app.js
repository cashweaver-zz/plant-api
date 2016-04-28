/**
 * Express app
 */
'use strict';

let express = require('express');
let app = express();

// Router
let router = express.Router();

// For debugging
router.use(function (req, res, next) {
  console.log('Received request.');
  next();
});


router.get('/', function (req, res) {
  res.send('Hello, world!');
});

app.use('/api', router);

let port = process.env.PORT || 3000;
let server = app.listen(port, function () {
  let host = server.address().address;

  console.log('Listening at http://%s:%s', host, port);
})
