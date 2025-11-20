#!/usr/bin/env python3
"""
Weather CLI - A command-line tool to fetch current weather from OpenWeatherMap API.
"""

import argparse
import os
import sys
from typing import Optional, Dict, Any
import requests


class WeatherAPIError(Exception):
    """Custom exception for weather API errors."""
    pass


class WeatherCLI:
    """Main class for the Weather CLI application."""

    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Weather CLI.

        Args:
            api_key: OpenWeatherMap API key. If not provided, reads from OPENWEATHER_API_KEY env variable.

        Raises:
            WeatherAPIError: If no API key is provided or found in environment.
        """
        self.api_key = api_key or os.getenv("OPENWEATHER_API_KEY")
        if not self.api_key:
            raise WeatherAPIError(
                "No API key provided. Set OPENWEATHER_API_KEY environment variable or pass it as an argument."
            )

    def get_weather(self, city: str, units: str = "metric") -> Dict[str, Any]:
        """
        Fetch weather data for a specific city.

        Args:
            city: Name of the city to get weather for.
            units: Unit system ('metric', 'imperial', or 'standard'). Default is 'metric'.

        Returns:
            Dictionary containing weather data.

        Raises:
            WeatherAPIError: If the API request fails or returns an error.
        """
        if not city or not city.strip():
            raise WeatherAPIError("City name cannot be empty.")

        params = {
            "q": city.strip(),
            "appid": self.api_key,
            "units": units
        }

        try:
            response = requests.get(self.BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout:
            raise WeatherAPIError("Request timed out. Please check your internet connection.")
        except requests.exceptions.ConnectionError:
            raise WeatherAPIError("Connection error. Please check your internet connection.")
        except requests.exceptions.HTTPError as e:
            if response.status_code == 401:
                raise WeatherAPIError("Invalid API key. Please check your OPENWEATHER_API_KEY.")
            elif response.status_code == 404:
                raise WeatherAPIError(f"City '{city}' not found. Please check the city name.")
            else:
                raise WeatherAPIError(f"HTTP error occurred: {e}")
        except requests.exceptions.RequestException as e:
            raise WeatherAPIError(f"An error occurred while fetching weather data: {e}")

    def format_weather_output(self, data: Dict[str, Any], units: str = "metric") -> str:
        """
        Format weather data into a human-readable string.

        Args:
            data: Weather data dictionary from the API.
            units: Unit system used ('metric', 'imperial', or 'standard').

        Returns:
            Formatted weather information string.
        """
        # Determine temperature unit symbol
        temp_unit = "°C" if units == "metric" else "°F" if units == "imperial" else "K"
        speed_unit = "m/s" if units == "metric" else "mph" if units == "imperial" else "m/s"

        city_name = data.get("name", "Unknown")
        country = data.get("sys", {}).get("country", "")

        weather_main = data.get("weather", [{}])[0].get("main", "N/A")
        weather_desc = data.get("weather", [{}])[0].get("description", "N/A")

        temp = data.get("main", {}).get("temp", "N/A")
        feels_like = data.get("main", {}).get("feels_like", "N/A")
        temp_min = data.get("main", {}).get("temp_min", "N/A")
        temp_max = data.get("main", {}).get("temp_max", "N/A")
        humidity = data.get("main", {}).get("humidity", "N/A")
        pressure = data.get("main", {}).get("pressure", "N/A")

        wind_speed = data.get("wind", {}).get("speed", "N/A")
        wind_deg = data.get("wind", {}).get("deg", "N/A")

        clouds = data.get("clouds", {}).get("all", "N/A")

        output = f"""
╔════════════════════════════════════════════════════════════╗
║  Weather Information for {city_name}, {country}
╚════════════════════════════════════════════════════════════╝

🌤️  Condition: {weather_main} ({weather_desc})

🌡️  Temperature:
    Current:    {temp}{temp_unit}
    Feels Like: {feels_like}{temp_unit}
    Min/Max:    {temp_min}{temp_unit} / {temp_max}{temp_unit}

💧 Humidity:    {humidity}%
🔽 Pressure:    {pressure} hPa

💨 Wind:
    Speed:      {wind_speed} {speed_unit}
    Direction:  {wind_deg}°

☁️  Cloudiness: {clouds}%
"""
        return output


def main():
    """Main entry point for the CLI application."""
    parser = argparse.ArgumentParser(
        description="Fetch current weather information from OpenWeatherMap API.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s London
  %(prog)s "New York" --units imperial
  %(prog)s Tokyo --api-key YOUR_API_KEY

Environment Variables:
  OPENWEATHER_API_KEY    Your OpenWeatherMap API key
        """
    )

    parser.add_argument(
        "city",
        type=str,
        help="Name of the city to get weather for"
    )

    parser.add_argument(
        "-u", "--units",
        type=str,
        choices=["metric", "imperial", "standard"],
        default="metric",
        help="Unit system: metric (°C), imperial (°F), or standard (K). Default: metric"
    )

    parser.add_argument(
        "-k", "--api-key",
        type=str,
        help="OpenWeatherMap API key (can also be set via OPENWEATHER_API_KEY env variable)"
    )

    parser.add_argument(
        "-v", "--version",
        action="version",
        version="%(prog)s 1.0.0"
    )

    args = parser.parse_args()

    try:
        # Initialize the Weather CLI
        weather_cli = WeatherCLI(api_key=args.api_key)

        # Fetch weather data
        weather_data = weather_cli.get_weather(args.city, args.units)

        # Format and display the output
        output = weather_cli.format_weather_output(weather_data, args.units)
        print(output)

        return 0

    except WeatherAPIError as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\n⚠️  Operation cancelled by user.", file=sys.stderr)
        return 130
    except Exception as e:
        print(f"❌ Unexpected error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
