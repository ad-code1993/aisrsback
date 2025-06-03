# Dynamic AI Proposal Generator (Gemini-powered)

This project is an AI-powered assistant for collecting information and generating a Software Requirements Specification (SRS) document. It uses Google Gemini models to guide users through a Q&A process, ensuring all necessary SRS fields are covered.

## Features

- Interactive SRS Q&A with reasoning for each question
- Structured SRS output
- Extensible for additional proposal or requirements workflows

## Requirements

- Python 3.10+
- `pydantic`, `pydantic_ai`, `python-dotenv`

## Setup

1. Clone the repository or copy the files to your workspace.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up your environment variables in a `.env` file as needed (e.g., API keys).

## Usage

Run the main script:

```bash
python app/utils.py
```

Follow the prompts to answer SRS questions. Type `exit` to quit at any time.

## Project Structure

- `app/utils.py`: Main logic for SRS Q&A and generation
- `app/`: Contains supporting modules

## License

Specify your license here.
