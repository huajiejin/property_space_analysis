from django.urls import path

from . import views

urlpatterns = [
    path(
		"property-space/",
		views.PropertySpaceView.as_view(),
		name="property_space"
	),
    path(
		"property-space/<int:id>/",
		views.PropertySpaceView.as_view(),
		name="property_space_detail"
	),
]