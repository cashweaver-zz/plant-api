'use strict';

let r = require('rethinkdb');
let conn = null;
r.connect(
  {
    host: 'localhost',
    port: 28015
  },
  function (err, connection) {
    if (err) throw err;
    conn = connection;
  }
);

// Plants
r.dbCreate('plantsapi').run(conn);
r.use('plantsapi');
r.createTable('plants');

r.close();
