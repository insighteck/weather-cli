"""
Comprehensive unit tests for the Weather CLI application.

This test suite includes:
- Mocked API responses for various scenarios
- Error handling tests
- Input validation tests
- Output formatting tests
- Edge case handling
"""

import os
import sys
import pytest
from unittest.mock import patch, Mock, MagicMock
import requests

# Add parent directory to path to import the module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from weather_cli import WeatherCLI, WeatherAPIError, main


# Test Fixtures
@pytest.fixture
def api_key():
    """Provide a test API key."""
    return "test_api_key_12345"


@pytest.fixture
def weather_cli(api_key):
    """Create a WeatherCLI instance with a test API key."""
    return WeatherCLI(api_key=api_key)


@pytest.fixture
def sample_weather_response():
    """Sample successful weather API response."""
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
            "deg": 230
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
def sample_weather_response_imperial():
    """Sample weather API response with imperial units."""
    return {
        "coord": {"lon": -74.006, "lat": 40.7143},
        "weather": [
            {
                "id": 801,
                "main": "Clouds",
                "description": "few clouds",
                "icon": "02d"
            }
        ],
        "main": {
            "temp": 65.3,
            "feels_like": 64.2,
            "temp_min": 62.5,
            "temp_max": 68.0,
            "pressure": 1015,
            "humidity": 68
        },
        "wind": {
            "speed": 8.5,
            "deg": 180
        },
        "clouds": {
            "all": 15
        },
        "sys": {
            "country": "US"
        },
        "name": "New York",
        "cod": 200
    }


# Initialization Tests
class TestWeatherCLIInitialization:
    """Test WeatherCLI initialization and configuration."""

    def test_init_with_api_key(self, api_key):
        """Test initialization with explicit API key."""
        cli = WeatherCLI(api_key=api_key)
        assert cli.api_key == api_key

    def test_init_with_env_variable(self, api_key, monkeypatch):
        """Test initialization with API key from environment variable."""
        monkeypatch.setenv("OPENWEATHER_API_KEY", api_key)
        cli = WeatherCLI()
        assert cli.api_key == api_key

    def test_init_without_api_key(self, monkeypatch):
        """Test initialization fails without API key."""
        monkeypatch.delenv("OPENWEATHER_API_KEY", raising=False)
        with pytest.raises(WeatherAPIError) as exc_info:
            WeatherCLI()
        assert "No API key provided" in str(exc_info.value)

    def test_init_env_variable_precedence(self, monkeypatch):
        """Test that explicit API key takes precedence over environment variable."""
        monkeypatch.setenv("OPENWEATHER_API_KEY", "env_key")
        cli = WeatherCLI(api_key="explicit_key")
        assert cli.api_key == "explicit_key"


# API Request Tests
class TestWeatherAPIRequests:
    """Test weather API request functionality."""

    @patch('weather_cli.requests.get')
    def test_get_weather_success(self, mock_get, weather_cli, sample_weather_response):
        """Test successful weather data retrieval."""
        mock_response = Mock()
        mock_response.json.return_value = sample_weather_response
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        result = weather_cli.get_weather("London")

        assert result == sample_weather_response
        mock_get.assert_called_once()
        call_args = mock_get.call_args
        assert call_args[0][0] == WeatherCLI.BASE_URL
        assert call_args[1]['params']['q'] == "London"
        assert call_args[1]['params']['appid'] == weather_cli.api_key
        assert call_args[1]['params']['units'] == "metric"

    @patch('weather_cli.requests.get')
    def test_get_weather_with_imperial_units(self, mock_get, weather_cli, sample_weather_response_imperial):
        """Test weather retrieval with imperial units."""
        mock_response = Mock()
        mock_response.json.return_value = sample_weather_response_imperial
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        result = weather_cli.get_weather("New York", units="imperial")

        assert result == sample_weather_response_imperial
        call_args = mock_get.call_args
        assert call_args[1]['params']['units'] == "imperial"

    @patch('weather_cli.requests.get')
    def test_get_weather_with_standard_units(self, mock_get, weather_cli, sample_weather_response):
        """Test weather retrieval with standard (Kelvin) units."""
        mock_response = Mock()
        mock_response.json.return_value = sample_weather_response
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        weather_cli.get_weather("Tokyo", units="standard")

        call_args = mock_get.call_args
        assert call_args[1]['params']['units'] == "standard"

    @patch('weather_cli.requests.get')
    def test_get_weather_strips_whitespace(self, mock_get, weather_cli, sample_weather_response):
        """Test that city names with whitespace are properly stripped."""
        mock_response = Mock()
        mock_response.json.return_value = sample_weather_response
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        weather_cli.get_weather("  London  ")

        call_args = mock_get.call_args
        assert call_args[1]['params']['q'] == "London"

    @patch('weather_cli.requests.get')
    def test_get_weather_timeout_parameter(self, mock_get, weather_cli, sample_weather_response):
        """Test that API requests include timeout parameter."""
        mock_response = Mock()
        mock_response.json.return_value = sample_weather_response
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        weather_cli.get_weather("Paris")

        call_args = mock_get.call_args
        assert call_args[1]['timeout'] == 10


