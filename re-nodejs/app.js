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
var CONCURRENCY = 100;
var request = require('request').forever({
  minSockets: CONCURRENCY,
  maxSockets: CONCURRENCY,
});
var xml2js = require('xml2js');
var utils = require('./lib/utils');
var async = require('async');

// setup middleware
var app = express();
app.use(express.errorHandler());
app.use(express.urlencoded()); // to support URL-encoded bodies
app.use(express.bodyParser());

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
app.get('/entities', function(req, res){
    res.render('index');
});

// Handle the form POST containing the text to identify with Watson and reply with the language
app.post('/entities', function(req, res){
  //console.log(req);
  console.log("====================================================REQUEST BODY====================================================");

  console.log(req.body);
  var paragraphs=req.body;
  

  async.mapLimit(paragraphs, CONCURRENCY, function(paragraph, callback) {
    request.post({
      url: service_url,
      headers: {
        'X-synctimeout' : '30',
        'Authorization' :  auth,
      },
      form: {
        txt:paragraph,
        sid:"ie-en-news"
      },
    }, function(err, res2, body) {
      if (err)
        return callback(err);

      xml2js.parseString(body, function(err, root) {
        if (err)
          callback(err);
        try {
          var paragraph_result = [];
          root.rep.doc[0].sents[0].sent.map(function(sent) {
            var parse = utils.parseType(sent.parse[0]._);
            console.log('sentence', parse);
            var sentence_result = parse;
            paragraph_result.push(sentence_result);
          });
          callback(null, paragraph_result);
        } catch (err) {
          callback(err || 'error');
        }
      });
    });

  }, function(err, paragraph_results) {
    if (err)
      return res.send(500, 'error ' + err);
    res.send(paragraph_results);
  });
});





// The IP address of the Cloud Foundry DEA (Droplet Execution Agent) that hosts this application:
var host = (process.env.VCAP_APP_HOST || 'localhost');
// The port on the DEA for communication with the application:
var port = (process.env.VCAP_APP_PORT || 3000);
// Start server
app.listen(port, host);
