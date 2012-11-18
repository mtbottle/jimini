from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', 'jimini.app.website.views.splash_page', name='home'),
	url(r'^how_this_works$', 'jimini.app.website.views.how_this_works', name='how_this_works'),
    # Examples:
    # url(r'^$', 'jimini.views.home', name='home'),
    # url(r'^jimini/', include('jimini.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
