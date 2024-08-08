# Canvas Course Extractor (CCE)

Canvas Course Extractor (CCE) is a Python-based command-line tool designed to extract and preprocess course data from Canvas Learning Management System. It's particularly useful for educators and researchers who want to analyze course content or prepare data for machine learning models, including GPT Builder.

## Features

- Extract detailed information about assignments and modules from Canvas courses
- Preprocess extracted data into formats suitable for:
  - Language Model (LLM) fine-tuning
  - GPT Builder projects
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
python main.py course_id [--raw] [--preprocessed {llm,gpt_builder}]
```

- `course_id`: The ID of the course you want to extract data from (required)
- `--raw`: Save the raw extracted data
- `--preprocessed`: Preprocess the data, with options:
  - `llm`: Format data for LLM fine-tuning (JSON output)
  - `gpt_builder`: Format data for GPT Builder projects (text output)

Examples:
```
python main.py 12345 --raw
python main.py 12345 --preprocessed llm
python main.py 12345 --preprocessed gpt_builder
```

## Project Structure

- `main.py`: Entry point of the application
- `extractor.py`: Contains the `CanvasDataExtractor` class for fetching data from Canvas
- `preprocessor_llm.py`: Contains functions for preprocessing data for LLM fine-tuning
- `preprocessor_gpt_builder.py`: Contains functions for preprocessing data for GPT Builder
- `utils.py`: Contains utility functions used across the project
- `config.py`: Handles configuration and environment variables

## Output

- Raw data is saved as JSON files
- LLM preprocessed data is saved as JSON files
- GPT Builder preprocessed data is saved as text files

## Using Preprocessed Data with GPT Builder

After preprocessing your course data for GPT Builder, you can use it to create a custom GPT that acts as an AI tutor for your course. Here's how to set it up:

1. Go to the GPT Builder interface on the OpenAI platform.
2. Create a new custom GPT.
3. In the "Knowledge" section, upload the preprocessed text file (e.g., `course_12345_preprocessed_gpt_builder.txt`).
4. In the "Instructions" section, use the following prompt prefix to guide the AI's behavior:

```
You are an AI tutor assistant for a specific course. Your knowledge comes from the uploaded course information, which includes details about assignments and modules. Your role is to:

1. Provide accurate information about assignments, including their names, due dates, point values, and submission types.
2. Explain the main objectives and key information for each assignment.
3. Offer an overview of course modules, their contents, and learning objectives.
4. Assist students in understanding assignment requirements and course structure.
5. Encourage good study habits and time management.
6. Remind students of important deadlines and submission guidelines.
7. Direct students to ask their instructor for clarification on any unclear points.

When asked about specific assignments or modules, refer to the provided course information. If a question is outside the scope of the provided information, politely explain that you can only assist with the information available in the course outline.

Never invent or assume information not present in the provided course data. If you're unsure about any details, ask the student to check with their instructor or the official course materials.

Remember, your goal is to support student learning and success in the course while maintaining academic integrity. Do not complete assignments for students or provide answers that would compromise the learning process.
```

5. Customize the instructions further based on your specific needs and the nature of your course.

When interacting with the custom GPT, students can ask questions about assignments, due dates, course structure, and receive helpful, course-specific guidance.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Thanks to the Canvas LMS team for providing the API
- Inspired by educators and researchers working with online learning data