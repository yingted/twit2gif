// ==UserScript==
// @name         twit2gif
// @version      1.0
// @description  Tweet to gif
// @match        https://twitter.com/*
// @grant        GM_xmlhttpRequest
// @require      http://ajax.googleapis.com/ajax/libs/jquery/1.11.2/jquery.min.js
// @resource     https://maxcdn.bootstrapcdn.com/bootstrap/3.3.2/css/bootstrap.min.css
// ==/UserScript==

var tweet_ui = $('.tweet-box-extras');
tweet_ui.append('<input class="btn btn-default" type="button" value="gifit">').click(function(){
    var sentence = $(this).parents('.tweet-form').find('.tweet-box').text();
    GM_xmlhttpRequest({
      method: 'POST',
      url: 'http://52.0.224.239:8080/query',
      //url: 'http://127.0.0.1:8080/query',
      data: 'text=' + encodeURIComponent(sentence),
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        Accept: 'application/json',
      },
      onload: function(response) {
        var text = response.responseText;
        if (response.responseText) {
          console.log('data: ' + response.responseText);
        }
      }
    });
}); // vim: ts=4:sw=4:et
