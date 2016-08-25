'use strict';

// ------------------------------------
// Database and App connections

let express = require('express');
let app = express();
let mongoose = require('mongoose');

mongoose.connect('mongodb://localhost/plantapi');

// ------------------------------------
// Models

let Plant = require('./models/plant');

// ------------------------------------
// Routes

let router = express.Router();

// This is run for every API call. It's included for debugging.
router.use(function (req, res, next) {
  console.log('Request received.');
  next();
});

router.route('/plants')
  .get(function (req, res) {
    Plant.find(function (err, results) {
      if (err) {
        res.send(err);
      }
      res.json(results);
    });
  });
