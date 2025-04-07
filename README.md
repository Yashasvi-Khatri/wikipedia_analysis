# Wikipedia Analysis Tool

A data analysis tool that extracts, processes, and visualizes information from Wikipedia articles. This application enables users to perform text analysis, generate insights, and visualize patterns from Wikipedia content.

## Features

- **Wikipedia Content Extraction**: Fetch and parse content from any Wikipedia article
- **Text Analysis**: Perform word frequency, sentiment analysis, and topic modeling
- **Data Visualization**: Generate visual representations of analysis results
- **Export Capabilities**: Save analysis results in various formats (CSV, JSON, PDF)

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/Yashasvi-Khatri/wikipedia_analysis.git
   cd wikipedia_analysis
   ```

2. Create and activate a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running the Application

```bash
python app.py
```

The application will start and be accessible at `http://localhost:5000` in your web browser.

### Basic Analysis

1. Enter a Wikipedia article title or URL in the search field
2. Select the analysis options you want to perform
3. Click "Analyze" to process the article
4. View the results in the dashboard

### Advanced Options

- **Custom Parameters**: Adjust analysis parameters through the settings panel
- **Batch Processing**: Analyze multiple articles at once using the batch mode
- **Comparative Analysis**: Compare metrics between different articles

## Project Structure

```
wikipedia_analysis/
├── app.py                  # Main application entry point
├── requirements.txt        # Project dependencies
├── config.py               # Configuration settings
├── static/                 # Static assets (CSS, JS, images)
├── templates/              # HTML templates
├── modules/                # Core functionality modules
│   ├── extractor.py        # Wikipedia content extraction
│   ├── analyzer.py         # Text analysis functionality
│   └── visualizer.py       # Data visualization tools
└── utils/                  # Utility functions
```

## Configuration

Configure application settings in `config.py`:

```python
# Example configuration
API_RATE_LIMIT = 100
CACHE_EXPIRY = 3600  # seconds
DEBUG_MODE = False
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [Wikipedia API](https://www.mediawiki.org/wiki/API:Main_page) for providing access to Wikipedia content
- All contributors who have helped improve this project

---

Created by [Yashasvi Khatri](https://github.com/Yashasvi-Khatri)
