$(document).ready(function(){



    $(".upvote").click(function(){

        // id passed by the template (Question id)
        var questionid;
        questionid = $(this).attr('data-questionid');
        console.log(questionid);

        // id for count
        var counttag;
        counttag = "#count-" + questionid;
        console.log(counttag);

        // id for button
        var buttontag;
        buttontag = "#upvote-" + questionid;
        console.log(buttontag);

        $.get('/main/upvote/',
            {'question_id': questionid},
            function(data){
                $(counttag).html("Votes: " + data);
                $(buttontag).attr("disabled", true);
            })



    });

});
