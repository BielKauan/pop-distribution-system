import os
import tempfile
import zipfile
from pathlib import Path

from server.spp.services.manifest import build_manifest
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from starlette.background import BackgroundTask

router = APIRouter(
    prefix="/api/v1/pops",
    tags=["Distribuição de POPs"]
)
PROJECT_ROOT = Path(__file__).resolve().parents[3]
POPS_DIR = PROJECT_ROOT / "storage" / "POPs"

@router.get("/dowload")
def dowload_pops():

    if not POPS_DIR.is_dir():
        raise HTTPException(
            status_code=404,
            detail="Repositório de POPs não encontrado."
        )
    files = [
        file for file in POPS_DIR.rglob("*")
        if file.is_file()

    ]

    if not files:
        raise HTTPException(
            status_code=404,
            detail="Nenhum arquivo POP encontrado para distribuição."
        )

    file_descriptor, zip_path = tempfile.mkstemp(suffix=".zip")
    os.close(file_descriptor)

    try:
        with zipfile.ZipFile(
            zip_path,
            "w",
            compression=zipfile.ZIP_DEFLATED
        )as archive:

            for file in files:
                relative_path =(
                    Path("POPs") / file.relative_to(POPS_DIR)
                )

                archive.write(
                    file,
                    arcname=relative_path
                )

    except Exception:
        os.unlink(zip_path)
        raise

    

    return FileResponse(
        path=zip_path,
        filename="POPs.zip",
        media_type="application/zip",
        background=BackgroundTask(os.unlink, zip_path)
    )  


@router.get("/manifest")
def manifest_pops():
    if not POPS_DIR.is_dir():
        raise HTTPException(
            status_code=404,
            detail="Repositório de POPs não encontrado."
        )

    manifest = build_manifest(POPS_DIR)

    if not manifest["files"]:
        raise HTTPException(
            status_code=404,
            detail="Nenhum arquivo POP encontrado para distribuição"
        )
    return manifest
