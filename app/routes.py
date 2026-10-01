import logging
from pathlib import Path

from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates

from app.config import get_settings
from app.dependencies import get_comic_service
from app.schemas import ImageTestRequest, PromptRequest
from app.services.image_generator import ImageGenerationUnavailable

router = APIRouter()

templates = Jinja2Templates(directory="templates")

logger = logging.getLogger("comiccraft")


def _payload_from_form(
    story_prompt: str,
    character_name: str,
    setting: str,
    tone: str,
    art_style: str,
) -> PromptRequest:

    return PromptRequest(
        story_prompt=story_prompt,
        character_name=character_name,
        setting=setting,
        tone=tone,
        art_style=art_style,
    )


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "title": "Create Your Comic",
        },
    )


@router.post("/generate", response_class=HTMLResponse)
async def generate(
    request: Request,
    story_prompt: str = Form(...),
    character_name: str = Form(...),
    setting: str = Form(...),
    tone: str = Form(...),
    art_style: str = Form(...),
    comic_service=Depends(get_comic_service),
):

    try:

        payload = _payload_from_form(
            story_prompt,
            character_name,
            setting,
            tone,
            art_style,
        )

        layout, pdf_filename = comic_service.generate(payload)

        return templates.TemplateResponse(
            request=request,
            name="comic_preview.html",
            context={
                "title": "Your Comic",
                "layout": layout.panels,
                "pdf_filename": pdf_filename,
            },
        )

    except Exception as exc:

        logger.exception("Comic generation failed")
        status_code = (
            503
            if isinstance(exc, ImageGenerationUnavailable)
            else 500
        )

        return templates.TemplateResponse(
            request=request,
            name="error.html",
            context={
                "title": "Generation Error",
                "message": str(exc),
            },
            status_code=status_code,
        )


@router.post("/generate-comic/json")
async def generate_json(
    payload: PromptRequest,
    comic_service=Depends(get_comic_service),
):

    try:

        layout, pdf_filename = comic_service.generate(payload)

        return {
            "success": True,
            "pdf_filename": pdf_filename,
            "pdf_url": f"/download/{pdf_filename}",
            "panels": [
                panel.model_dump()
                for panel in layout.panels
            ],
        }

    except Exception as exc:

        logger.exception("JSON comic generation failed")

        raise HTTPException(
            status_code=(
                503
                if isinstance(exc, ImageGenerationUnavailable)
                else 500
            ),
            detail=str(exc),
        ) from exc


@router.post("/test-image")
async def test_image(
    payload: ImageTestRequest,
    comic_service=Depends(get_comic_service),
):

    try:

        image_url = comic_service.test_image(
            payload.prompt
        )

        return {
            "success": True,
            "image_url": image_url,
        }

    except Exception as exc:

        logger.exception("Image generation test failed")

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc


@router.get("/download/{filename}")
async def download(filename: str):

    settings = get_settings()

    safe_name = Path(filename).name

    if safe_name != filename:
        raise HTTPException(
            status_code=400,
            detail="Invalid PDF filename.",
        )

    if not safe_name.endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files can be downloaded.",
        )

    output = (
        settings.exports_dir / safe_name
    ).resolve()

    root = settings.exports_dir.resolve()

    if root not in output.parents:

        raise HTTPException(
            status_code=400,
            detail="Invalid PDF path.",
        )

    if not output.is_file():

        raise HTTPException(
            status_code=404,
            detail="PDF not found.",
        )

    return FileResponse(
        output,
        media_type="application/pdf",
        filename=safe_name,
    )


@router.get(
    "/export-success",
    response_class=HTMLResponse,
)
async def export_success(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="export_success.html",
        context={
            "title": "Export Complete",
        },
    )


@router.get("/health")
async def health(request: Request):

    settings = request.app.state.settings

    return {
        "status": "ok",
        "service": settings.app_name,
        "gemini_configured": bool(
            settings.gemini_api_key
        ),
        "huggingface_configured": bool(
            settings.hf_token
        ),
    }