'use strict';

let apiConfig = {
  base: '/api',
  name: 'Plant API'
}
let express = require('express');
let API = require('json-api');
let APIError = API.types.Error;
let mongoose = require('mongoose');
let models = {
  Plant: require('./models/plant')
  Station: require('./models/station')
};

mongoose.connect('mongodb://localhost/plantapi');

// Register models with json-api
let adapter = new API.dbAdapters.Mongoose(models);
let registry = new API.ResourceTypeRegistry(
  { plants: require('./resource-descriptions/plants') },
  { stations: require('./resource-descriptions/stations') },
  { dbAdapter: adapter }
);

// Initialize automatic documentation
let Controller = new API.controllers.API(registry);
let Docs = new API.controllers.Documentation(registry, {name: apiConfig.name})

// Initialize the express app and front controller
let app = express();
let Front = new API.httpStrategies.Express(Controller, Docs);
let apiReqHandler = Front.apiRequest.bind(Front);

// Routes
let router = express.Router();

// This is run for every API call. It's included for debugging.
router.use(function (req, res, next) {
  console.log('Request received. (' + req.url + ')');
  next();
});

router.get('/', Front.docsRequest.bind(Front));
router.route('/:type(plants|stations)')
  .get(apiReqHandler);
router.route('/:type(plants|stations)/:id')
  .get(apiReqHandler);

router.use(function (req, res, next) {
  Front.sendError(new APIError(404, undefined, 'Not Found'), req, res);
});

app.use(apiConfig.base, router);

// Start the server
let server = app.listen(process.env.PORT || 3000, function () {
  let host = server.address().address;
  let port = server.address().port;

  console.log('Listening at http://%s:%s'+apiConfig.base, host, port);
});
