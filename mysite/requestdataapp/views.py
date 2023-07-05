from django.core.exceptions import ValidationError
from django.core.files.storage import FileSystemStorage
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
import os

from .forms import UserBioForm, UploadFileForm

def process_get_view(request: HttpRequest) -> HttpResponse:
    a = request.GET.get('a', '')
    b = request.GET.get('b', '')
    result = a + b
    context = {
        'a': a,
        'b': b,
        'result': result,
    }
    return render(request, 'requestdataapp/request-query-params.html', context=context)

def user_form(request: HttpRequest) -> HttpResponse:
    context = {
        'form': UserBioForm(),
    }
    return render(request, 'requestdataapp/user-bio-form.html', context=context)

def handle_file_upload(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # myfile = request.FILES['myfile']
            myfile = form.cleaned_data['file']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            print('saved file', filename)
    else:
        form = UploadFileForm()

    context = {
        'form': form,
    }

    return render(request, 'requestdataapp/file-upload.html', context=context)


def handle_limited_file_upload(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST' and request.FILES.get('limited_file'):
        limited_file = request.FILES['limited_file']
        size = os.path.getsize(os.path.abspath(limited_file.name))
        if size > 4 * 1024 * 1024:
            raise ValidationError("File too large ( > 4mb )")
        fs = FileSystemStorage()
        filename = fs.save(limited_file.name, limited_file)
        print('saved file', filename)

    return render(request, 'requestdataapp/limited-file-upload.html')