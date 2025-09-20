from django.urls import path
from . import views

urlpatterns = [
    path("<slug:post_slug>/", views.CommentView.as_view(), name="post-comments"),
    path("<int:comment_id>/report/", views.ReportCommentView.as_view(), name="comment-report"),
]
