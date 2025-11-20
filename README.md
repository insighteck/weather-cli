# Weather CLI ☀️🌧️

A beautiful command-line application for fetching real-time weather information from the OpenWeatherMap API. Get current weather conditions, temperature, humidity, wind speed, and more—all from your terminal!

## Features ✨

- 🌍 **Global Weather Data**: Get weather information for any city worldwide
- 🌡️ **Multiple Unit Systems**: Support for metric (°C), imperial (°F), and standard (Kelvin) units
- 🎨 **Beautiful Output**: Formatted, easy-to-read weather information with emojis
- 🛡️ **Robust Error Handling**: Comprehensive error handling for API issues, network errors, and invalid inputs
- ⚡ **Fast & Lightweight**: Minimal dependencies, quick response times
- 🧪 **Well-Tested**: Comprehensive test suite with >95% code coverage

## Table of Contents

- [Installation](#installation)
- [API Key Setup](#api-key-setup)
- [Usage](#usage)
- [Examples](#examples)
- [Testing](#testing)
- [Development](#development)
- [Error Handling](#error-handling)
- [Contributing](#contributing)
- [License](#license)

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)
- An OpenWeatherMap API key (free tier available)

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/weather-cli.git
cd weather-cli
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

The required dependencies are:
- `requests>=2.31.0` - For making HTTP requests to the OpenWeatherMap API
- `pytest>=7.4.0` - For running tests (development)
- `pytest-mock>=3.12.0` - For mocking in tests (development)
- `pytest-cov>=4.1.0` - For code coverage reports (development)

## API Key Setup

To use this application, you need a free API key from OpenWeatherMap.

### Step 1: Get Your API Key

1. Visit [OpenWeatherMap](https://openweathermap.org/)
2. Click on "Sign Up" (or "Sign In" if you have an account)
3. After signing in, go to [API Keys](https://home.openweathermap.org/api_keys)
4. Copy your API key (or generate a new one)

**Note**: It may take a few minutes for a newly created API key to become active.

### Step 2: Configure the API Key

You have two options to provide your API key:

#### Option 1: Environment Variable (Recommended)

Set the `OPENWEATHER_API_KEY` environment variable:

**Linux/macOS:**
```bash
export OPENWEATHER_API_KEY="your_api_key_here"
```

To make it permanent, add the above line to your `~/.bashrc`, `~/.zshrc`, or `~/.profile`:
```bash
echo 'export OPENWEATHER_API_KEY="your_api_key_here"' >> ~/.bashrc
source ~/.bashrc
```

**Windows (Command Prompt):**
```cmd
set OPENWEATHER_API_KEY=your_api_key_here
```

**Windows (PowerShell):**
```powershell
$env:OPENWEATHER_API_KEY="your_api_key_here"
```

#### Option 2: Command-Line Argument

Pass the API key directly when running the application:
```bash
python weather_cli.py "London" --api-key your_api_key_here
```

## Usage

### Basic Syntax

```bash
python weather_cli.py CITY [OPTIONS]
```

### Command-Line Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `city` | (positional) | Name of the city to get weather for | Required |
| `--units` | `-u` | Unit system: `metric`, `imperial`, or `standard` | `metric` |
| `--api-key` | `-k` | OpenWeatherMap API key | From env variable |
| `--version` | `-v` | Show version information | - |
| `--help` | `-h` | Show help message | - |

### Unit Systems

- **metric**: Temperature in Celsius (°C), wind speed in m/s
- **imperial**: Temperature in Fahrenheit (°F), wind speed in mph
- **standard**: Temperature in Kelvin (K), wind speed in m/s

## Examples

### Basic Usage (Metric Units)

```bash
python weather_cli.py London
```

Output:
```
╔════════════════════════════════════════════════════════════╗
║  Weather Information for London, GB
╚════════════════════════════════════════════════════════════╝

🌤️  Condition: Clear (clear sky)

🌡️  Temperature:
    Current:    18.5°C
    Feels Like: 17.8°C
    Min/Max:    16.2°C / 20.1°C

💧 Humidity:    72%
🔽 Pressure:    1013 hPa

💨 Wind:
    Speed:      3.6 m/s
    Direction:  230°

☁️  Cloudiness: 20%
```

### Using Imperial Units

```bash
python weather_cli.py "New York" --units imperial
```

### Multi-Word City Names

For cities with spaces in their names, use quotes:
```bash
python weather_cli.py "Los Angeles"
python weather_cli.py "San Francisco" -u imperial
```

### Using Standard Units (Kelvin)

```bash
python weather_cli.py Tokyo --units standard
```

### Providing API Key via Command Line

```bash
python weather_cli.py Paris --api-key your_api_key_here
```

### Combining Options

```bash
python weather_cli.py "Mexico City" --units imperial --api-key your_api_key_here
```

### Making the Script Executable (Linux/macOS)

For convenience, you can make the script executable:

```bash
chmod +x weather_cli.py
./weather_cli.py London
```

Or create an alias in your shell configuration:
```bash
alias weather="python /path/to/weather_cli.py"
weather London
```

## Testing

The project includes a comprehensive test suite using pytest.

### Running All Tests

```bash
pytest
```

### Running Tests with Verbose Output

```bash
pytest -v
```

### Running Tests with Coverage Report

```bash
pytest --cov=weather_cli --cov-report=html
```

This will generate an HTML coverage report in the `htmlcov/` directory. Open `htmlcov/index.html` in your browser to view detailed coverage information.

### Running Tests with Coverage Summary

```bash
pytest --cov=weather_cli --cov-report=term-missing
```

### Running Specific Test Classes

```bash
# Test only initialization
pytest tests/test_weather_cli.py::TestWeatherCLIInitialization -v

# Test only API requests
pytest tests/test_weather_cli.py::TestWeatherAPIRequests -v

# Test only error handling
pytest tests/test_weather_cli.py::TestErrorHandling -v
```

### Running Specific Tests

```bash
pytest tests/test_weather_cli.py::TestWeatherCLIInitialization::test_init_with_api_key -v
```

### Test Coverage

The test suite includes:

- ✅ **Initialization tests**: API key handling, environment variables
- ✅ **API request tests**: Successful requests, different unit systems
- ✅ **Input validation**: Empty city names, whitespace handling
- ✅ **Error handling**: Timeouts, connection errors, HTTP errors (401, 404, 500)
- ✅ **Output formatting**: Metric, imperial, and standard units
- ✅ **Main function tests**: Command-line argument parsing, error handling
- ✅ **Integration tests**: End-to-end workflows
- ✅ **Edge cases**: Special characters, multi-word cities

Current test coverage: **95%+**

## Development

### Project Structure

```
weather-cli/
├── weather_cli.py          # Main application code
├── requirements.txt        # Project dependencies
├── pytest.ini             # Pytest configuration
├── .gitignore            # Git ignore rules
├── tests/
│   ├── __init__.py       # Test package initialization
│   ├── conftest.py       # Pytest fixtures and configuration
│   └── test_weather_cli.py  # Comprehensive test suite
└── README.md             # This file
```

### Code Structure

The application consists of:

- **WeatherAPIError**: Custom exception class for API-related errors
- **WeatherCLI**: Main class containing the core functionality
  - `__init__()`: Initialize with API key
  - `get_weather()`: Fetch weather data from the API
  - `format_weather_output()`: Format the data for display
- **main()**: CLI entry point with argument parsing

### Adding New Features

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Write tests for your changes
5. Ensure all tests pass: `pytest`
6. Commit your changes: `git commit -m "Add feature"`
7. Push to your fork: `git push origin feature-name`
8. Create a Pull Request

## Error Handling

The application handles various error scenarios gracefully:

### API Key Errors
```
❌ Error: No API key provided. Set OPENWEATHER_API_KEY environment variable or pass it as an argument.
```

### Invalid API Key
```
❌ Error: Invalid API key. Please check your OPENWEATHER_API_KEY.
```

### City Not Found
```
❌ Error: City 'InvalidCity' not found. Please check the city name.
```

### Network Errors
```
❌ Error: Connection error. Please check your internet connection.
```

### Timeout Errors
```
❌ Error: Request timed out. Please check your internet connection.
```

### User Cancellation
```
⚠️  Operation cancelled by user.
```

## Troubleshooting

### Issue: "No API key provided"
**Solution**: Set the `OPENWEATHER_API_KEY` environment variable or use the `--api-key` option.

### Issue: "Invalid API key"
**Solution**:
- Verify your API key at [OpenWeatherMap](https://home.openweathermap.org/api_keys)
- Wait a few minutes if you just created a new key
- Check for extra spaces or characters in your key

### Issue: "City not found"
**Solution**:
- Check the spelling of the city name
- Try using quotes for multi-word cities: `"New York"`
- Try adding country code: `"London,UK"`

### Issue: "Request timed out"
**Solution**:
- Check your internet connection
- The API might be experiencing issues; try again later
- Try increasing the timeout in the code (default is 10 seconds)

### Issue: "Connection error"
**Solution**:
- Verify you have an active internet connection
- Check if you're behind a proxy or firewall
- Ensure port 443 (HTTPS) is not blocked

## API Rate Limits

The free tier of OpenWeatherMap API has the following limits:
- **60 calls/minute**
- **1,000,000 calls/month**

If you exceed these limits, you'll receive a 429 error. Consider:
- Implementing caching for frequently requested cities
- Upgrading to a paid plan for higher limits

## Technical Details

### Dependencies
- **requests**: HTTP library for making API calls
- **pytest**: Testing framework
- **pytest-mock**: Mocking library for tests
- **pytest-cov**: Code coverage plugin

### API Endpoint
The application uses the OpenWeatherMap Current Weather Data API:
```
https://api.openweathermap.org/data/2.5/weather
```

### Timeout
All API requests have a 10-second timeout to prevent hanging.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Guidelines
1. Write tests for any new features
2. Ensure all tests pass
3. Follow PEP 8 style guidelines
4. Update documentation as needed

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Weather data provided by [OpenWeatherMap](https://openweathermap.org/)
- Built with ❤️ using Python

## Support

If you encounter any issues or have questions:
1. Check the [Troubleshooting](#troubleshooting) section
2. Review existing [GitHub Issues](https://github.com/yourusername/weather-cli/issues)
3. Create a new issue with:
   - Your Python version
   - Operating system
   - Full error message
   - Steps to reproduce

---

**Happy Weather Checking! ☀️🌧️⛈️❄️**
