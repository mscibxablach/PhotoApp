from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, CreateView
from django.core.files.storage import FileSystemStorage
from io import BytesIO
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from PIL import Image
import numpy as np
import cv2
from .forms import PhotoForm, WithoutDBPhotoForm
from .models import Photo
from mysite.utils.image_utils import ImageUtils
from mysite.plot_cutter.plot_recognizer import PlotRecognizer
from mysite.plot_cutter.plot_cutter import  PlotCutter
from mysite.services.plot_bound_service import PlotBoundService
from mysite.plot_bound_detector.ImageProcessor import ImageProcessor
from mysite.plot_bound_detector.PlotBoundDetector import PlotBoundDetector

class Home(TemplateView):
    template_name = 'home.html'


def upload(request):
    context = {}
    if request.method == 'POST':
        # przekazany z upload.html
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        # zapisywanie pliku
        name = fs.save(uploaded_file.name, uploaded_file)
        context['url'] = fs.url(name)
    return render(request, 'upload.html', context)


def photo_list(request):
    photos = Photo.objects.all()
    return render(request, 'photo_list.html', {
        'photos': photos
    })


def upload_photo(request):
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('photo_list')

    else:
        form = PhotoForm()
    return render(request, 'upload_photo.html', {
        'form': form
    })


def delete_photo(request, pk):
    if request.method == 'POST':
        photo = Photo.objects.get(pk=pk)
        photo.delete()
    return redirect('photo_list')


# TO DO - ma pobierać dane z formularza i wpychać je do PDFa i potem wypluwać PDFa
def some_view(request, name, surname, description):

    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    filename = name + "_" + surname + ".pdf"
    response['Content-Disposition'] = 'attachment; filename= "%s"' % filename

    buffer = BytesIO()

    # Create the PDF object, using the BytesIO object as its "file."
    p = canvas.Canvas(buffer)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(30, 800, name + " " + surname)
    p.drawString(30, 770, description)
    # p.drawImage(photo, 80, 30)


    # Close the PDF object cleanly.
    p.showPage()
    p.save()

    # Get the value of the BytesIO buffer and write it to the response.
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response


def upload_photo_without_DB(request):
    context = {}
    if request.method == 'POST':     # if this is a POST request we need to process the form data
        form = WithoutDBPhotoForm(request.POST, request.FILES)     # create a form instance and populate it with data from the request:
        if form.is_valid():
            photo_bytes = form.cleaned_data['photo'].read()
            photo = ImageUtils.convert_inmemory_file_to_cv2_image(photo_bytes)
            plot_recgonizer = PlotRecognizer()

            plot_cutter = PlotCutter(plot_recgonizer)
            image_processor = ImageProcessor()
            plot_bound_detector = PlotBoundDetector(image_processor)
            plot_bound_service = PlotBoundService(plot_bound_detector)

            result = plot_cutter.cut_plot(photo)
            top, bottom, ratio = plot_bound_service.get_plot_bound_ratio(result)
            # return redirect('photo_list') form.files['photo']
            return some_view(request, form.cleaned_data['name'], form.cleaned_data['surname'], form.cleaned_data['description'])

    else:
        form = WithoutDBPhotoForm()
    return render(request, 'upload_photo_without_DB.html', {
        'form': form
    })


