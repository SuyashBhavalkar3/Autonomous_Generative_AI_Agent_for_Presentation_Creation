import logging
from pathlib import Path
import httpx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
import uuid

logger = logging.getLogger(__name__)


def download_image(url: str, dest_folder: Path, timeout: int = 10) -> Path | None:
	"""Download image to dest_folder and return file path, or None on failure."""
	if not url or not isinstance(url, str) or not url.startswith(("http://", "https://")):
		logger.warning("Invalid image URL, skipping download: %s", url)
		return None

	try:
		dest_folder.mkdir(parents=True, exist_ok=True)
		fname = url.split("/")[-1].split("?")[0]
		if not fname.lower().endswith((".jpg", ".jpeg", ".png")):
			fname = fname + ".jpg"
		out = dest_folder / fname
		with httpx.Client(timeout=timeout) as client:
			r = client.get(url)
			if r.status_code == 200 and r.content:
				out.write_bytes(r.content)
				return out
			else:
				logger.warning("Image download failed %s status=%s", url, r.status_code)
				return None
	except Exception as e:
		logger.warning("Image download exception %s: %s", url, e)
		return None


def _apply_gamma_theme(prs: Presentation):
	"""Apply a simple dark Gamma-like theme to the Presentation.

	- Dark background
	- Bold white titles
	- Muted gray bullets
	"""
	# Attempt to set slide background for existing slides (new slides will get style from here)
	for slide in prs.slides:
		try:
			fill = slide.background.fill
			fill.solid()
			fill.fore_color.rgb = RGBColor(18, 18, 18)  # very dark gray
		except Exception:
			continue


def build_presentation(slides: list[dict], out_path: Path | str) -> Path:
	"""Create a Gamma-styled PPTX with given slides schema and save to out_path."""
	prs = Presentation()

	# Prepare a temporary image folder for on-demand downloads when slides provide `image_url`
	tmp_dir = Path("output") / "images" / f"ppt_builder_{uuid.uuid4().hex}"

	# Ensure a blank slide layout exists for image-focused slides
	blank_layout = prs.slide_layouts[6] if len(prs.slide_layouts) > 6 else prs.slide_layouts[-1]

	for s in slides:
		title = s.get("title", "Untitled")
		bullets = s.get("bullets", [])[:4]  # minimal bullets

		# Support slides that provide either `image_path` (already downloaded)
		# or `image_url` (download on-demand). Do not duplicate external/image
		# fetching logic; reuse `download_image` defined above.
		image_path = s.get("image_path")
		if not image_path:
			image_url = s.get("image_url")
			if image_url:
				try:
					_downloaded = download_image(image_url, tmp_dir)
					image_path = str(_downloaded) if _downloaded else None
				except Exception:
					image_path = None

		slide = prs.slides.add_slide(blank_layout)

		# set dark background
		try:
			fill = slide.background.fill
			fill.solid()
			fill.fore_color.rgb = RGBColor(18, 18, 18)
		except Exception:
			pass

	# Title textbox at top
		try:
			left = Inches(0.5)
			top = Inches(0.2)
			width = Inches(9)
			height = Inches(1.0)
			title_box = slide.shapes.add_textbox(left, top, width, height)
			tf = title_box.text_frame
			tf.clear()
			p = tf.paragraphs[0]
			p.text = title
			p.font.bold = True
			p.font.size = Pt(28)
			p.font.color.rgb = RGBColor(255, 255, 255)
		except Exception:
			logger.debug("Failed to add title box")

		try:
			left = Inches(0.5)
			top = Inches(1.4)
			width = Inches(4.2)
			height = Inches(4.6)
			body_box = slide.shapes.add_textbox(left, top, width, height)
			tf = body_box.text_frame
			tf.clear()
			# Use readable font size and color
			for idx, b in enumerate(bullets):
				if idx == 0:
					p = tf.paragraphs[0]
					p.text = b
				else:
					p = tf.add_paragraph()
					p.text = b
				p.level = 0
				p.font.size = Pt(16)
				p.font.color.rgb = RGBColor(200, 200, 200)
		except Exception:
			logger.debug("Failed to add bullets")

		# Large image on the right if available; placed under the title to avoid overlap
		if image_path:
			try:
				pic_left = Inches(5.0)
				pic_top = Inches(1.2)
				pic_width = Inches(4.0)



				# Ensure image fits vertically; allow pptx to preserve aspect ratio by only setting width
				slide.shapes.add_picture(str(image_path), pic_left, pic_top, width=pic_width)
			except Exception as e:
				logger.warning("Embedding image failed: %s", e)

	out = Path(out_path)
	out.parent.mkdir(parents=True, exist_ok=True)
	prs.save(str(out))
	# Apply theme to saved presentation (best-effort; most styling already applied)
	return out


class PPTBuilder:
	"""Small wrapper class for compatibility with older tests/code.

	Usage:
	    builder = PPTBuilder(output_path="output/foo.pptx")
	    builder.build(slide_agent_output)
	"""

	def __init__(self, output_path: str | Path):
		self.output_path = Path(output_path)

	def build(self, slide_agent_output: dict | list) -> Path:
		# Accept either a dict with `slides` key or a direct list
		if isinstance(slide_agent_output, dict):
			slides = slide_agent_output.get("slides") or []
		else:
			slides = slide_agent_output
		# Defensive: ensure slides is a list of dict
		if not isinstance(slides, list):
			raise ValueError("Invalid slides input for PPTBuilder")
		return build_presentation(slides, self.output_path)