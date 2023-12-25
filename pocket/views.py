from django.shortcuts import render, get_object_or_404, redirect

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response


from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.staticfiles import finders

from django.db.models import Sum

from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from django.db.models import Q

from datetime import datetime

from . import models
from . import serializers

from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR,
)


@csrf_exempt
@api_view(["POST", ])
@permission_classes((AllowAny,))
def createTransaction(request):
    # form data
    wallet = request.data['wallet']
    name = request.data['name']
    amount = request.data['amount']
    type = request.data['type']
    date = request.data['date']
    remark = request.data['remark']

    # status
    http_status = HTTP_200_OK
    
    # Check User
    try:
        writer = User.objects.get(id=request.session['_auth_user_id']).username
        # fix value
        if date == "":
            date = datetime.now()
        else :
            date=date.replace('T', ' ')
            
        wallet = models.Wallet.objects.get(id=int(wallet))
        # Create transactions
        try:

            models.Transaction.objects.create(
                wallet=wallet,
                name=name,
                amount=amount,
                type=type,
                date=date,
                remark=remark,
                writer=writer
            )

            http_status = HTTP_201_CREATED

        except IOError as err:
            http_status = HTTP_400_BAD_REQUEST
            print(err)
    except:
        http_status = HTTP_401_UNAUTHORIZED

    return Response(status=http_status)


@csrf_exempt
@api_view(["GET", ])
@permission_classes((AllowAny,))
def readTransaction(request):

    http_status = HTTP_200_OK

    transactionQuery = models.Transaction.objects.all()
    transactionSerializer = serializers.TransactionSerializers(
        transactionQuery, many=True)

    return Response(
        data={
            "transaction": transactionSerializer.data
        },
        status=http_status
    )


@csrf_exempt
@api_view(["POST", ])
@permission_classes((AllowAny,))
def readTransactionId(request):

    http_status = HTTP_200_OK
    id = int(request.data['id'])
    transactionQuery = models.Transaction.objects.filter(
        wallet=id).order_by('-created_at')
    transactionSerializer = serializers.TransactionSerializers(
        transactionQuery, many=True)
    
    expenses = 0
    income = 0
    balance = 0
    
    for item in transactionQuery:
        
        if item.type == 1:
            income += item.amount
        else :
            expenses += item.amount
        
        balance += (item.amount * item.type)

    return Response(
        data={
            "transaction": transactionSerializer.data,
            "amount":{
                "expenses":expenses,
                "income":income,
                "balance":balance
            }
        },
        status=http_status
    )


@csrf_exempt
@api_view(["POST", ])
@permission_classes((AllowAny,))
def createWallet(request):
    http_status = HTTP_200_OK

    name = request.data['name']
    type = int(request.data['type'])
    desc = request.data['desc']

    try:
        models.Wallet.objects.create(
            name=name,
            desc=desc,
            type=type
        )
        http_status = HTTP_201_CREATED
    except:
        http_status = HTTP_400_BAD_REQUEST

    return Response(status=http_status)


@csrf_exempt
@api_view(["GET", ])
@permission_classes((AllowAny,))
def readWallet(request):
    http_status = HTTP_200_OK

    walletQuery = models.Wallet.objects.all()
    walletSerializer = serializers.WalletSerializers(
        walletQuery, many=True)
    
    cash = 0
    bank = 0
    walletData = []

    for item in walletSerializer.data:
        item = dict(item)
        transactionQuery = models.Transaction.objects.filter(
            wallet=int(item['id']))
        transactionSerializer = serializers.TransactionSerializers(
            transactionQuery, many=True).data
        item['transaction'] = transactionSerializer
        amount = 0
        
        for transaction in transactionQuery:
            amount += transaction.amount * transaction.type
            
        if item['type'] == 1:
            cash += amount
        else :
            bank += amount
            
        item['amount'] = amount
        walletData.append(item)

    total = bank + cash
    
    return Response(
        data={
            "wallet": walletData,
            "process":{
                "cash":cash,
                "bank":bank,
                "total":total
            }
        },
        status=http_status
    )


@csrf_exempt
@api_view(["POST",])
@permission_classes((AllowAny,))
def userLogin(request):
    http_status = HTTP_200_OK
    username = request.data['username']
    password = request.data['password']

    user = authenticate(
        username=username,
        password=password
    )

    if user is not None:
        if user.is_active:
            status = True
            msg = 'user is logined'
            login(request, user)
        else:
            status = False
            msg = 'Currently, This user is not active'
            http_status = HTTP_401_UNAUTHORIZED
    else:
        status = False
        msg = 'Error wrong username/password'
        http_status = HTTP_400_BAD_REQUEST

    return Response({'status': status, 'message': msg}, status=http_status)



def userLogout(request):
    logout(request)
    return redirect('index-page')

def indexPage(request):
    return render(request, 'index.html', )

def walletPage(request, id):
    wallet = models.Wallet.objects.get(id=id)
    
    return render(request, 'wallet.html', {"wallet": wallet})

