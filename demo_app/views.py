from django.shortcuts import render, redirect
from .forms import InputForm
from .models import Customers
from sklearn.externals import joblib #モデルの保存と読み込み(ない場合はmyenvでpip installする)
import numpy as np
from django.contrib.auth.decorators import login_required #ログイン認証

# global変数として読んでおく(アプリ起動時にだけ読み込まれるようにする，関数呼び出し毎に読み込まない)
loaded_model = joblib.load('demo_app/demo_model.pkl')
#loaded_model = joblib.load('/home/chezyn/chezyn.pythonanywhere.com/demo_app/demo_model.pkl')

@login_required
def index(request):
    return render(request, 'demo_app/index.html', {})

@login_required
def input_form(request):
    if request.method == 'POST':
        form = InputForm(request.POST)
        if form.is_valid(): #入力の検証
            form.save() #入力された値の保存
            return redirect('result') #フォーム送信のあとはリダイレクト

    else:
        form = InputForm()
        return render(request, 'demo_app/input_form.html', {'form':form})

@login_required
def result(request):
    # DBから最新データを読み込み
    _data = Customers.objects.order_by('id').reverse().values_list('limit_balance', 'sex', 'education', 'marriage', 'age', 'pay_0', 'pay_2', 'pay_3', 'pay_4', 'pay_5', 'pay_6', 'bill_amt_1', 'pay_amt_1', 'pay_amt_2', 'pay_amt_3', 'pay_amt_4', 'pay_amt_5', 'pay_amt_6') #id基準で順序並び替え(一番古いデータが上にあるので反転)
    # values_list()でNumpyリスト形式へ変更
    x = np.array(_data[0])
    ##print(x)
    ##print(type(x))

    # 予測
    y = loaded_model.predict([x]) #行列形式にする!!
    y_proba = loaded_model.predict_proba([x])

    ##print(y)
    ##print(y_proba)

    if y[0] == 0:
        if y_proba[0][y[0]] >= 0.75:
            comment = "悪いことは言わない．やめておきましょう"
        else:
            comment = "まあ，やめておいた方がいいかな"
    else:
        if y_proba[0][y[0]] >= 0.75:
            comment = "じゃんじゃん貸しましょう!!"
        else:
            comment = "まあ，貸してもいいかな"

    # 審査結果のDBへの保存
    customer = Customers.objects.order_by('id').reverse()[0]
    customer.result = y[0] # cutomer.result: カラム名
    customer.proba = round(y_proba[0][y[0]], 2)*100
    customer.comment = comment
    customer.save()

    return render(request, 'demo_app/result.html', {'y':y[0], 'y_proba':round(y_proba[0][y[0]], 2)*100, 'comment':comment})

@login_required
def history(request):
    if request.method == 'POST':
        # 顧客データの削除
        d_id = request.POST #{{d_id}}で送られてきた値
        #print(d_id)
        d_customer = Customers.objects.filter(id=d_id['d_id'])
        #print(d_customer)
        d_customer.delete()

        # 再表示
        customers = Customers.objects.all()
        return render(request, 'demo_app/history.html', {'customers':customers})

    # 顧客一覧の取得
    customers = Customers.objects.all()
    return render(request, 'demo_app/history.html', {'customers':customers})
