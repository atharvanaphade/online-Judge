$.ajaxSetup({
    cache: false
});
$(document).ready(function () {

    $("#submit").click(function () {
        let question_id = parseInt(document.querySelector('.card-header').textContent.trim().split(' ')[1]);
        let lang = document.getElementById('lang').value;
        let user_code = editor.getValue();
        if (user_code != "") {
            $.ajax({
                url: "{% url 'coding- page' question_id %}",
                type: "POST",
                data: {
                csrfmiddlewaretoken: '{{csrf_token}}',
                ext: lang,
                code: user_code,
            },
                success: function (data) {
                    console.log(data);
                    if (data['message'])
                        alert(data["message"]);
                    else
                        $('html').html(data);
                },
                cache: false,
                });
}
            else
    alert('Please write some code in the editor before submitting.');

        });

$("#run").click(function () {
    let question_id = parseInt(document.querySelector('.card-header').textContent.trim().split(' ')[1]);
    let input = $('#input-textarea').val();
    console.log(input);
    if (input != "") {
        $.ajax({
            url: "{% url 'get-output' %}",
            type: "POST",
            data: {
                csrfmiddlewaretoken: '{{csrf_token}}',
                ip: input,
                question_no: question_id,
            },
            success: function (output) {
                console.log(output);
                let out = output["out"];
                console.log(out);
                $('#output-textarea').val(output["out"]);
            },
            cache: false,
        });
    }
    else {
        $('#output-textarea').val("Please enter an input to see its corresponding output.");
    }
});

$("#load").click(function () {
    let question_id = parseInt(document.querySelector('.card-header').textContent.trim().split(' ')[1]);
    let lang = document.getElementById('lang').value;
    $.ajax({
        url: "{% url 'loadbuffer' %}",
        type: "POST",
        data: {
            csrfmiddlewaretoken: '{{csrf_token}}',
            qno: question_id,
            ext: lang,
        }, dataType: 'json',
        success: function (result) {
            let code = result["txt"];
            if (code != "")
                editor.setValue(code);
            else
                alert('You have no previous submissions of this question with the selected language to load.');
        },
        cache: false,
    });
});

$("#choose-file").change(function () {
    let ext = $('#choose-file').val().split('.')[1];
    if (ext == 'py' || ext == 'cpp' || ext == 'c') {
        let reader = new FileReader();
        reader.onload = handleFileLoad;
        reader.readAsText(event.target.files[0]);

        function handleFileLoad(event) {
            let code = event.target.result;
            editor.setValue(code);
        }
    }
    else
        alert('You can only upload .c, .cpp or .py files.');
});
    });