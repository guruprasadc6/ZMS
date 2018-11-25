from django.urls import path
from django.conf.urls import url
from . import views
urlpatterns = [
    path('',views.home,name = "home"),
    path('login/',views.login_user,name = "login"),
    path('logout/',views.logout_user,name ="logout"),
    path('change_password/',views.change_password,name = 'change_password'),

    path('add_department',views.add_department,name='add_department'),
    path('add_exhibit',views.add_exhibit,name='add_exhibit'),
    path('add_animal',views.add_animal,name='add_animal'),
    # path('add_staff',views.add_staff,name = 'add_staff'),

    path('add_staff',views.register,name = 'add_staff'),

    path('view_animals',views.view_animals, name = 'view_animals'),
    path('department_list/',views.deptList,name='department_list'),
    path(r'^profile/(?P<id>[0-9]+)/$',views.department_profile,name='department_profile'),
    path('sidebar/',views.sidebar,name = 'sidebar'),
    path('test/',views.test,name = 'test'),
    path(r'^delete/(?P<id>[0-9]+)/$',views.delete,name = 'delete'),
    path(r'^edit_department/(?P<id>[0-9]+)/$', views.edit_department, name='edit_department'),
    path(r'^delete_animal/(?P<id>[0-9]+)/$',views.animal_delete,name = 'animal_delete'),
    path(r'^edit_animal/(?P<id>[0-9]+)/$', views.edit_animal, name='edit_animal'),
    path(r'^animal_profile/(?P<id>[0-9]+)/$',views.animal_profile,name='animal_profile'),
    path(r'^delete_staff/(?P<id>[0-9]+)/$',views.staff_delete,name = 'staff_delete'),
    path(r'^edit_staff/(?P<id>[0-9]+)/$', views.edit_staff, name='edit_staff'),
    path(r'^staff_profile/(?P<id>[0-9]+)/$',views.staff_profile,name='stafff_profile'),
    path('staff_list/',views.view_staff,name='staff_list'),
    path(r'^delete_exhibit/(?P<id>[0-9]+)/$',views.exhibit_delete,name = 'exhibit_delete'),
    path(r'^edit_exhibit/(?P<id>[0-9]+)/$', views.edit_exhibit, name='edit_exhibit'),
    path(r'^exhibit_profile/(?P<id>[0-9]+)/$',views.exhibit_profile,name='exhibit_profile'),
    path('exhibit_list/',views.view_exhibit,name='exhibit_list'),

    #path('search_department/',views.search_department,name = 'search_department'),



    path('bookTickets/', views.book_ticket, name='bookTickets'),
    path('ticketBill/',views.ticket_bill, name = 'ticketBill'),

    path('feedback/',views.feedback,name = 'feedback'),
    path('addFeedback/',views.add_Feedback, name='addFeedback' ),

    path('lives_in/',views.lives_in, name='lives_in'),

    path('pie_chart/',views.pie_chart, name='pie_chart'),

    path('works_in/',views.works_in, name='works_in'),

    path('manages/',views.manages, name='manages'),

    path('looks_after/',views.looks_after, name='looks_after'),

    path('list_lives_in/', views.view_lives_in, name='list_lives_in'),

    path(r'^lives_in_profile/(?P<id>[0-9]+)/$',views.lives_in_profile,name='lives_in_profile'),

    path(r'^edit_lives_in/(?P<id>[0-9]+)/$', views.edit_lives_in, name='edit_lives_in'),

    path(r'^delete_lives_in/(?P<id>[0-9]+)/$',views.delete_lives_in,name = 'delete_lives_in'),
    
    
    path('list_works_in/', views.view_works_in, name='list_works_in'),
    
    path(r'^works_in_profile/(?P<id>[0-9]+)/$',views.works_in_profile,name='works_in_profile'),

    path(r'^edit_works_in/(?P<id>[0-9]+)/$', views.edit_works_in, name='edit_works_in'),

    path(r'^delete_works_in/(?P<id>[0-9]+)/$',views.delete_works_in,name = 'delete_works_in'),
    
    

    path('list_manages/', views.view_manages, name='list_manages'),

    path(r'^manages_profile/(?P<id>[0-9]+)/$', views.manages_profile, name='manages_profile'),

    path(r'^edit_manages/(?P<id>[0-9]+)/$', views.edit_manages, name='edit_manages'),

    path(r'^delete_manages/(?P<id>[0-9]+)/$', views.delete_manages, name='delete_manages'),
    
    

    path('list_looks_after/', views.view_looks_after, name='list_looks_after'),

    path(r'^looks_after_profile/(?P<id>[0-9]+)/$', views.looks_after_profile, name='looks_after_profile'),

    path(r'^edit_looks_after/(?P<id>[0-9]+)/$', views.edit_looks_after, name='edit_looks_after'),

    path(r'^delete_looks_after/(?P<id>[0-9]+)/$', views.delete_looks_after, name='delete_looks_after'),



    # url(r'^signup/$', views.register, name='register'),
    path('signup/', views.register, name='register'),
    
    
    
    
    
    
    path('permissionError/',views.permissionError, name='permissionError'),

    path('animal_gallery', views.animal_gallery, name='animal_gallery'),
    path('bird_gallery', views.bird_gallery, name='bird_gallery'),
    path('aquatic_gallery', views.aquatic_gallery, name='aquatic_gallery'),
    
    
    
    
    
    
    
    
    
]
