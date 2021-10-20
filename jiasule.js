function jsl(js) {
	window = {
		navigator: {
			userAgent: "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36"
		},
		outerWidth: 1920,
		outerHeight: 1050,
	};
	location = {
		reload: function() {}
	};
	document = {};
    eval(js);
	return document.cookie
}
