$(document).ready(function(){

     $(".showreplies").hover(function(){
        this.style.setProperty('background-color', 'darkgray', 'important');
     }, function(){
        this.style.setProperty('background-color', 'rgba(240, 240, 240, 0.9)', 'important');
     });

    $(".showreplies").click(function(){

        // id passed by the template (Question id)
        var questionid;
        questionid = $(this).attr('data-questionid');
        console.log(questionid);

        // id for count
        var repliestag;
        repliestag = ".replies-" + questionid;
        console.log(repliestag);

        // id for 'answer' text
        var answertag;
        answertag = ".answer-" + questionid
        console.log(answertag);

        // id for 'comment' text
        var commenttag;
        commenttag = ".comment-" + questionid
        console.log(commenttag);

        // slide to view
        $(repliestag).slideToggle();

        // toggle between 'Answer' and 'Answer (Click to view)'
        $(answertag).text($(answertag).text() == 'Answer (Click to view)' ? 'Answer' : 'Answer (Click to view)');



    });






});