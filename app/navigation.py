from itertools import chain

from flask import request


class Navigation:

    mapping = {}
    exclude = {}
    selected_attribute = "class=selected"

    def __init__(self):
        self.mapping = {
            navigation: {
                'main.{}'.format(endpoint) for endpoint in endpoints
            } for navigation, endpoints in self.mapping.items()
        }

    @property
    def endpoints_with_navigation(self):
        return tuple(chain.from_iterable((
            endpoints
            for navigation_item, endpoints in self.mapping.items()
        )))

    @property
    def endpoints_without_navigation(self):
        return tuple(
            'main.{}'.format(endpoint) for endpoint in self.exclude
        ) + ('static', 'status.show_status')

    def is_selected(self, navigation_item):
        if request.endpoint in self.mapping[navigation_item]:
            return self.selected_attribute
        return ''


class HeaderNavigation(Navigation):

    selected_attribute = "class=active"

    mapping = {
        'support': {
            'bat_phone',
            'feedback',
            'support',
            'thanks',
            'triage',
        },
        'features': {
            'features',
            'roadmap',
            'security',
            'terms',
            'using_notify',
        },
        'pricing': {
            'pricing',
        },
        'documentation': {
            'documentation',
            'integration_testing',
        },
        'user-profile': {
            'user_profile',
            'user_profile_email',
            'user_profile_email_authenticate',
            'user_profile_email_confirm',
            'user_profile_mobile_number',
            'user_profile_mobile_number_authenticate',
            'user_profile_mobile_number_confirm',
            'user_profile_name',
            'user_profile_password',
        },
        'platform-admin': {
            'add_organisation',
            'create_email_branding',
            'create_letter_branding',
            'email_branding',
            'find_users_by_email',
            'live_services',
            'organisations',
            'platform_admin',
            'platform_admin_letter_validation_preview',
            'platform_admin_list_complaints',
            'platform_admin_returned_letters',
            'suspend_service',
            'trial_services',
            'update_email_branding',
            'user_information',
            'view_provider',
            'view_providers',
        },
        'sign-in': {
            'sign_in',
            'two_factor',
            'two_factor_email',
            'two_factor_email_sent',
            'verify',
            'verify_email',
            'verify_mobile',
        },
    }

    exclude = {
        'accept_invite',
        'accept_org_invite',
        'action_blocked',
        'add_data_retention',
        'add_service',
        'add_service_template',
        'add_template_by_type',
        'add_template_folder',
        'agreement',
        'api_callbacks',
        'api_documentation',
        'api_integration',
        'api_keys',
        'archive_service',
        'branding_request',
        'callbacks',
        'cancel_invited_org_user',
        'cancel_invited_user',
        'cancel_job',
        'cancel_letter',
        'check_and_resend_text_code',
        'check_and_resend_verification_code',
        'check_messages',
        'check_messages_preview',
        'check_notification',
        'check_notification_preview',
        'choose_account',
        'choose_service',
        'choose_template',
        'choose_template_to_copy',
        'confirm_edit_organisation_name',
        'confirm_redact_template',
        'conversation',
        'conversation_reply',
        'conversation_reply_with_template',
        'conversation_updates',
        'cookies',
        'copy_template',
        'create_api_key',
        'data_retention',
        'delete_service_template',
        'delete_template_folder',
        'delivery_and_failure',
        'delivery_status_callback',
        'design_content',
        'download_agreement',
        'download_notifications_csv',
        'edit_data_retention',
        'edit_organisation_name',
        'edit_provider',
        'edit_service_template',
        'edit_template_postage',
        'edit_user_org_permissions',
        'edit_user_permissions',
        'email_not_received',
        'email_template',
        'error',
        'forgot_password',
        'get_example_csv',
        'get_notifications_as_json',
        'go_to_dashboard_after_tour',
        'inbound_sms_admin',
        'inbox',
        'inbox_download',
        'inbox_updates',
        'index',
        'information_risk_management',
        'information_security',
        'invite_org_user',
        'invite_user',
        'link_service_to_organisation',
        'manage_org_users',
        'manage_template_folder',
        'manage_users',
        'monthly',
        'new_password',
        'old_integration_testing',
        'old_roadmap',
        'old_service_dashboard',
        'old_terms',
        'old_using_notify',
        'organisation_dashboard',
        'organisation_settings',
        'privacy',
        'public_agreement',
        'public_download_agreement',
        'received_text_messages_callback',
        'redact_template',
        'register',
        'register_from_invite',
        'register_from_org_invite',
        'registration_continue',
        'remove_user_from_organisation',
        'remove_user_from_service',
        'request_letter_branding',
        'request_to_go_live',
        'resend_email_link',
        'resend_email_verification',
        'resume_service',
        'revoke_api_key',
        'robots',
        'send_messages',
        'send_notification',
        'send_one_off',
        'send_one_off_step',
        'send_test',
        'send_test_preview',
        'send_test_step',
        'service_add_email_reply_to',
        'service_add_letter_contact',
        'service_add_sms_sender',
        'service_confirm_delete_email_reply_to',
        'service_confirm_delete_sms_sender',
        'service_dashboard',
        'service_dashboard_updates',
        'service_delete_email_reply_to',
        'service_delete_sms_sender',
        'service_edit_email_reply_to',
        'service_edit_letter_contact',
        'service_edit_sms_sender',
        'service_email_reply_to',
        'service_letter_contact_details',
        'service_name_change',
        'service_name_change_confirm',
        'service_preview_email_branding',
        'service_set_auth_type',
        'service_set_channel',
        'service_set_contact_link',
        'service_set_email_branding',
        'service_set_inbound_number',
        'service_set_inbound_sms',
        'service_set_international_sms',
        'service_set_letter_contact_block',
        'service_set_letters',
        'service_set_reply_to_email',
        'service_set_sms_prefix',
        'service_settings',
        'service_sms_senders',
        'service_switch_can_send_precompiled_letter',
        'service_switch_can_upload_document',
        'service_switch_email_auth',
        'service_switch_live',
        'service_switch_research_mode',
        'services_or_dashboard',
        'set_free_sms_allowance',
        'service_set_letter_branding',
        'set_organisation_type',
        'set_sender',
        'set_template_sender',
        'show_accounts_or_dashboard',
        'sign_out',
        'start_job',
        'start_tour',
        'styleguide',
        'submit_request_to_go_live',
        'temp_service_history',
        'template_history',
        'template_usage',
        'trial_mode',
        'usage',
        'view_job',
        'view_job_csv',
        'view_job_updates',
        'view_jobs',
        'view_letter_notification_as_preview',
        'view_letter_template_preview',
        'view_notification',
        'view_notification_updates',
        'view_notifications',
        'view_notifications_csv',
        'view_template',
        'view_template_version',
        'view_template_version_preview',
        'view_template_versions',
        'whitelist',
    }


