var express = require("express");
 
 //use the application off of express.
 var app = express();
 
 //define the route for "/"
 app.get("/", function (request, response){
     //show this file when the "/" is requested
     response.sendFile(__dirname+"/views/index.html");
 });
 
 //start the server
 app.listen(8080);
 
 console.log("Something awesome to happen at http://localhost:8080");