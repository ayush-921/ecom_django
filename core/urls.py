from django.contrib import admin
from django.urls import path, include

# new imports to handle static files
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("store.urls", namespace="store")),
    path("cart/", include("cart.urls", namespace="cart")),
    path("account/", include("account.urls", namespace="account")),
    path("payment/", include("payment.urls", namespace="payment")),
    path("usercart/", include("usercart.urls", namespace="usercart")),
]

# if debug is true we add the static file url to urlpatterns
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