class MainNavigation(Navigation):

    mapping = {
        'dashboard': {
            'conversation',
            'inbox',
            'monthly',
            'service_dashboard',
            'template_usage',
            'view_job',
            'view_jobs',
            'view_notification',
            'view_notifications',
        },
        'templates': {
            'action_blocked',
            'add_service_template',
            'add_template_by_type',
            'add_template_folder',
            'check_messages',
            'check_notification',
            'choose_template',
            'choose_template_to_copy',
            'confirm_redact_template',
            'conversation_reply',
            'copy_template',
            'delete_service_template',
            'edit_service_template',
            'edit_template_postage',
            'manage_template_folder',
            'send_messages',
            'send_one_off',
            'send_one_off_step',
            'send_test',
            'send_test_preview',
            'send_test_step',
            'set_sender',
            'set_template_sender',
            'view_template',
            'view_template_version',
            'view_template_versions',
        },
        'team-members': {
            'edit_user_permissions',
            'invite_user',
            'manage_users',
            'remove_user_from_service',
        },
        'usage': {
            'usage',
        },
        'settings': {
            'branding_request',
            'link_service_to_organisation',
            'request_letter_branding',
            'request_to_go_live',
            'service_add_email_reply_to',
            'service_add_letter_contact',
            'service_add_sms_sender',
            'service_confirm_delete_email_reply_to',
            'service_confirm_delete_sms_sender',
            'service_edit_email_reply_to',
            'service_edit_letter_contact',
            'service_edit_sms_sender',
            'service_email_reply_to',
            'service_letter_contact_details',
            'service_name_change',
            'service_name_change_confirm',
            'service_preview_email_branding',
            'service_set_auth_type',
            'service_set_channel',
            'service_set_contact_link',
            'service_set_email_branding',
            'service_set_inbound_number',
            'service_set_inbound_sms',
            'service_set_international_sms',
            'service_set_letter_contact_block',
            'service_set_letters',
            'service_set_reply_to_email',
            'service_set_sms_prefix',
            'service_settings',
            'service_sms_senders',
            'set_free_sms_allowance',
            'service_set_letter_branding',
            'set_organisation_type',
            'submit_request_to_go_live',
        },
        'api-integration': {
            'api_callbacks',
            'api_documentation',
            'api_integration',
            'api_keys',
            'create_api_key',
            'delivery_status_callback',
            'received_text_messages_callback',
            'revoke_api_key',
            'whitelist',
        },
    }

    exclude = {
        'accept_invite',
        'accept_org_invite',
        'add_data_retention',
        'add_organisation',
        'add_service',
        'agreement',
        'archive_service',
        'bat_phone',
        'callbacks',
        'cancel_invited_org_user',
        'cancel_invited_user',
        'cancel_job',
        'cancel_letter',
        'check_and_resend_text_code',
        'check_and_resend_verification_code',
        'check_messages_preview',
        'check_notification_preview',
        'choose_account',
        'choose_service',
        'confirm_edit_organisation_name',
        'conversation_reply_with_template',
        'conversation_updates',
        'cookies',
        'create_email_branding',
        'create_letter_branding',
        'data_retention',
        'delete_template_folder',
        'delivery_and_failure',
        'design_content',
        'documentation',
        'download_agreement',
        'download_notifications_csv',
        'edit_data_retention',
        'edit_organisation_name',
        'edit_provider',
        'edit_user_org_permissions',
        'email_branding',
        'email_not_received',
        'email_template',
        'error',
        'features',
        'feedback',
        'find_users_by_email',
        'forgot_password',
        'get_example_csv',
        'get_notifications_as_json',
        'go_to_dashboard_after_tour',
        'inbound_sms_admin',
        'inbox_download',
        'inbox_updates',
        'index',
        'information_risk_management',
        'information_security',
        'integration_testing',
        'invite_org_user',
        'live_services',
        'manage_org_users',
        'new_password',
        'old_integration_testing',
        'old_roadmap',
        'old_service_dashboard',
        'old_terms',
        'old_using_notify',
        'organisation_dashboard',
        'organisation_settings',
        'organisations',
        'platform_admin',
        'platform_admin_letter_validation_preview',
        'platform_admin_list_complaints',
        'platform_admin_returned_letters',
        'pricing',
        'privacy',
        'public_agreement',
        'public_download_agreement',
        'redact_template',
        'register',
        'register_from_invite',
        'register_from_org_invite',
        'registration_continue',
        'remove_user_from_organisation',
        'resend_email_link',
        'resend_email_verification',
        'resume_service',
        'roadmap',
        'robots',
        'security',
        'send_notification',
        'service_dashboard_updates',
        'service_delete_email_reply_to',
        'service_delete_sms_sender',
        'service_switch_can_send_precompiled_letter',
        'service_switch_can_upload_document',
        'service_switch_email_auth',
        'service_switch_live',
        'service_switch_research_mode',
        'services_or_dashboard',
        'show_accounts_or_dashboard',
        'sign_in',
        'sign_out',
        'start_job',
        'start_tour',
        'styleguide',
        'support',
        'suspend_service',
        'temp_service_history',
        'template_history',
        'terms',
        'thanks',
        'triage',
        'trial_mode',
        'trial_services',
        'two_factor',
        'two_factor_email',
        'two_factor_email_sent',
        'update_email_branding',
        'user_information',
        'user_profile',
        'user_profile_email',
        'user_profile_email_authenticate',
        'user_profile_email_confirm',
        'user_profile_mobile_number',
        'user_profile_mobile_number_authenticate',
        'user_profile_mobile_number_confirm',
        'user_profile_name',
        'user_profile_password',
        'using_notify',
        'verify',
        'verify_email',
        'verify_mobile',
        'view_job_csv',
        'view_job_updates',
        'view_letter_notification_as_preview',
        'view_letter_template_preview',
        'view_notification_updates',
        'view_notifications_csv',
        'view_provider',
        'view_providers',
        'view_template_version_preview',
    }


