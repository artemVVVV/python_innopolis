$(document).ready(function(){
    var csrf = $("input[name=csrfmiddlewaretoken]").val();
    $(".btn").click(function(){
        $.ajax({
            url: '',
            type: 'post',
            data: {
                rename_new:document.getElementById("rename_new").text,
                id_file:document.getElementById("id_file").text,
                check_btn: document.getElementById("check_btn").text,
                csrfmiddlewaretoken: csrf
            }
        });
    });
});