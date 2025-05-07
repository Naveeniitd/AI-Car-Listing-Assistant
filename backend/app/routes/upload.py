# In backend/app/routes/upload.py
from fastapi import APIRouter, UploadFile, File, Form
import json

router = APIRouter()

@router.post("/upload")
async def upload_car(
    images: list[UploadFile] = File(...),
    metadata: str = Form(...)  # Receive as string
):
    try:
        # Parse the JSON string
        metadata_dict = json.loads(metadata)
    except json.JSONDecodeError as e:
        return {"error": f"Invalid JSON: {str(e)}"}
    
    # Now use metadata_dict as a proper dictionary
    return {
        "message": "Upload successful",
        "metadata": metadata_dict,
        "file_count": len(images)
    }