'use strict';
let mongoose = require('mongoose');

let schema = new mongoose.Schema({
  name: String
});

module.exports = mongoose.model('Plant', schema);
