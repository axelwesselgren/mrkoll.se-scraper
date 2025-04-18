var modal = document.getElementById("modal_dialog");
var btn = document.getElementById("pnrid");
var span = document.getElementById("close_pnr");
btn.onclick = function() {
    modal.style.display = "block";
}
span.onclick = function() {
    modal.style.display = "none";
}
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}

function showHideFlex(s, id) {
    var s, id;
    if (s == 1) {
        document.getElementById(id).style.display = "flex";
    } else if (s == 0) {
        document.getElementById(id).style.display = "none";
    }
}

function showHideBlock(s, id) {
    var s, id;
    if (s == 1) {
        document.getElementById(id).style.display = "block";
    } else if (s == 0) {
        document.getElementById(id).style.display = "none";
    }
}

function openCodebox() {
    document.getElementById("valueInp").style.display = "flex";
    document.getElementById("valueLink").style.display = "none";
}

function processValueCode(pnq, customerTempId, orderId) {
    var pnq, productCode, customerTempId, key, nowUrl, orderId
    var valueCode = document.getElementById("valueCode").value;
    key = "2sdfds7871ds87f8sSDs2SD2xf8sd72fx9s8x57sdf18ds7f1TDJjkSD7485Ssdf";
    nowUrl = window.location.href;
    var d = new Date();
    var rnz = d.getTime();
    var urlStr = "https://api.mrkoll.se/frontend/v1/check-code/?valueCode=" + valueCode + "&pnq=" + pnq + "&customerTempId=" + customerTempId + "&orderId=" + orderId + "&key=" + key + "&rnz=" + rnz
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var jsonResp = JSON.parse(xhttp.response);
            responseCode = jsonResp.responseCode;
            if (responseCode == 2000) {
                showHideFlex(1, "load_puff");
                showHideBlock(0, "bkontroll_dummy");
                showHideBlock(0, "adyPayBlock");
                location = "#bControlHeader";
                location.reload(true);
            }
            if (responseCode !== 2000) {
                document.getElementById("valueCode").className = "textRed";
            }
        }
    }
    xhttp.open("GET", urlStr, true);
    xhttp.send();
}

function sendEmail(orderId) {
    var orderId;
    var email = document.getElementById("orderEmail").value;
    key = "2sdfds7871ds87f8sSDs2SD2xf8sd72fx9s8x57sdf18ds7f1TDJjkSD7485Ssdf";
    var d = new Date();
    var rnz = d.getTime();
    var urlStr = "https://api.mrkoll.se/frontend/v1/send-receipt/?orderId=" + orderId + "&email=" + email + "&key=" + key + "&rnz=" + rnz
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var jsonResp = JSON.parse(xhttp.response);
            responseCode = jsonResp.responseCode;
            if (responseCode == 2000) {
                showHideBlock(0, "sendEmailWrap");
            }
            if (responseCode !== 2000) {
                document.getElementById("orderEmail").className = "textRed";
            }
        }
    }
    xhttp.open("GET", urlStr, true);
    xhttp.send();
}