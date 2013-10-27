from django.conf.urls import patterns, include, url
import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'jimini.app.website.views.splash_page', name='home'),
    url(r'^how_this_works$', 'jimini.app.website.views.how_this_works', name='how_this_works'),
    url(r'^wrap/(?P<coupon>[^/]+)$', 'jimini.app.website.views.wrap_page', name='wrap'),
    url(r'^origamis$', 'jimini.app.website.views.origamis', name='origamis'),
    url(r'^coupon/(?P<coupon>.+)$', 'jimini.app.website.views.coupon_redirect', name='redirect'),
    url(r'^user_page', 'jimini.app.website.views.user_page', name='user_page'),
    url(r'^handle_login', 'jimini.app.website.views.handle_login', name='handle_login'),
    url(r'^choose_origami.html/(?P<origami_id>[0-9]+)/(?P<order_id>[0-9]+)$', 'jimini.app.website.views.choose_origami', name='choose_origami'),
    url(r'^choose_origami.html/(?P<origami_id>[0-9]+)$', 'jimini.app.website.views.choose_origami', name='choose_origami'),
    url(r'^choose_origami.html', 'jimini.app.website.views.choose_origami', name='choose_origami'),
    url(r'^choose_recipient.html/(?P<origami_id>[0-9]+)$', 'jimini.app.website.views.choose_recipient', name='choose_recipient'),
    url(r'^choose_recipient.html/(?P<origami_id>[0-9]+)/(?P<order_id>[0-9]+)$', 'jimini.app.website.views.choose_recipient', name='choose_recipient'),
    url(r'^payment.html/(?P<origami_id>[0-9]+)/(?P<order_id>[0-9]+)$', 'jimini.app.website.views.payment', name='payment'),
    url(r'^confirmation.html/(?P<order_id>[0-9]+)$', 'jimini.app.website.views.confirmation', name='confirmation'),

    # Examples:
    # url(r'^$', 'jimini.views.home', name='home'),
    # url(r'^jimini/', include('jimini.foo.urls')),

    # Uncomment the admin/doc line below tenable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
)
