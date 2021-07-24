const functions = require("firebase-functions");
const express = require("express");
const fs = require('fs');

const app = express();
app.get('/events', (request, response) => {
    let raw_data = fs.readFileSync('../events.json');
    response.send(JSON.parse(raw_data));
});
app.get('/events/:section', (request, response) => {
    const { section } = request.params;
    let raw_data = fs.readFileSync('../events.json');
    let parsed_object = JSON.parse(raw_data);
    response.send(parsed_object[section])
});
app.get('/events/:section/:uid', (request, response) => {
    const { section, uid } = request.params;
    let raw_data = fs.readFileSync('../events.json');
    let parsed_object = JSON.parse(raw_data);
    response.send(parsed_object[section][uid])
});

exports.app = functions.https.onRequest(app);