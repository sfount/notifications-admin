import pytest
from bs4 import BeautifulSoup
from flask import url_for
from freezegun import freeze_time

from tests.conftest import (
    SERVICE_ONE_ID,
    normalize_spaces,
    set_config,
    url_for_endpoint_with_token,
)


def test_should_render_two_factor_page(
    client,
    api_user_active,
    mock_get_user_by_email,
    mocker
):
    # TODO this lives here until we work out how to
    # reassign the session after it is lost mid register process
    with client.session_transaction() as session:
        session['user_details'] = {
            'id': api_user_active['id'],
            'email': api_user_active['email_address']}
    mocker.patch('app.user_api_client.get_user', return_value=api_user_active)
    response = client.get(url_for('main.two_factor'))
    assert response.status_code == 200
    page = BeautifulSoup(response.data.decode('utf-8'), 'html.parser')
    assert page.select_one('main p').text.strip() == (
        'We’ve sent you a text message with a security code.'
    )
    assert page.select_one('label').text.strip() == (
        'Text message code'
    )
    assert page.select_one('input')['type'] == 'tel'
    assert page.select_one('input')['pattern'] == '[0-9]*'


@freeze_time('2020-01-27T12:00:00')
def test_should_login_user_and_should_redirect_to_next_url(
    client,
    api_user_active,
    mock_get_user,
    mock_get_user_by_email,
    mock_check_verify_code,
    mock_create_event,
):
    with client.session_transaction() as session:
        session['user_details'] = {
            'id': api_user_active['id'],
            'email': api_user_active['email_address']}
    api_user_active['email_access_validated_at'] = '2020-01-23T11:35:21.726132Z'

    response = client.post(url_for('main.two_factor', next='/services/{}'.format(SERVICE_ONE_ID)),
                           data={'sms_code': '12345'})
    assert response.status_code == 302
    assert response.location == url_for(
        'main.service_dashboard',
        service_id=SERVICE_ONE_ID,
        _external=True
    )


@freeze_time('2020-01-27T12:00:00')
def test_should_send_email_and_redirect_to_info_page_if_user_needs_to_revalidate_email(
    client,
    api_user_active,
    mock_get_user,
    mock_check_verify_code,
    mock_create_event,
    mock_send_verify_code,
    mocker
):
    mocker.patch('app.user_api_client.get_user', return_value=api_user_active)
    api_user_active['email_access_validated_at'] = '2019-03-23T11:35:21.726132Z'
    with client.session_transaction() as session:
        session['user_details'] = {
            'id': api_user_active['id'],
            'email': api_user_active['email_address']}
    response = client.post(url_for('main.two_factor', next='/services/{}'.format(SERVICE_ONE_ID)),
                           data={'sms_code': '12345'})

    assert response.status_code == 302
    assert response.location == url_for('main.revalidate_email_sent', _external=True)
    mock_send_verify_code.assert_called_with(api_user_active['id'], 'email', None, mocker.ANY)


@freeze_time('2020-01-27T12:00:00')
def test_should_login_user_and_not_redirect_to_external_url(
    client,
    api_user_active,
    mock_get_user,
    mock_get_user_by_email,
    mock_check_verify_code,
    mock_get_services_with_one_service,
    mock_create_event,
):
    with client.session_transaction() as session:
        session['user_details'] = {
            'id': api_user_active['id'],
            'email': api_user_active['email_address']}
    api_user_active['email_access_validated_at'] = '2020-01-23T11:35:21.726132Z'

    response = client.post(url_for('main.two_factor', next='http://www.google.com'),
                           data={'sms_code': '12345'})
    assert response.status_code == 302
    assert response.location == url_for('main.show_accounts_or_dashboard', _external=True)


@pytest.mark.parametrize('platform_admin', (
    True, False,
))
@freeze_time('2020-01-27T12:00:00')
def test_should_login_user_and_redirect_to_show_accounts(
    client,
    api_user_active,
    mock_get_user,
    mock_get_user_by_email,
    mock_check_verify_code,
    mock_create_event,
    platform_admin,
):
    with client.session_transaction() as session:
        session['user_details'] = {
            'id': api_user_active['id'],
            'email': api_user_active['email_address']}
    api_user_active['email_access_validated_at'] = '2020-01-23T11:35:21.726132Z'
    api_user_active['platform_admin'] = platform_admin

    response = client.post(url_for('main.two_factor'),
                           data={'sms_code': '12345'})

    assert response.status_code == 302
    assert response.location == url_for('main.show_accounts_or_dashboard', _external=True)


