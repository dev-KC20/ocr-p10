# users/urls.py
from django.urls import path, include
# from rest_framework import routers
from rest_framework_nested import routers
from .views import ProjectViewSet, ContributorViewSet, IssueViewSet, CommentViewSet

router = routers.SimpleRouter()
router.register('projects', ProjectViewSet, basename='projects')

project_router = routers.NestedSimpleRouter(router, r'projects', lookup='project')
project_router.register('users', ContributorViewSet, basename='users')
project_router.register('issues', IssueViewSet, basename='issues')
issue_router = routers.NestedSimpleRouter(project_router, r'issues', lookup='issue')
issue_router.register('comments', CommentViewSet, basename='comments')

# contributor_list = ContributorViewSet.as_view({
#     'get': 'list',
#     'post': 'create'
# })

# contributor_detail = ContributorViewSet.as_view({
#     'delete': 'destroy',
#     'get': 'retrieve'
# })

urlpatterns = [
    # path('projects/<int:project_id>/users/', ContributorViewSet.as_view({'get': 'list', 'post': 'create'}),  name='contributor_list'),
    path('', include(router.urls)) ,
    path('', include(project_router.urls)) ,
    path('', include(issue_router.urls)) ,
    # path('projects/<int:project_id>/users/<int:pk>/', contributor_detail,  name='contributor_detail'),
]