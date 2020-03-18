$(document).ready(function(){

    console.log("Test");

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
                $(counttag).html(data);
                $(buttontag).attr("disabled", true);
            })



    });

});


   // var buttontag;
   // buttontag = str.concat("#upvote-", $(this).attr('data-questionid'));

   // var counttag;
  //  counttag = str.concat("#count-", $(this).attr('data-questionid'));

   // Console.log(buttontag);

   // $(buttontag).click(function(){
      //  var questionid;
    //    questionid = $(this).attr('data-questionid');

    //    $.get('/main/upvote/',
          //  {'question_id': questionid},
          //  function(data){
             //   $(counttag).html(data);
             //   $(buttontag).hide();
          //  })


   // });
//});