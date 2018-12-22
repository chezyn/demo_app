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

def calculate(request):
    if request.method == 'POST':
        nums = request.POST #POSTされた値の取得
        #print(nums) #printでデバッグ(ターミナルに表示)
        #print(nums['num1'])
        ans = int(nums['num1']) + int(nums['num2'])
        print(ans)
        return render(request, 'demo_app/calculate.html', {'answer':ans}) #htmlの表示 {}に入れたものをhtmlに渡す(htmlでは'answer'で扱える)
    else:
        return render(request, 'demo_app/calculate.html', {}) #htmlの表示
    #受け取ったものの演算処理

    #if request.method == 'POST':
    #    form = InputFormCalc(request.POST)
    #    if form.is_valid():
    #        # TODO
    #        return redirect('calculate')

    #else:
    #    form = InputFormCalc()
    #    return render(request, 'demo_app/calculate.html', {})
