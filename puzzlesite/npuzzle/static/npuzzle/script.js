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

function appendNewMatriz(matriz, dimension){
    container = $("#divTable")

    $("#table").remove()

    container.append("<table id='table' border='1'></table>")

    table = $("#table")

    console.log(matriz)

    for(let i = 0; i< matriz.length ; i++){
        table.append("<tr id='row"+i+"'/>")
        for(let j = 0; j < matriz.length; j++){
            $("#row"+i).append(`<td id='col${j}' onclick='move(${i},${j},[${matriz}], ${dimension});' >`+matriz[i][j]+`</td>`)
        }
    }

    container.append(
    `<form action="#" method="post">
       <input type="hidden" class="form-control" id="matriz" placeholder="" value="[${matriz}]"
              name='matriz'>
       <input type="submit" value="Resolver">
    </form>`)

}


var inputElem = document.createElement('input');
inputElem.type = 'hidden';
inputElem.name = 'csrfmiddlewaretoken';
inputElem.value = '{{ csrf_token }}';
selectform.appendChild(inputElem);