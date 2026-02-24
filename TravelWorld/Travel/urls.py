from django.urls import path
from . import views

from .views import LeadListView
from .views import *


urlpatterns = [


     path('',views.Index,name='index'),

     path('suppliers/', views.supplier_list, name='supplier_list'),
     path('suppliers/add/', views.add_supplier, name='add_supplier'),
     path('suppliers/edit/<int:supplier_id>/', views.edit_supplier, name='edit_supplier'),
     path('suppliers/delete/<int:supplier_id>/', views.delete_supplier, name='delete_supplier'),


     path('destinations/',views.destination_list, name='destination_list'),
     path('destination/add/',views. add_destinations, name='add_destinations'),
     path('destinations/edit/<int:destinations_id>/',views. edit_destinations, name='edit_destinations'),
     path('destinations/delete/<int:destinations_id>/',views. delete_destinations, name='delete_destinations'),


     path('room-types/',views. room_type_list, name='room_type_list'),
     path('room-types/add/',views. add_room_type, name='add_room_type'),
     path('room-types/edit/<int:room_type_id>/',views. edit_room_type, name='edit_room_type'),
     path('room-types/delete/<int:room_type_id>/',views. delete_room_type, name='delete_room_type'),




     path('meal-plans/',views. meal_plan_list, name='meal_plan_list'),
     path('meal-plans/add/',views. add_meal_plan, name='add_meal_plan'),
     path('meal-plans/edit/<int:meal_plan_id>/',views. edit_meal_plan, name='edit_meal_plan'),
     path('meal-plans/delete/<int:meal_plan_id>/',views. delete_meal_plan, name='delete_meal_plan'),


     path('hotels/', views.hotel_list, name='hotel_list'),
     path('hotels/add/', views.add_hotel, name='add_hotel'),
     path('hotels/<int:hotel_id>/edit/', views.edit_hotel, name='edit_hotel'),
     path('hotels/<int:hotel_id>/delete/', views.delete_hotel, name='delete_hotel'),
     path('hotels/bulk-delete/', views.hotel_bulk_delete, name='hotel_bulk_delete'),



     path('hotels/bulk-upload/', views.hotel_bulk_upload, name='hotel_bulk_upload'),
     path('hotels/download-template/', views.download_hotel_template, name='download_hotel_template'),

     # Price URLs
     path('hotels/<int:hotel_id>/prices/', views.Hotel_price_list, name='price_list'),
     path('hotels/<int:hotel_id>/prices/add/', views.Hotel_add_price, name='add_price'),
     path('hotel/<int:hotel_id>/price/edit/<int:price_id>/', views.Hotel_edit_price, name='edit_price'),
     path('hotel/<int:hotel_id>/price/delete/<int:price_id>/', views.Hotel_delete_price, name='delete_price'),


     path('houseboats/', views.houseboat_list, name='houseboat_list'),
     path('houseboats/add/', views.houseboat_create, name='houseboat_create'),
     path('houseboats/edit/<int:pk>/', views.houseboat_update, name='houseboat_update'),
     path('houseboats/delete/<int:pk>/', views.houseboat_delete, name='houseboat_delete'),
     path('houseboats/bulk-delete/', views.houseboat_bulk_delete, name='houseboat_bulk_delete'),


          # NEW: AJAX endpoints for image management within the modal
     path('houseboat/<int:houseboat_id>/images/upload/', views.houseboat_image_upload_modal, name='houseboat_image_upload_modal'),
     path('houseboat/<int:houseboat_id>/images/delete/<int:pk>/', views.houseboat_image_delete_modal, name='houseboat_image_delete_modal'),

     path('houseboat/<int:houseboat_id>/images/', views.get_houseboat_images, name='get_houseboat_images'),
     path('houseboat/images/delete/<int:pk>/', views.houseboat_image_delete_modal, name='houseboat_image_delete_modal'),

     # Houseboat Price URLs
     # path('houseboats/<int:houseboat_id>/prices/', views.houseboat_price_list, name='houseboat_price_list'),
     # path('houseboats/<int:houseboat_id>/prices/add/', views.houseboat_price_create, name='houseboat_price_create'),
     # path('houseboats/prices/edit/<int:pk>/', views.houseboat_price_update, name='houseboat_price_update'),
     # path('houseboats/prices/delete/<int:pk>/', views.houseboat_price_delete, name='houseboat_price_delete'),

     path('houseboat/<int:houseboat_id>/pricing/', views.houseboat_price_manager, name='houseboat_price_list'),
     path('houseboat/<int:houseboat_id>/pricing/<int:price_id>/edit/', views.houseboat_price_manager, name='houseboat_price_update'),
     path('houseboat/<int:houseboat_id>/pricing/<int:price_id>/delete/', views.delete_houseboat_price, name='houseboat_price_delete'),




     path('activities/', views.activity_list, name='activity_list'),
     path('activities/add/', views.add_activity, name='add_activity'),
     path('activities/edit/<int:activity_id>/', views.edit_activity, name='edit_activity'),
     path('activities/delete/<int:activity_id>/', views.delete_activity, name='delete_activity'),
     path('activities/<int:activity_id>/prices/', views.activity_price_list, name='activity_price_list'),
     path('prices/edit/<int:price_id>/', views.edit_activity_price, name='edit_activity_price'),
     path('prices/delete/<int:price_id>/', views.delete_activity_price, name='delete_activity_price'),



     # Special Inclusion URLs
     path('special-inclusions/', views.special_inclusion_list, name='special_inclusion_list'),
     path('special-inclusions/add/', views.add_special_inclusion, name='add_special_inclusion'),
     path('special-inclusions/edit/<int:pk>/', views.edit_special_inclusion, name='edit_special_inclusion'),
     path('special-inclusions/delete/<int:pk>/', views.delete_special_inclusion, name='delete_special_inclusion'),

     # Inclusion Price URLs
     path('special-inclusions/<int:inclusion_id>/prices/', views.inclusion_price_list, name='inclusion_price_list'),
     path('special-inclusions/<int:inclusion_id>/prices/add/', views.add_inclusion_price, name='add_inclusion_price'),
     path('special-inclusions/prices/edit/<int:pk>/', views.edit_inclusion_price, name='edit_inclusion_price'),
     path('special-inclusions/prices/delete/<int:pk>/', views.delete_inclusion_price, name='delete_inclusion_price'),

    path('vehicles/', views.vehicle_list, name='vehicle_list'),
    path('vehicles/add/', views.add_vehicle, name='add_vehicle'),
    path('vehicles/edit/<int:vehicle_id>/', views.edit_vehicle, name='edit_vehicle'),
    path('vehicles/delete/<int:vehicle_id>/', views.delete_vehicle, name='delete_vehicle'),

    path('vehicles/<int:vehicle_id>/pricing/', views.vehicle_pricing_list, name='vehicle_pricing_list'),
    path('vehicles/<int:vehicle_id>/pricing/add/', views.add_vehicle_pricing, name='add_vehicle_pricing'),
    path('vehicles/<int:vehicle_id>/pricing/edit/<int:price_id>/', views.edit_vehicle_pricing, name='edit_vehicle_pricing'),
    path('vehicles/<int:vehicle_id>/pricing/delete/<int:price_id>/', views.delete_vehicle_pricing, name='delete_vehicle_pricing'),

     path('itineraries/', views.list_itineraries, name='list_itineraries'),
     # path('itineraries/add/',views. add_itinerary, name='add_itinerary'),
     # path('itineraries/edit/<int:pk>/',views. edit_itinerary, napackage-themesme='edit_itinerary'),
     path('itinerary/<int:itinerary_id>/delete/', views.delete_itinerary, name='delete_itinerary'),
     # path('search-itineraries/',views. search_itineraries, name='search_itineraries'),

     path('leadsources/', views.leadsource_list, name='leadsource_list'),
     path('leadsources/add/', views.add_leadsource, name='add_leadsource'),
     path('leadsources/edit/<int:pk>/', views.edit_leadsource, name='edit_leadsource'),
     path('leadsources/delete/<int:pk>/', views.delete_leadsource, name='delete_leadsource'),

     path('package-themes/', views.package_theme_list, name='package_theme_list'),
     path('package-themes/add/', views.add_package_theme, name='add_package_theme'),
     path('package-themes/edit/<int:pk>/', views.edit_package_theme, name='edit_package_theme'),
     path('package-themes/delete/<int:pk>/', views.delete_package_theme, name='delete_package_theme'),


     path('currencies/', views.currency_list, name='currency_list'),
     path('currencies/add/', views.add_currency, name='add_currency'),
     path('currencies/edit/<int:pk>/', views.edit_currency, name='edit_currency'),
     path('currencies/delete/<int:pk>/', views.delete_currency, name='delete_currency'),

     path('admin_board',views.Admin_Board,name='admin_board'),
     path('admin_settings',views.Admin_Settings,name='admin_settings'),
     path('settings/', views.organisational_setting_list, name='organisational_setting_list'),
     path('settings/edit/<int:pk>/', views.organisational_setting_edit, name='organisational_setting_edit'),


     # path('invoice-logo/',views. edit_invoice_logo, name='edit_invoice_logo'),
     # path('invoice-terms/',views. edit_invoice_terms, name='edit_invoice_terms'),
     # path('package-terms/',views. edit_package_terms, name='edit_package_terms'),
     # path('bank-information/',views. edit_bank_information, name='edit_bank_information'),
     # path('settings/edit/', views.edit_all_settings, name='edit_all_settings'),
     path('settings/edit/', views.edit_all_settings, name='edit_all_settings'),
     path('package/details/', views.package_details, name='package_details'),
     # AJAX endpoints for package terms modal
     path('itinerary/<int:itinerary_id>/get-package-terms/', views.get_package_terms_ajax, name='get_package_terms_ajax'),
     path('itinerary/<int:itinerary_id>/save-package-terms/', views.save_package_terms_ajax, name='save_package_terms_ajax'),

     path('branches/', views.branch_list, name='branch_list'),
     path('branches/add/', views.branch_create, name='branch_add'),
     path('branches/<int:pk>/edit/', views.branch_update, name='branch_edit'),
     path('branches/<int:pk>/delete/', views.branch_delete, name='branch_delete'),



     path('roles/', views.role_list, name='role_list'),
     path('roles/add/', views.add_role, name='add_role'),
     path('roles/<int:pk>/edit/', views.edit_role, name='edit_role'),
     path('roles/<int:pk>/delete/', views.delete_role, name='delete_role'),

     path('queries/', views.query_list, name='query_list'),
     path('query/add/', views.add_query, name='add_query'),
     path('query/<int:pk>/edit/', views.edit_query, name='edit_query'),


     # Query API Endpoints for Modals
     path('api/query/<int:query_id>/', views.get_query_api, name='get_query_api'),
     path('api/query/<int:query_id>/delete/', views.delete_query_api, name='delete_query_api'),

     path('itineraries-dayplans/', views.itinerary_dayplan_list, name='itinerary_dayplan_list'),
     path('itinerary/create/<int:query_id>/',views. create_itinerary, name='create_itinerary'),
     path('itinerary/<int:itinerary_id>/day-plan/', views.itinerary_day_plan, name='itinerary_day_plan'),
     path('itinerary/edit/', views.edit_itinerary, name='edit_itinerary'),
     path('query/<int:query_id>/history/', views.itinerary_history, name='itinerary_history'),
     path('api/itinerary/<int:itinerary_id>/unarchive/', views.unarchive_itinerary, name='unarchive_itinerary'),


     path('api/itinerary/<int:itinerary_id>/details/', views.get_itinerary_details, name='api_itinerary_details'),

    # Houseboat valid options API for itinerary
     path('get-hotel-inclusions/<int:hotel_id>/', views.get_hotel_inclusions, name='get_hotel_inclusions'),
     path('get-houseboat-inclusions/<int:houseboat_id>/', views.get_houseboat_inclusions, name='get_houseboat_inclusions'),
     path('itinerary/<int:itinerary_id>/create-hotel-booking/', views.create_hotel_booking, name='create_hotel_booking'),
     path('hotel-booking/<int:booking_id>/update/', views.update_hotel_booking, name='update_hotel_booking'),
     path('hotel-booking/<int:booking_id>/update/', views.update_hotel_booking, name='update_hotel_booking'),
     path('hotel-booking/<int:booking_id>/delete/', views.delete_hotel_booking, name='delete_hotel_booking'),


     path('itinerary/<int:itinerary_id>/standalone-inclusion/create/',
          views.create_standalone_inclusion,
          name='create_standalone_inclusion'),

     path('standalone-inclusion/<int:booking_id>/update/',
          views.update_standalone_inclusion,
          name='update_standalone_inclusion'),

     path('standalone-inclusion/<int:booking_id>/delete/',
          views.delete_standalone_inclusion,
          name='delete_standalone_inclusion'),

     path('vehicle-booking/create/<int:itinerary_id>/', views.create_vehicle_booking, name='create_vehicle_booking'),
     path('vehicle-booking/update/<int:booking_id>/', views.update_vehicle_booking, name='update_vehicle_booking'),
     path('vehicle-booking/delete/<int:booking_id>/', views.delete_vehicle_booking, name='delete_vehicle_booking'),
     path(
        'api/vehicles/by-destination/',
        views.vehicles_by_destination,
        name='vehicles_by_destination'
    ),


     path('itinerary/<int:itinerary_id>/activity/add/', views.create_activity_booking, name='create_activity_booking'),
     path('activity-booking/<int:booking_id>/update/', views.update_activity_booking, name='update_activity_booking'),
     path('activity-booking/<int:booking_id>/delete/', views.delete_activity_booking, name='delete_activity_booking'),

     path('itinerary/<int:itinerary_id>/houseboat/add/', views.create_houseboat_booking, name='create_houseboat_booking'),
     path('houseboat-booking/<int:booking_id>/update/', views.update_houseboat_booking, name='update_houseboat_booking'),
     path('houseboat-booking/<int:booking_id>/delete/', views.delete_houseboat_booking, name='delete_houseboat_booking'),

     # pricing section
     path('itinerary/<int:itinerary_id>/pricing/', views.itinerary_pricing, name='itinerary_pricing'),
     path('update-booking-totals/', views.update_booking_totals, name='update_booking_totals'),



     path('query/<int:query_id>/proposals', views.query_proposals, name='query_proposals'),
     path('query/<int:query_id>/status/', views.update_query_status, name='update_query_status'),


     # API endpoints for itinerary confirmation
     path('api/itinerary/<int:itinerary_id>/options/', views.get_itinerary_options, name='get_itinerary_options'),
     path('api/itinerary/<int:itinerary_id>/confirm/', views.confirm_itinerary, name='confirm_itinerary'),
     path('api/itinerary/<int:itinerary_id>/cancel/', views.cancel_itinerary, name='cancel_itinerary'),
     path('api/itinerary/<int:itinerary_id>/draft/', views.set_draft_itinerary, name='set_draft_itinerary'),
     path('api/itinerary/<int:itinerary_id>/delete/', views.delete_itinerary, name='delete_itinerary'),



     # QUTATION
     path('itinerary/<int:itinerary_id>/quotation/', views.view_quotation, name='view_quotation'),
    #  path('itinerary/<int:itinerary_id>/quotation/pdf/', views.download_quotation_pdf, name='download_quotation_pdf'),

     path('day-itineraries/', views.day_itinerary_list, name='day_itinerary_list'),
     path('day-itineraries/add/', views.add_day_itinerary, name='add_day_itinerary'),
     path('day-itineraries/edit/<int:pk>/', views.edit_day_itinerary, name='edit_day_itinerary'),
     path('day-itineraries/delete/<int:pk>/', views.delete_day_itinerary, name='delete_day_itinerary'),
     path('day-itineraries/toggle-pin/<int:pk>/', views.toggle_pin_itinerary, name='toggle_pin_itinerary'),
     path('day-itineraries/delete-multiple/', views.delete_selected_day_itineraries, name='delete_selected_day_itineraries'),

    # Gallery Image URLs
    path('gallery/images/', views.gallery_image_list, name='gallery_image_list'),
    path('gallery/images/add/', views.add_gallery_image, name='add_gallery_image'),
    path('gallery/images/delete/<int:pk>/', views.delete_gallery_image, name='delete_gallery_image'),
    path('gallery/images/json/', views.get_gallery_images_json, name='get_gallery_images_json'),
    path('day-itineraries/search/', views.search_day_itineraries, name='search_day_itineraries'),














    # Hotel Inclusions
    path('hotels/<int:hotel_id>/inclusions/', views.manage_hotel_inclusions, name='manage_hotel_inclusions'),
    path('hotels/<int:hotel_id>/inclusions/add/', views.add_hotel_inclusion, name='add_hotel_inclusion'),
    path('hotel-inclusions/<int:inclusion_id>/delete/', views.delete_hotel_inclusion, name='delete_hotel_inclusion'),
    path('hotel-inclusions/<int:inclusion_id>/edit/', views.edit_hotel_inclusion, name='edit_hotel_inclusion'),
    path('hotel-inclusions/<int:inclusion_id>/toggle/', views.toggle_inclusion_availability, name='toggle_inclusion_availability'),


     path('houseboats/<int:houseboat_id>/inclusions/',  views.manage_houseboat_inclusions, name='manage_houseboat_inclusions'),
     path('houseboats/<int:houseboat_id>/inclusions/add/', views.add_houseboat_inclusion, name='add_houseboat_inclusion'),
     path('houseboat-inclusions/<int:inclusion_id>/delete/', views.delete_houseboat_inclusion,name='delete_houseboat_inclusion'),
     path('houseboat-inclusions/<int:inclusion_id>/edit/', views.edit_houseboat_inclusion, name='edit_houseboat_inclusion'),  # ✅ ADD THIS




     path('packages/', views.list_package_templates, name='list_package_templates'),
     path('packages/create/', views.create_package_template, name='create_package_template'),
     path('packages/<int:package_id>/edit/', views.edit_package_template, name='edit_package_template'),
     path('packages/<int:package_id>/delete/', views.delete_package_template, name='delete_package_template'),

     path('api/packages/<int:package_id>/details/', views.get_package_details, name='get_package_details'),
     path('packages/<int:package_id>/day-plans/', views.manage_package_day_plans, name='manage_package_day_plans'),
     path('packages/<int:package_id>/add-general-inclusion/', views.add_general_inclusion_to_package, name='add_general_inclusion_to_package'),
     path('packages/<int:package_id>/remove-general-inclusion/<int:inclusion_id>/', views.remove_general_inclusion_from_package, name='remove_general_inclusion_from_package'),

     path('hotel-booking/create-package/<int:package_id>/', views.create_hotel_booking_for_package, name='create_hotel_booking_for_package'),
     path('vehicle-booking/create-package/<int:package_id>/', views.create_vehicle_booking_for_package, name='create_vehicle_booking_for_package'),

     path('activity-booking/create-package/<int:package_id>/', views.create_activity_booking_for_package, name='create_activity_booking_for_package'),
     path('houseboat-booking/create-package/<int:package_id>/', views.create_houseboat_booking_for_package, name='create_houseboat_booking_for_package'),


     # Package Template Pricing (NEW)
     path('package/<int:package_id>/pricing/', views.package_template_pricing,name='package_template_pricing'),


     path('query/<int:query_id>/insert-package/', views.insert_package_to_itinerary, name='insert_package_to_itinerary'),
     path('api/check-package-availability/', views.check_package_availability, name='check_package_availability'),

     #   supplier management
     path('query/<int:query_id>/supplier-communication/', views.supplier_communication, name='supplier_communication'),

     path('itinerary/<int:itinerary_id>/confirmation/', views.view_confirmation, name='view_confirmation'),
     path('itinerary/<int:itinerary_id>/confirmation/download/', views.download_confirmation_pdf, name='download_confirmation_pdf'),




     path("leadss/", LeadListView.as_view(), name="home"),
     path("leads/", LeadListView.as_view(), name="lead-list"),
     path("api/leads/", ApiLeadListCreateView.as_view(), name="api-lead-list-create"),
     path("api/leads/<int:pk>/", ApiLeadDetailView.as_view(), name="api-lead-detail"),





     path("assign/", views.leads_list_assign, name="lead_assign"),

     path("cres/", views.team_member_list_page, name="cre_list"),
     path("cres/table/", views.team_member_table_partial, name="cre_table_partial"),
     path("leads/rows/", LeadRowsView.as_view(), name="lead_rows"),
     path("leads/excel/all/",views.leads_excel_all, name="leads_excel_all"),


              # ✅ NEW: AJAX endpoint for fetching section data
    path('itinerary/<int:itinerary_id>/get-section-data/', views.get_section_data_ajax, name='get_section_data_ajax'),

     path("leads/pdf/",views.leads_pdf_all, name="leads_pdf_all"),

         # ==========================================
    # 🗑️ BULK DELETE URLS
    # ==========================================
    path(
        'itinerary/<int:itinerary_id>/bulk-delete/hotels/',
        views.bulk_delete_hotels,
        name='bulk_delete_hotels'
    ),

    path(
        'itinerary/<int:itinerary_id>/bulk-delete/activities/',
        views.bulk_delete_activities,
        name='bulk_delete_activities'
    ),

    path(
        'itinerary/<int:itinerary_id>/bulk-delete/houseboats/',
        views.bulk_delete_houseboats,
        name='bulk_delete_houseboats'
    ),

    path(
        'itinerary/<int:itinerary_id>/bulk-delete/vehicles/',
        views.bulk_delete_vehicles,
        name='bulk_delete_vehicles'
    ),

    path(
        'itinerary/<int:itinerary_id>/bulk-delete/day-itineraries/',
        views.bulk_delete_day_itineraries,
        name='bulk_delete_day_itineraries'
    ),
    # urls.py
     path('itinerary/day-plan/<int:day_plan_id>/remove/',
     views.remove_day_plan_from_itinerary,
     name='delete_day_plan_from_itinerary'),

     path('api/get-special-inclusions/', views.get_special_inclusions, name='get_special_inclusions'),
     path('api/get-houseboat-booking-inclusions/<int:booking_id>/', views.get_houseboat_booking_inclusions, name='get_houseboat_booking_inclusions'),
     path('api/get-booking-inclusions/<int:booking_id>/', views.get_booking_inclusions, name='get_booking_inclusions'),
     path('hotel/<int:hotel_id>/valid-options/',
         views.get_valid_hotel_options,
         name='get_valid_hotel_options'),

    path('houseboat/<int:houseboat_id>/valid-options/',
         views.get_valid_houseboat_options,
         name='get_valid_houseboat_options'),

    path('api/hotels/by-destination/', views.get_hotels_by_destination, name='hotels_by_destination'),
    path('hotel/get-priced-hotels/', views.get_priced_hotels, name='get_priced_hotels'),


        # Driver PDF Views
    path('view-driver-itinerary/<int:itinerary_id>/', views.view_driver_itinerary, name='view_driver_itinerary'),
    path('download-driver-pdf/<int:itinerary_id>/', views.download_driver_pdf, name='download_driver_pdf'),
        # Client PDF
    path('view-client-quotation/<int:itinerary_id>/', views.view_client_quotation, name='view_client_quotation'),
    path('download-client-pdf/<int:itinerary_id>/', views.download_client_pdf, name='download_client_pdf'),




    path('itinerary/<int:itinerary_id>/prepare-edit/',
         views.prepare_edit_itinerary,
         name='prepare_edit_itinerary'),
     path('query/<int:query_id>/version-history/',
         views.itinerary_version_history,
         name='itinerary_version_history'),
     path('itinerary/<int:itinerary_id>/delete-version/',
         views.delete_itinerary_version,
         name='delete_itinerary_version'),
         # ✅ Restore archived itinerary
     path('itinerary/<int:itinerary_id>/restore/',
          views.restore_archived_itinerary,
          name='restore_archived_itinerary'),



    path('get-available-hotels-for-change/', views.get_available_hotels_for_change, name='get_available_hotels_for_change'),
    path('change-hotel-booking/', views.change_hotel_booking, name='change_hotel_booking'),








]






