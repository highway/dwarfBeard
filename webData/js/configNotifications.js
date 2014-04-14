$(document).ready(function () {
    var loading = '<img src="' + siteRoot + '/images/loading16.gif" height="16" width="16" />';

   
    $('#twitterStep1').click(function () {
        $('#testTwitter-result').html(loading);
        $.get(siteRoot + "/home/twitterStep1", function (data) {window.open(data); })
            .done(function () { $('#testTwitter-result').html('<b>Step1:</b> Confirm Authorization'); });
    });

    $('#twitterStep2').click(function () {
        $('#testTwitter-result').html(loading);
        var twitter_key = $("#twitter_key").val();
        $.get(siteRoot + "/home/twitterStep2", {'key': twitter_key},
            function (data) { $('#testTwitter-result').html(data); });
    });

    $('#testTwitter').click(function () {
        $.get(siteRoot + "/home/testTwitter",
            function (data) { $('#testTwitter-result').html(data); });
    });

});
