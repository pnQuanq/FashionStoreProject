from django.urls import path
from accounts.views import login_page,register_page , add_to_cart, cart, remove_cart, remove_coupon, editProfile, profile


urlpatterns = [
   path('login/' , login_page , name="login" ),
   path('register/' , register_page , name="register"),
   path('editProfile/' , editProfile , name="editProfile"),
   path('profile/' , profile , name="profile"),
   path('cart/' , cart , name="cart"),
   path('add-to-cart/<uid>/' , add_to_cart, name="add_to_cart"),
   path('remove-cart/<cart_item_uid>/' , remove_cart, name="remove_cart"),
   path('remove-coupon/<cart_id>/' , remove_coupon , name="remove_coupon"),
]