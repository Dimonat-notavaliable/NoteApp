from .models import SiteLinks


def settings(request):
    return {'settings': SiteLinks.load()}
