# ComicCraft AI – Setup Guide

Hi! This guide is for anyone who wants to run the ComicCraft AI project on a fresh Windows laptop.

If you have not worked with a Python project before, that's okay. Just follow the steps in the same order. You don't need to know the whole project before starting.

---

## 1. What do I need?

Before starting, make sure you have:

- Windows 10 or Windows 11
- Internet connection
- A web browser
- Visual Studio Code
- Python 3.11
- Git
- A Google Gemini API key
- A Hugging Face token

The Python libraries needed by the project are already listed in `requirements.txt`, so you don't have to install them one by one.

---

## 2. Install Visual Studio Code

First install Visual Studio Code on the laptop.

After installing it, open VS Code.

We will use VS Code to open the project, run commands, edit files, and start the application.

---

## 3. Install Python

ComicCraft AI is a Python project, so Python needs to be installed first.

Install **Python 3.11**.

After installing Python, open VS Code and open:

**Terminal → New Terminal**

Then run:

```powershell
python --version
```

You should get something similar to:

```text
Python 3.11.x
```

If Python is not recognized immediately after installation, close VS Code, open it again, and try the command once more.

---

## 4. Install Git

Git is useful for getting the project from GitHub.

After installing Git, open a new VS Code terminal and run:

```powershell
git --version
```

If a Git version is shown, Git is ready.

---

## 5. Get the ComicCraft project

You can get the project from GitHub in either of these ways.

### Method 1 – Download ZIP

1. Open the ComicCraft GitHub repository.
2. Click **Code**.
3. Select **Download ZIP**.
4. Extract the downloaded ZIP.
5. Open the extracted project folder.

### Method 2 – Clone using Git

If Git is installed, you can run:

```powershell
git clone https://github.com/jabez17a-cmd/Comic-Craft-GenAI.git
```

After cloning, open the downloaded project folder in VS Code.

---

## 6. Open the project in VS Code

In VS Code, go to:

**File → Open Folder**

Select the ComicCraft project folder.

You should see something roughly like this:

```text
Comic-Craft AI/
│
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── dependencies.py
│   ├── main.py
│   ├── routes.py
│   ├── schemas.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── comic_service.py
│   │   ├── gemini.py
│   │   ├── image_generator.py
│   │   ├── layout_builder.py
│   │   └── pdf.py
│   │
│   └── utils/
│       └── __init__.py
│
├── templates/
├── static/
├── exports/
├── tests/
├── .env.example
├── .gitignore
├── requirements.txt
├── README.md
└── pyproject.toml
```

The exact number of files may change as the project is updated, but the important part is that you are inside the ComicCraft project folder.

---

## 7. Open the terminal in the project folder

In VS Code, select:

**Terminal → New Terminal**

Make sure the terminal is pointing to the ComicCraft folder.

It should look similar to:

```text
PS C:\Users\YourName\...\Comic-Craft AI>
```

All the commands below should be run from this project folder.

---

## 8. Create a virtual environment

We use a virtual environment so that the packages used by ComicCraft don't interfere with other Python projects on the laptop.

Run:

```powershell
python -m venv .venv
```

After this finishes, you should see a new `.venv` folder in the project.

---

## 9. Activate the virtual environment

Run:

```powershell
.\.venv\Scripts\Activate.ps1
```

If it works, you should see `(.venv)` at the beginning of the terminal line:

```text
(.venv) PS C:\Users\YourName\...\Comic-Craft AI>
```

That means the virtual environment is active.

### If Windows blocks the activation

