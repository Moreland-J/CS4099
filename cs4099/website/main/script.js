var csv = "../../database/db.csv";
// must define this as a file
var json;
let divs = [];

draw = function() {
    // read through db of names
    console.log("hello");

    if(window.FileReader) {
        console.log(true);
    }

    json = csvToJson();
    console.log("json made");
    
    console.log(json);
    // now convert the JSON object into divs
    // go through 
}


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