# Input Validation Tests
class TestInputValidation:
    """Test input validation and error handling."""

    def test_empty_city_name(self, weather_cli):
        """Test that empty city name raises error."""
        with pytest.raises(WeatherAPIError) as exc_info:
            weather_cli.get_weather("")
        assert "City name cannot be empty" in str(exc_info.value)

    def test_whitespace_only_city_name(self, weather_cli):
        """Test that whitespace-only city name raises error."""
        with pytest.raises(WeatherAPIError) as exc_info:
            weather_cli.get_weather("   ")
        assert "City name cannot be empty" in str(exc_info.value)


# Error Handling Tests
class TestErrorHandling:
    """Test error handling for various API failure scenarios."""

    @patch('weather_cli.requests.get')
    def test_timeout_error(self, mock_get, weather_cli):
        """Test handling of request timeout."""
        mock_get.side_effect = requests.exceptions.Timeout()

        with pytest.raises(WeatherAPIError) as exc_info:
            weather_cli.get_weather("London")
        assert "Request timed out" in str(exc_info.value)

    @patch('weather_cli.requests.get')
    def test_connection_error(self, mock_get, weather_cli):
        """Test handling of connection errors."""
        mock_get.side_effect = requests.exceptions.ConnectionError()

        with pytest.raises(WeatherAPIError) as exc_info:
            weather_cli.get_weather("London")
        assert "Connection error" in str(exc_info.value)

    @patch('weather_cli.requests.get')
    def test_401_unauthorized_error(self, mock_get, weather_cli):
        """Test handling of 401 Unauthorized (invalid API key)."""
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError()
        mock_get.return_value = mock_response

        with pytest.raises(WeatherAPIError) as exc_info:
            weather_cli.get_weather("London")
        assert "Invalid API key" in str(exc_info.value)

    @patch('weather_cli.requests.get')
    def test_404_city_not_found_error(self, mock_get, weather_cli):
        """Test handling of 404 Not Found (invalid city)."""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError()
        mock_get.return_value = mock_response

        with pytest.raises(WeatherAPIError) as exc_info:
            weather_cli.get_weather("NonexistentCity123")
        assert "City 'NonexistentCity123' not found" in str(exc_info.value)

    @patch('weather_cli.requests.get')
    def test_500_server_error(self, mock_get, weather_cli):
        """Test handling of 500 Internal Server Error."""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("500 Server Error")
        mock_get.return_value = mock_response

        with pytest.raises(WeatherAPIError) as exc_info:
            weather_cli.get_weather("London")
        assert "HTTP error occurred" in str(exc_info.value)

    @patch('weather_cli.requests.get')
    def test_generic_request_exception(self, mock_get, weather_cli):
        """Test handling of generic request exceptions."""
        mock_get.side_effect = requests.exceptions.RequestException("Generic error")

        with pytest.raises(WeatherAPIError) as exc_info:
            weather_cli.get_weather("London")
        assert "An error occurred while fetching weather data" in str(exc_info.value)