If PowerShell doesn't allow the activation script, run this:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force
```

Then run the activation command again:

```powershell
.\.venv\Scripts\Activate.ps1
```

---

## 10. Install the required Python packages

Now install everything listed in `requirements.txt`.

Run:

```powershell
python -m pip install -r requirements.txt
```

This may take a little time because it downloads the required Python packages.

Once it finishes, the project dependencies are ready.

---

## 11. Create the `.env` file

ComicCraft needs API keys for the AI services.

The project includes `.env.example`, which is a template.

Create your own `.env` file by running:

```powershell
Copy-Item .env.example .env
```

You can then open `.env` in VS Code.

You can also open it with:

```powershell
notepad .env
```

---

## 12. Add the project settings

Your `.env` should have this basic structure:

```env
GEMINI_API_KEY=your_google_gemini_api_key
HF_TOKEN=your_huggingface_token

GEMINI_OUTLINE_MODEL=gemini-3.8-flash
GEMINI_STORY_MODEL=gemini-3.5-flash-lite
IMAGE_MODEL=black-forest-labs/FLUX.1-schnell

APP_NAME=ComicCraft
DEBUG=true

PANEL_COUNT=5

IMAGE_WIDTH=768
IMAGE_HEIGHT=768
IMAGE_STEPS=4
IMAGE_GUIDANCE_SCALE=3.5
```

You need to replace the two placeholder values:

```text
your_google_gemini_api_key
```

and

```text
your_huggingface_token
```

with your actual keys.

---

## 13. Get the Gemini API key

ComicCraft uses Gemini for generating the story content.

The general steps are:

1. Open Google AI Studio.
2. Sign in with your Google account.
3. Create or access an API key.
4. Copy the key.
5. Put it in the `.env` file.

For example:

```env
GEMINI_API_KEY=YOUR_REAL_KEY
```

Keep the real key private.

---

## 14. Get the Hugging Face token

ComicCraft uses Hugging Face for generating the comic images.

The general steps are:

1. Create or sign in to a Hugging Face account.
2. Go to the account settings.
3. Create an access token.
4. Give the token the required permission for inference calls.
5. Copy the token.
6. Add it to `.env`.

For example:

```env
HF_TOKEN=YOUR_REAL_TOKEN
```

Keep this token private too.

---

## 15. Important: Don't upload `.env`

This is important if you are using GitHub.

Your real `.env` contains private API credentials, so **do not upload it to GitHub**.

The repository should have:

```text
.env.example
```

with placeholder values.

It should not contain your real:

```text
GEMINI_API_KEY
HF_TOKEN
```

The `.gitignore` should also ignore files such as:

```text
.env
.venv/
__pycache__/
.pytest_cache/
```

---

## 16. Start ComicCraft AI

Now the setup is almost done.

First make sure the virtual environment is active:

```powershell
.\.venv\Scripts\Activate.ps1
```

Then start the FastAPI server:

```powershell
python -m uvicorn app.main:app --reload
```

Keep this terminal open while you are using the application.

---

## 17. Open ComicCraft in the browser

Open your browser and go to:

```text
http://127.0.0.1:8000/
```

You should now see the ComicCraft AI homepage.

---

## 18. Try generating a comic

For the first test, you can use these values.

### Main Character

```text
Finn
```

### Setting

```text
A magical forest at night
```

### Tone

```text
Magical, emotional and heartwarming
```

### Art Style

```text
Cinematic children's comic book illustration
```

### Story Prompt

```text
Finn, a young fox, finds a lost glowing star in the forest and helps it return to the night sky.
```

Then click the Generate button.

Give the application some time to generate the story and images.

---

## 19. Check the comic preview

After generation, the Comic Preview page should show the panels one after another.

The panels can contain:

- Panel Title
- Comic Image
- Scene Description
- Caption
- Narration
- Dialogue
- Image Prompt Reference

ComicCraft is designed around a five-panel comic flow.

---

## 20. What is Image Prompt Reference?

The **Image Prompt Reference** is the prompt/description used for generating the illustration for that panel.

It is shown so that the user can see what kind of visual description was given to the image-generation model.

This is also one of the requirements mentioned in the project documentation.

---

## 21. Download the comic as PDF

Once the comic looks good, use:

**Download Your Comic as PDF**

The PDF contains the comic information along with the generated images.

It includes things such as:

- Panel title
- Comic image
- Scene description
- Caption
- Narration
- Dialogue
- Image Prompt Reference

The generated PDF files are saved inside:

```text
exports/
```

---

## 22. Export success page

After the PDF is created, the application shows the export success page.

From there, you can download the comic and choose to create another comic.

---

## 23. FastAPI documentation

ComicCraft uses FastAPI, so it also has an interactive API page.

Open:

```text
http://127.0.0.1:8000/docs
```

You can use this page to see the available API routes.

---

## 24. Health check

To quickly check whether the server is running, open:

```text
http://127.0.0.1:8000/health
```

---

## 25. Run the tests

After setting everything up, it's a good idea to check the project tests.

Stop the server first if needed, then run:

```powershell
python -m pytest -q
```

The current verified project test suite reaches:

```text
9 passed
```

---

## 26. How to run ComicCraft next time

Once you have completed the setup, you don't need to install Python packages again every time.

Just:

1. Open the ComicCraft project in VS Code.
2. Open the terminal.
3. Activate the virtual environment.
4. Start the server.
5. Open the browser.

Commands:

```powershell
.\.venv\Scripts\Activate.ps1
```

Then:

```powershell
python -m uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000/
```

That's it.

---

## 27. If you don't want to activate `.venv`

You can also run the project directly using the Python inside the virtual environment:

```powershell
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

