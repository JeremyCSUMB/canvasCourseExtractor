# Canvas Course Extractor (CCE)

Canvas Course Extractor (CCE) is a Python-based command-line tool designed to extract and preprocess course data from Canvas Learning Management System. It's particularly useful for educators and researchers who want to analyze course content or prepare data for machine learning models.

## Features

- Extract detailed information about assignments and modules from Canvas courses
- Preprocess extracted data into a format suitable for Language Learning Models (LLMs)
- Command-line interface for easy use
- Modular structure for easy maintenance and contribution

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/canvas-course-extractor.git
   cd canvas-course-extractor
   ```

2. Install the required packages:
   ```
   pip install requests python-dotenv
   ```

3. Create a `.env` file in the project root directory with your Canvas API key and domain:
   ```
   CANVAS_API_KEY=your_api_key_here
   CANVAS_DOMAIN=your_canvas_domain.instructure.com
   ```

## Usage

Run the script from the command line:

```
python main.py course_id [--raw] [--preprocessed]
```

- `course_id`: The ID of the course you want to extract data from (required)
- `--raw`: Save the raw extracted data
- `--preprocessed`: Save the preprocessed data
- If neither `--raw` nor `--preprocessed` is specified, both will be saved

Example:
```
python main.py 12345 --preprocessed
```
This will extract data from course 12345 and save the preprocessed version.

## Project Structure

- `main.py`: Entry point of the application
- `extractor.py`: Contains the `CanvasDataExtractor` class for fetching data from Canvas
- `preprocessor.py`: Contains functions for preprocessing the extracted data
- `utils.py`: Contains utility functions used across the project
- `config.py`: Handles configuration and environment variables

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Thanks to the Canvas LMS team for providing the API
- Inspired by educators and researchers working with online learning data

