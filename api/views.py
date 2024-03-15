from email import message
import re
from urllib import request
from django.contrib.auth import models
from django.shortcuts import render
from news.models import CategoryNewsModel, TopNewsModel
from office.models import OfficeModel
from django.db.models import Q
from rest_framework.parsers import MultiPartParser
from datetime import datetime
from django.http import HttpResponse
from django.db.models import F
import ast
import datetime
import hashlib
from random import randint
import io
from django.core.files.images import ImageFile
from rest_framework.permissions import AllowAny
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from categories.models import CategoryModel, SubCategoryModel, SubtitleModel, CityModel
from detail.models import Banner
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView, UpdateAPIView, RetrieveAPIView
import random
import string
from rest_framework import filters
from .serializers import *
from infousers.models import InfoUserModel, ManagerStore, QuestionProfileModel, Shop_Image, ContactUsModel, VerifyCodeModel
from django.contrib.auth.models import Permission, User
from rest_framework import status
import jwt
from django.conf import settings
from django.contrib.auth.hashers import make_password

import requests

import json


# Create your views here.

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 15


class StandardResultsSetPaginationMESSAGE(PageNumberPagination):
    page_size = 20


class StandardResultsSetPaginationOFFICE(PageNumberPagination):
    page_size = 30


class getCategoriesToday(APIView):

    permission_classes = [AllowAny]

    def get(self, request):

        endjson = {}

        subbb = []

        categorys = CategoryModel.objects.all().order_by('-top')

        for i in categorys:
            endjson[i.name] = {'id': i.id, 'image': i.icon.url}

            subcategory = SubCategoryModel.objects.filter(category=i)
            subbb = []

            if(len(subcategory) != 0):

                for j in subcategory:

                    subtitle = SubtitleModel.objects.filter(subcategory=j)

                    print(subtitle)
                    print('-------------------------------')

                    subbb.append({'name': j.name, 'id': j.id,
                                 'subtitle': subtitle.values()})

                    endjson[i.name].update({'subtitle': subbb})

            else:
                endjson[i.name].update({'subtitle': []})

        return Response(endjson)


class getInforamationUser(ListAPIView):
    serializer_class = GetInfoUserSerializer  # UPDATE

    def get_queryset(self):

        print('hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh')
        print(self.request.user)

        info = InfoUserModel.objects.get(user=self.request.user)

        return [info]


class getInfoOfficeUser(ListAPIView):
    serializer_class = GetInfoOfficeUserSerializer

    def get_queryset(self):

        office_user = UserOfficeModel.objects.get(user=self.request.user)
        print('hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh')
        print(self.request.user)
        print('hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh')

        return [office_user]


class getSubCategory(APIView):
    def get(self, requst):

        user = User.objects.get(username=self.request.user.username)
        info = InfoUserModel.objects.get(user=user)

        end = {}

        for i in info.category.all():
            print(i)
            sub = SubCategoryModel.objects.filter(category=i)
            if(len(sub) != 0):
                end[i.name] = sub.values()

        print(end)

        return Response([end])


class getQuestionRequired(ListAPIView):

    serializer_class = QuestionSerializer

    def get_queryset(self):
        print('-------------------------------------------------------------------------')
        print(self.kwargs['id'])

        questions = QuestionProfileModel.objects.filter(
            category_id=self.kwargs['id'], is_required=True)
        return questions


class getQuestionOptional(ListAPIView):

    serializer_class = QuestionSerializer

    def get_queryset(self):
        print('-------------------------------------------------------------------------')
        print(self.kwargs['id'])

        questions = QuestionProfileModel.objects.filter(
            category_id=self.kwargs['id'], is_required=False)
        return questions


class RegisterUser(CreateAPIView):
    serializer_class = RegisterUserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):

        # RegisterUserSerializer.save(password=make_password(serializer.data.get("password")))
        user = User.objects.create(
            username=serializer.data.get("username"),
            password=make_password(serializer.data.get("password"))
        )


class RegisterShop(APIView):

    def post(self, request):

        AnswerQuestion = []
        ImageStore = []
        answer_true = []
        ImageStore_true = []

        for i in ast.literal_eval(request.data['AnswerQuestion']):
            AnswerQuestion.append(i)

        infoUser = ast.literal_eval(request.data['InfoUser'])
        print('infoUserinfoUserinfoUserinfoUserinfoUserinfoUser')
        print(infoUser)
        print('infoUserinfoUserinfoUserinfoUserinfoUserinfoUser')

        infoUser['profile'] = request.data['Profile']

        if('Vido' in request.data.keys()):
            infoUser['video'] = request.data['Vido']

        Answer_Question = AnswerQuestion

        payload = jwt.decode(
            jwt=infoUser['user'], key=settings.SECRET_KEY, algorithms=["HS256"])
        User_Pk = payload['user_id']
        infoUser['user'] = str(User_Pk)

        for i in request.data.dict().keys():
            if('ImageStore' in i):
                ImageStore.append(
                    {"imag": request.data.dict()[i], 'user': User_Pk})

        image_stroe = ImageStore

        for i in Answer_Question:
            i['user'] = str(User_Pk)

            serializer_answer_quesion = AnswerQuestionSerializer(data=i)

            if serializer_answer_quesion.is_valid():
                answer_true.append(serializer_answer_quesion)

            else:
                return Response(serializer_answer_quesion.errors, status=status.HTTP_400_BAD_REQUEST)

        for i in image_stroe:
            i['user'] = str(User_Pk)
            serializer_image_store = ImageStoreSerializer(data=i)

            if serializer_image_store.is_valid():
                ImageStore_true.append(serializer_image_store)

            else:
                return Response(serializer_image_store.errors, status=status.HTTP_400_BAD_REQUEST)

        # if(infoUser['subcategory'] == []):
        #     infoUser['subcategory'] = None

        serializer_info_user = InfoUserRegisterSerializer(data=infoUser)

        print('herrreeee')
        print('mmmmmmmmmmmmmmmmmmmm')
        if serializer_info_user.is_valid():
            print('hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh')

            serializer_info_user.save()

            for i in answer_true:
                i.save()

            for i in ImageStore_true:
                i.save()

            return Response(serializer_info_user.data, status=status.HTTP_201_CREATED)
        return Response(serializer_info_user.errors, status=status.HTTP_400_BAD_REQUEST)


