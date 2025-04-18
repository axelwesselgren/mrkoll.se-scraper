function clearAllTimers() {
    for (let i = 0; i < 1000; i++) {
        window.clearInterval(i);
        clearInterval(i);
        console.log("clear " + i);
    }
}
var allDone;
var waitInter;

function waitForProduct(payType, pnq, productCode, customerTempId) {
    var pnq, productCode, customerTempId, key;
    waitInter = setInterval(checkProduct, 2000, payType, pnq, productCode, customerTempId);
    console.log("TIMER:");
    console.log(waitInter);
}

function checkProduct(payType, pnq, productCode, customerTempId) {
    var pnq, productCode, customerTempId, key, nowUrl;
    key = "2sdfds7871ds87f8sSDs2SD2xf8sd72fx9s8x57sdf18ds7f1TDJjkSD7485Ssdf";
    var d = new Date();
    var rnz = d.getTime();
    console.log("CHECK");
    nowUrl = window.location.href;
    doneUrl = "https://mrkoll.se/person/swish-redirect/" + pnq + "?" + rnz + "#bControlHeader";
    var urlStr = "https://api.mrkoll.se/frontend/v1/check-order/?pnq=" + pnq + "&productCode=" + productCode + "&customerTempId=" + customerTempId + "&key=" + key + "&rnz=" + rnz
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var jsonResp = JSON.parse(xhttp.response);
            responseCode = jsonResp.responseCode;
            if (responseCode == 2000) {
                if (payType == 'swishDesktop') {
                    var btn = document.getElementById("swishBtn");
                    var btnWrap = document.getElementById("swishBtnWrap");
                    var ico = document.getElementById("swishIco");
                    btn.innerHTML = "Betalning klar! Ett Ã¶gonblick...";
                    btnWrap.className = "swishBtnWrap swishWrapActive swishSuccess";
                    ico.className = "swishIco swishAnim";
                    clearAllTimers();
                    location = "#bControlHeader";
                    console.log("relNOW");
                    window.location.href = doneUrl;
                }
                if (payType == 'swish') {
                    var btn = document.getElementById("swishBtn");
                    var btnWrap = document.getElementById("swishBtnWrap");
                    var ico = document.getElementById("swishIco");
                    btn.innerHTML = "Betalning klar! Laddar...";
                    btnWrap.className = "swishBtnWrap swishWrapActive swishSuccess";
                    ico.className = "swishIco swishAnim";
                    allDone = 'true';
                    clearAllTimers();
                    btnBlockState = 0;
                    location = "#bControlHeader";
                    window.location.href = doneUrl;
                }
                if (payType == 'stripe') {
                    clearAllTimers();
                    location = "#bControlHeader";
                    window.location.href = doneUrl;
                }
            }
            if (responseCode == 2001) {
                if (payType == 'swishDesktop') {
                    var btn = document.getElementById("swishBtn");
                    var btnWrap = document.getElementById("swishBtnWrap");
                    var ico = document.getElementById("swishIco");
                    btn.className = "swishBtn2 swishBtnActive";
                    btn.innerHTML = "VÃ¤ntar pÃ¥ din signering...";
                    ico.className = "swishIco swishAnim";
                    btnWrap.className = "swishBtnWrap swishWrapActive";
                }
                if (payType == 'swish') {
                    var btn = document.getElementById("swishBtn");
                    var btnWrap = document.getElementById("swishBtnWrap");
                    var ico = document.getElementById("swishIco");
                    btn.className = "swishBtn2 swishBtnActive";
                    btn.innerHTML = "VÃ¤ntar pÃ¥ signering...";
                    ico.className = "swishIco swishAnim";
                    btnWrap.className = "swishBtnWrap swishWrapActive";
                }
            }
            if (responseCode == 2002) {
                if (payType == 'swishDesktop') {
                    var btn = document.getElementById("swishBtn");
                    var btnWrap = document.getElementById("swishBtnWrap");
                    var ico = document.getElementById("swishIco");
                    btn.innerHTML = "Betalningen avvisades";
                    btn.className = "swishBtn2 swishBtnActive";
                    btnWrap.className = "swishBtnWrap swishWrapActive swishFail";
                    btnWrap.setAttribute("onClick", "initSwishDesktop('" + pnq + "','" + productCode + "','" + customerTempId + "')");
                    ico.className = "swishIco";
                    clearAllTimers();
                    btnBlockState = 0;
                }
                if (payType == 'swish') {
                    var btn = document.getElementById("swishBtn");
                    var btnWrap = document.getElementById("swishBtnWrap");
                    var ico = document.getElementById("swishIco")
                    btn.innerHTML = "Betalningen avvisades";
                    ico.className = "swishIco";
                    btn.className = "swishBtn2 swishBtnActive";
                    btnWrap.className = "swishBtnWrap swishWrapActive swishFail";
                    btnWrap.setAttribute("onClick", "initSwish('" + pnq + "','" + productCode + "','" + customerTempId + "')")
                    clearAllTimers();
                    btnBlockState = 0;
                }
            }
            if (responseCode == 6000) {
                clearAllTimers();
                document.getElementById("load_puff").innerHTML = "Betalningen misslyckades. Kontrollera felmeddelandet i din Swish-app";
                if (payType == 'swishDesktop') {
                    var btn = document.getElementById("swishBtn_desktop");
                    var btnWrap = document.getElementById("swishBtnWrap");
                    var ico = document.getElementById("swishIco");
                    btn.innerHTML = "Betalning misslyckades";
                    ico.className = "swishIco";
                    btn.className = "swishBtn2 swishBtnActive";
                    btnWrap.className = "swishBtnWrap swishWrapActive swishFail";
                    btnWrap.setAttribute("onClick", "initSwishDesktop('" + pnq + "','" + product + "','" + customerTempId + "')");
                    clearAllTimers();
                    btnBlockState = 0;
                }
                if (payType == 'swish') {
                    var btn = document.getElementById("swishBtn");
                    var btnWrap = document.getElementById("swishBtnWrap");
                    var ico = document.getElementById("swishIco")
                    btn.innerHTML = "Betalning misslyckades";
                    btn.className = "swishBtn2 swishBtnActive";
                    btnWrap.className = "swishBtnWrap swishWrapActive swishFail";
                    ico.className = "swishIco";
                    btnWrap.setAttribute("onClick", "initSwishDesktop('" + pnq + "','" + product + "','" + customerTempId + "')");
                    clearAllTimers();
                    btnBlockState = 0;
                }
            }
        }
    }
    xhttp.open("GET", urlStr, true);
    xhttp.send();
}

function checkPhone() {
    var inputPhone = document.getElementById("swishPhone").value;
    var btn = document.getElementById("swishBtn");
    var btnWrap = document.getElementById("swishBtnWrap");
    console.log(Number.isInteger(inputPhone));
    if (inputPhone.length == 10) {
        document.getElementById("swishBtn").className = "swishBtn2 swishBtnActive";
        btnWrap.className = "swishBtnWrap swishWrapActive";
        btn.className = "swishBtn2 swishBtnActive";
        btn.innerHTML = "Starta betalning via Swish";
    } else {
        document.getElementById("swishBtn").className = "swishBtn2";
        btnWrap.className = "swishBtnWrap";
        btn.className = "swishBtn2";
    }
}

function initSwish(pnq, product, customerTempId) {
    var btn = document.getElementById("swishBtn");
    var btnWrap = document.getElementById("swishBtnWrap");
    var xhttp = new XMLHttpRequest();
    btn.innerHTML = "FÃ¶rsÃ¶ker Ã¶ppna Swish...";
    var responseCode, swishLocationResponse, swishTokenResponse, pnq, product, customerTempId;
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var jsonResp = JSON.parse(xhttp.response);
            responseCode = jsonResp.responseCode;
            swishLocationResponse = jsonResp.swishLocationResponse;
            swishTokenResponse = jsonResp.swishTokenResponse;
            console.log(swishTokenResponse);
            if (responseCode == 2000) {
                location.href = 'swish://paymentrequest?token=' + swishTokenResponse + '&callbackurl=https://mrkoll.se/person/swish-rediredct/' + pnq + '/%3FpayType=swish%26pnq=' + pnq + '%26productCode=' + product + '%26customerTempId=' + customerTempId;
                document.getElementById("swishBtnWrap").removeAttribute("onClick");
                btn.innerHTML = "VÃ¤ntar pÃ¥ signering...";
                waitForProduct('swish', pnq, product, customerTempId);
                btnWrap.className = "swishBtnWrap swishBtnActive";
            }
            if (responseCode !== 2000) {
                btnWrap.setAttribute("onClick", "initSwish('" + pnq + "','" + product + "','" + customerTempId + "')");
                btn.innerHTML = "FÃ¶rsÃ¶k igen";
                btnWrap.className = "swishBtnWrap swishFail swishBtnActive";
                btnBlockState = 0;
            }
        }
        if (this.readyState == 4 && this.status == 201) {
            btn.innerHTML = "NÃ¥got gick fel";
        }
    }
    xhttp.open("POST", "https://api.nusvar.se/payHandle/v1/?orderId=&pnq=" + pnq + "&productCode=" + product + "&payMethod=swish&customerTempId=" + customerTempId + "&cors=mrk&key=2sdfds7871ds87f8sSDs2SD2xf8sd72fx9s8x57sdf18ds7f1TDJjkSD7485Ssdf", true);
    xhttp.send();
}

