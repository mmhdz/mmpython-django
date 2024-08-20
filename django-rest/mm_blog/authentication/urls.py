from django.urls import path
from .views import SingUpView, SingInView


app_name = "authentication"


urlpatterns = [
    path("/signup", SingUpView.as_view()),
    path("/singin", SingInView.as_view()),


]