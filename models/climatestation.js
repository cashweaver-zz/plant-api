'use strict';
let mongoose = require('mongoose');

let schema = new mongoose.Schema({
  dlyTMaxNormal: {
    data: [Number],
    completeness: String,
  },
  dlyTMaxStddev: {
    data: [Number],
    completeness: String,
  },
  dlyTMinNormal: {
    data: [Number],
    completeness: String,
  },
  dlyTMinStddev: {
    data: [Number],
    completeness: String,
  },
  location: {
    ncdc_meta: {
      gsn_flag: String,
      hcn_flag: String,
      wmoid: String,
      method: String
    },
    //address : {
      //formatted: String
    //},
    lnglat: {
      type: {type: String},
      coordinates: {type: [Number], index: '2dsphere'}
    }
  },
  stationId: String,
  frostDates: {
    90: [Number],
    95: [Number],
    99: [Number]
  },
  dlySoilTAvg: {
    data: [Number],
    completeness: String,
  }
});

schema.index({'location.lnglat': '2dsphere'});

module.exports = mongoose.model('Climatestation', schema);
