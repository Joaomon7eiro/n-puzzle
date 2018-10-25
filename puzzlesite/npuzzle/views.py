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
        matrix = request.POST.get('matrix')
        dimension = request.POST.get('dimension')
        search_type = request.POST.get('search_type')
        limit = request.POST.get('limit')

        matrix_list, nodes_processed, time_spent, total_steps = main(matrix, int(dimension), search_type, limit)
        results = {
            'matrix_list': matrix_list,
            'nodes_processed': nodes_processed,
            'time_spent': time_spent,
            'total_steps': total_steps
        }
        return HttpResponse(
            json.dumps(results),
            content_type="application/json"
        )
    else:
        return HttpResponse("nao autorizado")