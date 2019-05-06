function get_z(x, y){
    f = function(x, y) {
    var a = 0,
    b = 0,
    c = 0;
    x = x.split("");
    y = y || 99;
    while ((a = x.shift()) && (b = a.charCodeAt(0) - 77.5)) c = (Math.abs(b) < 13 ? (b + 48.5) : parseInt(a, 36)) + y * c;
    return c
};
    x = x.replace(/@*$/,"").split("@");
    z = f(y.match(/\w/g).sort(function(x, y) {
    return f(x) - f(y)
}).pop());
    return [x,y,z]

}

function get_js(x, y, z){
    f = function(x, y) {
    var a = 0,
    b = 0,
    c = 0;
    x = x.split("");
    y = y || 99;
    while ((a = x.shift()) && (b = a.charCodeAt(0) - 77.5)) c = (Math.abs(b) < 13 ? (b + 48.5) : parseInt(a, 36)) + y * c;
    return c
};
    x = eval(x);
    z = z +1;
    p = y.replace(/\b\w+\b/g,
        function(y) {
            return x[f(y, z) - 1] || ("_" + y)
        });
    return p

}


function once_js(x, y) {
    f = function(x, y) {
    var a = 0,
    b = 0,
    c = 0;
    x = x.split("");
    y = y || 99;
    while ((a = x.shift()) && (b = a.charCodeAt(0) - 77.5)) c = (Math.abs(b) < 13 ? (b + 48.5) : parseInt(a, 36)) + y * c;
    return c
},
        x = x.replace(/@*$/,"").split("@");
z = f(y.match(/\w/g).sort(function(x, y) {
    return f(x) - f(y)
}).pop());
while (z++) try {
    g = y.replace(/\b\w+\b/g,
    function(y) {
        return x[f(y, z) - 1] || ("_" + y)
    });
    return g
} catch(_) {}
}