def test_should_return_200_with_sms_code_error_when_sms_code_is_wrong(
    client,
    api_user_active,
    mock_get_user_by_email,
    mock_check_verify_code_code_not_found,
    mocker
):
    with client.session_transaction() as session:
        session['user_details'] = {
            'id': api_user_active['id'],
            'email': api_user_active['email_address']}
    mocker.patch('app.user_api_client.get_user', return_value=api_user_active)

    response = client.post(url_for('main.two_factor'),
                           data={'sms_code': '23456'})
    assert response.status_code == 200
    assert 'Code not found' in response.get_data(as_text=True)


@freeze_time('2020-01-27T12:00:00')
def test_should_login_user_when_multiple_valid_codes_exist(
    client,
    api_user_active,
    mock_get_user,
    mock_get_user_by_email,
    mock_check_verify_code,
    mock_get_services_with_one_service,
    mock_create_event,
):
    with client.session_transaction() as session:
        session['user_details'] = {
            'id': api_user_active['id'],
            'email': api_user_active['email_address']}
    api_user_active['email_access_validated_at'] = '2020-01-23T11:35:21.726132Z'

    response = client.post(url_for('main.two_factor'),
                           data={'sms_code': '23456'})
    assert response.status_code == 302


@freeze_time('2020-01-27T12:00:00')
def test_two_factor_should_set_password_when_new_password_exists_in_session(
    client,
    api_user_active,
    mock_get_user,
    mock_check_verify_code,
    mock_get_services_with_one_service,
    mock_update_user_password,
    mock_create_event,
):
    with client.session_transaction() as session:
        session['user_details'] = {
            'id': api_user_active['id'],
            'email': api_user_active['email_address'],
            'password': 'changedpassword'}
    api_user_active['email_access_validated_at'] = '2020-01-23T11:35:21.726132Z'

    response = client.post(url_for('main.two_factor'),
                           data={'sms_code': '12345'})
    assert response.status_code == 302
    assert response.location == url_for('main.show_accounts_or_dashboard', _external=True)

    mock_update_user_password.assert_called_once_with(
        api_user_active['id'], 'changedpassword', validated_email_access=True
    )


def test_two_factor_returns_error_when_user_is_locked(
    client,
    api_user_locked,
    mock_get_locked_user,
    mock_check_verify_code_code_not_found,
    mock_get_services_with_one_service
):
    with client.session_transaction() as session:
        session['user_details'] = {
            'id': api_user_locked['id'],
            'email': api_user_locked['email_address'],
        }
    response = client.post(url_for('main.two_factor'),
                           data={'sms_code': '12345'})
    assert response.status_code == 200
    assert 'Code not found' in response.get_data(as_text=True)


def test_two_factor_should_redirect_to_sign_in_if_user_not_in_session(
    client,
    api_user_active,
    mock_get_user,
):
    response = client.post(url_for('main.two_factor'),
                           data={'sms_code': '12345'})
    assert response.status_code == 302
    assert response.location == url_for('main.sign_in', _external=True)


@freeze_time('2020-01-27T12:00:00')
def test_two_factor_should_activate_pending_user(
    client,
    mocker,
    api_user_pending,
    mock_check_verify_code,
    mock_create_event,
    mock_activate_user,
):
    mocker.patch('app.user_api_client.get_user', return_value=api_user_pending)
    mocker.patch('app.service_api_client.get_services', return_value={'data': []})
    api_user_pending['email_access_validated_at'] = '2020-01-23T11:35:21.726132Z'
    with client.session_transaction() as session:
        session['user_details'] = {
            'id': api_user_pending['id'],
            'email_address': api_user_pending['email_address']
        }
    client.post(url_for('main.two_factor'), data={'sms_code': '12345'})

    assert mock_activate_user.called


