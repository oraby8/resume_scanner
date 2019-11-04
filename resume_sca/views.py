from django.shortcuts import render
from django.http import HttpResponseRedirect
from. import resume_scane
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from PyPDF2 import PdfFileReader
import os

 
 
def read_pdf(path):
    try:
        text=''
        path=os.path.join(settings.MEDIA_ROOT, path)
        pdf2=PdfFileReader(path)
        print(path)
        for page in range(pdf2.getNumPages()):
            pages = pdf2.getPage(page)
            #print(page) 
            text += pages.extractText()
        return(text)
    except: None


#module_dir = os.path.dirname(__file__)


def home(request):
	return render(request,'base.html')



# Create your views here.
def new_search(request):
    #Get Data
    try:
        new_search = request.POST.get('search')
        dis = request.POST.get('dis')
        if request.FILES.get('pdf',False) !=False and request.FILES['pdf'].name[-3:]=='pdf':
        #if request.POST.get("")
            pdf=request.FILES['pdf']
    except:
        new_search=None
        dis=None
        
    else:
        pdf=None

    if dis=='':
        dis=None

    elif new_search=='':
        if pdf==None:
            new_search=None
        else:
            try:                
                file=FileSystemStorage()
                file.save(pdf.name,pdf)
                new_search=read_pdf(pdf.name)
            except:
                new_search=None
    
    try:        
        output=resume_scane.scan(str(dis),str(new_search))
    except:
        output=0
    

    allout={'out':output,}
    #delete file after finsh
    if pdf != None:
        try:
            os.remove(os.path.join(settings.MEDIA_ROOT, pdf.name))
        except:
            pass

    return render(request,'new_search.html',allout)
