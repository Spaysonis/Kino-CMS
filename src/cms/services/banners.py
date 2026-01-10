from src.cms.models import HomePageBanner

BANNER_CONFIG = {

# 'TB': {
#         'key':'TB',
#         'form_prefix':'top_banner_form',
#         'formset_prefix':'top_banner_formset'

    HomePageBanner.TOP_BANNER : { # TOP_BANNER = TB
        'key':'tb',
        'form_prefix':'top_banner_form',
        'formset_prefix':'top_banner_formset'

    },
    HomePageBanner.NEWS_BANNER : { # NEWS_BANNER == NB
        'key':'nb',
        'form_prefix':'news_banner_form',
        'formset_prefix':'news_banner_formset'
    }
}


