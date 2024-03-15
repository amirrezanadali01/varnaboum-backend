from django.urls import path
from .views import *


urlpatterns = [

    path('getcategoriesToday/', getCategoriesToday.as_view()),
    path('retryuser/', getInforamationUser.as_view()),
    path('RegisterFirest/', getSubCategory.as_view()),
    path('retryQuestionRequired/<int:id>', getQuestionRequired.as_view()),
    path('UpdateInfoUser/<int:user>', UpdateInfoUser.as_view()),
    path('retryQuestionOptional/<int:id>', getQuestionOptional.as_view()),
    path('registerUser/', RegisterUser.as_view()),
    path('registerShop/', RegisterShop.as_view()),
    path('TestImage/', TestImage.as_view()),
    path('getCity/', GetCity.as_view()),
    path('getBanner/', GetBanner.as_view()),
    path("ItemShop/<int:category>/<int:subcategory>/<int:subtitle>/<int:city>",
         ListItmeShop.as_view()),
    path("ImageShop/<int:id>/", ListImageStroeUser.as_view()),
    path("ImageShopUser/", ListImageStroe.as_view()),
    path("InfoUser/<int:id>/", ListInfoUser.as_view()),
    path("AnswerUser/<int:id>/", ListQuestionAnswerUser.as_view()),
    path("CreateShopImage/", CreateImage.as_view()),
    path("RemoveShopImage/<int:pk>/delete/", RemoveImageShop.as_view()),
    path('AnswerQuestionProfile/', ListAnswerQuestion.as_view()),
    path('UpdateAnswer/<int:pk>/', UpdateAnswerQuestion.as_view()),
    path('SearchInfoUser/', SearchInfoUser.as_view()),
    path('AllItem/<int:id>', GetAllItem.as_view()),
    path('ContectUs/', ContectUs.as_view()),
    path('ShopImageContectUs/', GetImageShopContectUs.as_view()),
    path('CreateVerifyUser/', CreateVerifyCode.as_view()),
    path('CheckVerifyCode/<int:number>/<int:code>/', CheckVerify.as_view()),
    path('CheckVerifyChangePassword/<int:number>/<int:code>/',
         CheckVerifyChangePassword.as_view()),
    path('ChangePasswordView/<str:token>/', ChangePasswordView.as_view()),
    path('retryOffice/', getInfoOfficeUser.as_view()),


    # UPDATE


    path('GetTypeEstate/<str:type>/', GetTypeEstate.as_view()),
    path('GetCitysWithVillage/', getCityWithVillage.as_view()),
    path('CreatePostEstate/', CreatePostEstate.as_view()),
    path('GetProductsEstate/', GetProductsEstate.as_view()),
    path('GetVillage/<int:city>/', GetVillage.as_view()),
    path('GetRetrieveProductsEatate/<int:pk>/',
         GetRetrieveProductsEatate.as_view()),

    path('GetRetrieveImageProductsEatate/<int:products>/',
         GetRetrieveImageProductsEatate.as_view()),

    path('GetProductsEstateProfile/<int:user>/',
         GetProductsEstateProfile.as_view()),

    path('GetProductsAnotherProfile/<int:user>/',
         GetProductsAnotherProfile.as_view()),

    path('CreatePostAnother/', CreatePostAnother.as_view()),

    path('GetProductsAnother/<int:id>/', GetProductsAnother.as_view()),

    path('GetProductsAnotherImage/<int:id>/',
         GetProductsAnotherImage.as_view()),

    path('EstateProductsUpdate/<int:pk>', EstateProductsUpdate.as_view()),
    path('RemoveProductsEstate/<int:pk>/', RemoveProductsEstate.as_view()),
    path('AnotherProductsUpdate/<int:pk>', AnotherProductsUpdate.as_view()),
    path('RemoveProductsAnother/<int:pk>/', RemoveProductsAnother.as_view()),

    # Transportation
    path('GetTypeTransportation/<str:type>/', GetTypeTransportation.as_view()),
    path('GetSubTypeTransportation/<int:type>/',
         GetSubTypeTransportation.as_view()),

    path('CreatePostTransportation/', CreatePostTransportation.as_view()),


    path('GetProductsTransportation/', GetProductsTransportation.as_view()),



    path('GetRetrieveImageProductsTransportation/<int:products>/',
         GetRetrieveImageProductsTransportation.as_view()),

    path('GetProductsTransportationProfile/<int:user>/',
         GetProductsTransportationProfile.as_view()),


    path('TransportationProductsUpdate/<int:pk>',
         TransportationProductsUpdate.as_view()),

    path('RemoveProductsTransportation/<int:pk>/',
         RemoveProductsTransportation.as_view()),

    path('CreateViolation/', CreateViolation.as_view()),
    path('GetCategoryNews/', GetCategoryNews.as_view()),
    path('CreateNews/', CreateNews.as_view()),
    path('ListProfileNews/', ListProfileNews.as_view()),
    path('RemoveNews/<int:pk>/', RemoveNews.as_view()),
    path('TopOffice/<int:city>/', TopOffice.as_view()),
    path('RetryNewsOffice/<int:office>/', RetryNewsOffice.as_view()),
    path('TodayNews/', TodayNews.as_view()),
    path('NewsCategory/', NewsCategory.as_view()),

    path('CreateNewsPeople/', CreateNewsPeople.as_view()),
    path('ProfileNewsPeople/', ProfileNewsPeople.as_view()),
    path('TopPeopleNews/', TopPeopleNews.as_view()),
    path('GetAllPeopleNews/', GetAllPeopleNews.as_view()),


    path('GetAllOffice/<int:city>/', GetAllOffice.as_view()),
    path('OfficeNewsUpdate/<int:pk>/', OfficeNewsUpdate.as_view()),
    path('RegionEstate/<int:city>/', RegionEstate.as_view()),
    path('GetShops/', GetShops.as_view()),
    path('UpdateVersion/', UpdateVersion.as_view()),
    path('GetListPersonalOffice/<int:office>/',
         GetListPersonalOffice.as_view()),
    path('CreateTicket/',  CreateTicket.as_view()),
    path('GetMyTicket/', GetMyTicket.as_view()),
    path('GetMessageTicket/<int:ticket>/', GetMessageTicket.as_view()),
    path('CreateMessage/', CreateMessage.as_view()),
    path('UpdateTicket/<int:pk>/', UpdateTicket.as_view()),
    path('GetTicketOfiice/<int:office>', GetTicketOfiice.as_view()),
    path('GetMessagePublicTicket/<int:ticket>/',
         GetMessagePublicTicket.as_view()),
    path('StatusManagerProduct/', StatusManagerProduct.as_view()),
    path('GetListStoreManager/', GetListStoreManager.as_view()),
    path('UpdateInfoUserManagerStore/<int:user>/',
         UpdateInfoUserManagerStore.as_view()),

    path('RemoveStoreInfouserManager/<int:user>/',
         RemoveStoreInfouserManager.as_view()),

    path('RemoveImageShopManagerStore/<int:user>/',
         RemoveImageShopManagerStore.as_view())

]
