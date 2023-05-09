from django.urls import include, path

from job_folio.users.views import UserDetailView, UserUpdateView

app_name = "users"
user_patterns = [
    path("<int:user_id>", view=UserDetailView.as_view(), name="users_detail"),
    path("<int:user_id>/update", view=UserUpdateView.as_view(), name="users_update"),
]

urlpatterns = [
    path("users/", include(user_patterns))
]
