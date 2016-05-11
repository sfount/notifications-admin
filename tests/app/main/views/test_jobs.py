from flask import url_for
from bs4 import BeautifulSoup
import json
from app.utils import generate_notifications_csv
from tests import notification_json, job_json_with_created_by
from tests.conftest import fake_uuid
from tests.conftest import mock_get_job as mock_get_job1


def test_should_return_list_of_all_jobs(app_,
                                        service_one,
                                        active_user_with_permissions,
                                        mock_get_jobs,
                                        mocker):
    with app_.test_request_context():
        with app_.test_client() as client:
            client.login(active_user_with_permissions, mocker, service_one)
            response = client.get(url_for('main.view_jobs', service_id=service_one['id']))

        assert response.status_code == 200
        page = BeautifulSoup(response.data.decode('utf-8'), 'html.parser')
        assert page.h1.string == 'Notifications activity'
        jobs = page.tbody.find_all('tr')
        assert len(jobs) == 5


def test_should_show_page_for_one_job(
    app_,
    service_one,
    active_user_with_permissions,
    mock_get_service_template,
    mocker,
    mock_get_notifications
):
    data = job_json_with_created_by(service_id=service_one['id'])
    job_id = data['id']
    file_name = data['original_file_name']
    with app_.test_request_context():
        with app_.test_client() as client:
            client.login(active_user_with_permissions, mocker, service_one)
            mock_get_job1(mocker=mocker, job_data=data)
            response = client.get(url_for('main.view_job', service_id=service_one['id'], job_id=job_id))

        assert response.status_code == 200
        content = response.get_data(as_text=True)
        assert "{}: Your vehicle tax is about to expire".format(service_one['name']) in content
        assert file_name in content


def test_should_show_updates_for_one_job_as_json(
    app_,
    service_one,
    active_user_with_permissions,
    mock_get_notifications,
    mocker
):
    job_id = fake_uuid()
    data = job_json_with_created_by(job_id, service_one['id'])
    with app_.test_request_context():
        with app_.test_client() as client:
            client.login(active_user_with_permissions, mocker, service_one)
            mock_get_job1(mocker=mocker, job_data=data)
            response = client.get(url_for('main.view_job_updates', service_id=service_one['id'], job_id=job_id))

        assert response.status_code == 200
        content = json.loads(response.get_data(as_text=True))
        assert 'processed' in content['counts']
        assert 'queued' in content['counts']
        assert 'Recipient' in content['notifications']
        assert 'Status' in content['notifications']
        assert 'Started' in content['status']
        assert 'Created by Test User' in content['status']


def test_should_show_notifications_for_a_service(app_,
                                                 service_one,
                                                 active_user_with_permissions,
                                                 mock_get_notifications,
                                                 mocker):
    with app_.test_request_context():
        with app_.test_client() as client:
            client.login(active_user_with_permissions, mocker, service_one)
            response = client.get(url_for('main.view_notifications', service_id=service_one['id']))
        assert response.status_code == 200
        content = response.get_data(as_text=True)
        notifications = notification_json(service_one['id'])
        notification = notifications['notifications'][0]
        assert notification['to'] in content
        assert notification['status'] in content
        assert notification['template']['name'] in content
        assert '.csv' in content
        page = BeautifulSoup(response.data.decode('utf-8'), 'html.parser')
        assert page.h1.string.strip() == 'Activity'

        mock_get_notifications.assert_called_with(limit_days=7, page=1, service_id=service_one['id'], status=['delivered', 'failed'], template_type=['email', 'sms'])  # noqa


def test_can_view_only_sms_notifications_for_a_service(app_,
                                                       service_one,
                                                       active_user_with_permissions,
                                                       mock_get_notifications,
                                                       mocker):
    with app_.test_request_context():
        with app_.test_client() as client:
            client.login(active_user_with_permissions, mocker, service_one)
            response = client.get(url_for(
                'main.view_notifications',
                service_id=service_one['id'],
                template_type='sms',
                status='delivered,failed'))
        assert response.status_code == 200
        content = response.get_data(as_text=True)

        notifications = notification_json(service_one['id'])
        notification = notifications['notifications'][0]
        assert notification['to'] in content
        assert notification['status'] in content
        assert notification['template']['name'] in content
        assert '.csv' in content
        page = BeautifulSoup(response.data.decode('utf-8'), 'html.parser')
        assert page.h1.string.strip() == 'Text messages'

        mock_get_notifications.assert_called_with(limit_days=7, page=1, service_id=service_one['id'], status=['delivered', 'failed'], template_type=['sms'])  # noqa


