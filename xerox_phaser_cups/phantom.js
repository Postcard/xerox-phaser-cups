"use strict";
var page = require('webpage').create();
var system = require('system');

var args = system.args;

var outputFilePath = args[2]

page.content = args[1];

page.onLoadFinished = function(){
    page.render(outputFilePath, {format: 'pdf'});
    phantom.exit();
}
