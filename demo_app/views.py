from django.shortcuts import render, redirect
from .forms import InputForm
from .models import Customers

def index(request):
    return render(request, 'demo_app/index.html', {})

def input_form(request):
    if request.method == 'POST':
        form = InputForm(request.POST)
        if form.is_valid(): #入力の検証
            form.save() #入力された値の保存
            return redirect('result') #フォーム送信のあとはリダイレクト

    else:
        form = InputForm()
        return render(request, 'demo_app/input_form.html', {'form':form})

def result(request):
    return render(request, 'demo_app/result.html', {})
