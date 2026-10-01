from app.schemas import (
    ComicStory,
    PanelStory,
)

from app.services.layout_builder import (
    build_comic_layout,
)


def test_layout_builder():

    story = ComicStory(
        panels=[
            PanelStory(
                panel_number=1,
                title="Start",
                scene_description=(
                    "A fox enters a forest."
                ),
                caption="Dawn.",
                narration=(
                    "The adventure begins."
                ),
                dialogue="Let's go!",
                image_prompt=(
                    "Fox in forest."
                ),
            )
        ]
    )

    layout = build_comic_layout(
        story,
        [
            "/static/panels/one.png"
        ],
    )

    assert (
        layout.panels[0].image_url
        == "/static/panels/one.png"
    )