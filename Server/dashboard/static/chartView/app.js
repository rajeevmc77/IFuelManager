var myLineChart;
var jsonCarProfile;
var fuelTimer ;
var fuelSlider;
var fuelSliderMinValue,fuelSliderMaxValue;
var prevAjaxRequest;

var labels = CarFuelHistory.map(function(value, index){
    return value[0];
});

var data = CarFuelHistory.map(function(value, index){
    return value[1];
});

var globalChartData = {
    "data": data,
    "labels" :labels
};

var carFuelHistoryTime = [ ];

function initLineGraph(){

    Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
    Chart.defaults.global.defaultFontColor = '#858796';

    var ctx = document.getElementById("myAreaChart");
    myLineChart = new Chart(ctx, {
      type: 'line',
      data: {
        labels: labels,
        datasets: [{
          label: "Fuel Level",
          lineTension: 0.3,
          backgroundColor: "rgba(78, 115, 223, 0.05)",
          borderColor: "rgba(78, 115, 223, 1)",
          pointRadius: 3,
          pointBackgroundColor: "rgba(78, 115, 223, 1)",
          pointBorderColor: "rgba(78, 115, 223, 1)",
          pointHoverRadius: 3,
          pointHoverBackgroundColor: "rgba(78, 115, 223, 1)",
          pointHoverBorderColor: "rgba(78, 115, 223, 1)",
          pointHitRadius: 10,
          pointBorderWidth: 2,
          data: data,
        }],
      },
      options: {
        maintainAspectRatio: true,
        responsive: true,
        title: {
            display: true,
            text: 'Fuel History'
        },
        layout: {
          padding: {
            left: 10,
            right: 25,
            top: 25,
            bottom: 0
          }
        },
        scales: {
          xAxes: [{
            time: {
              unit: 'number'
            },
            gridLines: {
              display: false,
              drawBorder: false
            },
            ticks: {
              maxTicksLimit: 7
            }
          }],
          yAxes: [{
            ticks: {
              maxTicksLimit: 5,
              padding: 10
            },
            gridLines: {
              color: "rgb(234, 236, 244)",
              zeroLineColor: "rgb(234, 236, 244)",
              drawBorder: false,
              borderDash: [2],
              zeroLineBorderDash: [2]
            }
          }],
        },
        legend: {
          display: true
        },
        tooltips: {
          backgroundColor: "rgb(255,255,255)",
          bodyFontColor: "#858796",
          titleMarginBottom: 10,
          titleFontColor: '#6e707e',
          titleFontSize: 14,
          borderColor: '#dddfeb',
          borderWidth: 1,
          xPadding: 15,
          yPadding: 15,
          displayColors: false,
          intersect: false,
          mode: 'index',
          caretPadding: 10
        }
      }
    });

}

function refreshLiveChart(){
    var diff = globalChartData.labels[0] - myLineChart.data.labels[0];
    for (  ; diff>=0; diff--){
        myLineChart.data.labels.shift();
        myLineChart.data.datasets[0].data.shift();
        myLineChart.data.labels.push(globalChartData.labels[globalChartData.labels.length - diff - 1]);
        myLineChart.data.datasets[0].data.push(globalChartData.data[globalChartData.data.length - diff - 1]);
        /*console.log(diff ) ;
        console.log( globalChartData.labels ) ;
        console.log( globalChartData.data ) ;*/
    }
    myLineChart.update();
}

function refreshRangeChart(){

    myLineChart.data.labels = [];
    myLineChart.data.datasets[0].data =[];

    for (  index=0; index < globalChartData.labels.length-1; index++){
        myLineChart.data.labels.push(globalChartData.labels[index]);
        myLineChart.data.datasets[0].data.push(globalChartData.data[index]);
    }
    myLineChart.update();
}

function refreshLabelsData(carData){
        carFuelHistoryTime = carData.map(function(value, index){
            return new  Date(value[2]);
        });
        labels = carData.map(function(value, index){
            return value[0];
        });
        data = carData.map(function(value, index){
            return value[1];
        });
        globalChartData.data = data;
        globalChartData.labels = labels;

}

function getFuelHistory(){
    if(jsonCarProfile && jsonCarProfile.length > 0){
         $.ajax("/dashboard/getFuelHistory/?vin="+jsonCarProfile[0].VIN,
                 {
                     dataType: "json",
                     success: function(data) {
                        data.reverse();
                        refreshLabelsData(data);
                        refreshLiveChart()
                     },
                     error: function(jqXHR, textStatus, errorThrown) {
                        alert("Failed to get Fuel history of VIN " +vin );
                         console.log(textStatus);
                     }
                 }
         );
         fuelTimer = setTimeout(function(){getFuelHistory()}, 1000); // poll in 1000 ms
     }
}

function sliderValChange(value){
    if(fuelTimer){
        clearTimeout(fuelTimer);
    }
    var sliderOverFlow =  fuelSliderMaxValue - ( value + 50 ) ;
    var sliderLowerBound , sliderUpperBound;
    sliderLowerBound = (sliderOverFlow >=  0 ) ? value : value + sliderOverFlow ;
    sliderUpperBound = (sliderOverFlow >=  0 ) ? value + 50 : fuelSliderMaxValue;

   /* if(prevAjaxRequest){
        prevAjaxRequest.abort();
    }*/
    prevAjaxRequest = $.ajax("/dashboard/getHistoryInRange/?vin="+jsonCarProfile[0].VIN +"&fromID="+(sliderLowerBound)+"&toId="+(sliderUpperBound),
       {
           dataType: "json",
           success: function(data) {
                 var fromTime= " ", toTime= " ";
                 refreshLabelsData(data);
                 refreshRangeChart();
                 if(carFuelHistoryTime){
                    len = carFuelHistoryTime.length;
                    if( len > 0){
                        fromTime = carFuelHistoryTime[0].toLocaleString();
                        toTime = carFuelHistoryTime[len - 1].toLocaleString();
                    }
                 }
                 var sliderMessage = "<b> Tick:" + value +"  From: " + fromTime + "  To: " + toTime + "</b>"
                 $( "#currentSliderValue" ).html( sliderMessage );
           },
           error: function(jqXHR, textStatus, errorThrown) {
              alert("Failed to get Fuel history Range of VIN " +vin );
               console.log(textStatus);
           }
       }
    );
}

function initFuelSlider() {

      $.ajax("/dashboard/getHistoryRange/?vin="+jsonCarProfile[0].VIN,
           {
               dataType: "json",
               success: function(data) {

                fuelSliderMinValue = data.MinID;
                fuelSliderMaxValue = data.MaxID;

                fuelSlider=  $( "#slider-range-max" ).slider({
                     range: "max",
                     min: data.MinID,
                     max: data.MaxID,
                     step: 1,
                     value: 1,
                     slide: function( event, ui ) {
                               sliderValChange(ui.value);
                           }
                   });

               },
               error: function(jqXHR, textStatus, errorThrown) {
                  alert("Failed to get Fuel history Range of VIN " +vin );
                   console.log(textStatus);
               }
           }
      );

}

function getLiveFuelLevel(){
    if(fuelTimer){
        clearTimeout(fuelTimer);
    }
    getFuelHistory();
}

$(document).ready(function() {
    initLineGraph();
    initFuelSlider();
});



