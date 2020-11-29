from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, TemplateView
from .models import Post
from .forms import UploadImageForm
from django.core.files.storage import FileSystemStorage
from travel import Using_Saved_Model

# Create your views here.
class mainview(LoginRequiredMixin, View):
    login_url = '/login'
    redirect_field_name = 'redirect to'

    def get(self, request):
        context = {
            'user': request.user.username,
            'default': True,
        }
        return render(request, 'travel/index.html', context)

def index(request):
    return render(request, 'travel/index.html')

def know(request):
    posts = Post.objects.filter(published_date__isnull=False).order_by('-created_date')
    context = {
        'posts': posts,
    } 
    return render(request, 'travel/know.html', context)

def know_show(request, pk):
    post = Post.objects.get(pk=pk)
    context={
        'post':post
    }
    return render(request, 'travel/know_show.html', context)

def howto(request):
    return render(request, 'travel/howto.html')

def login(request):
    return render(request, 'travel/login.html')

def upload(request):
    return render(request, 'travel/map.html')

def loading(request):
    return render(request, 'travel/loading.html')

class PostTemplateView(TemplateView):
    template_name = 'travel/loading.html'

def uimage(request):
    if request.method == 'POST':
        form = UploadImageForm(request.POST, request.FILES)  # 이미지르 업로드할때 쓰는 form
        if form.is_valid():
            myfile = request.FILES['image']
            fs = FileSystemStorage()  # 이미지 파일을 저장
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = "{}".format(myfile)
            img_path = 'C:/Users/songtg/Desktop/Final_project/eztravel/media/' + uploaded_file_url
            print(uploaded_file_url)
            result = Using_Saved_Model.execute_model(img_path)
            print(result)
            file_url=fs.url(filename)
            context = {
                'result' : result,
                'uploaded_file_url' : img_path
            }
            print(type(context))
            print(context['result'])
            return JsonResponse({"result":result, "file_url":file_url})
            #return render(request, 'travel/uimage.html', context)
    else:
        form = UploadImageForm()
        print(form, "----------------------------------------------------------------------")
        return render(request, 'travel/uimage.html', {'form': form})

