from django.http import HttpResponse
from django.shortcuts import render
import json

from .python.puzzle import main


def index(request):
    res = {
        'matriz': [[1, 2, 3], [4, 5, 6], [7, 8, 0]],
    }

    return render(request, 'npuzzle/index.html', res)


def solve_puzzle(request):
    if request.method == 'POST':
        matriz = request.POST.get('matriz')
        dimension = request.POST.get('dimension')
        result = main(matriz, int(dimension))
        result_list = {
            'result_list': result
        }
        return HttpResponse(
            json.dumps(result_list),
            content_type="application/json"
        )
    else:
        return HttpResponse("nao autorizado")