# ComicCraft

AI Comic Story Creator using FastAPI, Gemini and Hugging Face.

## Architecture

Browser
    |
    v
FastAPI + Jinja2
    |
    +---- Gemini Outline
    |
    +---- Gemini Story/Dialogues
    |
    +---- Hugging Face Images
    |
    +---- Layout Builder
    |
    +---- PDF Export
    |
    v
Comic Preview / Download

## Windows Setup

Create environment:

```powershell
py -3.11 -m venv .venv