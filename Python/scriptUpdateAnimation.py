import os
import unreal

# --- Configurazione ---
FPS = 30  # frame al secondo della sequenza
CONTROL_RIG_NAME = "Face_ControlBoard_CtrlRig"  # nome del Control Rig facciale da cercare
LEFT_EYE_CHANNEL_IDX = 130   # indice canale palpebra sinistra (assunzione specifica della scena)
RIGHT_EYE_CHANNEL_IDX = 133  # indice canale palpebra destra (assunzione specifica della scena)
PRE_OFFSET = 3    # frame prima del picco di chiusura
POST_OFFSET = 3   # frame dopo il picco di chiusura
PARAM_FILE_NAME = "blink_times.txt"

# --- Lettura parametri (secondi) da file ---
project_path = unreal.SystemLibrary.get_project_directory()
param_path = os.path.join(project_path, "Python", PARAM_FILE_NAME)

try:
    with open(param_path, "r") as f:
        content = f.read().strip()
        BLINK_TIMES = [float(s.strip()) for s in content.split(",") if s.strip()]
except Exception as e:
    unreal.log_error(f"[BlinkUpdate] Errore di lettura '{param_path}': {e}")
    BLINK_TIMES = []

if not BLINK_TIMES:
    unreal.log_warning("[BlinkUpdate] Nessun tempo di blink definito. Interrompo.")
    raise SystemExit

# --- Recupero sequenza attiva ---
sequence = unreal.LevelSequenceEditorBlueprintLibrary.get_current_level_sequence()
if not sequence:
    unreal.log_error("[BlinkUpdate] Nessuna Level Sequence aperta nel Sequencer.")
    raise SystemExit

# --- Inserimento keyframe su canali palpebre del Control Rig ---
for binding in sequence.get_bindings():
    for track in binding.get_tracks():
        # Considera solo tracce di tipo Control Rig
        if not isinstance(track, unreal.MovieSceneControlRigParameterTrack):
            continue

        # Verifica che sia il Control Rig facciale atteso
        if CONTROL_RIG_NAME.lower() not in str(track.get_display_name()).lower():
            continue

        sections = track.get_sections()
        if not sections:
            unreal.log_warning(f"[BlinkUpdate] Nessuna sezione in '{track.get_display_name()}'.")
            continue

        section = sections[0]
        float_channels = [
            ch for ch in section.get_all_channels()
            if isinstance(ch, unreal.MovieSceneScriptingFloatChannel)
        ]

        # Verifica che gli indici esistano
        max_idx = max(LEFT_EYE_CHANNEL_IDX, RIGHT_EYE_CHANNEL_IDX)
        if len(float_channels) <= max_idx:
            unreal.log_error(
                f"[BlinkUpdate] Canali insufficienti ({len(float_channels)}) per '{track.get_display_name()}'."
            )
            continue

        channel_left = float_channels[LEFT_EYE_CHANNEL_IDX]
        channel_right = float_channels[RIGHT_EYE_CHANNEL_IDX]

        # Pulisce eventuali key preesistenti
        for key in list(channel_left.get_keys()):
            channel_left.remove_key(key)
        for key in list(channel_right.get_keys()):
            channel_right.remove_key(key)

        # Aggiunge nuovi keyframe per ciascun tempo
        for t in BLINK_TIMES:
            base_frame = int(t * FPS)
            # 0.0 = occhio aperto, 1.0 = occhio chiuso
            keyframes = [
                (base_frame - PRE_OFFSET, 0.0),
                (base_frame,               1.0),
                (base_frame + POST_OFFSET, 0.0),
            ]
            for frame, value in keyframes:
                channel_left.add_key(unreal.FrameNumber(frame), value)
                channel_right.add_key(unreal.FrameNumber(frame), value)

        unreal.log(f"[BlinkUpdate] Blink inseriti in '{track.get_display_name()}' ai tempi: {BLINK_TIMES}")
