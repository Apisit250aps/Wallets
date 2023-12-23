from django.shortcuts import render, get_object_or_404

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.staticfiles import finders

from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from django.db.models import Q

from datetime import datetime

from . import models

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