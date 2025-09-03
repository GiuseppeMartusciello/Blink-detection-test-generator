import unreal
import os
import time
from pathlib import Path
import shutil
import sys

try:
    project_path = unreal.SystemLibrary.get_project_directory()
    param_path = os.path.join(project_path, "Python", "parameters.txt")
    
    with open(param_path, "r") as f:
        nuovo_nome = f.read().strip()
except Exception as e:
    unreal.log_error(f"[ERRORE] Lettura file: {e}")

# === CONFIGURAZIONE ===
# Cartella dove Unreal salva i render (può essere assoluto o relativo)
render_output_dir = os.path.join(project_path, "Saved", "MovieRenders")

# Nuovo nome da assegnare (senza estensione)
#nuovo_nome = "Render_Light5_Cam2"

# Estensioni da considerare (puoi modificarle)
estensioni_video = [".mp4", ".mov", ".avi", ".exr"]

# === LOGICA ===
def trova_file_video_recente(directory, estensioni):
    files = [f for f in Path(directory).glob("*") if f.suffix.lower() in estensioni]
    if not files:
        return None
    # Ordina per tempo di modifica (decrescente)
    files.sort(key=lambda f: f.stat().st_mtime, reverse=True)
    return files[0]

def rinomina_file(file_path, nuovo_nome):
    new_path = file_path.with_name(nuovo_nome + file_path.suffix)
    shutil.move(str(file_path), str(new_path))
    print(f"✅ File rinominato: {file_path.name} → {new_path.name}")

# === ESECUZIONE ===
file_video = trova_file_video_recente(render_output_dir, estensioni_video)
if file_video:
    rinomina_file(file_video, nuovo_nome)
else:
    print("⚠️ Nessun file video trovato.")