def test_can_view_only_email_notifications_for_a_service(app_,
                                                         service_one,
                                                         active_user_with_permissions,
                                                         mock_get_notifications,
                                                         mocker):
    with app_.test_request_context():
        with app_.test_client() as client:
            client.login(active_user_with_permissions, mocker, service_one)
            response = client.get(url_for(
                'main.view_notifications',
                service_id=service_one['id'],
                status='delivered,failed',
                template_type='email'))
        assert response.status_code == 200
        content = response.get_data(as_text=True)

        notifications = notification_json(service_one['id'])
        notification = notifications['notifications'][0]
        assert notification['to'] in content
        assert notification['status'] in content
        assert notification['template']['name'] in content
        assert '.csv' in content
        page = BeautifulSoup(response.data.decode('utf-8'), 'html.parser')
        assert page.h1.string.strip() == 'Emails'

        mock_get_notifications.assert_called_with(limit_days=7, page=1, service_id=service_one['id'], status=['delivered', 'failed'], template_type=['email'])  # noqa


def test_can_view_successful_notifications_for_a_service(app_,
                                                         service_one,
                                                         active_user_with_permissions,
                                                         mock_get_notifications,
                                                         mocker):
    with app_.test_request_context():
        with app_.test_client() as client:
            client.login(active_user_with_permissions, mocker, service_one)
            response = client.get(url_for(
                'main.view_notifications',
                service_id=service_one['id'],
                status='delivered'))
        assert response.status_code == 200
        content = response.get_data(as_text=True)
        notifications = notification_json(service_one['id'])
        notification = notifications['notifications'][0]
        assert notification['to'] in content
        assert notification['status'] in content
        assert notification['template']['name'] in content
        assert '.csv' in content
        page = BeautifulSoup(response.data.decode('utf-8'), 'html.parser')
        assert page.h1.string.strip() == 'Successful  emails and text messages'

        mock_get_notifications.assert_called_with(limit_days=7, page=1, service_id=service_one['id'], status=['delivered'], template_type=['email', 'sms'])  # noqa


def test_can_view_failed_notifications_for_a_service(app_,
                                                     service_one,
                                                     active_user_with_permissions,
                                                     mock_get_notifications,
                                                     mocker):
    with app_.test_request_context():
        with app_.test_client() as client:
            client.login(active_user_with_permissions, mocker, service_one)
            response = client.get(url_for(
                'main.view_notifications',
                service_id=service_one['id'],
                status='failed'))
        assert response.status_code == 200
        content = response.get_data(as_text=True)
        notifications = notification_json(service_one['id'])
        notification = notifications['notifications'][0]
        assert notification['to'] in content
        assert notification['status'] in content
        assert notification['template']['name'] in content
        assert '.csv' in content
        page = BeautifulSoup(response.data.decode('utf-8'), 'html.parser')
        assert page.h1.string.strip() == 'Failed  emails and text messages'

        mock_get_notifications.assert_called_with(limit_days=7, page=1, service_id=service_one['id'], status=['failed'], template_type=['email', 'sms'])  # noqa


def test_can_view_failed_combination_of_notification_type_and_status(
    app_,
    service_one,
    active_user_with_permissions,
    mock_get_notifications,
    mocker
):
    with app_.test_request_context():
        with app_.test_client() as client:
            client.login(active_user_with_permissions, mocker, service_one)
            response = client.get(url_for(
                'main.view_notifications',
                service_id=service_one['id'],
                status='failed',
                template_type='sms'))
        assert response.status_code == 200
        page = BeautifulSoup(response.data.decode('utf-8'), 'html.parser')
        assert page.h1.string.strip() == 'Failed text messages'

        mock_get_notifications.assert_called_with(limit_days=7, page=1, service_id=service_one['id'], status=['failed'], template_type=['sms'])  # noqa


def test_should_show_notifications_for_a_service_with_next_previous(app_,
                                                                    service_one,
                                                                    active_user_with_permissions,
                                                                    mock_get_notifications_with_previous_next,
                                                                    mocker):
    with app_.test_request_context():
        with app_.test_client() as client:
            client.login(active_user_with_permissions, mocker, service_one)
            response = client.get(url_for('main.view_notifications', service_id=service_one['id'], page=2))
        assert response.status_code == 200
        content = response.get_data(as_text=True)
        assert url_for('main.view_notifications', service_id=service_one['id'], page=3) in content
        assert url_for('main.view_notifications', service_id=service_one['id'], page=1) in content
        assert 'Previous page' in content
        assert 'Next page' in content


def test_should_download_notifications_for_a_service(app_,
                                                     service_one,
                                                     active_user_with_permissions,
                                                     mock_get_notifications,
                                                     mocker):
    with app_.test_request_context():
        with app_.test_client() as client:
            client.login(active_user_with_permissions, mocker, service_one)
            response = client.get(url_for(
                'main.view_notifications',
                service_id=service_one['id'],
                download='csv'))
        csv_content = generate_notifications_csv(
            mock_get_notifications(service_one['id'])['notifications'])
        assert response.status_code == 200
        assert response.get_data(as_text=True) == csv_content
        assert 'text/csv' in response.headers['Content-Type']
