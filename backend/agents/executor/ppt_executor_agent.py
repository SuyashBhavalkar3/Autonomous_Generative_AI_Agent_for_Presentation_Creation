import asyncio
import logging
from pathlib import Path
from typing import Dict
import uuid

# Import ppt builder robustly: prefer package import, fallback to loading by file path
try:
    from ppt.ppt_builder import download_image, build_presentation
except Exception:
    import importlib.util
    from pathlib import Path as _P

    backend_root = _P(__file__).resolve().parents[2]
    ppt_file = backend_root / "ppt" / "ppt_builder.py"
    spec = importlib.util.spec_from_file_location("ppt_builder", str(ppt_file))
    ppt_mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ppt_mod)
    download_image = ppt_mod.download_image
    build_presentation = ppt_mod.build_presentation

logger = logging.getLogger(__name__)


async def executor_agent(input_data: Dict) -> Dict:
    """Builds a Gamma-styled PPTX using `ppt_builder`.

    Expects `state` to contain `slide_agent` with {'slides': [...]}.
    Downloads images to a temporary folder and returns a unique output path.
    """
    state = input_data.get("state", {})
    num_slides = int(state.get("num_slides", 14) or 14)

    slides_data = state.get("slide_agent")
    if slides_data is None:
        logger.error("executor_agent: missing slide_agent output in state")
        return {"error": "missing slide data"}

    slides = slides_data.get("slides") if isinstance(slides_data, dict) else slides_data
    if not isinstance(slides, list):
        logger.error("executor_agent: unexpected slide format")
        return {"error": "invalid slide format"}

    out_slides = []
    tmp_dir = Path("output") / "images" / uuid.uuid4().hex

    for idx, s in enumerate(slides[:num_slides], start=1):
        image_url = s.get("image_url")
        image_path = None
        if image_url:
            try:
                # run blocking download in threadpool
                image_path = await asyncio.to_thread(download_image, image_url, tmp_dir)
            except Exception as e:
                logger.warning("Image download failed for slide %s: %s", idx, e)
                image_path = None

        out_slides.append({
            "slide_id": idx,
            "title": s.get("title", f"Slide {idx}"),
            "bullets": s.get("bullets", []),
            "image_path": str(image_path) if image_path else None,
            "image_url": image_url if image_url else None,
        })

    # Build and save the pptx to output/presentations
    out_dir = Path("output") / "presentations"
    out_dir.mkdir(parents=True, exist_ok=True)
    filename = f"presentation_{uuid.uuid4().hex}.pptx"
    out_path = out_dir / filename

    try:
        # build_presentation is IO-bound; run in threadpool
        await asyncio.to_thread(build_presentation, out_slides, out_path)
    except Exception as e:
        logger.exception("Failed to build presentation: %s", e)
        return {"error": str(e)}

    return {"output_file": str(out_path), "slides": out_slides}
