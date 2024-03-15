from email import message
from pyexpat import model
import re
from django.db import models
from news.models import CategoryNewsModel, NewsModel, NewsPeopleModel
from office.models import OfficeModel, UserOfficeModel
from rest_framework import fields, serializers
from rest_framework.fields import CurrentUserDefault
from estate.models import ProductsEstateModel, ImageEstateProductsModel
from infousers.models import InfoUserModel, ProductsAnotherModel, ProductsImageAnotherModel, QuestionProfileModel, AnswerProfileModel, Shop_Image, CityModel, ContactUsModel, VerifyCodeModel
from estate.models import TypeEstateModel
from categories.models import CategoryModel, RegionCityModel, SubCategoryModel, VillageModel
from detail.models import Banner, UpdateVersionModel
from ticket.models import MessageTicketModel, TicketModel
from violation.models import ViolationModel
from django.contrib.auth.models import User

from transportation.models import ImageTransportationroductsModel, ProductsTransportationModel, SubTypeTransportationModel, TypeTransportationModel


class VerifyCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VerifyCodeModel
        fields = '__all__'


class InfoUserSerializer(serializers.ModelSerializer):
    CategoryName = serializers.CharField(source='category.name')
    # CategoryProducts = serializers.CharField(source='category.isProducts')

    class Meta:
        model = InfoUserModel
        fields = '__all__'


class InfoUserRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = InfoUserModel
        fields = '__all__'


class ContectUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUsModel
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionProfileModel
        fields = '__all__'


class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']


class TestImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop_Image
        fields = '__all__'


class AnswerQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerProfileModel
        fields = '__all__'


class ImageStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop_Image
        fields = '__all__'


class DestryoInfoUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = InfoUserModel
        fields = '__all__'


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = CityModel
        fields = '__all__'


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = '__all__'


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategoryModel
        fields = '__all__'


class InfoUserItemSerializer(serializers.ModelSerializer):
    subcategory = SubCategorySerializer(read_only=True, many=True)

    class Meta:
        model = InfoUserModel
        fields = '__all__'


class AnswerQuestionInfoUserSerializer(serializers.ModelSerializer):
    questions = serializers.CharField(source='question.question')

    class Meta:
        model = AnswerProfileModel
        fields = '__all__'


class AnswerQuestionInfoUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerProfileModel
        fields = '__all__'


