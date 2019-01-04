// 
// Copyright (C) 2017 FSFE e.V. <contact@fsfe.org>
// 
// SPDX-License-Identifier: GPL-3.0+

var http = require("http");

http.createServer(function (request, response) {
   response.writeHead(200, {'Content-Type': 'text/plain'});
   
   response.end('Hello World\n');
}).listen(8082);

