from job_folio.users.models import User


def users_update_user(*, user: User, data: dict = None):
    if data is None:
        data = {}

    prefs, created = User.objects.update_or_create(user=user, defaults=data)
    if created:
        # send notification?
        pass

    return prefs
