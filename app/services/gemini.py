import time

from google.genai import errors

from app.schemas import ComicOutline, ComicStory


class GeminiService:
    """Gemini text-generation layer."""

    def __init__(
        self,
        api_key: str,
        outline_model: str,
        story_model: str,
        panel_count: int,
    ):

        self.api_key = api_key
        self.outline_model = outline_model
        self.story_model = story_model
        self.panel_count = panel_count

        self.client = None

        if api_key:

            from google import genai

            self.client = genai.Client(
                api_key=api_key
            )

    def _generate_content(
        self,
        client,
        fallback_model=None,
        **kwargs,
    ):
        retryable_codes = {429, 500, 502, 503, 504}
        primary_model = kwargs.get("model")
        models = [primary_model]

        if fallback_model and fallback_model != primary_model:
            models.append(fallback_model)

        for model_index, model in enumerate(models):
            retries = 0

            while True:
                try:
                    return client.models.generate_content(
                        **{**kwargs, "model": model}
                    )
                except errors.APIError as exc:
                    if exc.code not in retryable_codes:
                        raise

                    if exc.code == 429:
                        if model_index == len(models) - 1:
                            raise
                        break

                    if retries >= 2:
                        if model_index == len(models) - 1:
                            raise
                        break

                    time.sleep(2**retries)
                    retries += 1

    def _require_client(self):

        if self.client is None:

            raise RuntimeError(
                "GEMINI_API_KEY is missing. "
                "Add it to your .env file and restart the server."
            )

        return self.client

    def generate_outline(self, request) -> ComicOutline:

        client = self._require_client()

        prompt = f"""
You are ComicCraft's comic outline director.

Create exactly {self.panel_count} sequential comic panels.

USER STORY:
{request.story_prompt}

MAIN CHARACTER:
{request.character_name}

SETTING:
{request.setting}

TONE:
{request.tone}

ART STYLE:
{request.art_style}

Requirements:

- Return exactly {self.panel_count} panels.
- Maintain protagonist consistency.
- Create a clear beginning.
- Develop the conflict.
- Include a turning point.
- End with a satisfying conclusion.
- Every panel must advance the story.
- scene_description describes the visual action.
- image_prompt describes what the image model should draw.
- Do not place written dialogue or speech bubbles in image_prompt.
"""

        from google.genai import types

        response = self._generate_content(
            client,
            fallback_model=self.story_model,
            model=self.outline_model,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.9,
                response_mime_type="application/json",
                response_schema=ComicOutline,
            ),
        )

        if getattr(response, "parsed", None) is not None:

            return ComicOutline.model_validate(
                response.parsed
            )

        return ComicOutline.model_validate_json(
            response.text
        )

    def generate_story(
        self,
        request,
        outline: ComicOutline,
    ) -> ComicStory:

        client = self._require_client()

        outline_json = outline.model_dump_json(
            indent=2
        )

        prompt = f"""
You are ComicCraft's senior comic writer.

Turn the supplied outline into polished comic storytelling.

STORY:
{request.story_prompt}

MAIN CHARACTER:
{request.character_name}

SETTING:
{request.setting}

TONE:
{request.tone}

ART STYLE:
{request.art_style}

OUTLINE:
{outline_json}

For every panel provide:

- panel_number
- title
- scene_description
- caption
- narration
- dialogue
- image_prompt

Rules:

- Preserve the same protagonist identity.
- Maintain visual continuity.
- Make events flow naturally.
- Keep narration concise.
- Dialogue should sound natural.
- If dialogue is unnecessary, use an empty string.
- image_prompt must be detailed enough for image generation.
"""

        from google.genai import types

        response = self._generate_content(
            client,
            fallback_model=self.outline_model,
            model=self.story_model,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.85,
                response_mime_type="application/json",
                response_schema=ComicStory,
            ),
        )

        if getattr(response, "parsed", None) is not None:

            return ComicStory.model_validate(
                response.parsed
            )

        return ComicStory.model_validate_json(
            response.text
        )