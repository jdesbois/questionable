$(document).ready(function(){

    $('#ajax_btn').click(function(){

//     var valToDouble = 2;
    valToDouble = $(this).attr('data-infoid');

    $.get('/main/double_response/',
        {'info_id':valToDouble},
        function(data){
            $('#returned_info').html(data);
        })
    });


})
