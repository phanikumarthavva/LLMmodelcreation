from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    with patch("app.model.pipeline", return_value=MagicMock()):
        from app.main import app

        with TestClient(app) as test_client:
            yield test_client
