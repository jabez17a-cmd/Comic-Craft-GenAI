from app.schemas import (
    ComicLayout,
    ComicPanel,
    ComicStory,
)


def build_comic_layout(
    story: ComicStory,
    image_urls: list[str],
) -> ComicLayout:

    if len(story.panels) != len(image_urls):

        raise ValueError(
            "Generated image count does not "
            "match story panel count."
        )

    panels = []

    for panel, image_url in zip(
        story.panels,
        image_urls,
    ):

        panels.append(
            ComicPanel(
                panel_number=panel.panel_number,
                title=panel.title,
                image_url=image_url,
                scene_description=panel.scene_description,
                caption=panel.caption,
                narration=panel.narration,
                dialogue=panel.dialogue,
                image_prompt=panel.image_prompt,
            )
        )

    return ComicLayout(
        panels=panels
    )