from django.shortcuts import render

def index(request):
    res = {
        'matriz': [[1, 2, 3], [4, 5, 6], [7, 8, 0]],
    }

    return render(request, 'npuzzle/index.html', res)
