# team_member/permissions.py

# ==========================================
# AUTO-GENERATE MASTER DATA PERMISSIONS
# ==========================================

# Define items that need View, Add, Edit, Delete permissions
MASTER_DATA_ITEMS = {
    'suppliers': {
        'label': 'Suppliers',
        'operations': ['view', 'add', 'edit', 'delete'],
    },
    'destinations_master': {  # Keep _master to match your existing key
        'label': 'Destinations',
        'operations': ['view', 'add', 'edit', 'delete'],
    },
    'room_types': {
        'label': 'Room Types',
        'operations': ['view', 'add', 'edit', 'delete'],
    },
    'meal_plans': {
        'label': 'Meal Plans',
        'operations': ['view', 'add', 'edit', 'delete'],
    },
    'hotels': {
        'label': 'Hotels',
        'operations': ['view', 'add', 'edit', 'delete', 'manage_inclusions', 'manage_prices'],
    },
    'houseboats': {
        'label': 'Houseboats',
        'operations': ['view', 'add', 'edit', 'delete'],
    },
    'activities': {
        'label': 'Activities',
        'operations': ['view', 'add', 'edit', 'delete'],
    },
    'special_inclusions': {
        'label': 'Special Inclusions',
        'operations': ['view', 'add', 'edit', 'delete'],
    },
    'vehicles': {
        'label': 'Vehicles',
        'operations': ['view', 'add', 'edit', 'delete'],
    },
    'package_templates': {
        'label': 'Package Templates',
        'operations': ['view', 'add', 'edit', 'delete'],
    },
    'lead_sources': {
        'label': 'Lead Sources',
        'operations': ['view', 'add', 'edit', 'delete'],
    },
    'package_themes': {
        'label': 'Package Themes',
        'operations': ['view', 'add', 'edit', 'delete'],
    },
    'currencies': {
        'label': 'Currencies',
        'operations': ['view', 'add', 'edit', 'delete'],
    },
}

# Auto-generate all Master Data permissions
GENERATED_MASTER_DATA_PERMISSIONS = {}

for key, config in MASTER_DATA_ITEMS.items():
    label = config['label']
    
    # Add main "Manage" permission
    GENERATED_MASTER_DATA_PERMISSIONS[f'can_manage_{key}'] = {
        'label': f'Manage {label}',
        'description': f'Can add, edit, and delete {label.lower()}',
        'category': 'Master Data',
    }
    
    # Generate sub-permissions
    for operation in config['operations']:
        if operation == 'view':
            GENERATED_MASTER_DATA_PERMISSIONS[f'can_view_{key}'] = {
                'label': f'View {label}',
                'description': f'Can view {label.lower()} listings',
                'category': 'Master Data',
            }
        elif operation == 'add':
            # Get singular form (remove 's' at end if present)
            singular_key = key.rstrip('s') if key.endswith('s') and not key.endswith('ss') else key
            singular_label = label.rstrip('s') if label.endswith('s') and not label.endswith('ss') else label
            GENERATED_MASTER_DATA_PERMISSIONS[f'can_add_{singular_key}'] = {
                'label': f'Add {singular_label}',
                'description': f'Can add new {singular_label.lower()}',
                'category': 'Master Data',
            }
        elif operation == 'edit':
            singular_key = key.rstrip('s') if key.endswith('s') and not key.endswith('ss') else key
            singular_label = label.rstrip('s') if label.endswith('s') and not label.endswith('ss') else label
            GENERATED_MASTER_DATA_PERMISSIONS[f'can_edit_{singular_key}'] = {
                'label': f'Edit {singular_label}',
                'description': f'Can edit {singular_label.lower()} details',
                'category': 'Master Data',
            }
        elif operation == 'delete':
            singular_key = key.rstrip('s') if key.endswith('s') and not key.endswith('ss') else key
            singular_label = label.rstrip('s') if label.endswith('s') and not label.endswith('ss') else label
            GENERATED_MASTER_DATA_PERMISSIONS[f'can_delete_{singular_key}'] = {
                'label': f'Delete {singular_label}',
                'description': f'Can delete {singular_label.lower()}',
                'category': 'Master Data',
            }
        elif operation == 'manage_inclusions':
            GENERATED_MASTER_DATA_PERMISSIONS[f'can_manage_hotel_inclusions'] = {
                'label': 'Manage Hotel Inclusions',
                'description': 'Can manage hotel special inclusions',
                'category': 'Master Data',
            }
        elif operation == 'manage_prices':
            GENERATED_MASTER_DATA_PERMISSIONS[f'can_manage_hotel_prices'] = {
                'label': 'Manage Hotel Prices',
                'description': 'Can manage hotel pricing',
                'category': 'Master Data',
            }


