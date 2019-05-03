from django.shortcuts import render


# Create your views here.
def index(
        request,
        template_name='pos/index.html',
        page_name='Index'):

    context = {
        'page_name': page_name,
    }

    return render(
        request,
        template_name,
        context,
    )
