from django.urls import path
from .views import *

urlpatterns = [
    path('', IndexView.as_view(), name="index"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),

    # person urls

    path('persons/create/', PersonCreateView.as_view(), name="create-person"),
    path('persons/list/', PersonListView.as_view(), name="list-person"),
    path('persons/<int:pk>/update/',
         PersonUpdateView.as_view(), name="update-person"),
    path('persons/<int:pk>/delete/',
         PersonDeleteView.as_view(), name="delete-person"),

    # menu Item urls


    path('menus/create/', MenuCreateView.as_view(), name="create-menu"),
    path('menus/list/', MenuListView.as_view(), name="list-menu"),
    path('menus/<int:pk>/update/',
         MenuUpdateView.as_view(), name="update-menu"),
    path('menus/<int:pk>/delete/',
         MenuDeleteView.as_view(), name="delete-menu"),

    # create order
    path('orders/create/<int:id>/', OrderCreateView.as_view(), name="create-order"),
    path('orders/create/', OrderCreateView.as_view(), name="create-order-post"),
    path('orders/list/', OrderListView.as_view(), name="list-order"),
    path('orders/<int:pk>/update/',
         OrderUpdateView.as_view(), name="update-order"),
    path('orders/<int:pk>/delete/',
         OrderDeleteView.as_view(), name="delete-order"),
    path('orders/<int:pk>/cancel/',
         OrderCancelView.as_view(), name="cancel-order"),

]
