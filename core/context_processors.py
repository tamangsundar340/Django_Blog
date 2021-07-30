from core.models import SiteInformation

def add_variable_to_context(request):
    siteInfo = SiteInformation.objects.first()
    return {
        'siteInfo': siteInfo
    }