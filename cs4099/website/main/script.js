var express = require('express');
var cors = require('cors');
var app = express();
app. use(cors);

// var file = '../../database/db.csv';
var file = 'cs/home/jelm/Documents/CS4099-master/cs4099/database/db.csv';
var csv;
// must define this as a file
var json;
let divs = [];

draw = function() {
    // read through db of names

    if (window.File && window.FileReader && window.FileList && window.Blob) {
        console.log(true);
    }

    csv = readFile();
    json = csvToJson();
    console.log("json made");
    
    console.log(json);
    // now convert the JSON object into divs
    // go through 
}

function readFile() {
    // XMLHttpRequest has ben deprecated
    var result = null;
    var xml = new XMLHttpRequest();
    xml.open("GET", file, false);
    xml.send();
    if (xml.status == 200) {
        result = xml.responseText;
    }
    return result;
}

function read(evt) {
    var f = evt.target.files[0];
    
    console.log("read");
    if (f) {
        console.log("2");
        var reader = new FileReader();
        reader.onload = function(e){
            console.log("3");
            var contents = e.target.result;
            console.log("Got the file.\n" +
                        "Name: " + f.name +
                        "\nSize: " + f.size + " bytes" +
                        "\nstarts with: " + contents.substr(0, contents.indexOf("\n")));
        }
        reader.readAsText(f);
        csv = reader.result;
        csvToJson();
    }
}

document.getElementById('fileinput').addEventListener('change', read, false);

function csvToJson() {
    var lines = csv.split("\n");
    var result = [];
    var headers = lines[0].split(",");
    console.log(headers);

    for (var i = 1; i < lines.length; i++) {
        var obj = {};
        var line = lines[i].split(",");
        console.log(line);

        for (var j = 0; j < headers.length; j++) {
            obj[headers[j]] = line[j];
        }

        result.push(obj);
    }

    return JSON.stringify(result);
}

// works reading in file when choose file input is selected
// doesn't work when using readFile from onload

// https://stackoverflow.com/questions/53258297/access-to-xmlhttprequest-has-been-blocked-by-cors-policy