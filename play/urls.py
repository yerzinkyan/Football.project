from django.urls import path
from .views import barca_vs_juve

urlpatterns = [
    # path('person', Person.as_view(), name='kick the ball'),
    # path('firsthalf', FirstHalf.as_view(), name='FirstHalf'),
    # path('barca', barca ,name='barca' ),
    path('barca_vs_juve', barca_vs_juve ,name='barca_vs_juve' ),
]