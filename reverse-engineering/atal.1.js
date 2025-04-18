var n = new Date().getTime();

function weather(p, k, lt, lng) {
    var p;
    var k;
    var lt;
    var lng;
    var weather_a = new XMLHttpRequest();
    weather_a.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 500) {
            document.getElementById('weatherBlock').innerHTML = '';
        } else if (this.readyState == 4 && this.status == 220) {
            document.getElementById('weatherBlock').innerHTML = this.responseText;
        }
    };
    weather_a.open("GET", "/ajax/weather/?p=" + p + "&k=" + k + "&lt=" + lt + "&lg=" + lng, true);
    weather_a.send();
}

function goreg(p, k, l) {
    var p;
    var k;
    var l;
    var greg = new XMLHttpRequest();
    greg.open("GET", "/ajax/goreg/?p=" + p + "&k=" + k + "&l=" + l, true);
    greg.send();
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