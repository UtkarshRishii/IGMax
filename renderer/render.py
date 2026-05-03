import os
from jinja2 import Template
from playwright.async_api import async_playwright
from config import config

class RenderEngine:
    def __init__(self):
        self.template_path = os.path.join(os.path.dirname(__file__), "template.html")
        self.styles_path = os.path.join(os.path.dirname(__file__), "styles.css")
        
        with open(self.template_path, "r", encoding="utf-8") as f:
            self.template = Template(f.read())
            
        with open(self.styles_path, "r", encoding="utf-8") as f:
            self.css_content = f.read()

    async def render_slides(self, slides_data, output_dir):
        """Renders multiple slides using a single browser instance."""
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(viewport={"width": 1080, "height": 1080})
            page = await context.new_page()
            
            image_paths = []
            for i, slide in enumerate(slides_data):
                # Prepare HTML
                html_content = self.template.render(
                    title=slide["title"],
                    content=slide["content"],
                    slide_index=i + 1,
                    total_slides=len(slides_data),
                    is_hook=(i == 0)
                )
                
                styled_html = html_content.replace('<link rel="stylesheet" href="styles.css">', f'<style>{self.css_content}</style>')
                
                await page.set_content(styled_html)
                await page.wait_for_load_state("networkidle")
                
                output_path = os.path.join(output_dir, f"slide_{i+1}.png")
                await page.screenshot(path=output_path, type="png")
                image_paths.append(output_path)
                
            await browser.close()
            return image_paths

render_engine = RenderEngine()
