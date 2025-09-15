from __future__ import annotations

import os
import uuid
from pathlib import Path
from typing import Dict, List

import gpxpy
from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import FileResponse

# Simple in-memory store for metadata about uploaded GPX files
GPX_STORAGE: Dict[str, Dict[str, str]] = {}

router = APIRouter(prefix="/api/gpx", tags=["gpx"])

# Base directory where uploaded files will be stored
UPLOAD_DIR = Path(__file__).resolve().parent.parent / "static" / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def _extract_geometry(gpx: gpxpy.gpx.GPX) -> Dict:
    """Extract a GeoJSON geometry from the first track in a GPX file.

    Parameters
    ----------
    gpx: gpxpy.gpx.GPX
        Parsed GPX object.

    Returns
    -------
    Dict
        GeoJSON-like representation of the track geometry.
    """
    coordinates: List[List[float]] = []
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                coordinates.append([point.longitude, point.latitude])
    return {"type": "LineString", "coordinates": coordinates}


def process_gpx_file(upload: UploadFile, save_dir: Path = UPLOAD_DIR) -> Dict:
    """Process an uploaded GPX file.

    The file is stored on disk and its geometry is extracted.

    Parameters
    ----------
    upload: UploadFile
        Incoming file from a request.
    save_dir: Path
        Directory where the file will be written.

    Returns
    -------
    Dict
        Metadata including ``id``, ``filename``, ``filepath`` and
        ``geometry``.
    """
    content = upload.file.read()
    try:
        gpx = gpxpy.parse(content.decode())
    except Exception as exc:  # pragma: no cover - defensive
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    geometry = _extract_geometry(gpx)

    file_id = str(uuid.uuid4())
    filename = f"{file_id}_{upload.filename}"
    filepath = save_dir / filename
    with open(filepath, "wb") as out_file:
        out_file.write(content)

    return {
        "id": file_id,
        "filename": filename,
        "filepath": str(filepath),
        "geometry": geometry,
    }


@router.post("/upload")
async def upload_gpx(file: UploadFile = File(...)) -> Dict:
    """Upload a GPX file and store metadata in memory."""
    meta = process_gpx_file(file)
    GPX_STORAGE[meta["id"]] = meta
    return {"id": meta["id"], "geometry": meta["geometry"]}


@router.get("/{gpx_id}/download")
async def download_gpx(gpx_id: str):
    """Download a previously uploaded GPX file by ``id``."""
    meta = GPX_STORAGE.get(gpx_id)
    if not meta:
        raise HTTPException(status_code=404, detail="GPX file not found")

    return FileResponse(
        path=meta["filepath"],
        media_type="application/gpx+xml",
        filename=meta["filename"],
    )
