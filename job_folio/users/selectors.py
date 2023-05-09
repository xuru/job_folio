from job_folio.users.models import User


def users_get_user(*, user_id: int) -> User:
    return User.objects.filter(id=user_id).first()
