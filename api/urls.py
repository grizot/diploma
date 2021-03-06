from django.conf.urls import url, include
from django.urls import path

from .views import api_root, time_test
from main.views import MainCommonViewSet
from news.views import BlockNewsViewSetAPI, AllNewsViewSet, NewsDetail
from federation.views import FederationPage
from events.views import BlockEventsViewSetAPI, EventDetail,EventsAllViewSet, EventsActiveViewSet, EventsCompletedViewSet
from mediafiles.views import BlockMediaViewSetAPI
from directions.views import AllTrends, TrendDetail, TrendDetailNews, TrendDetailEvents
from searchgr.views import SearchView
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title="FOOTBALL FEDERATION API")

urlpatterns = [
    url(r'^root/$', api_root),
    url(r'^$', schema_view),
    url(r'^auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('common/', MainCommonViewSet.as_view(), name='common-fh-list'),
    path('common/news/', BlockNewsViewSetAPI.as_view(), name='common-news-list'),
    path('common/media/', BlockMediaViewSetAPI.as_view(), name='common-media-list'),
    path('common/trends/', AllTrends.as_view(), name='common-trends-list'),
    path('common/events/', BlockEventsViewSetAPI.as_view(), name='common-events-list'),
    path('news/detail/<int:pk>', NewsDetail.as_view(), name='news-detail'),
    path('news/list/<int:page>', AllNewsViewSet.as_view(), name='news-list'),
    path('federation/info/', FederationPage.as_view(), name='federation-page'),
    path('events/all/list/<int:page>', EventsAllViewSet.as_view(), name='events-all-list'),
    path('events/active/list/<int:page>', EventsActiveViewSet.as_view(), name='events-active-list'),
    path('events/completed/list/<int:page>', EventsCompletedViewSet.as_view(), name='events-completed-list'),
    path('events/detail/<int:pk>', EventDetail.as_view(), name='events-detail'),
    path('trend/<int:pk>', TrendDetail.as_view(), name='trend-detail'),
    path('trend/directions/<int:pk>/news/<int:page>', TrendDetailNews.as_view(), name='trend-detail-news'),
    path('trend/directions/<int:pk>/events/<int:page>', TrendDetailEvents.as_view(), name='trend-detail-events'),
    path('search/<int:page>', SearchView.as_view(), name='search'),
]
