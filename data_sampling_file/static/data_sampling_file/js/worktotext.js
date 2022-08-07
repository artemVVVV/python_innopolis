$(document).ready(function(){
    var csrf = $("input[name=csrfmiddlewaretoken]").val();
    $(".btn").click(function(){
        $.ajax({
            url: '',
            type: 'post',
            data: {
                text_data:document.getElementById("text_data").text,
                csrfmiddlewaretoken: csrf
            }
        });
    });
});