from types import SimpleNamespace
from unittest.mock import Mock

import pytest
from huggingface_hub.errors import HfHubHTTPError
from fastapi.testclient import TestClient

from app.dependencies import get_comic_service
from app.main import app
from app.schemas import PromptRequest
from app.services.image_generator import (
    ImageGenerationUnavailable,
    ImageGenerator,
)


def test_home_and_health():

    client = TestClient(app)

    home = client.get("/")

    assert home.status_code == 200
    assert 'name="tone"' in home.text
    assert 'name="art_style"' in home.text
    assert 'maxlength="300"' in home.text

    health = client.get("/health")

    assert health.status_code == 200

    assert (
        health.json()["status"]
        == "ok"
    )


def test_prompt_request_accepts_descriptive_art_style():

    request = PromptRequest(
        story_prompt="A hero crosses a stormy sea.",
        character_name="Miriam",
        setting=(
            "A magical forest at night, with ancient trees and glowing flowers "
            "surrounding a small stone cottage overlooking the forest"
        ),
        tone="Epic",
        art_style=(
            "Cinematic biblical comic illustration, dramatic inking, "
            "rich colors, realistic stormy sea"
        ),
    )

    assert len(request.art_style) > 80
    assert len(request.setting) > 120


def test_generation_reports_exhausted_image_credits_as_unavailable():

    class UnavailableComicService:

        def generate(self, payload):
            raise ImageGenerationUnavailable(
                "Hugging Face image-generation credits are exhausted."
            )

    app.dependency_overrides[get_comic_service] = (
        lambda: UnavailableComicService()
    )

    try:
        client = TestClient(app)
        response = client.post(
            "/generate",
            data={
                "story_prompt": "A hero crosses a stormy sea.",
                "character_name": "Miriam",
                "setting": "A stormy sea",
                "tone": "Epic",
                "art_style": "Comic illustration",
            },
        )

        assert response.status_code == 503
        assert "credits are exhausted" in response.text
    finally:
        app.dependency_overrides.pop(get_comic_service, None)


def test_image_generator_translates_hugging_face_payment_required(tmp_path):

    generator = ImageGenerator(
        token="token",
        model="model",
        output_dir=tmp_path,
        width=512,
        height=512,
        steps=4,
        guidance_scale=3.5,
    )
    generator.client = Mock()
    generator.client.text_to_image.side_effect = HfHubHTTPError(
        "Payment Required",
        response=SimpleNamespace(status_code=402, headers={}, request=None),
    )

    with pytest.raises(
        ImageGenerationUnavailable,
        match="credits are exhausted",
    ):
        generator.generate_image("A scene", 1)