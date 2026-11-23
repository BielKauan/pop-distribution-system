import hashlib
from pathlib import Path

def _sha256(file: Path) -> str:
    digest = hashlib.sha256()
    with file.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            digest.update(chunk)
    return digest.hexdigest()

def build_manifest(pops_dir: Path) -> dict:
    files = sorted(f for f in pops_dir.rglob("*") if f.is_file())

    entries = [
        {
            "path": f.relative_to(pops_dir).as_posix(),
            "sha256": _sha256(f),
            "size": f.stat().st_size,
        }
        for f in files
    ]

    overall = hashlib.sha256()
    for e in entries:
        overall.update(f'{e["path"]}:{e["sha256"]}\n'.encode())

    return {"version": overall.hexdigest(), "files": entries}