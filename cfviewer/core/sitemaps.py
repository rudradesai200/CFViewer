from django.contrib import sitemaps
from django.urls import reverse

class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.9
    changefreq = 'weekly'

    def items(self):
        return ['home','dashboard','problems','contests','books','friendsunsolved','adspage']

    def location(self, item):
        return reverse(item)

class SuggestViewSitemap(sitemaps.Sitemap):
    priority = 0.8
    changefreq = 'weekly'

    def items(self):
        return ['problem','contest']
    
    def location(self,item):
        return reverse('suggestor',args=[item])