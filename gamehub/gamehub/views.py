from django.shortcuts import render


def main_page(request):
    return render(request, 'gamehub/index.html')


def detail_page(request):
    return render(request, 'gamehub/detail_page.html')
