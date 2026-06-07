from fastapi import FastAPI
from brochure import create_brochure
from brochure import open_ai_call
from fastapi.responses import StreamingResponse

app = FastAPI()

@app.post("/createBrochure")
async def recieved_data(name:str,url:str):
    return StreamingResponse(
        create_brochure(name,url),
        media_type="text/plain"
    )


