from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
import os
import csv

correct_marks = 5
wrong_marks = -1

class MyCustomStorage(FileSystemStorage):
    def get_available_name(self, name, max_length = None):
        return name

    def _save(self, name, content):
        if self.exists(name):
            self.delete(name)
        return super(MyCustomStorage, self)._save(name, content)

# Create your views here.
def index(request):
    return HttpResponse("Index Page")

def valuePos(request):
    if request.GET.get('pos'):
        message1 = 'You submitted: %r' % request.GET['pos']
    else:
        message1 = 'You submitted nothing!'
    
    if request.GET.get('neg'):
        message1 += ' <br> You submitted: %r' % request.GET['neg']
    else:
        message1 += ' <br> You submitted nothing!'
    # print(request)
    # print(request.GET)
    # print(request.GET.get)
    # print(request.GET.get["pos"], request.GET.get["neg"])
    correct_marks = request.GET["pos"]
    wrong_marks = request.GET["neg"]
    # print(request.GET["pos"], correct_marks)
    # print(request.GET["neg"], wrong_marks)
    if os.path.exists("Project_App/marks.csv"):
        os.remove("Project_App/marks.csv")
    
    with open("Project_App/marks.csv", "a") as file:
        writer = csv.writer(file)
        # writer.writerow(header)
        # writer.writerow(concise_info)
        writer.writerow([request.GET["pos"], request.GET["neg"]])
        # writer.writerow([3, -3])
        file.close()
    return HttpResponse(message1)

def home(request):
    # return HttpResponse("Home Page")
    # return render(request, "Project_App/home.html")
    if request.method == 'POST' and request.FILES['upload']:
        upload = request.FILES['upload']
        fss = MyCustomStorage()
        file = fss.save(upload.name, upload)
        file_url = fss.url(file)
        return render(request, 'Project_App/home.html', {'file_url': file_url})
    return render(request, 'Project_App/home.html')

from .Vishal_Marksheet import *
def marksheet(request):
    # print(request.GET)
    # correct_marks = request.GET["pos"]
    # wrong_marks = request.GET["neg"]
    # print(correct_marks, wrong_marks)
    # if not os.path.exists("Project_App/marks.csv"):
    #     return HttpResponse("Please Enter Marks")

    # with open("Project_App/marks.csv", "a") as file:
    #     reader = csv.reader(file)
    #     for row in reader:
    #         print(row)
        # pass
    Marksheet_Generator()
    return HttpResponse("Successfull")

from .Vishal_Concise import *
def concise(request):
    # print(correct_marks, wrong_marks)
    concise_marksheet_generator()
    return HttpResponse("Successfull")

from .Vishal_Email import *
def email(request):
    send_Email()
    return HttpResponse("Successfull")

