from unittest.mock import patch


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@patch("app.main.generate_text", return_value="Hello, world!")
def test_generate(mock_generate, client):
    response = client.post("/generate", json={"prompt": "Hello"})
    assert response.status_code == 200
    data = response.json()
    assert data["prompt"] == "Hello"
    assert data["generated_text"] == "Hello, world!"
    mock_generate.assert_called_once_with("Hello", max_new_tokens=50)


@patch("app.main.generate_text", return_value="Short reply")
def test_generate_custom_max_tokens(mock_generate, client):
    response = client.post("/generate", json={"prompt": "Hi", "max_new_tokens": 10})
    assert response.status_code == 200
    mock_generate.assert_called_once_with("Hi", max_new_tokens=10)


def test_generate_empty_prompt_rejected(client):
    response = client.post("/generate", json={"prompt": ""})
    assert response.status_code == 422
