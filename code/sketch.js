/*
logic:
- load the JSON file with all the stored censored tweets
- randomly extract the message from the json file
- loop and display each of the message in a grid format
- each tweet will display in a character-by-character format
- specific message will stop according to the originnal visible period
- loop everything again (reload) until all the text objects are disappeared on the screen for a certain period of time

updates:
- add console log for future bug fix on characters encoding
*/


let datafile;
let datafiles = [];
let nodel = [];
let myFont;
let time;
let grid_space = 30;
let cols, rows;  //for drawing the grid purpose

function preload() {
	//myFont = loadFont('assets/HanyiSentyTang.ttf');
  datafile = loadJSON("data.json");
}
function setup(){
	createCanvas(windowWidth,windowHeight);
	frameRate(5);
	time = millis();
	datafiles = datafile.data;
	//calculate grid
	cols = (width-10)/grid_space;
	rows = (height-10)/grid_space;
	for (let i=0; i < cols; i++) {//no of cols
		for (let j=0; j < rows; j++){ //no of rows
			let x = i * grid_space; //actual x coordinate
			let y = j * grid_space; //actual y coordinate
			let s1 = int(random(datafiles.length));
			let s = datafiles[s1].content;
			nodel.push(new Nodel(s, x+5, y-5, 12, datafiles[s1].createdAt, datafiles[s1].censoredAt));  //s, x, y, sp, startT, delT
      console.log(i + "," + j + ": " + datafiles[s1].id);
		}
	}

}

function draw() {
	background(0);
	time = millis();
	for (let i =0; i < nodel.length; i++) {
		nodel[i].display();
	}
	checkCensored();
	checkReload();
}

function checkCensored(){
	for (let i =0; i < nodel.length; i++) {
		if (!nodel[i].status) {
			nodel.splice(i,1);
		}
	}
}

function checkReload(){
	if(nodel.length==0) {
		setTimeout(() => { location.reload(); }, 2000);
	}
}
