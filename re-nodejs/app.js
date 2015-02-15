'use strict';

// app.js
// This file contains the server side JavaScript code for your application.
// This sample application uses express as web application framework (http://expressjs.com/),
// and jade as template engine (http://jade-lang.com/).

var express = require('express');
var https = require('https');
var url = require('url');
var querystring = require('querystring');
var xmlescape = require('xml-escape');
var request = require('request').forever();
var xml2js = require('xml2js');

// setup middleware
var app = express();
app.use(express.errorHandler());
app.use(express.urlencoded()); // to support URL-encoded bodies
app.use(app.router);

app.use(express.static(__dirname + '/public')); //setup static public directory
app.set('view engine', 'jade');
app.set('views', __dirname + '/views'); //optional since express defaults to CWD/views

// There are many useful environment variables available in process.env.
// VCAP_APPLICATION contains useful information about a deployed application.
var appInfo = JSON.parse(process.env.VCAP_APPLICATION || "{}");
// TODO: Get application information and use it in your app.

// defaults for dev outside bluemix
var service_url = 'https://gateway.watsonplatform.net/relationship-extraction-beta/api';
var service_username = '11a96023-6294-4cc0-81ed-0fc64d65b88d';
var service_password = 'p@55w0rd';

// VCAP_SERVICES contains all the credentials of services bound to
// this application. For details of its content, please refer to
// the document or sample of each service.
if (process.env.VCAP_SERVICES) {
  console.log('Parsing VCAP_SERVICES');
  var services = JSON.parse(process.env.VCAP_SERVICES);
  //service name, check the VCAP_SERVICES in bluemix to get the name of the services you have
  var service_name = 'relationship_extraction';
  
  if (services[service_name]) {
    var svc = services[service_name][0].credentials;
    service_url = svc.url;
    service_username = svc.username;
    service_password = svc.password;
  } else {
    console.log('The service '+service_name+' is not in the VCAP_SERVICES, did you forget to bind it?');
  }

} else {
  console.log('No VCAP_SERVICES found in ENV, using defaults for local development');
}

console.log('service_url = ' + service_url);
console.log('service_username = ' + service_username);
console.log('service_password = ' + new Array(service_password.length).join("X"));

var auth = 'Basic ' + new Buffer(service_username + ':' + service_password).toString('base64');

// render index page
app.get('/', function(req, res){
    res.render('index');
});

// Handle the form POST containing the text to identify with Watson and reply with the language
app.post('/', function(req, res){

  request.post({
    url: service_url,
    headers: {
      'X-synctimeout' : '30',
      'Authorization' :  auth,
    },
    form: req.body,
  }, function(err, res2, body) {
    xml2js.parseString(body, function(err, root) {
      if (err || root.rep.$.sts !== 'OK')
        return res.send(500, 'error');
      root.rep.doc[0].sents[0].sent.map(function(sent) {
        var parse = sent.parse[0]._;
        console.log('parse', parse);
      });
      res.render('index',{'xml':xmlescape(body), 'text':req.body.txt});
    });
  });
});


//=========================================================================MY CODE=====================================================================================
// render index page
app.get('/test', function(req, res){
    res.render('index');
});

app.post('/test', function(req, res){

  var parts = url.parse(service_url);

  // create the request options from our form to POST to Watson
  var options = { 
    host: parts.hostname,
    port: parts.port,
    path: parts.pathname,
    method: 'POST',
    headers: {
      'Content-Type'  :'application/x-www-form-urlencoded',
      'X-synctimeout' : '30',
      'Authorization' :  auth }
  };

  // Create a request to POST to Watson
  var watson_req = https.request(options, function(result) {
    result.setEncoding('utf-8');
    var resp_string = '';

    result.on("data", function(chunk) {
      resp_string += chunk;
    });

    result.on('end', function() {
      console.log("=========================================================================================================================");
      console.log(resp_string);
      console.log("=========================================================================================================================");
      console.log(xmlescape(resp_string));
      console.log("=========================================================================================================================");
      //return res.send(resp_string);
      return res.send(xmlescape(resp_string));
      //return res.render('index',{'xml':xmlescape(resp_string), 'text':req.body.txt})
    })

  });

  watson_req.on('error', function(e) {
    return res.render('index', {'error':e.message})
  });

  // Whire the form data to the service
  watson_req.write(querystring.stringify(req.body));
  watson_req.end();
});







//=========================================================================MY CODE=====================================================================================



// The IP address of the Cloud Foundry DEA (Droplet Execution Agent) that hosts this application:
var host = (process.env.VCAP_APP_HOST || 'localhost');
// The port on the DEA for communication with the application:
var port = (process.env.VCAP_APP_PORT || 3000);
// Start server
app.listen(port, host);
