'use strict';

let r = require('rethinkdb');
let connection = null;
r.connect(
  {
    host: 'localhost',
    port: 28015
  },
  function (err, conn) {
    if (err) throw err;
    connection = conn;
  }
);
