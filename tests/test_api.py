import os
import pytest

from app import app

from unittest.mock import patch, MagicMock


@pytest.fixture(autouse=True)
def set_env(monkeypatch):
    # ensure tests don't depend on external env
    monkeypatch.setenv('JULES_API_KEY', 'test-key-123')


def test_jules_success(monkeypatch):
    with app.test_client() as c:
        data = {'org': 'myorg', 'repo': 'myrepo', 'branch': 'main', 'title': 't', 'prompt': 'p'}
        with patch('app.requests.post') as mock_post:
            mock_resp = MagicMock()
            mock_resp.raise_for_status.return_value = None
            mock_resp.json.return_value = {'ok': True, 'id': 'session-123'}
            mock_post.return_value = mock_resp

            resp = c.post('/api/jules', json=data)
            assert resp.status_code == 200
            assert 'session-123' in resp.get_data(as_text=True)


def test_jules_bad_request():
    with app.test_client() as c:
        resp = c.post('/api/jules', data='not-json', content_type='text/plain')
        assert resp.status_code == 400
        assert 'Request must be application/json' in resp.get_data(as_text=True)
