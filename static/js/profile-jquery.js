$(document).ready(function(){
//    alert('Hello, world!');
    $('#jq-button').click(function(){
        alert('You clicked the button using JQuery');
    });

    $('p').hover(
        function(){
            $(this).css('color', 'red');
        },
        function(){
            $(this).css('color', 'black');
        }
    );

    $('#add-html').click(function(){
        msgStr = $('#msg').html();
        msgStr = msgStr + "Some extra HTML.";
        $('#msg').html(msgStr);
    })
});