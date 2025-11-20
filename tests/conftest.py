"""
Pytest configuration and shared fixtures for Weather CLI tests.

This module provides common test fixtures and configuration that can be
shared across all test modules.
"""

import pytest
import os


@pytest.fixture(autouse=True)
def clean_environment(monkeypatch):
    """
    Automatically clean environment variables before each test.

    This ensures tests don't accidentally use real API keys from the environment.
    """
    # Remove API key from environment if it exists
    monkeypatch.delenv("OPENWEATHER_API_KEY", raising=False)


@pytest.fixture
def mock_api_key():
    """Provide a consistent mock API key for testing."""
    return "mock_test_api_key_abc123"


@pytest.fixture
def real_weather_response():
    """
    Provide a realistic weather API response for testing.

    This fixture represents a typical successful response from OpenWeatherMap API.
    """
    return {
        "coord": {"lon": -0.1257, "lat": 51.5085},
        "weather": [
            {
                "id": 800,
                "main": "Clear",
                "description": "clear sky",
                "icon": "01d"
            }
        ],
        "base": "stations",
        "main": {
            "temp": 18.5,
            "feels_like": 17.8,
            "temp_min": 16.2,
            "temp_max": 20.1,
            "pressure": 1013,
            "humidity": 72
        },
        "visibility": 10000,
        "wind": {
            "speed": 3.6,
            "deg": 230,
            "gust": 5.1
        },
        "clouds": {
            "all": 20
        },
        "dt": 1634567890,
        "sys": {
            "type": 2,
            "id": 2019646,
            "country": "GB",
            "sunrise": 1634537890,
            "sunset": 1634577890
        },
        "timezone": 0,
        "id": 2643743,
        "name": "London",
        "cod": 200
    }


@pytest.fixture
def rainy_weather_response():
    """Provide weather response for rainy conditions."""
    return {
        "coord": {"lon": 2.3522, "lat": 48.8566},
        "weather": [
            {
                "id": 500,
                "main": "Rain",
                "description": "light rain",
                "icon": "10d"
            }
        ],
        "main": {
            "temp": 15.2,
            "feels_like": 14.5,
            "temp_min": 13.8,
            "temp_max": 16.4,
            "pressure": 1008,
            "humidity": 85
        },
        "wind": {
            "speed": 4.2,
            "deg": 270
        },
        "rain": {
            "1h": 2.5
        },
        "clouds": {
            "all": 90
        },
        "sys": {
            "country": "FR"
        },
        "name": "Paris",
        "cod": 200
    }


@pytest.fixture
def snowy_weather_response():
    """Provide weather response for snowy conditions."""
    return {
        "coord": {"lon": 37.6156, "lat": 55.7522},
        "weather": [
            {
                "id": 600,
                "main": "Snow",
                "description": "light snow",
                "icon": "13d"
            }
        ],
        "main": {
            "temp": -5.3,
            "feels_like": -10.2,
            "temp_min": -7.1,
            "temp_max": -3.5,
            "pressure": 1020,
            "humidity": 92
        },
        "wind": {
            "speed": 6.8,
            "deg": 45
        },
        "snow": {
            "1h": 1.2
        },
        "clouds": {
            "all": 100
        },
        "sys": {
            "country": "RU"
        },
        "name": "Moscow",
        "cod": 200
    }


def pytest_configure(config):
    """
    Pytest configuration hook.

    Add custom markers and configuration.
    """
    config.addinivalue_line(
        "markers", "integration: mark test as integration test"
    )
    config.addinivalue_line(
        "markers", "unit: mark test as unit test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )
