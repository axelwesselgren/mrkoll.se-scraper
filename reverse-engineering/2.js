var LazyLoader = {};
LazyLoader.timer = {};
LazyLoader.scripts = [];
LazyLoader.load = function(url, context, callback) {
    var classname = null,
        properties = null;
    try {
        LazyLoader.scripts.push(url);
        var script = document.createElement("script");
        script.src = url;
        script.type = "text/javascript";
        context.get(0).appendChild(script);
        if (callback) {
            script.onreadystatechange = function() {
                if (script.readyState === 'loaded' || script.readyState === 'complete') {
                    callback();
                    jQuery(script).remove();
                }
            };
            script.onload = function() {
                callback();
                jQuery(script).remove();
                return;
            };
            try {
                if (($.browser.webkit && !navigator.userAgent.match(/Version\/3/)) || $.browser.opera) {
                    LazyLoader.timer[url] = setInterval(function() {
                        if (/loaded|complete/.test(document.readyState)) {
                            clearInterval(LazyLoader.timer[url]);
                            callback();
                        }
                    }, 10);
                }
            } catch (e) {}
        }
    } catch (er) {
        alert(er);
    }
};
var xrayAd = {
    div: null,
    viewport: null,
    thresold: 200,
    elements: [],
    adBlockCount: 0,
    w: 160,
    h: 200,
    init: function() {
        this.div = $('#xrayAd');
        if (!this.div) {
            this.div = $('<div>', {
                id: 'xrayAd',
                css: {
                    position: 'fixed',
                    top: 10,
                    left: 10,
                    width: this.w,
                    height: this.h,
                    zIndex: 10000,
                    background: 'rgba(0,0,0, 0.5)'
                }
            });
            this.div.appendTo($('body'));
        }
    },
    viewportUpdate: function() {
        if (!this.viewport) {
            this.viewport = $('<div>', {
                id: 'xrayAdViewport',
                css: {
                    position: 'absolute',
                    width: this.w,
                    height: 10,
                    zIndex: 10001,
                    background: 'rgba(255,255,255, 0.3)'
                }
            });
            this.viewport.appendTo(this.div);
        }
        if (!this.viewThresoldTop) {
            this.viewThresoldTop = $('<div>', {
                id: 'xrayAdThresold',
                css: {
                    position: 'absolute',
                    width: this.w,
                    height: 1,
                    zIndex: 10002,
                    background: 'rgba(255,0,0, 0.5)'
                }
            });
            this.viewThresoldTop.appendTo(this.div);
            this.viewThresoldBottom = this.viewThresoldTop.clone().appendTo(this.div);
        }
        this.bodyHeight = $(document).height();
        this.bodyWidth = $(window).width();
        var vH = ($(window).height() / this.bodyHeight) * xrayAd.h,
            vT = ($(window).scrollTop() / this.bodyHeight) * xrayAd.h;
        this.viewport.css({
            height: vH,
            top: vT
        });
        this.viewThresoldTop.css({
            top: (($(window).scrollTop() - xrayAd.thresold) / this.bodyHeight) * xrayAd.h
        });
        this.viewThresoldBottom.css({
            top: (($(window).scrollTop() + xrayAd.thresold) / this.bodyHeight) * xrayAd.h + vH - 1
        });
        if (this.div && this.div.length) {
            var blocks = this.div.find('.xrayAdBlock');
            $.each(blocks, function(key, val) {
                var xrayBlock = $(this);
                var adBlock = $(xrayAd.elements[key]);
                if (xrayBlock.length && adBlock.length) {
                    var size = {};
                    size.off = adBlock.offset();
                    if (size.off) {
                        size.top = (size.off.top / xrayAd.bodyHeight) * xrayAd.h;
                        size.left = (size.off.left / xrayAd.bodyWidth) * xrayAd.w;
                        size.w = (Math.max(adBlock.width(), 10) / xrayAd.bodyWidth) * xrayAd.w;
                        size.h = (Math.max(adBlock.height(), 10) / xrayAd.bodyHeight) * xrayAd.h;
                        var bgColor = '#FF0071';
                        bgColor = (adBlock.data('loading') === 'true' ? 'orange' : bgColor);
                        bgColor = (adBlock.data('loaded') === 'true' ? '#00FF00' : bgColor);
                        xrayBlock.css({
                            top: size.top,
                            left: size.left,
                            width: size.w,
                            height: size.h,
                            borderColor: bgColor
                        });
                    }
                }
            });
        }
    },
    load: function(el, thresold) {
        this.thresold = thresold || 0;
        this.init();
        var adBlock = $('<div>', {
            'class': 'xrayAdBlock',
            'css': {
                position: 'absolute',
                background: '#ffffff',
                border: '1px solid #FF0071',
                top: 0,
                left: 0,
                width: 0,
                height: 0,
                zIndex: 10003
            }
        });
        $.each(el, function() {
            adBlock.clone().attr('xrayblock', 'xrayAdBlock_' + (xrayAd.adBlockCount++)).appendTo(xrayAd.div);
            $(this).bind('onCompleteXray', function() {
                xrayAd.viewportUpdate();
            });
            $(this).bind('onLoadXray', function() {
                xrayAd.viewportUpdate();
            });
            xrayAd.elements.push(this);
        });
        xrayAd.viewportUpdate();
        $(window).bind("scroll", function(event) {
            xrayAd.viewportUpdate();
        });
    }
};
(function($) {
    $.lazyLoadAdRunning = false;
    $.lazyLoadAdTimers = [];
    $.fn.lazyLoadAd = function(options) {
        var settings = {
            threshold: 0,
            failurelimit: 1,
            forceLoad: false,
            event: "scroll",
            viewport: window,
            placeholder: false,
            onLoad: false,
            onComplete: false,
            timeout: 1500,
            debug: false,
            xray: false
        };
        if (options) {
            $.extend(settings, options);
        }

        function _debug() {
            if (typeof console !== 'undefined' && settings.debug) {
                var args = [];
                for (var i = 0; i < arguments.length; i++) {
                    args.push(arguments[i]);
                }
                try {
                    console.log('LazyLoadAD |', args);
                } catch (e) {}
            }
        }
        if (settings.xray && (typeof xrayAd === 'object')) {
            xrayAd.load(this, settings.threshold);
        }
        var elements = this;
        $(settings.viewport).bind("checkLazyLoadAd", function() {
            var counter = 0;
            elements.each(function() {
                if ($.lazyLoadAdRunning) {
                    if ($.lazyLoadAdTimers.runTimeOut) {
                        clearTimeout($.lazyLoadAdTimers.runTimeOut);
                    }
                    $.lazyLoadAdTimers.runTimeOut = setTimeout(function() {
                        $(settings.viewport).trigger("checkLazyLoadAd");
                    }, 300);
                    return false;
                } else if (settings.forceLoad === true) {
                    $(this).trigger("load");
                } else if (!$.belowthefold(this, settings) && !$.abovethetop(this, settings)) {
                    $(this).trigger("load");
                } else {
                    if (counter++ > settings.failurelimit) {
                        return false;
                    }
                }
            });
            var temp = $.grep(elements, function(element) {
                return !(($(element).data('loaded') === 'true') ? true : false);
            });
            elements = $(temp);
        });
        if ("scroll" === settings.event) {
            $(settings.viewport).bind("scroll", function(event) {
                if (elements.length === 0) {
                    return false;
                }
                $(settings.viewport).trigger("checkLazyLoadAd");
            });
        }
        this.each(function(_index, _value) {
            var self = $(this);
            if (undefined === self.attr("original")) {
                self.attr("original", self.attr("src"));
            }
            self.isLoaded = function() {
                return ((self.data('loaded') === 'true') ? true : false);
            };
            self.bind("debug", function(e, status) {
                status = status || 'start';
                if (settings.xray) {
                    if (status === 'start') {
                        self.trigger('onLoadXray');
                    } else if (status === 'error') {
                        self.trigger('onErrorXray');
                    } else if (status === 'complete') {
                        self.trigger('onCompleteXray');
                    }
                }
                if (settings.debug) {
                    if (status === 'start') {
                        self.css({
                            border: '3px solid orange'
                        });
                    } else if (status === 'error') {
                        self.css({
                            border: '3px solid red'
                        });
                    } else if (status === 'complete') {
                        self.css({
                            border: '3px solid green'
                        });
                    }
                }
            });
            self.one('onComplete', function() {
                _debug('---> lazyLoadComplete');
                $(self).removeAttr("original");
                $.lazyLoadAdRunning = false;
                self.data('loaded', 'true');
                self.trigger('debug', 'complete');
                if (typeof settings.onComplete === 'function') {
                    try {
                        settings.onComplete();
                    } catch (e) {}
                }
            });
            self.stack = [];
            self.makinaBlock = false;
            self.bind('makina_go', function() {
                if (self.makinaBlock) {
                    return false;
                }
                if (self.stack.length > 0) {
                    var el = self.stack.shift();
                    var wrapAd = self.find('.wrapAd');
                    if (!wrapAd.length) {
                        wrapAd = $('<div class="wrapAd"></div>').clone();
                        wrapAd.appendTo(self);
                    }
                    var wrap = $('<div>').clone().appendTo(wrapAd);
                    if (typeof el === 'string') {
                        wrap.replaceWith(el);
                    } else if (typeof el === 'object') {
                        if (el.is('script')) {
                            if (el.attr('src')) {
                                _debug('JS to load !! --> ' + el.attr('src'));
                                LazyLoader.load(el.attr('src'), self, function() {
                                    self.makinaBlock = false;
                                    _debug('JS to load !! ++> ' + el.attr('src'));
                                    self.trigger('makina_go');
                                });
                            } else {
                                wrap.replaceWith(el);
                            }
                        } else {
                            wrap.replaceWith(el);
                        }
                    }
                    self.trigger('makina_go');
                } else {
                    if ($.lazyLoadAdTimers.loadJS) {
                        clearTimeout($.lazyLoadAdTimers.loadJS);
                    }
                    $.lazyLoadAdTimers.loadJS = setTimeout(function() {
                        self.trigger('onComplete');
                    }, settings.timeout);
                }
            });
            self.bind('docWrite_direct', function(e, html) {
                var el = $(html);
                _debug('Fragment Direct Write : ', el, el.length);
                $.each(el, function() {
                    self.stack.push($(this));
                });
                self.trigger('makina_go');
            });
            self.bind('docWrite_delayed', function(e, html) {
                _debug('Fragment Delayed Write : ', html);
                self.numWrappers--;
                _debug("Fragment append : ", self.numWrappers, html);
                self.docHtmlCurrent += html;
                if (self.numWrappers === 0) {
                    html = self.docHtmlCurrent;
                    self.docHtmlCurrent = '';
                    setTimeout(function() {
                        self.stack.push(html);
                        self.docHtmlCurrent = '';
                        self.trigger('makina_go');
                    }, 0);
                }
            });
            self.numWrappers = 0;
            self.docHtmlCurrent = '';
            self.bind('docWrite_overload', function() {
                document._writeOriginal = document.write;
                document.write = document.writeln = function() {
                    var args = arguments,
                        id = null;
                    var html = '';
                    for (var i = 0; i < args.length; i++) {
                        html += args[i];
                    }
                    var testHTML = '',
                        directWrite = false;
                    try {
                        testHTML = $(html);
                        directWrite = ((testHTML.is('div') || testHTML.is('script')) ? true : false);
                    } catch (e) {}
                    self.history[self.fragmentId] = self.history[self.fragmentId] || {};
                    if (self.history[self.fragmentId][html] === undefined) {
                        self.history[self.fragmentId][html] = true;
                        if (directWrite) {
                            self.trigger('docWrite_direct', html);
                        } else {
                            self.numWrappers++;
                            setTimeout(function() {
                                self.trigger('docWrite_delayed', html);
                            }, 0);
                        }
                    }
                };
            });
            self.bind('evalCode', function() {
                var scripts = [],
                    script, regexp = /<code[^>]*>([\s\S]*?)<\/code>/gi;
                while ((script = regexp.exec(self.html()))) {
                    var _s = script[1];
                    _s = _s.replace('<!--//<![CDATA[', '').replace('//]]>-->', '').replace('<!--', '').replace('//-->', '');
                    _s = _s.replace(/\&gt\;/g, '>').replace(/\&lt\;/g, '<');
                    scripts.push($.trim(_s));
                }
                try {
                    scripts = (scripts.length ? scripts.join('\n') : '');
                    _debug('Script to eval : ', scripts);
                    if (scripts !== '') {
                        eval(scripts);
                    }
                } catch (e) {}
            });
            self.bind('loadJS', function(e, js2load) {
                var callback = null,
                    script = null;
                if (js2load.src) {
                    callback = js2load.callback || null;
                    js2load = js2load.src;
                }
                if (js2load.indexOf('?') === -1) {
                    js2load += '?_=' + (new Date().getTime());
                } else {
                    js2load += '&_=' + (new Date().getTime());
                }
                _debug('loadJS :: ', js2load);
                LazyLoader.load(js2load, self, function() {
                    _debug('loadJS COMPLETE :: ' + js2load);
                    if (callback) {
                        callback();
                    } else {
                        $.lazyLoadAdTimers.loadJS = setTimeout(function() {
                            self.trigger('onComplete');
                        }, settings.timeout);
                    }
                });
            });
            self.one("load", function() {
                if (!self.isLoaded()) {
                    $.lazyLoadAdRunning = true;
                    self.data('loading', 'true');
                    self.trigger('debug', 'start');
                    var srcOriginal = $(self).attr("original");
                    self.history = {};
                    _debug('------------------------------  Lazy Load Ad CALL ----');
                    _debug('Context : ', self);
                    self.trigger('docWrite_overload');
                    self.trigger('evalCode');
                    if (srcOriginal) {
                        self.trigger('loadJS', srcOriginal);
                    }
                }
            });
            if ("scroll" !== settings.event) {
                self.bind(settings.event, function(event) {
                    if (!self.isLoaded()) {
                        self.trigger("load");
                    }
                });
            }
        });
        $(settings.viewport).trigger('checkLazyLoadAd');
        return this;
    };
    $.belowthefold = function(element, settings) {
        var fold = 0;
        if (settings.viewport === undefined || settings.viewport === window) {
            fold = $(window).height() + $(window).scrollTop();
        } else {
            fold = $(settings.viewport).offset().top + $(settings.viewport).height();
        }
        return fold <= $(element).offset().top - settings.threshold;
    };
    $.abovethetop = function(element, settings) {
        var fold = 0;
        if (settings.viewport === undefined || settings.viewport === window) {
            fold = $(window).scrollTop();
        } else {
            fold = $(settings.viewport).offset().top;
        }
        return fold >= $(element).offset().top + settings.threshold + $(element).height();
    };
})(jQuery);