import uuid
from pathlib import Path

from huggingface_hub import InferenceClient
from huggingface_hub.errors import HfHubHTTPError


class ImageGenerationUnavailable(RuntimeError):
    """Image generation cannot proceed because provider capacity is unavailable."""


class ImageGenerator:
    """Text-to-image generation using Hugging Face."""

    def __init__(
        self,
        token: str,
        model: str,
        output_dir: Path,
        width: int,
        height: int,
        steps: int,
        guidance_scale: float,
    ):

        self.token = token
        self.model = model
        self.output_dir = output_dir
        self.width = width
        self.height = height
        self.steps = steps
        self.guidance_scale = guidance_scale

        self.client = None

        if token:

            self.client = InferenceClient(
                api_key=token,
                provider="auto",
            )

        self.output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

    def _require_client(self):

        if self.client is None:

            raise RuntimeError(
                "HF_TOKEN is missing. "
                "Add your Hugging Face token to .env "
                "and restart the server."
            )

        return self.client

    def generate_image(
        self,
        prompt: str,
        panel_number: int,
    ):

        client = self._require_client()

        # Strong character-consistency instructions are included in every
        # panel prompt. This improves consistency, but cannot guarantee
        # pixel-identical characters without a reference-image workflow.
        consistency_prompt = (
            "CHARACTER CONSISTENCY: Preserve the exact character identity "
            "described in the story prompt across every comic panel. "
            "Keep the same species, age, face shape, facial features, "
            "fur or hair color and pattern, eye color, body proportions, "
            "ears, tail, clothing, accessories, and overall appearance. "
            "Do not redesign, replace, age, or change the main character. "
            "If the character appears in multiple panels, make the character "
            "look like the same individual every time. "
        )

        final_prompt = (
            f"{consistency_prompt}"
            f"CURRENT PANEL SCENE: {prompt}. "
            "Professional sequential comic illustration, "
            "expressive character, cinematic composition, "
            "detailed environment, polished linework, rich color, "
            "consistent character design, no written words, "
            "no watermark, no logo."
        )

        try:
            image = client.text_to_image(
                final_prompt,
                model=self.model,
                width=self.width,
                height=self.height,
                num_inference_steps=self.steps,
                guidance_scale=self.guidance_scale,
                negative_prompt=(
                    "blurry, distorted anatomy, duplicate characters, "
                    "different character design, changed fur or hair color, "
                    "changed face, changed clothing, changed body proportions, "
                    "text, watermark, logo"
                ),
            )
        except HfHubHTTPError as exc:
            response = getattr(exc, "response", None)
            if getattr(response, "status_code", None) == 402:
                raise ImageGenerationUnavailable(
                    "Hugging Face image-generation credits are exhausted. "
                    "Add credits in your Hugging Face account or configure "
                    "a different image-generation provider, then try again."
                ) from exc
            raise

        filename = (
            f"panel_{panel_number}_"
            f"{uuid.uuid4().hex[:10]}.png"
        )

        path = self.output_dir / filename

        image.save(path)

        return f"/static/panels/{filename}"