class CaseworkNavigation(Navigation):

    mapping = {
        'send-one-off': {
            'choose_template',
            'send_one_off',
            'send_one_off_step',
            'send_test',
            'send_test_step',
        },
        'sent-messages': {
            'view_notifications',
            'view_notification',
        },
        'uploaded-files': {
            'view_jobs',
            'view_job',
        },
    }

    exclude = {
        'accept_invite',
        'accept_org_invite',
        'action_blocked',
        'add_data_retention',
        'add_organisation',
        'add_service',
        'add_service_template',
        'add_template_by_type',
        'add_template_folder',
        'agreement',
        'api_callbacks',
        'api_documentation',
        'api_integration',
        'api_keys',
        'archive_service',
        'bat_phone',
        'branding_request',
        'callbacks',
        'cancel_invited_org_user',
        'cancel_invited_user',
        'cancel_job',
        'cancel_letter',
        'check_and_resend_text_code',
        'check_and_resend_verification_code',
        'check_messages',
        'check_messages_preview',
        'check_notification',
        'check_notification_preview',
        'choose_account',
        'choose_service',
        'choose_template_to_copy',
        'confirm_edit_organisation_name',
        'confirm_redact_template',
        'conversation',
        'conversation_reply',
        'conversation_reply_with_template',
        'conversation_updates',
        'cookies',
        'copy_template',
        'create_api_key',
        'create_email_branding',
        'create_letter_branding',
        'data_retention',
        'delete_service_template',
        'delete_template_folder',
        'delivery_and_failure',
        'delivery_status_callback',
        'design_content',
        'documentation',
        'download_agreement',
        'download_notifications_csv',
        'edit_data_retention',
        'edit_organisation_name',
        'edit_provider',
        'edit_service_template',
        'edit_template_postage',
        'edit_user_org_permissions',
        'edit_user_permissions',
        'email_branding',
        'email_not_received',
        'email_template',
        'error',
        'features',
        'feedback',
        'find_users_by_email',
        'forgot_password',
        'get_example_csv',
        'get_notifications_as_json',
        'go_to_dashboard_after_tour',
        'inbound_sms_admin',
        'inbox',
        'inbox_download',
        'inbox_updates',
        'index',
        'information_risk_management',
        'information_security',
        'integration_testing',
        'invite_org_user',
        'invite_user',
        'link_service_to_organisation',
        'live_services',
        'manage_org_users',
        'manage_template_folder',
        'manage_users',
        'monthly',
        'new_password',
        'old_integration_testing',
        'old_roadmap',
        'old_service_dashboard',
        'old_terms',
        'old_using_notify',
        'organisation_dashboard',
        'organisation_settings',
        'organisations',
        'platform_admin',
        'platform_admin_letter_validation_preview',
        'platform_admin_list_complaints',
        'platform_admin_returned_letters',
        'pricing',
        'privacy',
        'public_agreement',
        'public_download_agreement',
        'received_text_messages_callback',
        'redact_template',
        'register',
        'register_from_invite',
        'register_from_org_invite',
        'registration_continue',
        'remove_user_from_organisation',
        'remove_user_from_service',
        'request_letter_branding',
        'request_to_go_live',
        'resend_email_link',
        'resend_email_verification',
        'resume_service',
        'revoke_api_key',
        'roadmap',
        'robots',
        'security',
        'send_messages',
        'send_notification',
        'send_test_preview',
        'service_add_email_reply_to',
        'service_add_letter_contact',
        'service_add_sms_sender',
        'service_confirm_delete_email_reply_to',
        'service_confirm_delete_sms_sender',
        'service_dashboard',
        'service_dashboard_updates',
        'service_delete_email_reply_to',
        'service_delete_sms_sender',
        'service_edit_email_reply_to',
        'service_edit_letter_contact',
        'service_edit_sms_sender',
        'service_email_reply_to',
        'service_letter_contact_details',
        'service_name_change',
        'service_name_change_confirm',
        'service_preview_email_branding',
        'service_set_auth_type',
        'service_set_channel',
        'service_set_contact_link',
        'service_set_email_branding',
        'service_set_inbound_number',
        'service_set_inbound_sms',
        'service_set_international_sms',
        'service_set_letter_contact_block',
        'service_set_letters',
        'service_set_reply_to_email',
        'service_set_sms_prefix',
        'service_settings',
        'service_sms_senders',
        'service_switch_can_send_precompiled_letter',
        'service_switch_can_upload_document',
        'service_switch_email_auth',
        'service_switch_live',
        'service_switch_research_mode',
        'services_or_dashboard',
        'set_free_sms_allowance',
        'service_set_letter_branding',
        'set_organisation_type',
        'set_sender',
        'set_template_sender',
        'show_accounts_or_dashboard',
        'sign_in',
        'sign_out',
        'start_job',
        'start_tour',
        'styleguide',
        'submit_request_to_go_live',
        'support',
        'suspend_service',
        'temp_service_history',
        'template_history',
        'template_usage',
        'terms',
        'thanks',
        'triage',
        'trial_mode',
        'trial_services',
        'two_factor',
        'two_factor_email',
        'two_factor_email_sent',
        'update_email_branding',
        'usage',
        'user_information',
        'user_profile',
        'user_profile_email',
        'user_profile_email_authenticate',
        'user_profile_email_confirm',
        'user_profile_mobile_number',
        'user_profile_mobile_number_authenticate',
        'user_profile_mobile_number_confirm',
        'user_profile_name',
        'user_profile_password',
        'using_notify',
        'verify',
        'verify_email',
        'verify_mobile',
        'view_job_csv',
        'view_job_updates',
        'view_letter_notification_as_preview',
        'view_letter_template_preview',
        'view_notification_updates',
        'view_notifications_csv',
        'view_provider',
        'view_providers',
        'view_template',
        'view_template_version',
        'view_template_version_preview',
        'view_template_versions',
        'whitelist',
    }


