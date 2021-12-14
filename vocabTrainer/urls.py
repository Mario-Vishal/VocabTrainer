from django.urls import path
from . import views 

urlpatterns = [

    path('',views.home,name='home'),
    path('added_today',views.added_today,name='today'),
    path('bookmark/<int:word_id>',views.bookmark,name='bookmark'),
    path('viewbookmarked',views.view_bookmarked,name='viewbookmarked'),
    path('addword',views.addword,name='addword'),
    path('word_detail/<int:word_id>',views.word_detail,name='worddetail'),
    path('edit_delete/<int:word_id>',views.edit_word,name="edit_delete"),
    path('delete_word/<int:word_id>',views.delete_word,name="delete_word"),
    path('update<int:word_id>',views.update_word,name="update_word"),
    path('search',views.search_page,name="search"),
    path('prev/<str:card_id>',views.card_slider_prev,name="prev"),
    path('next/<str:card_id>',views.card_slider_next,name="next"),
    path('revise/sets/revise_set<int:set_number>',views.card_slider_main,name="revise_set"),
    path('revise/sets',views.set_page,name="sets"),
    path('set<int:set_number>',views.set,name="set")
]