# Output Formatting Tests
class TestOutputFormatting:
    """Test weather data output formatting."""

    def test_format_weather_output_metric(self, weather_cli, sample_weather_response):
        """Test formatting of weather output with metric units."""
        output = weather_cli.format_weather_output(sample_weather_response, units="metric")

        assert "London" in output
        assert "GB" in output
        assert "Clear" in output
        assert "clear sky" in output
        assert "18.5°C" in output
        assert "17.8°C" in output
        assert "72%" in output
        assert "1013 hPa" in output
        assert "3.6 m/s" in output
        assert "230°" in output
        assert "20%" in output

    def test_format_weather_output_imperial(self, weather_cli, sample_weather_response_imperial):
        """Test formatting of weather output with imperial units."""
        output = weather_cli.format_weather_output(sample_weather_response_imperial, units="imperial")

        assert "New York" in output
        assert "US" in output
        assert "65.3°F" in output
        assert "64.2°F" in output
        assert "8.5 mph" in output

    def test_format_weather_output_standard(self, weather_cli, sample_weather_response):
        """Test formatting of weather output with standard (Kelvin) units."""
        output = weather_cli.format_weather_output(sample_weather_response, units="standard")

        # Standard units use Kelvin (no degree symbol added, just K)
        assert "18.5K" in output
        assert "17.8K" in output

    def test_format_weather_output_missing_data(self, weather_cli):
        """Test formatting with missing or incomplete data."""
        incomplete_data = {
            "name": "TestCity",
            "sys": {},
            "weather": [{}],
            "main": {},
            "wind": {},
            "clouds": {}
        }

        output = weather_cli.format_weather_output(incomplete_data)

        assert "TestCity" in output
        assert "N/A" in output

    def test_format_weather_output_empty_weather_array(self, weather_cli):
        """Test formatting when weather array is empty."""
        data = {
            "name": "TestCity",
            "sys": {"country": "XX"},
            "weather": [],
            "main": {"temp": 20, "feels_like": 19, "temp_min": 18, "temp_max": 22, "humidity": 60, "pressure": 1000},
            "wind": {"speed": 5, "deg": 180},
            "clouds": {"all": 30}
        }

        output = weather_cli.format_weather_output(data)

        assert "TestCity" in output
        assert "N/A" in output  # Weather description should be N/A


# Main Function Tests
class TestMainFunction:
    """Test the main CLI entry point."""

    @patch('weather_cli.WeatherCLI')
    @patch('sys.argv', ['weather_cli.py', 'London'])
    def test_main_success(self, mock_weather_cli_class, sample_weather_response, capsys):
        """Test successful main function execution."""
        mock_instance = Mock()
        mock_instance.get_weather.return_value = sample_weather_response
        mock_instance.format_weather_output.return_value = "Weather output"
        mock_weather_cli_class.return_value = mock_instance

        exit_code = main()

        assert exit_code == 0
        captured = capsys.readouterr()
        assert "Weather output" in captured.out

    @patch('weather_cli.WeatherCLI')
    @patch('sys.argv', ['weather_cli.py', 'London', '--units', 'imperial'])
    def test_main_with_imperial_units(self, mock_weather_cli_class, sample_weather_response_imperial):
        """Test main function with imperial units argument."""
        mock_instance = Mock()
        mock_instance.get_weather.return_value = sample_weather_response_imperial
        mock_instance.format_weather_output.return_value = "Weather output"
        mock_weather_cli_class.return_value = mock_instance

        exit_code = main()

        assert exit_code == 0
        mock_instance.get_weather.assert_called_once_with('London', 'imperial')

    @patch('weather_cli.WeatherCLI')
    @patch('sys.argv', ['weather_cli.py', 'Paris', '--api-key', 'custom_key'])
    def test_main_with_custom_api_key(self, mock_weather_cli_class, sample_weather_response):
        """Test main function with custom API key argument."""
        mock_instance = Mock()
        mock_instance.get_weather.return_value = sample_weather_response
        mock_instance.format_weather_output.return_value = "Weather output"
        mock_weather_cli_class.return_value = mock_instance

        exit_code = main()

        assert exit_code == 0
        mock_weather_cli_class.assert_called_once_with(api_key='custom_key')

    @patch('weather_cli.WeatherCLI')
    @patch('sys.argv', ['weather_cli.py', 'InvalidCity'])
    def test_main_api_error(self, mock_weather_cli_class, capsys):
        """Test main function handling of API errors."""
        mock_instance = Mock()
        mock_instance.get_weather.side_effect = WeatherAPIError("City not found")
        mock_weather_cli_class.return_value = mock_instance

        exit_code = main()

        assert exit_code == 1
        captured = capsys.readouterr()
        assert "Error: City not found" in captured.err

    @patch('weather_cli.WeatherCLI')
    @patch('sys.argv', ['weather_cli.py', 'London'])
    def test_main_keyboard_interrupt(self, mock_weather_cli_class, capsys):
        """Test main function handling of keyboard interrupt."""
        mock_instance = Mock()
        mock_instance.get_weather.side_effect = KeyboardInterrupt()
        mock_weather_cli_class.return_value = mock_instance

        exit_code = main()

        assert exit_code == 130
        captured = capsys.readouterr()
        assert "Operation cancelled by user" in captured.err

    @patch('weather_cli.WeatherCLI')
    @patch('sys.argv', ['weather_cli.py', 'London'])
    def test_main_unexpected_error(self, mock_weather_cli_class, capsys):
        """Test main function handling of unexpected errors."""
        mock_instance = Mock()
        mock_instance.get_weather.side_effect = Exception("Unexpected error")
        mock_weather_cli_class.return_value = mock_instance

        exit_code = main()

        assert exit_code == 1
        captured = capsys.readouterr()
        assert "Unexpected error" in captured.err


