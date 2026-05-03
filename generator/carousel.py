import os
import shutil
import zipfile
import asyncio
from ai.groq_client import groq_client
from renderer.render import render_engine
from config import config

class CarouselGenerator:
    async def generate(self, topic, tone, slide_count):
        # 1. Generate Content
        data = groq_client.generate_carousel_content(topic, tone, slide_count)
        slides = data["slides"]
        
        # 2. Prepare output directory
        session_id = os.urandom(4).hex()
        session_dir = os.path.join(config.SLIDES_DIR, session_id)
        os.makedirs(session_dir, exist_ok=True)
        
        # 3. Render Slides
        image_paths = await render_engine.render_slides(slides, session_dir)
            
        # 4. Save metadata
        with open(os.path.join(session_dir, "metadata.txt"), "w", encoding="utf-8") as f:
            f.write(f"Caption:\n{data['caption']}\n\n")
            f.write(f"Hashtags:\n{' '.join(data['hashtags'])}\n")
            
        # 5. Create ZIP
        zip_path = os.path.join(config.OUTPUT_DIR, f"carousel_{session_id}.zip")
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for file in os.listdir(session_dir):
                zipf.write(os.path.join(session_dir, file), file)
                
        return {
            "session_id": session_id,
            "slides": slides,
            "caption": data["caption"],
            "hashtags": data["hashtags"],
            "zip_url": f"/download/{os.path.basename(zip_path)}",
            "images": [f"/output/slides/{session_id}/{os.path.basename(p)}" for p in image_paths]
        }

carousel_generator = CarouselGenerator()
