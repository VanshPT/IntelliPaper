from django.urls import path,include
from django.shortcuts import render
from . import views

urlpatterns = [
    path('', views.landing, name="landing"),
    path('assistant/fetch_chat_messages/', views.load_chats, name='fetch_chat_messages'),
    path('assistant/delete_chats/', views.delete_chats, name='delete_chats'),
    path('dashboard/<str:username>/', views.render_dashboard, name="render_dashboard"),
    path('auto_cluster/<str:username>/', views.render_auto_cluster, name="render_auto_cluster"),
    path('auto_cluster/<str:username>/cluster/', views.auto_cluster, name="auto_cluster"),
    path('auto_cluster/<str:username>/<int:id>/', views.render_papers_per_cluster, name="render_papers_per_cluster"),
    path('explore_topics/<str:username>/', views.render_explore_topics, name="render_explore_topics"),
    path('explore_topics/<str:username>/<int:id>/', views.render_papers_per_readlist, name="render_papers_per_readlist"),
    path('explore_topics/<str:username>/save_papers/', views.save_papers_to_readlist, name="save_paper_to_readlist"),
    path('explore_topics/<str:username>/remove_paper_from_readlist/', views.remove_paper_from_readlist, name="remove_paper_from_readlist"),
    path('explore_topics/<str:username>/<int:id>/delete_readlist/', views.delete_readlist, name="delete_readlist"),
    path('search_paper/<str:username>/', views.render_search_paper, name="render_search_paper"),
    path('assistant/<str:username>/', views.render_assistant, name="render_assistant"),
    path('assistant/<str:username>/send_query/', views.rag_assistant, name="rag_assistant"),
    path('extract_save_pdf/', views.extract_save_pdf, name="extract_save_pdf"),
    path('delete_paper/<str:username>/<int:id>/', views.delete_paper, name="render_history"),
    path('delete_paper1/<str:username>/<int:id>/', views.delete_paper1, name="render_history"),
    path('api/rename_readlist', views.rename_readlist, name='rename_readlist'),
    path('view_pdf/<int:id>/', views.render_pdf_viewer, name="render_pdf_viewer"),
    path('view_pdf/<int:id>/generate_summary/', views.generate_summary, name="generate_summary"),
    path('view_pdf/notes/<int:id>/', views.render_pdf_notes, name="render_pdf_notes"),
    path('view_pdf/<int:paper_id>/generate_citations/', views.GenerateCitationsView.as_view(), name='generate_citations'),
    path('save_notes/<str:username>/<int:paper_id>/', views.save_notes, name='save_notes'),
    path('search/', views.search_engine, name="search"),
    path('web-search/', views.web_search,name="Web Search" ),
    
]