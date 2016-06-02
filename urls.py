from django.conf.urls import url
from src.api.v1.views.userview import UserView
from src.api.v1.views.tokenview import TokenView
from src.api.v1.views.pullrequests import PullRequestsView


urlpatterns = [
     url(r'^gitsync/user/$', UserView.as_view()),
     url(r'^gitsync/login/$', TokenView.as_view()),
     url(r'^gitsync/pull_requests/$', PullRequestsView.as_view()),
     ]

