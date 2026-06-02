import os
import pytest
from unittest.mock import patch, MagicMock

# Configuration de l'environnement pour éviter que l'import de main.py ne plante
os.environ["REDIS"] = "localhost"

# On mock (simule) Redis pour ne pas avoir besoin d'un vrai serveur Redis pendant les tests
with patch("redis.Redis") as mock_redis, patch("redis.StrictRedis") as mock_strict_redis:
    mock_r = MagicMock()
    mock_redis.return_value = mock_r
    mock_strict_redis.return_value = mock_r
    mock_r.get.return_value = b'0'  # Simule 0 votes
    
    # Maintenant on peut importer main de manière sécurisée
    import main

@pytest.fixture
def client():
    main.app.testing = True
    with main.app.test_client() as client:
        yield client

def test_homepage(client):
    """Vérifie que la page d'accueil charge correctement (Code 200) et affiche Cats et Dogs"""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Cats" in response.data
    assert b"Dogs" in response.data

def test_vote_cats(client):
    """Vérifie que l'action de voter fonctionne et renvoie sur la page d'accueil"""
    response = client.post('/', data={'vote': 'Cats'})
    assert response.status_code == 200
    # Vérifie que la base de données redis a bien reçu l'incrément
    main.r.incr.assert_called_with('Cats', 1)