class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """

    new_password = serializers.CharField(required=True)


# UPDATE


class VillageSerializer(serializers.ModelSerializer):
    class Meta:
        model = VillageModel
        fields = '__all__'


class GetInfoUserSerializer(serializers.ModelSerializer):
    CategoryName = serializers.CharField(source='category.name')
    CategoryProducts = serializers.CharField(source='category.isProducts')
    CtegoryPrice = serializers.CharField(source='category.isPrice')

    class Meta:
        model = InfoUserModel
        fields = '__all__'


class TypeEstateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeEstateModel
        fields = '__all__'


class GetInfoOfficeUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserOfficeModel
        fields = '__all__'


class GetCategoryNewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryNewsModel
        fields = '__all__'


class CreatePostImageEstateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageEstateProductsModel
        fields = ['image']


class CreatePostEstateSerializer(serializers.ModelSerializer):
    imagesPost = CreatePostImageEstateSerializer(many=True)

    class Meta:
        model = ProductsEstateModel
        fields = ['name', 'city', 'village', 'price', 'rent', 'mortgage', 'infouser', 'image', 'description', 'region',
                  'year', 'address', 'BuildingArea', 'LanArea', 'parking', 'warehouse', 'balcony', 'room', 'TypeEstate', 'imagesPost']

    def create(self, validated_data):
        imagesPost = validated_data.pop('imagesPost')
        products = ProductsEstateModel.objects.create(**validated_data)
        for i in imagesPost:
            ImageEstateProductsModel.objects.create(products=products, **i)
        return products


class CreatePostImageAnotherSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductsImageAnotherModel
        fields = ['image']


class CreatePostAnotherSerializer(serializers.ModelSerializer):
    imagesPost = CreatePostImageAnotherSerializer(many=True)

    class Meta:
        model = ProductsAnotherModel
        fields = ['imagesPost', 'name', 'preview',
                  'description', 'infouser', 'price']

    def create(self, validated_data):
        imagesPost = validated_data.pop('imagesPost')
        products = ProductsAnotherModel.objects.create(**validated_data)
        for i in imagesPost:
            ProductsImageAnotherModel.objects.create(products=products, **i)
        return products


class GetPostEstateSerializer(serializers.ModelSerializer):
    CityName = serializers.CharField(source='city.name')
    User = serializers.CharField(source='infouser.user.pk')
    NameUser = serializers.CharField(source='infouser.name')

    class Meta:
        model = ProductsEstateModel
        fields = '__all__'


class GetPostImageEstateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageEstateProductsModel
        fields = '__all__'


class GetProductsAnotherSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductsAnotherModel
        fields = '__all__'


class GetProductsAnotherImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductsImageAnotherModel
        fields = '__all__'


class ProductsEstateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductsEstateModel
        fields = '__all__'


# Transportation
class TypeTransportationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeTransportationModel
        fields = '__all__'


class SubTypeTransportatioSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTypeTransportationModel
        fields = '__all__'


class CreatePostImageTransportatioSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageTransportationroductsModel
        fields = ['image']


class CreatePostTransportatioSerializer(serializers.ModelSerializer):
    imagesPost = CreatePostImageTransportatioSerializer(many=True)

    class Meta:
        model = ProductsTransportationModel
        fields = ['infouser', 'image', 'name', 'imagesPost',
                  'TypeTransportation', 'SubTypeTransportation', 'used', 'price', 'description']

    def create(self, validated_data):
        imagesPost = validated_data.pop('imagesPost')
        products = ProductsTransportationModel.objects.create(**validated_data)
        for i in imagesPost:
            ImageTransportationroductsModel.objects.create(
                products=products, **i)
        return products


class GetPostTransportationSerializer(serializers.ModelSerializer):
    User = serializers.CharField(source='infouser.user.pk')
    NameUser = serializers.CharField(source='infouser.name')

    class Meta:
        model = ProductsTransportationModel
        fields = '__all__'


class GetePostImageTransportatioSerializer(serializers.ModelSerializer):

    class Meta:
        model = ImageTransportationroductsModel
        fields = '__all__'


class ViolationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ViolationModel
        fields = '__all__'


class CreateNewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsModel
        fields = '__all__'


class NewsPeopleSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsPeopleModel
        fields = '__all__'


class ListProfileNewsSerializer(serializers.ModelSerializer):
    UserOfiice = serializers.CharField(source='user.name')

    class Meta:
        model = NewsModel
        fields = '__all__'


class RemoveNewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsModel
        fields = '__all__'


class TopOfficeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfficeModel
        fields = '__all__'


class NewsesOfficeSerializer(serializers.ModelSerializer):
    UserOfiice = serializers.CharField(source='office.name')
    CityName = serializers.CharField(source='city.name')
    CategoryName = serializers.CharField(source='category.name')

    class Meta:
        model = NewsModel
        fields = '__all__'


class NewsPeopleRetrySerializer(serializers.ModelSerializer):
    CityName = serializers.CharField(source='city.name')

    class Meta:
        model = NewsPeopleModel
        fields = '__all__'


class NewsesOfficeUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsModel
        fields = '__all__'


class RegionEstateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegionCityModel
        fields = '__all__'


class UpdateVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UpdateVersionModel
        fields = '__all__'


class GetListPersonalOfficeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserOfficeModel
        fields = '__all__'


class CreateMessageTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageTicketModel
        fields = ['text', 'image', 'video', 'sender']


class CreateTicketSerializer(serializers.ModelSerializer):
    message = CreateMessageTicketSerializer()

    class Meta:
        model = TicketModel
        fields = [
            'name',
            'creator',
            'typeask',
            'personal',
            'message',
            'office'
        ]

    def create(self, validated_data):
        print('heheehehehheheheehheehheehhe')
        message = validated_data.pop('message')

        ticket = TicketModel.objects.create(**validated_data)

        MessageTicketModel.objects.create(
            ticket=ticket, **message)

        return ticket


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageTicketModel
        fields = '__all__'


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketModel
        fields = '__all__'


class MyTicketSerializer(serializers.ModelSerializer):
    officeName = serializers.CharField(source='office.name')
    officeCity = serializers.CharField(source='office.city')
    message = serializers.SerializerMethodField()
    personalOffice = serializers.SerializerMethodField()

    class Meta:
        model = TicketModel
        fields = '__all__'

    def get_message(self, obj):

        message = MessageTicketModel.objects.filter(ticket=obj).last()

        return message.sender.pk == self.context['user']

    def get_personalOffice(self, obj):
        if(obj.personal == None):
            return obj.personal
        else:
            return obj.personal.name


class MessageTicketSerializer(serializers.ModelSerializer):
    isMe = serializers.SerializerMethodField()

    class Meta:
        model = MessageTicketModel
        fields = '__all__'

    def get_isMe(self, obj):
        return obj.sender.pk == self.context['user']


class GetMessagePublicTicketSerializer(serializers.ModelSerializer):
    isMe = serializers.SerializerMethodField()

    class Meta:
        model = MessageTicketModel
        fields = '__all__'

    def get_isMe(self, obj):
        return obj.sender.pk == obj.ticket.creator.pk
