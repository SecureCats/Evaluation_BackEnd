from django.urls import include, path
from . import views
from django.conf.urls import handler404

handler404 = views.static
urlpatterns = [

    path('api/', include([
        path('v1/', include([
            path('init', views.query_question_list),
            path('auth', views.verify_user),
            path('result', views.submit_evaluation),
        ]))
    ])),
    path('', views.static),
    path('class/<int:cl>/semester/<str:sm>',views.static), # 其实可以省略，但是显式优于隐式
    path('<path:_>', views.static)
]
