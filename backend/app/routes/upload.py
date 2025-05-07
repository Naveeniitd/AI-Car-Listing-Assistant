# backend/app/routes/upload.py
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import List
import json
import tempfile
import shutil
import os
from app.services.image_processor import ImageProcessor
from datetime import datetime
import logging
from app.models.schemas import CarMetadata 
router = APIRouter()
logger = logging.getLogger(__name__)

# Initialize processor (consider dependency injection for production)
processor = ImageProcessor()

@router.post("/upload")
async def upload_car(
    images: List[UploadFile] = File(...),
    metadata: str = Form(...)
):
    """
    Endpoint for car image upload and processing.
    
    Args:
        images: List of car images (front, side, rear, interior)
        metadata: JSON string containing:
            {
                "user_id": str,
                "platform": "olx|cars24|...",
                "additional_info": {}  # Any manual overrides
            }
    
    Returns:
        Processed car specifications and compliance status
    """
    try:
        # Parse and validate metadata
        try:
            metadata_dict = json.loads(metadata)
            required_fields = ["user_id", "platform"]
            if not all(field in metadata_dict for field in required_fields):
                raise ValueError(f"Missing required fields: {required_fields}")
        except (json.JSONDecodeError, ValueError) as e:
            raise HTTPException(status_code=422, detail=str(e))

        # Process images
        processing_results = []
        temp_dir = tempfile.mkdtemp()
        
        try:
            for idx, image in enumerate(images):
                # Save temporarily (consider async I/O for production)
                file_path = f"{temp_dir}/{datetime.now().timestamp()}_{image.filename}"
                with open(file_path, "wb") as buffer:
                    shutil.copyfileobj(image.file, buffer)
                
                # Process image
                try:
                    result = processor.process_image(file_path)
                    processing_results.append({
                        "original_filename": image.filename,
                        "analysis": result,
                        "processed_at": datetime.now().isoformat()
                    })
                except Exception as e:
                    logger.error(f"Failed to process {image.filename}: {str(e)}")
                    processing_results.append({
                        "original_filename": image.filename,
                        "error": str(e)
                    })
                
                # Clean up temp file immediately
                os.unlink(file_path)

            # Aggregate results from all images
            aggregated = _aggregate_results(processing_results)
            
            # Generate compliance report
            compliance = _check_compliance(processing_results)
            
            return {
                "status": "success",
                "user_id": metadata_dict["user_id"],
                "platform": metadata_dict["platform"],
                "car_specs": aggregated,
                "compliance_report": compliance,
                "warnings": [r for r in processing_results if "error" in r]
            }
            
        finally:
            # Clean up temp directory
            shutil.rmtree(temp_dir, ignore_errors=True)
            
    except Exception as e:
        logger.exception("Upload processing failed")
        raise HTTPException(status_code=500, detail="Internal processing error")

def _aggregate_results(results: List[dict]) -> dict:
    """
    Combine analysis from multiple images into unified specs
    """
    aggregated = {
        "make_model": None,
        "color": None,
        "damages": [],
        "license_plates": []
    }
    
    # Implement your aggregation logic here
    for result in results:
        if "analysis" not in result:
            continue
            
        analysis = result["analysis"]
        
        # Take highest confidence make/model
        if (aggregated["make_model"] is None or 
            analysis["make_model"]["confidence"] > aggregated["make_model"]["confidence"]):
            aggregated["make_model"] = analysis["make_model"]
            
        # Similar logic for color
        if aggregated["color"] is None:
            aggregated["color"] = analysis.get("color")
            
        # Combine all damages and plates
        aggregated["damages"].extend(analysis.get("damages", []))
        aggregated["license_plates"].extend(analysis.get("license_plates", []))
    
    return aggregated

def _check_compliance(results: List[dict]) -> dict:
    """
    Generate compliance report based on platform requirements
    """
    compliance = {
        "background_issues": [],
        "image_quality_issues": [],
        "required_angles_missing": []
    }
    
    # Check background uniformity
    for result in results:
        if "analysis" in result and not result["analysis"]["background_check"]["is_compliant"]:
            compliance["background_issues"].append(result["original_filename"])
    
    # Add other compliance checks as needed
    
    compliance["is_compliant"] = all(
        not compliance[k] for k in compliance if k != "is_compliant"
    )
    
    return compliance