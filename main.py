from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from fastapi.responses import FileResponse
import qrcode

app = FastAPI()

app.mount("/qrcodes", StaticFiles(directory=Path("qrcodes")), name="qrcodes")


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
            img.save("./qrcodes/" + filename)
            return {"message": "QR code generated successfully!", "qrcode": filename}
        else:
            raise HTTPException(status_code=422, detail="Invalid data format")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")
