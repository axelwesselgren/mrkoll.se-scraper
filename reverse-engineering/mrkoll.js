function showMore() {
    document.getElementById('moreBlock').style.maxHeight = "unset";
    document.getElementById('moreBtn01').style.maxHeight = "";
    document.getElementById('moreBtn01').style.display = "none";
}

function openSuper() {
    document.getElementById('spBlock').style.height = "unset";
    document.getElementById('superBtn').style.display = "none";
    document.getElementById('superPuff').style.display = "none";
    document.getElementById('superHeader').style.display = "none";
}
var n = new Date().getTime();

function cars(p, k) {
    var p;
    var k;
    var car_a = new XMLHttpRequest();
    car_a.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 500) {
            document.getElementById('carBlock').innerHTML = 'Vi kunde inte kontrollera fordonsinnehav just nu.';
        } else if (this.readyState == 4 && this.status == 220) {
            document.getElementById('carBlock').innerHTML = this.responseText;
        }
    };
    car_a.open("GET", "/ajax/cars/?p=" + p + "&k=" + k + "&t=" + n, true);
    car_a.send();
}

function weather(p, k, lt, lng) {
    var p;
    var k;
    var lt;
    var lng;
    var weather_a = new XMLHttpRequest();
    weather_a.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 500) {
            document.getElementById('weatherBlock').innerHTML = '';
        } else if (this.readyState == 4 && this.status == 200) {
            document.getElementById('weatherBlock').innerHTML = this.responseText;
        }
    };
    weather_a.open("GET", "/ajax/weather/?p=" + p + "&k=" + k + "&lt=" + lt + "&lg=" + lng, true);
    weather_a.send();
}

function bn(p, k) {
    var p;
    var k;
    var bna = new XMLHttpRequest();
    bna.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 500) {
            document.getElementById('ajaxBoData').innerHTML = 'Vi kunde inte kontrollera bostadssituation just nu.';
        } else if (this.readyState == 4 && this.status == 200) {
            document.getElementById('ajaxBoData').innerHTML = this.responseText;
        } else {
            document.getElementById('ajaxBoData').innerHTML = '';
        }
    };
    bna.open("GET", "/ajax/b/?p=" + p + "&k=" + k + "&t=" + n, true);
    bna.send();
}

function goreg(p, k, l) {
    var p;
    var k;
    var l;
    var greg = new XMLHttpRequest();
    greg.open("GET", "/ajax/goreg/?p=" + p + "&k=" + k + "&l=" + l, true);
    greg.send();
}

function dayShow(m, b) {
    var m;
    var b;
    document.getElementById('tableDayShow').innerHTML = m;
    document.getElementById('tableDayShow').innerHTML = m + ' / <strong>' + b + '</strong>';
}

function showPersnr(p, k) {
    var xhp = new XMLHttpRequest();
    var p;
    var k;
    xhp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 500) {
            document.getElementById('pnrid').innerHTML = 'XXXX';
            document.getElementById('puffmeg').innerHTML = 'Vi kunde tyvÃ¤rr inte lÃ¤sa in personnumret just nu.';
        } else if (this.readyState == 4 && this.status == 200) {
            document.getElementById('pnrid').innerHTML = this.responseText;
            document.getElementById('pnrid').style.color = "#3a3a3a";
            document.getElementById('modal_dialog').style.display = "none";
        } else if (this.readyState == 4) {
            document.getElementById('puffmeg').innerHTML = 'LÃ¤ser in personnummer...'
        }
    }
    xhp.open("GET", "/ajax/lastDigits/?p=" + p + "&k=" + k, true);
    xhp.send();
}