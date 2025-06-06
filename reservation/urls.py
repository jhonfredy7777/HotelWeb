from django.urls import path
from reservation import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name="Home" ),
    path('about_us/', views.about_us, name="About_us" ),
    path('activities/', views.hotel_activities, name="Activities" ),
    path('contact/', views.contact, name="Contact" ),
    path('rooms/', views.rooms_list, name="Rooms" ),
    path('room/<int:number>/', views.room_detail, name="Room_detail" ),
    path('book_room/<int:number>/', views.book_room, name="Book_room" ),
    path('book_room_free/<int:number>/', views.book_room_free, name="Book_room_free" ),
    path('cancel_reservation/<str:code>/', views.cancel_reservation, name="Cancel_reservation" ),






]

urlpatterns= urlpatterns + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT) 