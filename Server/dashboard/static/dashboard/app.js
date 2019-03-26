function loadAjaxData(){
    var table = $('#obdData').DataTable();
    table.ajax.reload();

    setTimeout(function(){loadAjaxData();}, 1000);
}


$(document).ready(function() {
    $('#obdData').DataTable( {
        "ajax": {
            "url": "/api/obdData/",
            "dataSrc": ""
        },
        "columns": [
           { "data": "VIN" },
           { "data": "RPM" },
           { "data": "Speed" },
           { "data": "FuelTankLevel" }
        ]
    });

    loadAjaxData();
});