from ppt.ppt_builder import PPTBuilder

# ---- Mock slide_agent output ----
mock_slide_agent_output = {
    "slides": [
        {
            "title": "Introduction to Generative AI",
            "bullets": [
                "AI systems that create content",
                "Uses deep learning models",
                "Text, images, audio generation"
            ],
            "image_url": "https://images.unsplash.com/photo-1581090700227-1e37b190418e"
        },
        {
            "title": "Applications",
            "bullets": [
                "Chatbots and assistants",
                "Image generation",
                "Code generation"
            ],
            "image_url": "https://images.unsplash.com/photo-1677442136019-21780ecad995"
        }
    ]
}

# ---- Run PPT Builder ----
builder = PPTBuilder(output_path="output/test_presentation.pptx")
ppt_path = builder.build(mock_slide_agent_output)

print("✅ PPT generated at:", ppt_path)