class OrgNavigation(Navigation):

    mapping = {
        'dashboard': {
            'organisation_dashboard',
        },
        'settings': {
            'confirm_edit_organisation_name',
            'edit_organisation_name',
            'organisation_settings',
        },
        'team-members': {
            'edit_user_org_permissions',
            'invite_org_user',
            'manage_org_users',
            'remove_user_from_organisation',
        }
    }

    exclude = {
        'accept_invite',
        'accept_org_invite',
        'action_blocked',
        'add_data_retention',
        'add_organisation',
        'add_service',
        'add_service_template',
        'add_template_by_type',
        'add_template_folder',
        'agreement',
        'api_callbacks',
        'api_documentation',
        'api_integration',
        'api_keys',
        'archive_service',
        'bat_phone',
        'branding_request',
        'callbacks',
        'cancel_invited_org_user',
        'cancel_invited_user',
        'cancel_job',
        'cancel_letter',
        'check_and_resend_text_code',
        'check_and_resend_verification_code',
        'check_messages',
        'check_messages_preview',
        'check_notification',
        'check_notification_preview',
        'choose_account',
        'choose_service',
        'choose_template',
        'choose_template_to_copy',
        'confirm_redact_template',
        'conversation',
        'conversation_reply',
        'conversation_reply_with_template',
        'conversation_updates',
        'cookies',
        'copy_template',
        'create_api_key',
        'create_email_branding',
        'create_letter_branding',
        'data_retention',
        'delete_service_template',
        'delete_template_folder',
        'delivery_and_failure',
        'delivery_status_callback',
        'design_content',
        'documentation',
        'download_agreement',
        'download_notifications_csv',
        'edit_data_retention',
        'edit_provider',
        'edit_service_template',
        'edit_template_postage',
        'edit_user_permissions',
        'email_branding',
        'email_not_received',
        'email_template',
        'error',
        'features',
        'feedback',
        'find_users_by_email',
        'forgot_password',
        'get_example_csv',
        'get_notifications_as_json',
        'go_to_dashboard_after_tour',
        'inbound_sms_admin',
        'inbox',
        'inbox_download',
        'inbox_updates',
        'index',
        'information_risk_management',
        'information_security',
        'integration_testing',
        'invite_user',
        'link_service_to_organisation',
        'live_services',
        'manage_template_folder',
        'manage_users',
        'monthly',
        'new_password',
        'old_integration_testing',
        'old_roadmap',
        'old_service_dashboard',
        'old_terms',
        'old_using_notify',
        'organisations',
        'platform_admin',
        'platform_admin_letter_validation_preview',
        'platform_admin_list_complaints',
        'platform_admin_returned_letters',
        'pricing',
        'privacy',
        'public_agreement',
        'public_download_agreement',
        'received_text_messages_callback',
        'redact_template',
        'register',
        'register_from_invite',
        'register_from_org_invite',
        'registration_continue',
        'remove_user_from_service',
        'request_letter_branding',
        'request_to_go_live',
        'resend_email_link',
        'resend_email_verification',
        'resume_service',
        'revoke_api_key',
        'roadmap',
        'robots',
        'security',
        'send_messages',
        'send_notification',
        'send_one_off',
        'send_one_off_step',
        'send_test',
        'send_test_preview',
        'send_test_step',
        'service_add_email_reply_to',
        'service_add_letter_contact',
        'service_add_sms_sender',
        'service_confirm_delete_email_reply_to',
        'service_confirm_delete_sms_sender',
        'service_dashboard',
        'service_dashboard_updates',
        'service_delete_email_reply_to',
        'service_delete_sms_sender',
        'service_edit_email_reply_to',
        'service_edit_letter_contact',
        'service_edit_sms_sender',
        'service_email_reply_to',
        'service_letter_contact_details',
        'service_name_change',
        'service_name_change_confirm',
        'service_preview_email_branding',
        'service_set_auth_type',
        'service_set_channel',
        'service_set_contact_link',
        'service_set_email_branding',
        'service_set_inbound_number',
        'service_set_inbound_sms',
        'service_set_international_sms',
        'service_set_letter_contact_block',
        'service_set_letters',
        'service_set_reply_to_email',
        'service_set_sms_prefix',
        'service_settings',
        'service_sms_senders',
        'service_switch_can_send_precompiled_letter',
        'service_switch_can_upload_document',
        'service_switch_email_auth',
        'service_switch_live',
        'service_switch_research_mode',
        'services_or_dashboard',
        'set_free_sms_allowance',
        'service_set_letter_branding',
        'set_organisation_type',
        'set_sender',
        'set_template_sender',
        'show_accounts_or_dashboard',
        'sign_in',
        'sign_out',
        'start_job',
        'start_tour',
        'styleguide',
        'submit_request_to_go_live',
        'support',
        'suspend_service',
        'temp_service_history',
        'template_history',
        'template_usage',
        'terms',
        'thanks',
        'triage',
        'trial_mode',
        'trial_services',
        'two_factor',
        'two_factor_email',
        'two_factor_email_sent',
        'update_email_branding',
        'usage',
        'user_information',
        'user_profile',
        'user_profile_email',
        'user_profile_email_authenticate',
        'user_profile_email_confirm',
        'user_profile_mobile_number',
        'user_profile_mobile_number_authenticate',
        'user_profile_mobile_number_confirm',
        'user_profile_name',
        'user_profile_password',
        'using_notify',
        'verify',
        'verify_email',
        'verify_mobile',
        'view_job',
        'view_job_csv',
        'view_job_updates',
        'view_jobs',
        'view_letter_notification_as_preview',
        'view_letter_template_preview',
        'view_notification',
        'view_notification_updates',
        'view_notifications',
        'view_notifications_csv',
        'view_provider',
        'view_providers',
        'view_template',
        'view_template_version',
        'view_template_version_preview',
        'view_template_versions',
        'whitelist',
    }
