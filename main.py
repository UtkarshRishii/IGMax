import os
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from generator.carousel import carousel_generator
from config import config

app = FastAPI(title="FalMax Carousel Agent")

# Serve static files (HTML/CSS/JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve generated outputs for preview
app.mount("/output", StaticFiles(directory="output"), name="output")

class CarouselRequest(BaseModel):
    topic: str
    tone: str = "engaging"
    slide_count: int = 6

@app.get("/")
async def read_index():
    return FileResponse("static/index.html")

@app.post("/generate")
async def generate_carousel(request: CarouselRequest):
    try:
        print(f"Generating carousel for topic: {request.topic}")
        result = await carousel_generator.generate(
            request.topic, 
            request.tone, 
            request.slide_count
        )
        return result
    except Exception as e:
        import traceback
        error_msg = traceback.format_exc()
        print(f"Error during generation:\n{error_msg}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/download/{zip_name}")
async def download_zip(zip_name: str):
    file_path = os.path.join(config.OUTPUT_DIR, zip_name)
    if os.path.exists(file_path):
        return FileResponse(file_path, filename=zip_name)
    raise HTTPException(status_code=404, detail="File not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
