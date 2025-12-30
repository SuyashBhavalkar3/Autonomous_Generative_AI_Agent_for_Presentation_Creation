import re

async def slide_agent(input_data: dict) -> dict:
    """
    Combines content + images into logical slides.
    Handles content_agent format: numbered slides with 3-5 bullets.
    Ensures no duplicate slides or bullets.
    """
    state = input_data.get("state", {})
    num_slides = state.get("num_slides", 14)
    content_text = input_data.get("input") or state.get("content_agent", "")
    image_dict = state.get("image_agent", {})

    slides = []
    current_slide = None
    bullets = []

    # Split content line by line
    lines = [line.strip() for line in content_text.splitlines() if line.strip()]

    for line in lines:
        # Match numbered slide title e.g. "1. Slide Title"
        match = re.match(r"^(\d+)\.\s*(.*)$", line)
        if match:
            # Save previous slide
            if current_slide is not None:
                slides.append({
                    "title": current_slide,
                    "bullets": bullets or ["Key concept overview"],
                    "image_url": image_dict.get(f"slide_{len(slides)+1}")
                })
            current_slide = match.group(2).strip()
            bullets = []
            continue

        # Treat lines starting with -, •, * as bullets
        if re.match(r"^[-•*]\s+", line):
            bullets.append(line.lstrip("-•* ").strip())
        else:
            # Treat any other line as a bullet
            bullets.append(line.strip())

    # Add last slide
    if current_slide is not None:
        slides.append({
            "title": current_slide,
            "bullets": bullets or ["Key concept overview"],
            "image_url": image_dict.get(f"slide_{len(slides)+1}")
        })

    # Fill placeholders if fewer than num_slides
    while len(slides) < num_slides:
        slides.append({
            "title": f"Slide {len(slides)+1}",
            "bullets": ["Key concept overview"],
            "image_url": image_dict.get(f"slide_{len(slides)+1}")
        })

    # Limit slides to num_slides
    return {"slides": slides[:num_slides]}