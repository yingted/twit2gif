// ==UserScript==
// @name         twit2gif
// @version      1.0
// @description  Tweet to gif
// @match        https://twitter.com/*
// @require              http://ajax.googleapis.com/ajax/libs/jquery/1.11.2/jquery.min.js
// @resource     https://maxcdn.bootstrapcdn.com/bootstrap/3.3.2/css/bootstrap.min.css
// ==/UserScript==

var tweet_ui = $(".tweet-box-extras");
tweet_ui.append('<input class="btn btn-default" type="button" value="gifit">').click(function(){
    var sentence = $("#tweet-box-global").children().text();
    alert("SENTENCE: " + sentence);
});
