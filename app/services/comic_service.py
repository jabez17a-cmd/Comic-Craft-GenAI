from app.schemas import PromptRequest
from app.services.gemini import GeminiService
from app.services.image_generator import ImageGenerator
from app.services.layout_builder import build_comic_layout
from app.services.pdf import save_pdf


class ComicService:
    """
    Complete ComicCraft pipeline:

    1. Gemini outline
    2. Gemini story/dialogue
    3. Image generation
    4. Layout construction
    5. PDF export
    """

    def __init__(self, settings):

        self.settings = settings

        self.gemini = GeminiService(
            settings.gemini_api_key,
            settings.gemini_outline_model,
            settings.gemini_story_model,
            settings.panel_count,
        )

        self.images = ImageGenerator(
            settings.hf_token,
            settings.image_model,
            settings.panels_dir,
            settings.image_width,
            settings.image_height,
            settings.image_steps,
            settings.image_guidance_scale,
        )

    def generate(
        self,
        request: PromptRequest,
    ):

        outline = self.gemini.generate_outline(
            request
        )

        story = self.gemini.generate_story(
            request,
            outline,
        )

        if len(story.panels) != self.settings.panel_count:

            raise RuntimeError(
                f"Gemini returned "
                f"{len(story.panels)} panels; "
                f"expected "
                f"{self.settings.panel_count}."
            )

        image_urls = []

        for panel in story.panels:

            image_url = self.images.generate_image(
                panel.image_prompt,
                panel.panel_number,
            )

            image_urls.append(
                image_url
            )

        layout = build_comic_layout(
            story,
            image_urls,
        )

        pdf_filename = save_pdf(
            layout,
            self.settings.static_dir,
            self.settings.exports_dir,
        )

        return layout, pdf_filename

    def test_image(
        self,
        prompt: str,
    ):

        return self.images.generate_image(
            prompt,
            0,
        )