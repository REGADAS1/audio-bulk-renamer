import os
from pathlib import Path

def generate_new_name(file_path, prefix="", suffix="", find_text="", replace_text=""):
    """Generates a new filename by applying a prefix, suffix, and replacements."""
    p = Path(file_path)
    base_name = p.stem            # nome do ficheiro sem extensão
    ext = p.suffix               # extensão, incluindo o ponto (ex: ".mp3")
    if find_text:
        base_name = base_name.replace(find_text, replace_text)
    # Aplica prefixo e sufixo
    new_base = f"{prefix}{base_name}{suffix}"
    return new_base + ext

def rename_files(file_paths, prefix="", suffix="", find_text="", replace_text=""):
    """Renames files based on the provided options. Returns a list of new file paths."""
    renamed_files = []
    for file_path in file_paths:
        new_name = generate_new_name(file_path, prefix, suffix, find_text, replace_text)
        src = Path(file_path)
        dst = src.with_name(new_name)  # novo caminho no mesmo diretório
        try:
            if dst.exists():
                # Evita sobrescrever ficheiro existente com o mesmo nome
                print(f"[Warning] Destination file '{dst.name}' already exists, skipping renaming.")
                continue
            src.rename(dst)
            renamed_files.append(str(dst))
        except Exception as e:
            print(f"[Error] Failed to Rename '{file_path}' -> '{new_name}': {e}")
    return renamed_files
