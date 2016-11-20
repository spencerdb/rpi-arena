// Load the Visualization API and the corechart package.
google.charts.load('current', {'packages':['corechart']});

// Set a callback to run when the Google Visualization API is loaded.
google.charts.setOnLoadCallback(initPlot);

// Create the data table.
var data;
var plot;
var options;
var date = new Date();
var t = date.getTime();
var startLoop = date.getTime();

//dummy test variables
var x = 0;
var y = 0;
var windowSize = 100;
var iter = 0;
var drawIter = 0;

function initPlot() {
	data = new google.visualization.DataTable();
	data.addColumn('number', 'adc1');
	data.addColumn('number', 'adc2');
	plot = new google.visualization.LineChart(document.getElementById('chart_div'));
	options = {title: 'Data test',
						 vAxis: {minValue: -1, maxValue: 1}};	

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
	date = new Date();
	t = date.getTime();
	if (t > startLoop + 32) {
		startLoop = t;
		drawPlot();
	}
	var x = t;
	var y = Math.sin(t * 0.006);
	var row = data.addRow([x,y]);
	
	
	if (data.getNumberOfRows() > windowSize) {
		data.removeRows(0,data.getNumberOfRows() - windowSize)	
	}
	
	var t = setTimeout(update, 10); 
	document.getElementById('chart1').innerHTML = windowSize;
}

function expandOncall(){
	windowSize = Math.round(windowSize * 1.3);
	
}

function contractOncall(){
	windowSize = Math.round(windowSize * 0.7);
}


