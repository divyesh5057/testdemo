from django.urls import path
from . import views

app_name = "frontend"


urlpatterns = [
    # path('', views.home, name='home'),
    path("login/",views.Login,name="login"),
    path("logout/",views.Logout,name="logout"),

    path("user-dashbaord/",views.Dashboard,name="dashboard"),
    path("show-project/",views.ShowProject,name="showproject"),
    path("add-project/",views.AddProject,name="addproject"),
    path("update-project/<int:id>/",views.AddProject,name="updateproject"),
    path("delete-project/<int:id>/",views.DeleteProject,name="deleteproject"),

    path("show-task/",views.ShowTask,name="showtask"),
    path("add-task/",views.AddTask,name="addtask"),
    # path("update-task/<int:pk>/",views.AddTask,name="updatetask"),
    # path("delete-task/<int:pk>/",views.DeleteTask,name="deletetask"),

    path("add-employee/",views.AddEmployee,name="addemployee"),
    path("update-employee/<int:id>/",views.AddEmployee,name="updateemployee"),
    path("delete-employee/<int:id>/",views.DeleteEmployee,name="deleteemployee"),
    path("show-employee/",views.ShowEmployee,name="showemployee"),

    path("user-profile/",views.UserProfile,name="userprofile"),

    path("all-images/",views.All_imgage,name="image"),
    path("update-images/<int:id>/",views.All_imgage,name="updateimage"),
    path("delete-img/<int:id>/",views.DeleteImage,name="deleteimg"),

    path('search/', views.search_view, name='search'),

    


]