# Integration-Style Tests (with mocked requests)
class TestIntegrationScenarios:
    """Test realistic end-to-end scenarios with mocked API."""

    @patch('weather_cli.requests.get')
    def test_complete_workflow_metric(self, mock_get, api_key, sample_weather_response):
        """Test complete workflow: initialize -> fetch -> format with metric units."""
        mock_response = Mock()
        mock_response.json.return_value = sample_weather_response
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        cli = WeatherCLI(api_key=api_key)
        weather_data = cli.get_weather("London", units="metric")
        output = cli.format_weather_output(weather_data, units="metric")

        assert "London" in output
        assert "°C" in output
        assert "m/s" in output

    @patch('weather_cli.requests.get')
    def test_complete_workflow_imperial(self, mock_get, api_key, sample_weather_response_imperial):
        """Test complete workflow with imperial units."""
        mock_response = Mock()
        mock_response.json.return_value = sample_weather_response_imperial
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        cli = WeatherCLI(api_key=api_key)
        weather_data = cli.get_weather("New York", units="imperial")
        output = cli.format_weather_output(weather_data, units="imperial")

        assert "New York" in output
        assert "°F" in output
        assert "mph" in output

    @patch('weather_cli.requests.get')
    def test_multiple_cities_sequential(self, mock_get, api_key, sample_weather_response):
        """Test fetching weather for multiple cities sequentially."""
        mock_response = Mock()
        mock_response.json.return_value = sample_weather_response
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        cli = WeatherCLI(api_key=api_key)

        cities = ["London", "Paris", "Berlin"]
        for city in cities:
            result = cli.get_weather(city)
            assert result == sample_weather_response

        assert mock_get.call_count == len(cities)


# Edge Case Tests
class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    @patch('weather_cli.requests.get')
    def test_city_with_special_characters(self, mock_get, weather_cli, sample_weather_response):
        """Test city names with special characters."""
        mock_response = Mock()
        mock_response.json.return_value = sample_weather_response
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        weather_cli.get_weather("São Paulo")

        call_args = mock_get.call_args
        assert call_args[1]['params']['q'] == "São Paulo"

    @patch('weather_cli.requests.get')
    def test_city_with_spaces(self, mock_get, weather_cli, sample_weather_response):
        """Test city names with multiple words."""
        mock_response = Mock()
        mock_response.json.return_value = sample_weather_response
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        weather_cli.get_weather("New York City")

        call_args = mock_get.call_args
        assert call_args[1]['params']['q'] == "New York City"

    def test_weather_api_error_exception(self):
        """Test WeatherAPIError exception can be raised and caught."""
        with pytest.raises(WeatherAPIError) as exc_info:
            raise WeatherAPIError("Test error message")
        assert "Test error message" in str(exc_info.value)

    def test_weather_api_error_is_exception(self):
        """Test that WeatherAPIError inherits from Exception."""
        assert issubclass(WeatherAPIError, Exception)


# Constants and Configuration Tests
class TestConfiguration:
    """Test configuration and constants."""

    def test_base_url_constant(self):
        """Test that BASE_URL is correctly set."""
        assert WeatherCLI.BASE_URL == "https://api.openweathermap.org/data/2.5/weather"

    def test_base_url_https(self):
        """Test that BASE_URL uses HTTPS."""
        assert WeatherCLI.BASE_URL.startswith("https://")
