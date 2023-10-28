from django.urls import path
from .views import ArticleList, ArticleDetail, ArticleCreate, ArticleUpdate, ArticleDelete, ResponseCreate, \
   ResponseList, MyArticles, MyResponsesView, delete_responses, accept_responses


urlpatterns = [
   path('', ArticleList.as_view(), name='article_list'),
   path('my_articles/', MyArticles.as_view(), name='my_articles'),
   path('<int:pk>', ArticleDetail.as_view(), name='article'),
   path('create', ArticleCreate.as_view(), name='article_create'),
   path('<int:pk>/update/', ArticleUpdate.as_view(), name='article_update'),
   path('<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete'),
   path('response', ResponseCreate.as_view(), name='response_create'),
   path('response_list', ResponseList.as_view(), name='response_list'),
   path('my_responses', MyResponsesView.as_view(), name='my_responses'),
   path('delete-response/<int:pk>/', delete_responses, name='delete_response'),
   path('accept-response/<int:pk>/', accept_responses, name='accept_response'),
]