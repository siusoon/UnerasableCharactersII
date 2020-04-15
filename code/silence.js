class Nodel { //create a class: template/blueprint of objects with properties and behaviors
	constructor(s, x, y, sp, startT, delT) {
		this.s = s;
		this.x = x;
		this.y = y;
		this.speed = sp;
		this.startT = new Date(startT.slice(0,4), startT.slice(5,7), startT.slice(8,10), startT.slice(11,13), startT.slice(14,16), startT.slice(17,19)).getTime();
		this.delT = new Date(delT.slice(0,4), delT.slice(5,7), delT.slice(8,10), delT.slice(11,13), delT.slice(14,16), delT.slice(17,19)).getTime();
		this.status = true;
		this.i = 0;
		this.calTime = Math.abs(this.delT - this.startT);  //return ms
	}

	display() {	//check the duration for silence, then display accordingly
		if (this.status){
			fill(255);
			//textFont(myFont);
			textSize(25);
			if (time < this.calTime/100) {
				text(this.s.charAt(this.i), this.x, this.y);
				this.i++;
				if (this.i == this.s.length) {
					this.i = 0;
				}
			}else{
				this.status = false;
			}
		}
	}

}
