$(function() {


    // This function gets cookie with a given name
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');

    /*
    The functions below will create a header with csrftoken
    */

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    function sameOrigin(url) {
        // test that a given url is a same-origin URL
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                // Send the token to same-origin, relative URLs only.
                // Send the token only if the method warrants CSRF protection
                // Using the CSRFToken value acquired earlier
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $('#post-form').on('submit', function(event){
        event.preventDefault();
        console.log("form submitted!")  // sanity check
        solve();
    });

});



function solve() {
    console.log("solve called!")

    $('.container').append("<h1 id='loading'> Aguarde a resolucao do puzzle...</h1><h1>voce pode checar o console para verificar o processamento </h1>")

    $.ajax({
        url : "solve_puzzle/",
        type : "POST",
        data : {
            matrix : $('#matrix').val(),
            dimension : $('#dimension').val(),
            search_type: $('input[name=optradio]:checked', '#post-form').val(),
            limit: $('#limit').val()
        },

        success : function(json) {
            console.log(json);

            $("#loading").remove()

            $("#solve").remove()

            matrix = json.matrix_list
            time_spent = json.time_spent
            nodes_processed = json.nodes_processed

            console.log(matrix)
            console.log(time_spent)
            console.log(nodes_processed)

            let container = $("#divTable")

            $("#submit").remove()

            //$('#mydiv').hide().html('Some new text').fadeIn(1500);

            var k = 0
            while(k < matrix.length){
                (function(k) {
                  setTimeout(function() {
                    current_result = matrix[k]

                    //$("#table").remove()
                    container.html("<table class='table table-bordered table-dark' id='table' border='1'></table>")

                    table = $("#table")

                    for(let i = 0; i< current_result.length ; i++){
                        table.append("<tr id='row"+i+"'/>")
                        for(let j = 0; j < current_result.length; j++){
                            if(current_result[i][j] == 0){
                                $("#row"+i).append(`<td class="empty">`+current_result[i][j]+`</td>`)
                            }else{
                                $("#row"+i).append(`<td>`+current_result[i][j]+`</td>`)
                            }

                        }
                    }
                  }, 200 * k )
               })(k++)
            }
            $('.container').append(`<h3> Tempo decorrido : ${time_spent} segundos</h3>`)
            $('.container').append(`<h3> Nos testados : ${nodes_processed}</h3>`)

            $('.container').append("<button class='btn btn-secondary' onclick='location.reload();'>Refazer</button>")
            console.log("success");
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $('#solve').html("<div class='alert-box alert radius' data-alert>Erro no processamento da resolucao <button class='btn btn-secondary' onclick='location.reload();'>Refazer</button></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
};


function createMatrix(){

    let dimension = $("#matrixDimension").val()

    $("#title").html(`<h1 id="title">Embaralhe a matriz</h1>`)

    $("#divStep").remove()

    if(!dimension){
        dimension = 0;
    }

    values = 1
    matrix = []

    for(let i = 0; i < dimension; i++){
        line_values = []
        for(let j=0; j < dimension ; j++){
            line_values.push(values)
            values ++
        }
        matrix.push(line_values)
    }

    matrix[dimension -1][dimension -1] = 0



    appendNewMatrix(matrix, dimension)
}


function appendNewMatrix(matrix, dimension){
    let container = $("#divTable")
    let csrfVar = $('meta[name="csrf-token"]').attr('content');

    $("#table").remove()

    container.append("<table class='table table-bordered table-dark' id='table' border='1'></table>")

    table = $("#table")

    for(let i = 0; i< matrix.length ; i++){
        table.append("<tr id='row"+i+"'/>")
        for(let j = 0; j < matrix.length; j++){
            if(matrix[i][j]== 0){
                $("#row"+i).append(`<td class='col${j} empty' onclick='move(${i},${j},[${matrix}], ${dimension});' >`+matrix[i][j]+`</td>`)
            }else{
                $("#row"+i).append(`<td class='col${j}' onclick='move(${i},${j},[${matrix}], ${dimension});' >`+matrix[i][j]+`</td>`)
            }

        }
    }


    $("#matrix").remove()
    $("#dimension").remove()

    $("#post-form").append(`<input type="hidden" class="form-control" id="matrix" placeholder="" value='${matrix}' name='matrix'>`)
    $("#post-form").append(`<input type="hidden" class="form-control" id="dimension" placeholder="" value="${dimension}" name='dimension'>`)

    $("#solve").show()
}


function move(row, col, matrixAsArray, dimension){

    matrix = []
    row_values = []
    for(let i= 0, j=0 ; i <= matrixAsArray.length ; i++, j++){
        if(j == dimension){
            matrix.push(row_values)
            row_values = []
            j = 0
        }
        row_values.push(matrixAsArray[i])
    }

    let distance = 0
    for(let i = 0; i < matrix.length; i++) {
        for(let j=0; j < matrix[0].length; j++){

            if(matrix[i][j] == 0){
                row0 = i;
                col0 = j;
            }
        }
    }

    if(row0 > row){
        distance += row0 - row
    }else{
        distance += row - row0
    }

    if(col0 > col){
        distance += col0 - col
    }else{
        distance += col - col0
    }



    if(distance > 1){
        console.log("movimento invalido")
    }else{
        matrix[row0][col0] = matrix[row][col]
        matrix[row][col] = 0

        console.log(matrix)
        appendNewMatrix(matrix, dimension)
    }
}
