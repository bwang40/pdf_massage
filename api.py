from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import shutil
import tempfile
from pipeline import run_pipeline

app = FastAPI()
app.mount('/static', StaticFiles(directory='static'), name='static')

@app.get('/', response_class=HTMLResponse)
async def index() -> str:
    return Path('static/index.html').read_text(encoding='utf-8')

@app.post('/process')
async def process_pdf(pdf: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
        shutil.copyfileobj(pdf.file, tmp)
        tmp_path = tmp.name
    run_pipeline(tmp_path)
    return {'status': 'completed'}