function initSwishDesktop(pnq, product, customerTempId) {
    var btn = document.getElementById("swishBtn");
    var btnWrap = document.getElementById("swishBtnWrap");
    var ico = document.getElementById("swishIco");
    var phone = document.getElementById("swishPhone").value;
    var xhttp = new XMLHttpRequest();
    btn.innerHTML = "Ett Ã¶gonblick...";
    var responseCode, swishLocationResponse, swishTokenResponse, pnq, product, customerTempId;
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var jsonResp = JSON.parse(xhttp.response);
            responseCode = jsonResp.responseCode;
            swishLocationResponse = jsonResp.swishLocationResponse;
            swishTokenResponse = jsonResp.swishTokenResponse;
            console.log(swishTokenResponse);
            if (responseCode == 2000) {
                document.getElementById("swishBtnWrap").removeAttribute("onClick");
                btn.innerHTML = "SlutfÃ¶r i din Swish-app";
                ico.className = "swishIco swishAnim";
                btnWrap.className = "swishBtnWrap swishBtnActive";
                waitForProduct('swishDesktop', pnq, product, customerTempId);
            }
            if (responseCode !== 2000) {
                document.getElementById("swishBtnWrap").setAttribute("onClick", "initSwishDesktop('" + pnq + "','" + product + "','" + customerTempId + "')");
                btn.innerHTML = "Kontrollera nummer och att du inte har en pÃ¥gÃ¥ende betalning";
                btnWrap.className = "swishBtnWrap swishFail swishBtnActive";
                ico.className = "swishIco";
                btnBlockState = 0;
            }
        }
        if (this.readyState == 4 && this.status == 201) {
            btn.innerHTML = "FÃ¶rsÃ¶k igen";
            btnBlockState = 0;
        }
    }
    xhttp.open("POST", "https://api.nusvar.se/payHandle/v1/?orderId=&pnq=" + pnq + "&productCode=" + product + "&payMethod=swishDesktop&phone=" + phone + "&customerTempId=" + customerTempId + "&cors=mrk&key=2sdfds7871ds87f8sSDs2SD2xf8sd72fx9s8x57sdf18ds7f1TDJjkSD7485Ssdf", true);
    xhttp.send();
}
var btnBlockState = 0;

function initPay(paytype, pnq, product, buyerId, amount, curency) {
    var paytype, pnq, product, buyerId, amount, curency;
    if (paytype == 'swish') {
        if (btnBlockState == 0) {
            initSwish(pnq, product, buyerId)
            btnBlockState = 1;
        }
    }
    if (paytype == 'swishDesktop') {
        if (btnBlockState == 0) {
            initSwishDesktop(pnq, product, buyerId)
            btnBlockState = 1;
        }
    }
    if (paytype == 'stripe') {
        initStripe(pnq, product, buyerId, amount)
    }
}
var intent_key, clientSecret, intent_secret;

