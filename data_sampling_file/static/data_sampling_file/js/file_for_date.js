$(document).ready(function(){
    var csrf = $("input[name=csrfmiddlewaretoken]").val();
    $(".btn").click(function(){
        $.ajax({
            url: '',
            type: 'post',
            data: {
                date_old:document.getElementById("date_old").text,
                date_new:document.getElementById("date_new").text,
                csrfmiddlewaretoken: csrf
            }
        });
    });
});