function draw() {
    // read through db of names
    console.log("hello");
    var rows = $.csv.toObjects("../../database/words.csv");

    // generate div for each name
    for (var i = 0; i <  rows.length; i++) {
        // read db and add to rows arr

        // write divs to page
        var div = document.createElement("div");
        div.setAttribute("id", "element" + i);

        document.getElementById('element' + i).innerHTML += rows[i];
        document.getElementById("list").appendChild(div);
    }

    // can I call js of other folder from here?
}