# ==========================================
# COMBINE ALL PERMISSIONS
# ==========================================
AVAILABLE_PERMISSIONS = {


    # ==========================================
    # DASHBOARD ACCESS
    # ==========================================
    'can_access_queries_dashboard': {
        'label': 'Queries Dashboard',
        'description': 'Can view and access the Queries card on the main dashboard',
        'category': 'Dashboard Access',
    },
    'can_access_itineraries_dashboard': {
        'label': 'Itineraries Dashboard',
        'description': 'Can view and access the Itineraries card on the main dashboard',
        'category': 'Dashboard Access',
    },
    'can_access_sales_dashboard': {
        'label': 'Sales Dashboard',
        'description': 'Can view and access the Sales card on the main dashboard',
        'category': 'Dashboard Access',
    },
    'can_access_leads_dashboard': {
        'label': 'Leads Dashboard',
        'description': 'Can view and access the Lead Management card on the main dashboard',
        'category': 'Dashboard Access',
    },
    # ==========================================
    # QUERIES
    # ==========================================
    'can_create_queries': {
        'label': 'Create Queries',
        'description': 'Can add new customer queries',
        'category': 'Queries',
    },
    'can_edit_all_queries': {
        'label': 'Edit All Queries',
        'description': 'Can edit any query (not just own)',
        'category': 'Queries',
    },
    'can_delete_queries': {
        'label': 'Delete Queries',
        'description': 'Can delete queries',
        'category': 'Queries',
    },
    'can_view_all_queries': {
        'label': 'View All Queries',
        'description': 'Can see queries from all team members',
        'category': 'Queries',
    },
    
    # ==========================================
    # PROPOSALS
    # ==========================================
    'can_view_proposals': {
        'label': 'View Proposals',
        'description': 'Can view and manage query proposals',
        'category': 'Proposals',
    },
    'can_create_itinerary': {
        'label': 'Create Itinerary',
        'description': 'Can create new itineraries for queries',
        'category': 'Proposals',
    },
    'can_insert_itinerary': {
        'label': 'Insert Itinerary',
        'description': 'Can insert existing packages as itineraries',
        'category': 'Proposals',
    },
    'can_supplier_communication': {
        'label': 'Supplier Communication',
        'description': 'Can communicate and manage suppliers',
        'category': 'Proposals',
    },
    'can_edit_day_plans': {
        'label': 'Edit Day Plans',
        'description': 'Can edit itinerary day plans',
        'category': 'Proposals',
    },
    'can_delete_itinerary': {
        'label': 'Delete Itinerary',
        'description': 'Can delete itineraries',
        'category': 'Proposals',
    },
    'can_confirm_itinerary': {
        'label': 'Make Confirm',
        'description': 'Can confirm/finalize itineraries',
        'category': 'Proposals',
    },
    'can_view_quotation': {
        'label': 'View Quotation',
        'description': 'Can view and generate quotations',
        'category': 'Proposals',
    },
    'can_change_itinerary_option': {
        'label': 'Change Itinerary Option',
        'description': 'Can change selected pricing option for confirmed itineraries',
        'category': 'Proposals',
    },
    'can_cancel_itinerary': {
        'label': 'Cancel Itinerary',
        'description': 'Can cancel confirmed itineraries',
        'category': 'Proposals',
    },
    'can_set_itinerary_draft': {
        'label': 'Set to Draft',
        'description': 'Can revert confirmed itineraries to draft status',
        'category': 'Proposals',
    },
    'can_generate_quotation': {
        'label': 'Generate Quotation',
        'description': 'Can view and generate quotations',
        'category': 'Itinerary Actions',
    },
    
    # ==========================================
    # ITINERARY BUILDING
    # ==========================================
    'can_view_query_tab': {
        'label': 'View Query Tab',
        'description': 'Can view query details tab',
        'category': 'Itinerary Building',
    },
    'can_access_build_tab': {
        'label': 'Access Build Tab',
        'description': 'Can build and edit itinerary day plans',
        'category': 'Itinerary Building',
    },
    'can_access_pricing_tab': {
        'label': 'Access Pricing Tab',
        'description': 'Can view and manage pricing/costing',
        'category': 'Itinerary Building',
    },
    'can_access_final_tab': {
        'label': 'Access Final Tab',
        'description': 'Can finalize and confirm itinerary',
        'category': 'Itinerary Building',
    },
    
    # ==========================================
    # DAY PLAN MANAGEMENT
    # ==========================================
    'can_manage_destinations': {
        'label': 'Manage Destinations',
        'description': 'Can select and save day destinations (Left Panel)',
        'category': 'Day Plan Management',
    },
    'can_view_saved_items': {
        'label': 'View Saved Items',
        'description': 'Can view booked items for each day (Center Panel)',
        'category': 'Day Plan Management',
    },
    'can_add_items_to_day': {
        'label': 'Add Items to Day',
        'description': 'Can load and add hotels/vehicles/activities (Right Panel)',
        'category': 'Day Plan Management',
    },
    
    # ==========================================
    # ITINERARY MANAGEMENT
    # ==========================================
    'can_edit_bookings': {
        'label': 'Edit Bookings',
        'description': 'Can edit hotel, vehicle, and activity bookings',
        'category': 'Itinerary Management',
    },
    'can_delete_bookings': {
        'label': 'Delete Bookings',
        'description': 'Can delete hotel, vehicle, and activity bookings',
        'category': 'Itinerary Management',
    },
    
    # ==========================================
    # PRICING CONTROLS
    # ==========================================
    'can_edit_item_prices': {
        'label': 'Edit Item Prices',
        'description': 'Can edit net price and markup for items',
        'category': 'Pricing',
    },
    'can_apply_global_markup': {
        'label': 'Apply Global Markup',
        'description': 'Can apply global markup options',
        'category': 'Pricing',
    },
    'can_edit_taxes': {
        'label': 'Edit Taxes',
        'description': 'Can edit CGST and SGST percentages',
        'category': 'Pricing',
    },
    'can_apply_discount': {
        'label': 'Apply Discount',
        'description': 'Can apply discounts to pricing',
        'category': 'Pricing',
    },
    'can_view_item_actions': {
        'label': 'View Item Actions',
        'description': 'Can view and use action buttons (3-dot menu)',
        'category': 'Pricing',
    },
    'can_finalize_pricing': {
        'label': 'Finalize Pricing',
        'description': 'Can save and finalize pricing for itineraries',
        'category': 'Pricing',
    },
    
    # ==========================================
    # ITINERARY ACTIONS
    # ==========================================
    'can_export_itinerary': {
        'label': 'Export Itinerary',
        'description': 'Can export itinerary as PDF/Excel',
        'category': 'Itinerary Actions',
    },
    'can_share_itinerary': {
        'label': 'Share Itinerary',
        'description': 'Can share itinerary with clients',
        'category': 'Itinerary Actions',
    },
    
    # ==========================================
    # ADMINISTRATION & SETTINGS
    # ==========================================
    'can_access_admin_settings': {
        'label': 'Access Admin Settings',
        'description': 'Can access admin settings dashboard',
        'category': 'Administration',
    },
    'can_manage_team_members': {
        'label': 'Manage Team Members',
        'description': 'Can add, edit, and remove team members',
        'category': 'Administration',
    },
    'can_manage_organization': {
        'label': 'Manage Organization',
        'description': 'Can edit organization settings and details',
        'category': 'Administration',
    },
    'can_manage_branches': {
        'label': 'Manage Branches',
        'description': 'Can add and edit branch locations',
        'category': 'Administration',
    },
    'can_manage_roles': {
        'label': 'Manage Roles',
        'description': 'Can create and edit user roles',
        'category': 'Administration',
    },
    'can_manage_business_settings': {
        'label': 'Manage Business Settings',
        'description': 'Can configure business rules and settings',
        'category': 'Administration',
    },
    'can_view_package_details': {
        'label': 'View Package Details',
        'description': 'Can view and edit package details',
        'category': 'Administration',
    },
    
    # ==========================================
    # ✅ ADD AUTO-GENERATED MASTER DATA PERMISSIONS
    # This includes all 13 items with view/add/edit/delete sub-permissions
    # ==========================================
    **GENERATED_MASTER_DATA_PERMISSIONS,
}


def get_permissions_by_category():
    """Group permissions by category for organized display"""
    categories = {}
    for key, value in AVAILABLE_PERMISSIONS.items():
        category = value['category']
        if category not in categories:
            categories[category] = []
        categories[category].append({
            'key': key,
            'label': value['label'],
            'description': value['description'],
        })
    return categories


def get_all_permission_keys():
    """Get list of all permission keys"""
    return list(AVAILABLE_PERMISSIONS.keys())


def get_permission_label(permission_key):
    """Get human-readable label for a permission"""
    permission = AVAILABLE_PERMISSIONS.get(permission_key)
    return permission['label'] if permission else None


def get_permission_description(permission_key):
    """Get description for a permission"""
    permission = AVAILABLE_PERMISSIONS.get(permission_key)
    return permission['description'] if permission else None


def validate_permission(permission_key):
    """Check if a permission key is valid"""
    return permission_key in AVAILABLE_PERMISSIONS
