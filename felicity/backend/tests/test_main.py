from fastapi import status
from pytest import fixture
from fastapi.testclient import TestClient

if __name__ == '__main__':
    from src.backend.main import app
else:
    from ..src.backend.main import app

@fixture()
def client():
    return TestClient(app)


def test_root(client: TestClient) -> None:
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "hello"}