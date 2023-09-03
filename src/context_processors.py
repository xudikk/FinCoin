from django.conf import settings


def main(requests):
    return {
        "app_name": settings.APP_NAME
    }



