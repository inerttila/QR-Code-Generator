from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from fastapi.responses import FileResponse
import qrcode

app = FastAPI()

# Ensure the 'qrcodes' directory exists
qrcodes_directory = Path("qrcodes")
qrcodes_directory.mkdir(exist_ok=True)  # Creates the directory if it doesn't exist

# Mount the directory for static file serving
app.mount("/qrcodes", StaticFiles(directory=qrcodes_directory), name="qrcodes")


@app.get("/")
async def home():
    return FileResponse("index.html")


@app.post("/generate-qr")
async def generate_qr_code(request: Request):
    try:
        data = await request.json()
        url = data.get("url")
        if url:
            img = qrcode.make(url)
            filename = "qrcode.png"
            img.save(str(qrcodes_directory / filename))  # Save the QR code in the 'qrcodes' folder
            return {"message": "QR code generated successfully!", "qrcode": filename}
        else:
            raise HTTPException(status_code=422, detail="Invalid data format")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")
