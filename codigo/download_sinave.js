
const fs = require('fs');
const jsdom = require("jsdom");
const { JSDOM } = jsdom;

const  url = "https://ncov.sinave.gob.mx/mapa.aspx";
var date = new Date();
date.setDate(date.getDate() - 1);
var dd = String(date.getDate()).padStart(2, '0');
var mm = String(date.getMonth() + 1).padStart(2, '0'); //January is 0!
var yyyy = date.getFullYear();
var outfile = yyyy + mm + dd + '.json';

var options = {
  pretendToBeVisual: true,
  runScripts: "dangerously"
};

var ajax = {
  type: "POST",
  contentType: "application/json; charset=utf-8",
  url: "Mapa.aspx/Grafica22",
  data: "{}",
  datatype: "json",
  // success: llenarChart21,
  error: function ajaxError(result) {
      alert(result.status + ' : ' + result.statusText);
  }
};


JSDOM.fromURL(url, options)
  .then(dom => {
    const $ = require('jquery')(dom.window);
    var request = $.ajax(ajax);

    request.done(function() {
      fs.writeFileSync(outfile, request.responseJSON.d);
      console.log('Archivo JSON escrito')
    });
  });
