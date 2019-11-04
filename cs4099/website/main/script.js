function draw() {
    // read through db of names
    console.log("hello");
    // var rows = csv.toObjects("../../database/words.csv");
    let file = new File([""], "/cs/home/jelm/Documents/CS4099-master/cs4099/database/words.json");

    let reader = new FileReader(file);
    reader.readAsArrayBuffer();
    // reader.onload = readSuccess;
    
    console.log(file);
    var array = JSON.parse(file);

    // generate div for each name
    console.log("before for");
    for (var i = 0; i < array.medicines.length; i++) {
        // read db and add to rows arr
        console.log("in for");
        var medicine = array.medicines[i];

        // write divs to page
        var div = document.createElement("div");
        div.setAttribute("id", "element" + i);

        document.getElementById('element' + i).innerHTML += medicine.name;
        console.log(medicine.name);
        document.getElementById("list").appendChild(div);
    }

    // can I call js of other folder from here?
}