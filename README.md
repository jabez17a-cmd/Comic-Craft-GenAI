# ComicCraft AI

ComicCraft AI is a web-based Generative AI application that creates a **5-panel comic** from a story idea provided by the user.

The user can enter a character, setting, tone, art style and story prompt. The application then generates the story content, comic illustrations and a downloadable PDF.

## What it does

- Takes a story prompt from the user
- Creates a 5-panel comic story
- Generates scene descriptions, captions, narration and dialogue
- Generates an illustration for each panel
- Shows the Image Prompt Reference used for the illustration
- Displays the completed comic in a preview page
- Exports the comic as a PDF
- Provides a simple web interface for creating another comic

## How it works

The basic flow of the application is:

```text
User Input
    ↓
FastAPI + Jinja2
    ↓
Gemini - Story Outline
    ↓
Gemini - Story / Dialogue
    ↓
Hugging Face - Comic Images
    ↓
Layout Builder
    ↓
Comic Preview
    ↓
PDF Export
```

The application uses FastAPI for the backend and Jinja2 templates for the web pages. Gemini is used for the story-generation part, while Hugging Face is used for image generation.

## Project Structure

```text
Comic-Craft AI/
│
├── app/
│   ├── config.py
│   ├── dependencies.py
│   ├── main.py
│   ├── routes.py
│   ├── schemas.py
│   │
│   ├── services/
│   │   ├── comic_service.py
│   │   ├── gemini.py
│   │   ├── image_generator.py
│   │   ├── layout_builder.py
│   │   └── pdf.py
│   │
│   └── utils/
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── comic_preview.html
│   ├── export_success.html
│   └── error.html
│
├── static/
│   ├── css/
│   ├── js/
│   └── panels/
│
├── exports/
├── tests/
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Technologies Used

- **Python**
- **FastAPI**
- **Uvicorn**
- **Jinja2**
- **Google Gemini**
- **Hugging Face**
- **Pillow**
- **fpdf2**
- **Pydantic**
- **Pytest**

The required Python packages are listed in [`requirements.txt`](requirements.txt).

## Setup

If you are setting up the project for the first time, follow the complete guide:

**[SETUP.md](SETUP.md)**

The setup guide covers:

- Installing Python and Git
- Opening the project in VS Code
- Creating the virtual environment
- Installing dependencies
- Creating the `.env` file
- Adding Gemini and Hugging Face API credentials
- Running the application
- Generating a comic
- Downloading the PDF
- Running the tests

## Running the Project

After completing the setup, start the application with:

```powershell
python -m uvicorn app.main:app --reload
```

Then open:

```text
http://127.0.0.1:8000/
```

## API Documentation

FastAPI provides an interactive API documentation page at:

```text
http://127.0.0.1:8000/docs
```

You can also check whether the application is running at:

```text
http://127.0.0.1:8000/health
```

## Testing

Run the project tests with:

```powershell
python -m pytest -q
```

The current verified test suite passes with **9 tests**.

## API Keys

ComicCraft needs:

- A Google Gemini API key
- A Hugging Face token

Add them to your local `.env` file.

**Do not upload the real `.env` file or API keys to GitHub.**

Use `.env.example` as the template for the required environment variables.

## Output

After generating a comic, the user can:

1. View the generated panels.
2. Read the scene, caption, narration and dialogue.
3. Check the Image Prompt Reference.
4. Download the complete comic as a PDF.

Generated PDF files are saved in the `exports/` folder.

## Project Status

The main ComicCraft workflow is implemented:

**User Input → AI Story Generation → AI Image Generation → Comic Preview → PDF Export**

The project can be run locally using the setup instructions in [`SETUP.md`](SETUP.md).