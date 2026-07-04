from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("test123/", include("favorites.urls")),
    path("admin/", admin.site.urls),

    path("", include("accounts.urls")),

    path("products/", include("products.urls")),

    path("cart/", include("cart.urls")),

    path("orders/", include("orders.urls")),

    path("favorites/", include("favorites.urls")),

    path("reviews/", include("reviews.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)