For tests:

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

---

## 28. How to stop the server

When ComicCraft is running in the terminal, press:

```text
Ctrl + C
```

The server will stop.

---

## 29. Main routes

These are the main routes available in the project:

| Method | Route | What it does |
|---|---|---|
| GET | `/` | Opens the ComicCraft homepage |
| POST | `/generate` | Generates a comic from the form |
| POST | `/generate-comic/json` | Generates a comic using JSON |
| POST | `/test-image` | Tests image generation |
| GET | `/download/{filename}` | Downloads a generated PDF |
| GET | `/health` | Checks whether the application is running |
| GET | `/docs` | Opens the FastAPI API documentation |

---

## 30. Quick setup version

If Python and Git are already installed, the basic setup is:

```powershell
git clone https://github.com/jabez17a-cmd/Comic-Craft-GenAI.git
```

Go into the project:

```powershell
cd Comic-Craft-GenAI
```

Create the environment:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install the packages:

```powershell
python -m pip install -r requirements.txt
```

Create `.env`:

```powershell
Copy-Item .env.example .env
```

Add your Gemini and Hugging Face keys to `.env`.

Then start ComicCraft:

```powershell
python -m uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000/
```

---

## 31. Before you finish, check these

Just quickly make sure:

- [ ] Python 3.11 is installed
- [ ] VS Code is installed
- [ ] Git is installed
- [ ] ComicCraft is opened in VS Code
- [ ] `.venv` was created
- [ ] `.venv` is activated
- [ ] `requirements.txt` was installed
- [ ] `.env` was created
- [ ] Gemini API key was added
- [ ] Hugging Face token was added
- [ ] `.env` is not uploaded to GitHub
- [ ] ComicCraft starts without problems
- [ ] Homepage opens
- [ ] A comic can be generated
- [ ] Five panels are generated
- [ ] Images appear correctly
- [ ] Image Prompt Reference appears
- [ ] PDF can be downloaded
- [ ] `/docs` opens
- [ ] `/health` works
- [ ] Tests pass

---

## 32. Useful URLs

### ComicCraft

```text
http://127.0.0.1:8000/
```

### API documentation

```text
http://127.0.0.1:8000/docs
```

### Health check

```text
http://127.0.0.1:8000/health
```

---

## 33. That's it

If this is your first time setting up ComicCraft, the order is basically:

**Install → Download the project → Open it in VS Code → Create `.venv` → Install packages → Add API keys → Run the server → Open the browser → Generate a comic → Download the PDF.**

Once the first setup is finished, running the project again is much easier. You only need to activate the environment, start the server, and open the browser.