function initStripe(pnq, product, customerTempId, amount) {
    var pnq, product, customerTempId, amount;
    var stripe = Stripe('pk_live_3lZ0HYfAF70KaA5WQYZDLFso');
    var xhttp = new XMLHttpRequest();
    var elements = stripe.elements();
    var amount = parseInt(amount + '00');
    var paymentRequest = stripe.paymentRequest({
        country: 'SE',
        currency: 'sek',
        total: {
            label: product,
            amount: amount,
        },
        requestPayerName: true,
        requestPayerEmail: false,
    });
    var prButton = elements.create('paymentRequestButton', {
        paymentRequest: paymentRequest,
    });
    paymentRequest.canMakePayment().then(function(result) {
        if (result) {
            prButton.mount('#payment-request-button');
            console.log('japp');
        } else {
            document.getElementById('payment-request-button').style.display = 'none';
            document.getElementById('walletContainer').style.display = 'none';
            console.log('nix');
        }
    });
    paymentRequest.on('paymentmethod', function(ev) {
        xhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                var jsonResp = JSON.parse(xhttp.response);
                paymentReference = jsonResp.paymentReference
                var intent_array = paymentReference.split("#");
                intent_key = intent_array[0];
                intent_secret = intent_array[1];
            }
        }
        xhttp.open("GET", "https://api.nusvar.se/payHandle/v1/?orderId=&pnq=" + pnq + "&productCode=" + product + "&payMethod=stripe&customerTempId=" + customerTempId + "&cors=mrk&key=2sdfds7871ds87f8sSDs2SD2xf8sd72fx9s8x57sdf18ds7f1TDJjkSD7485Ssdf", false);
        xhttp.send();
        stripe.confirmCardPayment(intent_secret, {
            payment_method: ev.paymentMethod.id
        }, {
            handleActions: false
        }).then(function(confirmResult) {
            if (confirmResult.error) {
                console.log('misslyckades1');
                ev.complete('fail');
            } else {
                console.log('lyckades1');
                waitForProduct('stripe', pnq, product, customerTempId);
                ev.complete('success');
                if (confirmResult.paymentIntent.status === "requires_action") {
                    stripe.confirmCardPayment(intent_secret).then(function(result) {
                        if (result.error) {
                            console.log('misslyckades2');
                        } else {
                            console.log('lyckades2');
                            waitForProduct('stripe', pnq, product, customerTempId);
                        }
                    });
                } else {
                    console.log('lyckades3');
                    waitForProduct('stripe', pnq, product, customerTempId);
                }
            }
        });
    });
    var cardElement = elements.create('card');
    cardElement.mount('#card-element');
    var cardholderName = document.getElementById('cardholder-name');
    var cardButton = document.getElementById('card-button');
    cardButton.addEventListener('click', function(ev) {
        cardButton.disabled = true;
        cardButton.innerHTML = '<div class="lds-ellipsis"><div></div><div></div><div></div><div></div></div>';
        xhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                var jsonResp = JSON.parse(xhttp.response);
                paymentReference = jsonResp.paymentReference
                var intent_array = paymentReference.split("#");
                intent_key = intent_array[0];
                intent_secret = intent_array[1];
                cardButton.setAttribute('data-secret', intent_secret);
            }
            if (this.readyState == 4 && this.status == 201) {
                console.log('api-error');
                document.getElementById("card-error").innerHTML = "KÃ¶pet kunde inte genomfÃ¶ras just nu";
                cardButton.disabled = false;
                cardButton.innerHTML = "Betala";
            }
        }
        xhttp.open("GET", "https://api.nusvar.se/payHandle/v1/?orderId=&pnq=" + pnq + "&productCode=" + product + "&payMethod=stripe&customerTempId=" + customerTempId + "&cors=mrk&key=2sdfds7871ds87f8sSDs2SD2xf8sd72fx9s8x57sdf18ds7f1TDJjkSD7485Ssdf", false);
        xhttp.send();
        clientSecret = cardButton.dataset.secret;
        stripe.handleCardPayment(clientSecret, cardElement, {
            payment_method_data: {
                billing_details: {
                    name: cardholderName.value
                }
            }
        }).then(function(result) {
            if (result.error) {
                document.getElementById("card-errors").style.display = "block";
                document.getElementById("card-errors").innerHTML = "NÃ¥got Ã¤r fel, kontrollera kortuppgifterna";
                cardButton.disabled = false;
                cardButton.innerHTML = "Betala";
            } else {
                console.log('betalning klar');
                waitForProduct('stripe', pnq, product, customerTempId);
            }
        });
    });
}