"""
URL configuration for chirpyStores project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from MAIN.views import add_to_cart, remove_from_cart, update_order_item, save_billing_info
# from django.conf.urls import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("auth/",include("USERS.urls")),
    path("",include("MAIN.urls")),
    path("payment",include("Payment.urls"))

]
urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

htmx_patterns = [
    path("add_to_cart",add_to_cart,name="add_to_cart"),
    path("remove/<int:pk>/",remove_from_cart,name="remove_from_cart"),
    path("update/<int:pk>",update_order_item,name="update_cart"),
    path("add_billing_info",save_billing_info,name="new_billing_info")
    ]

urlpatterns += htmx_patterns