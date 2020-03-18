$(document).ready(function(){

     $(".showreplies").hover(function(){
        //$(this).css("background-color", "darkgray")
        this.style.setProperty('background-color', 'darkgray', 'important');
        console.log("Test");
     }, function(){
        this.style.setProperty('background-color', 'gainsboro', 'important');
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

        $(repliestag).slideToggle();



    });






});