from django.urls import path
from . import views

# -------------------------------
# URL patterns for the application
# Each path is linked to a function in views.py
# -------------------------------
urlpatterns = [
    # 1. User Registration → New users create account
    path('register/', views.register, name='register'),

    # 2. Login → Both user & admin login here
    path('login/', views.login_view, name='login'),

    # 3. Logout → Logs out current user and redirects to login
    path('logout/', views.logout_view, name='logout'),

    # 4. User Home → Upload waste image
    path('home/', views.user_home, name='home'),

    # 5. Prediction Result → Show uploaded image + ML prediction
    # record_id ensures we display correct prediction for that upload
    path('predict/<int:record_id>/', views.predict_result, name='predict_result'),

    # 6. Recycle Product List → Show recycling options for predicted waste
    # waste_type passed as string (e.g., "Plastic")
    path('recycle/<str:waste_type>/', views.recycle_list, name='recycle_list'),

    # 7. Admin Dashboard → Admin-only landing page
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),

    # 8. Admin View → List of registered users (via Profile)
    path('dashboard/users/', views.user_list, name='user_list'),

    # 9. Admin View → List of all waste records (uploads + results)
    path('dashboard/waste-records/', views.waste_records, name='waste_records'),
]
