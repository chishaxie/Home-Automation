Date.prototype.format = function(format) {
    var o = {
        "M+": this.getMonth() + 1,
        "d+": this.getDate(),
        "h+": this.getHours(),
        "m+": this.getMinutes(),
        "s+": this.getSeconds(),
        "q+": Math.floor((this.getMonth() + 3) / 3),
        "S": this.getMilliseconds()
    };
    if (/(y+)/.test(format) || /(Y+)/.test(format)) {
        format = format.replace(RegExp.$1, (this.getFullYear() + "").substr(4 - RegExp.$1.length));
    }
    for (var k in o) {
        if (new RegExp("(" + k + ")").test(format)) {
            format = format.replace(RegExp.$1, RegExp.$1.length == 1 ? o[k] : ("00" + o[k]).substr(("" + o[k]).length));
        }
    }
    return format;
};

var timestampformat = function (timestamp) {
    return (new Date(timestamp * 1000)).format("yyyy-MM-dd hh:mm:ss");
};

var parse_url_search = function () {
    str = window.location.search.substr(1);
    ss = str.split('&');
    var obj = {}
    for (var i=0; i<ss.length; i++) {
        kv = ss[i].split('=');
        obj[kv[0]] = kv[1];
    }
    return obj;
};

var show_err_msg = function (msg) {
    $('#modal_err').html(msg);
    $('#errModal').modal('show');
};
var show_msg = function (msg) {
    $('#modal_msg').html(msg);
    $('#msgModal').modal({backdrop: 'static', keyboard: false});
};
var hide_msg = function() {
    $('#msgModal').modal('hide');
};
