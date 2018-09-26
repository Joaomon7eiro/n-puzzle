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
        create_post();
    });

});


function alerta(matriz){
    alert(matriz)
}

function move(row, col, matrizAsArray, dimension){

    matriz = []
    row_values = []
    for(let i= 0, j=0 ; i <= matrizAsArray.length ; i++, j++){
        if(j == dimension){
            matriz.push(row_values)
            row_values = []
            j = 0
        }
        row_values.push(matrizAsArray[i])
    }

    let distance = 0
    for(let i = 0; i < matriz.length; i++) {
        for(let j=0; j < matriz[0].length; j++){

            if(matriz[i][j] == 0){
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
        matriz[row0][col0] = matriz[row][col]
        matriz[row][col] = 0

        console.log(matriz)
        appendNewMatriz(matriz, dimension)
    }
}

function createMatriz(){
    let dimension = $("#dimension").val()

    $("#stepOne").remove()

    if(!dimension){
        dimension = 0;
    }
    console.log(dimension)

    values = 1
    matriz = []

    for(let i = 0; i < dimension; i++){
        line_values = []
        for(let j=0; j < dimension ; j++){
            line_values.push(values)
            values ++
        }
        matriz.push(line_values)
    }

    matriz[dimension -1][dimension -1] = 0



    appendNewMatriz(matriz, dimension)
}

function create_post() {
    console.log("create post is working!") // sanity check

    $.ajax({
        url : "solve_puzzle/", // the endpoint
        type : "POST", // http method
        data : {
            matriz : $('#matriz').val(),
            dimension : $('#dimension').val()
        }, // data sent with the post request
        // handle a successful response
        success : function(json) {
            $('#matriz').val(''); // remove the value from the input
            console.log(json); // log the returned json to the console
            matriz = json.result_list

            console.log(matriz)

            var k = 0
            while(k < matriz.length){
                (function(k) {
                  setTimeout(function() {
                    current_result = matriz[k]

                    $("#table").remove()
                    container.append("<table id='table' border='1'></table>")

                    table = $("#table")

                    for(let i = 0; i< current_result.length ; i++){
                        table.append("<tr id='row"+i+"'/>")
                        for(let j = 0; j < current_result.length; j++){
                            $("#row"+i).append(`<td>`+current_result[i][j]+`</td>`)
                        }
                    }
                  }, 1000 * k )
               })(k++)
            }

            console.log("success"); // another sanity check
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $('#solve').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
};

function appendNewMatriz(matriz, dimension){
    container = $("#divTable")
    var csrfVar = $('meta[name="csrf-token"]').attr('content');

    $("#table").remove()

    container.append("<table id='table' border='1'></table>")

    table = $("#table")

    for(let i = 0; i< matriz.length ; i++){
        table.append("<tr id='row"+i+"'/>")
        for(let j = 0; j < matriz.length; j++){
            $("#row"+i).append(`<td id='col${j}' onclick='move(${i},${j},[${matriz}], ${dimension});' >`+matriz[i][j]+`</td>`)
        }
    }

    $("#submit").remove()
    $("#matriz").remove()
    $("#dimension").remove()
    form = $("#post-form")
    form.append(`
    <input type="hidden" class="form-control" id="matriz" placeholder="" value='${matriz}'
         name='matriz'>
    `)
    form.append(`<input type="hidden" class="form-control" id="dimension" placeholder="" value="${dimension}"
    name='dimension'>`)
    form.append(`<input id="submit" type="submit" value="Resolver">`)

    $("#solve").show()
}
