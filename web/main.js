// Load the Visualization API and the corechart package.
google.charts.load('current', {'packages':['corechart']});

// Set a callback to run when the Google Visualization API is loaded.
google.charts.setOnLoadCallback(initPlot);

// Create the data table.
var data;
var plot;
var options;

//dummy test variables
var x = 0;
var y = 0;
var windowSize = 3600;
var iter = 0;

function initPlot() {
	data = new google.visualization.DataTable();
	data.addColumn('number', 'adc1');
	data.addColumn('number', 'adc2');
	plot = new google.visualization.LineChart(document.getElementById('chart_div'));
	options = {title: 'Data test',
						 vAxis: {minValue: 0, maxValue: 1}};	

	drawPlot();
	update();
}

// Callback that creates and populates a data table,
// instantiates the pie chart, passes in the data and
// draws it.
function drawPlot() {

	plot.draw(data, options);
}

function update() {
	y = Math.sin(x);
	x = x + 0.1;
	var row = data.addRow([x,y]);
	drawPlot();
	console.log("loop");
	if ( iter < windowSize ) {
		iter = iter + 1;		
	} else {
		data.removeRow(row - windowSize);
  }
	
	var t = setTimeout(update, 16); 
}