@pytest.mark.parametrize('extra_args, expected_encoded_next_arg', (
    ({}, ''),
    ({'next': 'https://example.com'}, '?next=https%3A%2F%2Fexample.com')
))
def test_valid_two_factor_email_link_shows_interstitial(
    client_request,
    valid_token,
    mocker,
    extra_args,
    expected_encoded_next_arg,
):
    mock_check_code = mocker.patch('app.user_api_client.check_verify_code')
    encoded_token = valid_token.replace('%2E', '.')
    token_url = url_for(
        'main.two_factor_email_interstitial',
        token=encoded_token,
        **extra_args
    )

    # This must match the URL we put in the emails
    assert token_url == f'/email-auth/{encoded_token}{expected_encoded_next_arg}'

    client_request.logout()
    page = client_request.get_url(token_url)

    assert normalize_spaces(page.select_one('main .js-hidden').text) == (
        'Sign in '
        'Continue to dashboard'
    )

    form = page.select_one('form')
    expected_form_id = 'use-email-auth'
    assert 'action' not in form
    assert form['method'] == 'post'
    assert form['id'] == expected_form_id
    assert page.select_one('main script').text.strip() == (
        f'document.getElementById("{expected_form_id}").submit();'
    )

    assert mock_check_code.called is False


def test_valid_two_factor_email_link_logs_in_user(
    client,
    valid_token,
    mock_get_user,
    mock_get_services_with_one_service,
    mocker,
    mock_create_event,
):
    mocker.patch('app.user_api_client.check_verify_code', return_value=(True, ''))

    response = client.post(
        url_for_endpoint_with_token('main.two_factor_email', token=valid_token),
    )

    assert response.status_code == 302
    assert response.location == url_for('main.show_accounts_or_dashboard', _external=True)


def test_two_factor_email_link_has_expired(
    app_,
    valid_token,
    client,
    mock_send_verify_code,
    fake_uuid
):

    with set_config(app_, 'EMAIL_2FA_EXPIRY_SECONDS', -1):
        response = client.post(
            url_for_endpoint_with_token('main.two_factor_email', token=valid_token),
            follow_redirects=True,
        )

    assert response.status_code == 200
    page = BeautifulSoup(response.data.decode('utf-8'), 'html.parser')

    assert page.h1.text.strip() == 'The link has expired'
    assert mock_send_verify_code.called is False


def test_two_factor_email_link_is_invalid(
    client
):
    token = 12345
    response = client.post(
        url_for('main.two_factor_email', token=token),
        follow_redirects=True
    )
    page = BeautifulSoup(response.data.decode('utf-8'), 'html.parser')
    assert normalize_spaces(
        page.select_one('.banner-dangerous').text
    ) == "There’s something wrong with the link you’ve used."
    assert response.status_code == 404


def test_two_factor_email_link_is_already_used(
    client,
    valid_token,
    mocker,
    mock_send_verify_code

):
    mocker.patch('app.user_api_client.check_verify_code', return_value=(False, 'Code has expired'))

    response = client.post(
        url_for_endpoint_with_token('main.two_factor_email', token=valid_token),
        follow_redirects=True
    )

    page = BeautifulSoup(response.data.decode('utf-8'), 'html.parser')
    assert response.status_code == 200

    assert page.h1.text.strip() == 'The link has expired'
    assert mock_send_verify_code.called is False


def test_two_factor_email_link_when_user_is_locked_out(
    client,
    valid_token,
    mocker,
    mock_send_verify_code
):
    mocker.patch('app.user_api_client.check_verify_code', return_value=(False, 'Code not found'))

    response = client.post(
        url_for_endpoint_with_token('main.two_factor_email', token=valid_token),
        follow_redirects=True
    )

    page = BeautifulSoup(response.data.decode('utf-8'), 'html.parser')
    assert response.status_code == 200

    assert page.h1.text.strip() == 'The link has expired'
    assert mock_send_verify_code.called is False


def test_two_factor_email_link_used_when_user_already_logged_in(
    logged_in_client,
    valid_token
):
    response = logged_in_client.post(
        url_for_endpoint_with_token('main.two_factor_email', token=valid_token)
    )
    assert response.status_code == 302
    assert response.location == url_for('main.show_accounts_or_dashboard', _external=True)