class TestImage(CreateAPIView):
    # parser_classes = [MultiPartParser]
    permission_classes = [AllowAny]
    serializer_class = TestImageSerializer


class GetCity(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = CitySerializer
    queryset = CityModel.objects.all()


class GetBanner(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = BannerSerializer
    queryset = Banner.objects.all()


class ListItmeShop(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = InfoUserItemSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):

        print(self.kwargs['city'])

        if(self.kwargs['city'] == 50000):

            if(self.kwargs['subcategory'] == 50000):
                print(
                    'fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff')
                items = InfoUserModel.objects.filter(
                    Confirmation=True, category=self.kwargs['category']).order_by('-top', '?')

            else:

                if(self.kwargs['subtitle'] == 50000):

                    items = InfoUserModel.objects.filter(
                        category=self.kwargs['category'], subcategory=self.kwargs['subcategory'], Confirmation=True).order_by('-top', '?')

                else:
                    items = InfoUserModel.objects.filter(
                        category=self.kwargs['category'], subcategory=self.kwargs['subcategory'], subtitle=self.kwargs['subtitle'], Confirmation=True).order_by('-top', '?')

        else:

            if(self.kwargs['subcategory'] == 50000):
                print(
                    'fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff')
                items = InfoUserModel.objects.filter(
                    city=self.kwargs['city'], Confirmation=True, category=self.kwargs['category']).order_by('-top', '?')

            else:

                if(self.kwargs['subtitle'] == 50000):

                    items = InfoUserModel.objects.filter(
                        category=self.kwargs['category'], subcategory=self.kwargs['subcategory'], city=self.kwargs['city'], Confirmation=True).order_by('-top', '?')

                else:
                    items = InfoUserModel.objects.filter(category=self.kwargs['category'], subcategory=self.kwargs['subcategory'],
                                                         city=self.kwargs['city'], subtitle=self.kwargs['subtitle'], Confirmation=True).order_by('-top', '?')

        return items


class ListImageStroeUser(ListAPIView):
    serializer_class = ImageStoreSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        # user = User.objects.get(id=self.kwargs['id'])
        user = User.objects.get(id=self.kwargs['id'])
        print('nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn')
        print(user.id)
        items = Shop_Image.objects.filter(user=user)
        return items


class ListImageStroe(ListAPIView):
    serializer_class = ImageStoreSerializer

    def get_queryset(self):
        # user = User.objects.get(id=self.kwargs['id'])
        items = Shop_Image.objects.filter(user=self.request.user)
        return items


class ListInfoUser(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = InfoUserSerializer

    def get_queryset(self):
        # user = User.objects.get(id=self.kwargs['id'])
        user = User.objects.get(id=self.kwargs['id'])
        print('nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn')
        print(user.id)
        items = InfoUserModel.objects.filter(user=user)
        return items


class ListQuestionAnswerUser(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = AnswerQuestionInfoUserSerializer

    def get_queryset(self):
        # user = User.objects.get(id=self.kwargs['id'])
        user = User.objects.get(id=self.kwargs['id'])
        print('nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn')
        print(user.id)
        items = AnswerProfileModel.objects.filter(user=user)
        return items


class SearchInfoUser(ListAPIView):

    search_fields = ['name', 'tags']
    pagination_class = StandardResultsSetPagination
    filter_backends = (filters.SearchFilter,)
    queryset = InfoUserModel.objects.filter(
        Confirmation=True).order_by('-top', '?')
    serializer_class = InfoUserSerializer


# UPDATE EDITE

class CreateImage(APIView):
    def post(self, request):
        payload = jwt.decode(
            jwt=request.data['user'], key=settings.SECRET_KEY, algorithms=["HS256"])
        User_Pk = payload['user_id']
        user = User_Pk
        image = request.data['imag']

        print(user)
        print(image)

        serializer_image = ImageStoreSerializer(
            data={'user': user, 'imag': image})

        if serializer_image.is_valid():
            print('hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh')
            serializer_image.save()
            return Response(serializer_image.data, status=status.HTTP_201_CREATED)

        else:
            return Response(serializer_image.errors, status=status.HTTP_400_BAD_REQUEST)


class RemoveImageShop(DestroyAPIView):
    serializer_class = ImageStoreSerializer
    queryset = Shop_Image.objects.all()


class UpdateInfoUser(UpdateAPIView):
    queryset = InfoUserModel.objects.all()
    serializer_class = InfoUserSerializer
    lookup_field = 'user'

    def update(self, request, *args, **kwargs):

        if(request.user.id == self.kwargs['user']):
            instance = self.get_object()

            serializer = self.get_serializer(
                instance, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response({"message": "updated successfully"})

            else:
                return Response({"message": "failed", "details": serializer.errors})

        else:

            return Response({"message": "failed", "details": 'user is false'})


class ListAnswerQuestion(ListAPIView):

    serializer_class = AnswerQuestionInfoUserSerializer

    def get_queryset(self):
        items = AnswerProfileModel.objects.filter(user=self.request.user)
        return items


class UpdateAnswerQuestion(UpdateAPIView):
    queryset = AnswerProfileModel.objects.all()
    serializer_class = AnswerQuestionInfoUpdateSerializer
    lookup_field = 'pk'

    def update(self, request, *args, **kwargs):

        answer = AnswerProfileModel.objects.filter(pk=self.kwargs['pk'])

        if(request.user == answer[0].user):

            instance = self.get_object()

            serializer = self.get_serializer(
                instance, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response({"message": "updated successfully"})

            else:
                return Response({"message": "failed", "details": serializer.errors})

        else:
            return Response({"message": "failed", "details": 'user is false'})


class GetAllItem(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = InfoUserItemSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):

        infousers = InfoUserModel.objects.filter(
            category=self.kwargs['id'], Confirmation=True).order_by('-top', '?')

       # infousers = infousers.order_by('-top')
        return infousers


class ContectUs(ListAPIView):
    serializer_class = ContectUsSerializer

    def get_queryset(self):
        contectus = ContactUsModel.objects.all()
        return contectus


class GetImageShopContectUs(ListAPIView):
    serializer_class = ImageStoreSerializer

    def get_queryset(self):
        # user = User.objects.get(id=self.kwargs['id'])
        user = User.objects.get(username='varnaboom')

        items = Shop_Image.objects.filter(user=user)
        return items


def RandomNDigits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)


def RandomNDigits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)


class CreateVerifyCode(CreateAPIView):

    permission_classes = [AllowAny]

    serializer_class = VerifyCodeSerializer

    def create(self, request, *args, **kwargs):
        # sms

        code = RandomNDigits(5)

        print('heeeeeeeeeeeeeeeeeeeerrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr')

        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.validated_data['code'] = code

            serializer.save()

            # TOKEN

            # url = "https://RestfulSms.com/api/Token"
            # header = {"Content-Type": "application/json"}
            # payload = {"SecretKey": "@mirrez@N",
            #           "UserApiKey": "f8fc9a8fef39e76f2808aba8"}
            # tokenSecret = requests.post(url, headers=header, json=payload)
            # token = tokenSecret.json()['TokenKey']
            
            #test
            
            payload = {
                "mobile": "{0}".format(request.data['number']),
                "templateId": 100000,
                "parameters": [
                  {
                    "name": "Code",
                    "value": str(code)
                  }
                ]
            }
            
            headers = {
                    'Content-Type': 'application/json',
                    'Accept': 'text/plain',
                    'x-api-key': 'fmLL5hGz74UBsPdHfoGvmew6mPmcyGfIqihwoxfNy2c9xwQgv2C96AfYv9QGLjw8'
                  }
                  
            
            sms = requests.post("https://api.sms.ir/v1/send/verify",headers=headers , json=payload)
            
            
            #test
            

            # Send Simple SMS

            # url = "https://RestfulSms.com/api/VerificationCode"
            # header = {"Content-Type": "application/json",
            #           "x-sms-ir-secure-token": token}

            # payload = {
            #     "Code": str(code),
            #     "MobileNumber": "0{0}".format(request.data['number']),

            # }

            # sms = requests.post(url, headers=header, json=payload)

            return Response(data={"message": True}, status=status.HTTP_201_CREATED)

        return Response(data={"message": False}, status=status.HTTP_400_BAD_REQUEST)


# request.data['num']
class CheckVerify(APIView):
    permission_classes = [AllowAny]

    def get(self, request, number, code):

        codeVerify = VerifyCodeModel.objects.filter(number=number).last()

        if(code == codeVerify.code):
            return Response(data={"message": True}, status=status.HTTP_201_CREATED)
        else:
            return Response(data={"message": False}, status=status.HTTP_400_BAD_REQUEST)


# "message": code

class CheckVerifyChangePassword(APIView):
    permission_classes = [AllowAny]

    def get(self, request, number, code):

        codeVerify = VerifyCodeModel.objects.filter(number=number).last()

        if(code == codeVerify.code):

            ss = ''.join(random.sample(string.ascii_lowercase, 20))
            token = hashlib.md5(ss.encode())

            print(token.hexdigest())

            codeVerify.token = token.hexdigest()
            codeVerify.save()

            print('fffffffffffffffffffffffffffffffffff')

            return Response(data={"message": str(token.hexdigest())}, status=status.HTTP_201_CREATED)
        else:
            return Response(data={"message": 'no'}, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(UpdateAPIView):
    permission_classes = [AllowAny]
    """
        An endpoint for changing password.
        """
    serializer_class = ChangePasswordSerializer
    model = User

    def get_object(self, queryset=None):

        token = self.kwargs['token']
        user = VerifyCodeModel.objects.get(token=token)

        user = User.objects.get(username=user.number)

        return user

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            token = self.kwargs['token']
            VerifyCode = VerifyCodeModel.objects.get(token=token)

            if(VerifyCode.valid == 0):

                VerifyCode.valid = 1
                VerifyCode.save()

                # set_password also hashes the password that the user will get
                self.object.set_password(serializer.data.get("new_password"))
                self.object.save()
                response = {
                    'status': 'success',
                    'code': status.HTTP_200_OK,
                    'message': 'Password updated successfully',
                    'data': []
                }

                return Response(data={"message": response}, status=status.HTTP_201_CREATED)

            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# UPDATE

class getCityWithVillage(APIView):

    def get(self, request):

        endjson = {}

        citys = CityModel.objects.all()

        for i in citys:
            endjson[i.name] = {'id': i.id, 'name': i.name}

            retryVillage = VillageModel.objects.filter(city=i)
            villages = []

            if(len(retryVillage) != 0):

                endjson[i.name].update({'village': retryVillage.values()})

            else:
                endjson[i.name].update({'village': []})

        return Response(endjson)


class GetTypeEstate(ListAPIView):
    serializer_class = TypeEstateSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):

        Type_Estate = TypeEstateModel.objects.filter(
            typeestate=self.kwargs['type'])

        return Type_Estate


class CreatePostEstate(APIView):
    def post(self, request):

        image_valie = []

        products = json.loads(request.data['product'])

        payload = jwt.decode(
            jwt=products['infouser'], key=settings.SECRET_KEY, algorithms=["HS256"])
        User_Pk = payload['user_id']

        infouser = InfoUserModel.objects.get(user=User_Pk)
        products['infouser'] = infouser.pk

        products['image'] = request.data['preview']

        for i in request.data.keys():
            if 'images[' in i:
                images = {'image': request.data[i]}
                image_valie.append(images)

        products['imagesPost'] = image_valie

        print(products)

        serializer_products = CreatePostEstateSerializer(data=products)

        if(serializer_products.is_valid()):
            serializer_products.save()
            return Response(status=status.HTTP_201_CREATED)

        else:
            return Response(serializer_products.errors, status=status.HTTP_400_BAD_REQUEST)


class GetVillage(ListAPIView):
    serializer_class = VillageSerializer

    def get_queryset(self):

        # self.kwargs['type']

        villages = VillageModel.objects.filter(city=self.kwargs['city'])

        return villages


class GetProductsEstate(APIView, StandardResultsSetPagination):

    def post(self, request):
        filters = request.data
        a = ProductsEstateModel.objects.filter(
            **filters).order_by('-created', '-time')

        results = self.paginate_queryset(a, request, view=self)
        serializer = GetPostEstateSerializer(results, many=True)
        return self.get_paginated_response(serializer.data)


class GetRetrieveProductsEatate(RetrieveAPIView):

    serializer_class = GetPostEstateSerializer
    queryset = ProductsEstateModel.objects.all().order_by('-created', '-time')


class GetRetrieveImageProductsEatate(ListAPIView):

    serializer_class = GetPostImageEstateSerializer

    def get_queryset(self):

        # self.kwargs['type']

        images = ImageEstateProductsModel.objects.filter(
            products=self.kwargs['products'])

        return images


class GetProductsEstateProfile(ListAPIView):
    serializer_class = GetPostEstateSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):

        products = ProductsEstateModel.objects.filter(
            infouser=self.kwargs['user']).order_by('-created', '-time')

        return products


class CreatePostAnother(APIView):

    def post(self, request):
        image_valie = []

        products = json.loads(request.data['product'])

        payload = jwt.decode(
            jwt=products['infouser'], key=settings.SECRET_KEY, algorithms=["HS256"])

        User_Pk = payload['user_id']

        infouser = InfoUserModel.objects.get(user=User_Pk)
        products['infouser'] = infouser.pk

        products['preview'] = request.data['preview']

        for i in request.data.keys():
            if 'images[' in i:
                images = {'image': request.data[i]}
                image_valie.append(images)

        products['imagesPost'] = image_valie

        serializer_products = CreatePostAnotherSerializer(data=products)

        if(serializer_products.is_valid()):
            serializer_products.save()
            return Response(status=status.HTTP_201_CREATED)

        else:
            print(serializer_products.errors)
            return Response(serializer_products.errors, status=status.HTTP_400_BAD_REQUEST)


class GetProductsAnother(ListAPIView):
    serializer_class = GetProductsAnotherSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        infouser = InfoUserModel.objects.get(user=self.kwargs['id'])

        products = ProductsAnotherModel.objects.filter(
            infouser=infouser).order_by('-created', '-time')
        return products


class GetProductsAnotherImage(ListAPIView):
    serializer_class = GetProductsAnotherImageSerializer

    def get_queryset(self):
        images = ProductsImageAnotherModel.objects.filter(
            products=self.kwargs['id'])
        return images


class RemoveProductsEstate(DestroyAPIView):
    serializer_class = ProductsEstateSerializer
    queryset = ProductsEstateModel.objects.all()


class EstateProductsUpdate(UpdateAPIView):
    queryset = ProductsEstateModel.objects.all()
    serializer_class = ProductsEstateSerializer
    lookup_field = 'pk'

    def update(self, request, *args, **kwargs):
        product = ProductsEstateModel.objects.get(pk=self.kwargs['pk'])
        print(product.infouser.pk)
        infouser = InfoUserModel.objects.get(pk=product.infouser.pk)
        print('fjfjfjfjfjjfjfjfjfjfjjffjfjfjfjj')
        print(infouser.name)
        if(request.user.pk == infouser.user.pk):
            instance = self.get_object()

            serializer = self.get_serializer(
                instance, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response({"message": "updated successfully"})

            else:
                return Response({"message": "failed", "details": serializer.errors})

        else:

            return Response({"message": "failed", "details": 'user is false'})


class GetProductsAnotherProfile(ListAPIView):
    serializer_class = GetProductsAnotherSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):

        products = ProductsAnotherModel.objects.filter(
            infouser=self.kwargs['user']).order_by('-created', '-time')

        return products


class RemoveProductsAnother(DestroyAPIView):
    serializer_class = GetProductsAnotherSerializer
    queryset = ProductsAnotherModel.objects.all()


class AnotherProductsUpdate(UpdateAPIView):
    queryset = ProductsAnotherModel.objects.all()
    serializer_class = GetProductsAnotherSerializer
    permission_classes = [AllowAny]
    lookup_field = 'pk'

    def update(self, request, *args, **kwargs):
        product = ProductsAnotherModel.objects.get(pk=self.kwargs['pk'])
        print(product.infouser.pk)
        infouser = InfoUserModel.objects.get(pk=product.infouser.pk)
        print('fjfjfjfjfjjfjfjfjfjfjjffjfjfjfjj')
        print(infouser.name)
        if(request.user.pk == infouser.user.pk):
            instance = self.get_object()

            serializer = self.get_serializer(
                instance, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response({"message": "updated successfully"})

            else:
                return Response({"message": "failed", "details": serializer.errors})

        else:

            return Response({"message": "failed", "details": 'user is false'})


class GetTypeTransportation(ListAPIView):
    serializer_class = TypeTransportationSerializer

    def get_queryset(self):

        types = TypeTransportationModel.objects.filter(
            TypeTransportation=self.kwargs['type'])

        return types


class GetSubTypeTransportation(ListAPIView):

    serializer_class = SubTypeTransportatioSerializer

    def get_queryset(self):

        types = SubTypeTransportationModel.objects.filter(
            TypeTransportation=self.kwargs['type'])

        return types


class CreatePostTransportation(APIView):

    def post(self, request):
        image_valie = []

        products = json.loads(request.data['product'])

        payload = jwt.decode(
            jwt=products['infouser'], key=settings.SECRET_KEY, algorithms=["HS256"])

        User_Pk = payload['user_id']

        infouser = InfoUserModel.objects.get(user=User_Pk)
        products['infouser'] = infouser.pk

        products['image'] = request.data['preview']

        for i in request.data.keys():
            if 'images[' in i:
                images = {'image': request.data[i]}
                image_valie.append(images)

        products['imagesPost'] = image_valie

        serializer_products = CreatePostTransportatioSerializer(data=products)

        if(serializer_products.is_valid()):
            serializer_products.save()
            return Response(status=status.HTTP_201_CREATED)

        else:

            return Response(serializer_products.errors, status=status.HTTP_400_BAD_REQUEST)


class GetProductsTransportation(APIView, StandardResultsSetPagination):

    def post(self, request):
        filters = request.data
        a = ProductsTransportationModel.objects.filter(
            **filters).order_by('-created', '-time')

        results = self.paginate_queryset(a, request, view=self)
        serializer = GetPostTransportationSerializer(results, many=True)
        return self.get_paginated_response(serializer.data)


class GetRetrieveImageProductsTransportation(ListAPIView):

    serializer_class = GetePostImageTransportatioSerializer

    def get_queryset(self):

        images = ImageTransportationroductsModel.objects.filter(
            products=self.kwargs['products'])

        return images


class GetProductsTransportationProfile(ListAPIView):
    serializer_class = GetPostTransportationSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):

        products = ProductsTransportationModel.objects.filter(
            infouser=self.kwargs['user']).order_by('-created', '-time')

        return products


class TransportationProductsUpdate(UpdateAPIView):
    queryset = ProductsTransportationModel.objects.all()
    serializer_class = GetPostTransportationSerializer
    lookup_field = 'pk'

    def update(self, request, *args, **kwargs):
        product = ProductsTransportationModel.objects.get(pk=self.kwargs['pk'])

        infouser = InfoUserModel.objects.get(pk=product.infouser.pk)

        if(request.user.pk == infouser.user.pk):
            instance = self.get_object()

            serializer = self.get_serializer(
                instance, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                print('bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb')
                return Response({"message": "updated successfully"})

            else:
                print(
                    ',mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm')
                return Response({"message": "failed", "details": serializer.errors})

        else:
            print(',vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv')

            return Response({"message": "failed", "details": 'user is false'})


class RemoveProductsTransportation(DestroyAPIView):
    serializer_class = GetPostTransportationSerializer
    queryset = ProductsTransportationModel.objects.all()


class CreateViolation(CreateAPIView):

    serializer_class = ViolationSerializer

    def create(self, request, *args, **kwargs):

        user = request.user
        print(request.data['infouser'])
        infouser = InfoUserModel.objects.get(user=request.data['infouser'])

        print('datadatadatadatadatadatadatadatadatadatadata')
        request.data._mutable = True

        request.data['user'] = user.pk
        request.data['infouser'] = infouser.pk

        request.data._mutable = False
        print('datadatadatadatadatadatadatadatadatadatadata')
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():

            serializer.save()

            return Response(data={"message": True}, status=status.HTTP_201_CREATED)

        print(serializer.errors)
        return Response(data={"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class GetCategoryNews(ListAPIView):
    serializer_class = GetCategoryNewsSerializer

    def get_queryset(self):

        categorys = CategoryNewsModel.objects.all()

        return categorys


# class CreateViolation(CreateAPIView):

#     serializer_class = ViolationSerializer

#     def create(self, request, *args, **kwargs):

#         user = request.user
#         print(request.data['infouser'])
#         infouser = InfoUserModel.objects.get(user=request.data['infouser'])

#         print('datadatadatadatadatadatadatadatadatadatadata')
#         request.data._mutable = True

#         request.data['user'] = user.pk
#         request.data['infouser'] = infouser.pk

#         request.data._mutable = False
#         print('datadatadatadatadatadatadatadatadatadatadata')
#         serializer = self.get_serializer(data=request.data)

#         if serializer.is_valid():

#             serializer.save()

#             return Response(data={"message": True}, status=status.HTTP_201_CREATED)

#         print(serializer.errors)
#         return Response(data={"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class CreateNews(CreateAPIView):
    serializer_class = CreateNewsSerializer

    def create(self, request, *args, **kwargs):

        user = UserOfficeModel.objects.get(user=request.user)

        city = user.office.city

        request.data['user'] = user.pk
        request.data['office'] = user.office.pk
        request.data['city'] = city.pk
        serializer = self.get_serializer(data=request.data)
        print('newsnewsnewsnewsnewsnewsnewsnewsnewsnewsnewsnewsnewsnewsnewsnews')
        if serializer.is_valid():
            serializer.save()
            return Response(data={"message": True}, status=status.HTTP_201_CREATED)

        else:
            print(serializer.errors)
            return Response(data={"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class ListProfileNews(ListAPIView):
    serializer_class = ListProfileNewsSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        user = UserOfficeModel.objects.get(user=self.request.user)
        print('hhhhhhhhh')
        office = user.office.pk
        newses = NewsModel.objects.filter(office=office).order_by('-date_time')

        return newses


class RemoveNews(DestroyAPIView):
    serializer_class = RemoveNewsSerializer
    queryset = NewsModel.objects.all()


class TopOffice(ListAPIView):

    serializer_class = TopOfficeSerializer

    def get_queryset(self):
        offices = OfficeModel.objects.filter(
            ~Q(top=0), city=self.kwargs['city']).order_by('-top')
        return offices


class RetryNewsOffice(ListAPIView):
    serializer_class = NewsesOfficeSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        newses = NewsModel.objects.filter(
            office=self.kwargs['office']).order_by('-date_time')
        return newses

# UPPPPPPPPPPPPPPPDDDDDDDDDDDAAAAAAAAAAAAAATTTTTTTTTTT


class TodayNews(APIView):

    serializer_class = NewsesOfficeSerializer

    def get(self, request):
        # TOP
        count_item = 6
        offices = TopNewsModel.objects.all()

        if len(offices) == 1:
            count = count_item
        elif len(offices) > count_item:
            count = count_item
        else:
            count = count_item // len(offices)

        items = []
        for i in offices:
            my_news = NewsModel.objects.filter(
                office=i.pk).order_by('-date_time').values(CityName=F('city__name'), CategoryName=F('category__name'), category__id=F('category__id'), UserOfiice=F('office__name')).values()[:count]

            # my_news['CategoryName'] = my_news.pop('category__name')
            # my_news['CityName'] = my_news.pop('city__name')
            # my_news['UserOfiice'] = my_news.pop('office__name')
            items.append(my_news)

        items = [x for l in items for x in l]

        # CATEGORY
        category_news = {}
        categorys = CategoryNewsModel.objects.all()
        for i in categorys:
            category_news[i.name] = NewsModel.objects.filter(
                category=i.id).order_by('date_time').values(CityName=F('city__name'), CategoryName=F('category__name'), category__id=F('category__id'), UserOfiice=F('office__name')).values()[:4]

        print(i)
        return Response({'top': items, 'category': category_news})


# class NewsCategory(ListAPIView):
#     serializer_class = NewsesOfficeSerializer
#     pagination_class = StandardResultsSetPagination

#     def get_queryset(self):
#         newses = NewsModel.objects.filter(
#             category=self.kwargs['id'])
#         return newses


class CreateNewsPeople(CreateAPIView):
    serializer_class = NewsPeopleSerializer

    def create(self, request, *args, **kwargs):

        request.data['user'] = request.user.pk
        serializer = self.get_serializer(data=request.data)

        print('newsnewsnewsnewsnewsnewsnewsnewsnewsnewsnewsnewsnewsnewsnewsnews')
        if serializer.is_valid():
            serializer.save()
            return Response(data={"message": True}, status=status.HTTP_201_CREATED)

        else:
            print(serializer.errors)
            return Response(data={"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class ProfileNewsPeople(ListAPIView):
    serializer_class = NewsPeopleRetrySerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        newses = NewsPeopleModel.objects.filter(
            user=self.request.user)
        return newses


class TopPeopleNews(ListAPIView):
    #serializer_class = NewsPeopleSerializer
    # UPPPPPPPPPPPPPPPDDDDDDDDDDDAAAAAAAAAAAAAATTTTTTTTTTT
    serializer_class = NewsPeopleRetrySerializer

    def get_queryset(self):
        newses = NewsPeopleModel.objects.filter(
            submit=True).order_by('-date_time')[:5]
        return newses


class GetAllPeopleNews(ListAPIView):
    serializer_class = NewsPeopleRetrySerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        newses = NewsPeopleModel.objects.filter(
            submit=True).order_by('-date_time')
        return newses


# class GetAllPeopleNews(ListAPIView):
#     serializer_class = NewsPeopleRetrySerializer
#     pagination_class = StandardResultsSetPagination

#     # UPDDDDDDDDDDDDDDAAAAAAAAAAAAUPDDDDDDDDDDDDDDAAAAAAAAAAAAUPDDDDDDDDDDDDDDAAAAAAAAAAAAUPDDDDDDDDDDDDDDAAAAAAAAAAAAUPDDDDDDDDDDDDDDAAAAAAAAAAAAUPDDDDDDDDDDDDDDAAAAAAAAAAAAUPDDDDDDDDDDDDDDAAAAAAAAAAAA

#     def get_queryset(self):
#         newses = NewsPeopleModel.objects.filter(
#             submit=True).order_by('-date_time')
#         return newses


class GetAllOffice(ListAPIView):
    serializer_class = TopOfficeSerializer
    pagination_class = StandardResultsSetPaginationOFFICE

    def get_queryset(self):
        offices = OfficeModel.objects.filter(city=self.kwargs['city'])
        return offices


class OfficeNewsUpdate(UpdateAPIView):
    queryset = NewsModel.objects.all()
    serializer_class = NewsesOfficeUpdateSerializer
    lookup_field = 'pk'

    def update(self, request, *args, **kwargs):

        news = NewsModel.objects.get(id=self.kwargs['pk'])

        user = news.user.user.id

        if(request.user.id == user):
            instance = self.get_object()

            serializer = self.get_serializer(
                instance, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response({"message": "updated successfully"})

            else:
                return Response({"message": "failed", "details": serializer.errors})

        else:

            return Response({"message": "failed", "details": 'user is false'})


class RegionEstate(ListAPIView):
    serializer_class = RegionEstateSerializer

    def get_queryset(self):
        regions = RegionCityModel.objects.filter(city=self.kwargs['city'])
        return regions


class GetShops(APIView, StandardResultsSetPagination):

    def post(self, request):
        filters = request.data

        a = InfoUserModel.objects.filter(
            **filters).order_by('-top', '?')
        results = self.paginate_queryset(a, request, view=self)
        serializer = InfoUserRegisterSerializer(results, many=True)
        return self.get_paginated_response(serializer.data)


class NewsCategory(APIView, StandardResultsSetPagination):

    def post(self, request):
        filters = request.data

        a = NewsModel.objects.filter(
            **filters)
        results = self.paginate_queryset(a, request, view=self)
        serializer = NewsesOfficeSerializer(results, many=True)
        return self.get_paginated_response(serializer.data)


class UpdateVersion(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = UpdateVersionSerializer

    def get_queryset(self):
        version = UpdateVersionModel.objects.last()
        return [version]


class GetListPersonalOffice(ListAPIView):

    serializer_class = GetListPersonalOfficeSerializer

    def get_queryset(self):
        users = UserOfficeModel.objects.filter(office=self.kwargs['office'])
        return users


class CreateTicket(APIView):
    def post(self, request):

        message = json.loads(request.data['message'])
        ticket = json.loads(request.data['ticket'])

        user = request.user.pk
        ticket['creator'] = user

        message['sender'] = user

        if('image' in request.data):
            message['image'] = request.data['image']

        ticket['message'] = message

        if('video' in request.data):
            message['video'] = request.data['video']

        print('seririririririririririririirir')
        serializer_products = CreateTicketSerializer(data=ticket)

        if(serializer_products.is_valid()):
            serializer_products.save()
            return Response(status=status.HTTP_201_CREATED)

        else:
            print(serializer_products.errors)
            return Response(serializer_products.errors, status=status.HTTP_400_BAD_REQUEST)


class GetMyTicket(APIView, StandardResultsSetPagination):

    def post(self, request):
        print('heeeerrrreeeeeeeeeheeeerrrreeeeeeeeeheeeerrrreeeeeeeeeheeeerrrreeeeeeeeeheeeerrrreeeeeeeeeheeeerrrreeeeeeeeeheeeerrrreeeeeeeeeheeeerrrreeeeeeeeeheeeerrrreeeeeeeee')

        filters = json.loads(request.data['filter'])

        if('creator' in filters):

            payload = jwt.decode(
                jwt=filters['creator'], key=settings.SECRET_KEY, algorithms=["HS256"])
            User_Pk = payload['user_id']

            print('affffffaffffffaffffffaffffffaffffffaffffffaffffffaffffffaffffffaffffffaffffffaffffffaffffffaffffffaffffffaffffffaffffffaffffff')
            print(User_Pk)
            filters['creator'] = User_Pk

        if('office' in filters):

            userOffice = UserOfficeModel.objects.get(user=request.user)
            filters['office'] = userOffice.office.pk

            if(filters['typeask'] == 'complaint'):
                filters['personal'] = userOffice.pk

        tickets = TicketModel.objects.filter(
            **filters).order_by('-date')

        results = self.paginate_queryset(tickets, request, view=self)
        serializer = MyTicketSerializer(
            results, many=True, context={'user': request.user.pk})
        return self.get_paginated_response(serializer.data)


class GetMessageTicket(ListAPIView):
    serializer_class = MessageTicketSerializer
    pagination_class = StandardResultsSetPaginationMESSAGE

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"user": self.request.user.pk})
        return context

    def get_queryset(self):
        messages = MessageTicketModel.objects.filter(
            ticket=self.kwargs['ticket']).order_by('-date')
        return messages


class CreateMessage(CreateAPIView):
    serializer_class = MessageSerializer

    def create(self, request, *args, **kwargs):
        request.data._mutable = True
        request.data['sender'] = request.user.pk
        request.data._mutable = False
        serializer = self.get_serializer(data=request.data)

        print('heeeeeeeeeerrrrrrreeeeee')

        if serializer.is_valid():
            serializer.save()
            return Response(data={"message": True}, status=status.HTTP_201_CREATED)

        else:
            print(serializer.errors)
            return Response(data={"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class UpdateTicket(UpdateAPIView):
    queryset = TicketModel.objects.all()
    serializer_class = TicketSerializer

    def update(self, request, *args, **kwargs):

        creator = TicketModel.objects.get(id=self.kwargs['pk']).creator

        if(request.user.id == creator.id):
            instance = self.get_object()

            serializer = self.get_serializer(
                instance, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response({"message": "updated successfully"})

            else:
                return Response({"message": "failed", "details": serializer.errors})

        else:

            return Response({"message": "failed", "details": 'user is false'})


class GetTicketOfiice(ListAPIView):
    serializer_class = TicketSerializer

    pagination_class = StandardResultsSetPagination

    def get_queryset(self):

        tickets = TicketModel.objects.filter(
            office=self.kwargs['office'], typeask='criticism', isfinish=True)

        return tickets


class GetMessagePublicTicket(ListAPIView):
    serializer_class = GetMessagePublicTicketSerializer
    pagination_class = StandardResultsSetPaginationMESSAGE

    def get_queryset(self):
        messages = MessageTicketModel.objects.filter(
            ticket=self.kwargs['ticket']).order_by('-date')
        return messages


#########################UPDATE########################################

class StatusManagerProduct(APIView):
    def get(self, request):

        print(self.request.user)

        user = ManagerStore.objects.filter(user=self.request.user.id)

        print('NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN')
        print(list(user) == [])

        if(list(user) == []):

            return Response({'status': False})

        else:
            return Response({'status': True})


class GetListStoreManager(ListAPIView):
    serializer_class = InfoUserSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):

        categorys = ManagerStore.objects.filter(user=self.request.user)

        storeis = InfoUserModel.objects.filter(
            category__in=categorys[0].category.all(), Confirmation=False)

        return storeis


class UpdateInfoUserManagerStore(UpdateAPIView):
    queryset = InfoUserModel.objects.all()
    serializer_class = DestryoInfoUserSerializer
    lookup_field = 'user'

    def update(self, request, *args, **kwargs):
        print('upddddaaatttttteupddddaaatttttteupddddaaatttttteupddddaaatttttteupddddaaatttttteupddddaaatttttteupddddaaatttttteupddddaaatttttte')
        myuser = ManagerStore.objects.filter(user=self.request.user)
        print(myuser)
        if(list(myuser) != []):
            instance = self.get_object()

            serializer = self.get_serializer(
                instance, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response({"message": "updated successfully"})

            else:
                return Response({"message": "failed", "details": serializer.errors})

        else:

            return Response({"message": "failed", "details": 'user is false'})


class RemoveStoreInfouserManager(DestroyAPIView):
    serializer_class = DestryoInfoUserSerializer
    lookup_field = 'user'
    queryset = InfoUserModel.objects.all()

    def destroy(self, request, *args, **kwargs):
        print("destroydestroydestroydestroydestroydestroydestroydestroydestroydestroydestroydestroydestroydestroydestroydestroydestroydestroydestroydestroydestroy")

        instance = self.get_object()
        myuser = ManagerStore.objects.filter(user=self.request.user)
        if(list(myuser) == []):
            return Response("you dont have permission", status=status.HTTP_403_FORBIDDEN)
        else:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)


class RemoveImageShopManagerStore(DestroyAPIView):
    serializer_class = ImageStoreSerializer
    queryset = Shop_Image.objects.all()
    lookup_field = 'user'

    def destroy(self, request, *args, **kwargs):
        print("Shop_ImageShop_ImageShop_ImageShop_ImageShop_ImageShop_ImageShop_ImageShop_ImageShop_ImageShop_ImageShop_ImageShop_ImageShop_ImageShop_ImageShop_ImageShop_ImageShop_ImageShop_ImageShop_ImageShop_ImageShop_ImageShop_ImageShop_ImageShop_ImageShop_ImageShop_ImageShop_ImageShop_ImageShop_ImageShop_ImageShop_ImageShop_ImageShop_ImageShop_ImageShop_ImageShop_ImageShop_Image")

        #instance = self.get_object()
        myuser = ManagerStore.objects.filter(user=self.request.user)
        if(list(myuser) == []):
            return Response("you dont have permission", status=status.HTTP_403_FORBIDDEN)

        else:
            images = Shop_Image.objects.filter(user=self.kwargs['user'])
            for i in images:
                self.perform_destroy(i)
            return Response(status=status.HTTP_204_NO_CONTENT)
