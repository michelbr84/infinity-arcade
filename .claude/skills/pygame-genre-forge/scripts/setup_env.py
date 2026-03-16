#!/usr/bin/env python3
"""
setup_env.py — Detecta o SO, cria .venv e instala dependências para Pygame Genre Forge.

Este script é o primeiro passo executado pela skill. Ele:
1. Detecta o sistema operacional (Linux/Windows/macOS)
2. Verifica Python >= 3.10
3. Cria um ambiente virtual .venv (se não existir)
4. Instala dependências (pygame, Pillow)
5. Valida a instalação
6. Configura headless se necessário (CI/sem display)
"""

import os
import platform
import re
import subprocess
import sys
from pathlib import Path

# Cores para output no terminal
class Colors:
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    CYAN = "\033[96m"
    BOLD = "\033[1m"
    RESET = "\033[0m"


def log_info(msg: str) -> None:
    print(f"{Colors.CYAN}[INFO]{Colors.RESET} {msg}")


def log_success(msg: str) -> None:
    print(f"{Colors.GREEN}[OK]{Colors.RESET} {msg}")


def log_warn(msg: str) -> None:
    print(f"{Colors.YELLOW}[WARN]{Colors.RESET} {msg}")


def log_error(msg: str) -> None:
    print(f"{Colors.RED}[ERRO]{Colors.RESET} {msg}")


def get_project_root() -> Path:
    """Retorna o diretório raiz do projeto (onde está o .claude/)."""
    # Navega a partir deste script: scripts/ -> pygame-genre-forge/ -> skills/ -> .claude/ -> root
    script_dir = Path(__file__).resolve().parent
    return script_dir.parent.parent.parent.parent


def detect_os() -> dict:
    """Detecta o sistema operacional e retorna informações relevantes."""
    os_name = platform.system()
    os_info = {
        "system": os_name,
        "release": platform.release(),
        "machine": platform.machine(),
        "python_cmd": "python3",
        "pip_cmd": None,  # será definido após criar venv
        "venv_python": None,
        "is_ci": os.environ.get("CI", "").lower() in ("true", "1", "yes"),
        "has_display": bool(os.environ.get("DISPLAY")) or os_name != "Linux",
    }

    if os_name == "Windows":
        os_info["python_cmd"] = "python"

    log_info(f"Sistema operacional: {Colors.BOLD}{os_name}{Colors.RESET} "
             f"({platform.release()}, {platform.machine()})")

    if os_info["is_ci"]:
        log_info("Ambiente de CI detectado")

    if not os_info["has_display"] and os_name == "Linux":
        log_warn("Sem display detectado (sem $DISPLAY). Modo headless será configurado.")

    return os_info


def check_python_version() -> None:
    """Verifica que Python >= 3.10 está disponível."""
    major, minor = sys.version_info[:2]
    version_str = f"{major}.{minor}.{sys.version_info[2]}"

    if major < 3 or (major == 3 and minor < 10):
        log_error(f"Python {version_str} detectado. Requer Python >= 3.10.")
        log_error("Instale Python 3.10+ e tente novamente:")
        log_error("  Linux:   sudo apt install python3.10 python3.10-venv")
        log_error("  macOS:   brew install python@3.10")
        log_error("  Windows: https://www.python.org/downloads/")
        sys.exit(1)

    log_success(f"Python {version_str} ✓")


def create_venv(project_root: Path, os_info: dict) -> dict:
    """Cria o ambiente virtual .venv se não existir."""
    venv_dir = project_root / ".venv"

    if os_info["system"] == "Windows":
        venv_python = venv_dir / "Scripts" / "python.exe"
        venv_pip = venv_dir / "Scripts" / "pip.exe"
    else:
        venv_python = venv_dir / "bin" / "python"
        venv_pip = venv_dir / "bin" / "pip"

    os_info["venv_python"] = str(venv_python)
    os_info["pip_cmd"] = str(venv_pip)

    if venv_dir.exists() and venv_python.exists():
        log_success(f".venv já existe em {venv_dir} ✓")
        return os_info

    log_info(f"Criando ambiente virtual em {venv_dir}...")

    try:
        subprocess.run(
            [sys.executable, "-m", "venv", str(venv_dir)],
            check=True,
            capture_output=True,
            text=True,
        )
        log_success(f".venv criada com sucesso ✓")
    except subprocess.CalledProcessError as e:
        log_error(f"Falha ao criar .venv: {e.stderr}")
        if "ensurepip" in e.stderr or "venv" in e.stderr:
            log_error("Instale o módulo venv:")
            log_error(f"  sudo apt install python{sys.version_info[0]}.{sys.version_info[1]}-venv")
        sys.exit(1)

    return os_info


def install_dependencies(project_root: Path, os_info: dict) -> None:
    """Instala dependências dentro da .venv."""
    pip_cmd = os_info["pip_cmd"]
    requirements_file = project_root / "requirements.txt"

    # Atualiza pip primeiro
    log_info("Atualizando pip...")
    try:
        subprocess.run(
            [os_info["venv_python"], "-m", "pip", "install", "--upgrade", "pip"],
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError:
        log_warn("Não foi possível atualizar pip, continuando com versão atual...")

    # Instala dependências do requirements.txt
    if requirements_file.exists():
        log_info(f"Instalando dependências de {requirements_file.name}...")
        try:
            result = subprocess.run(
                [pip_cmd, "install", "-r", str(requirements_file)],
                check=True,
                capture_output=True,
                text=True,
            )
            # Conta pacotes instalados
            installed = [l for l in result.stdout.split("\n")
                         if "Successfully installed" in l or "already satisfied" in l.lower()]
            for line in installed:
                log_info(f"  {line.strip()}")
            log_success("Dependências instaladas ✓")
        except subprocess.CalledProcessError as e:
            log_error(f"Falha ao instalar dependências: {e.stderr}")
            sys.exit(1)
    else:
        # Instala manualmente se requirements.txt não existir
        log_warn("requirements.txt não encontrado. Instalando dependências mínimas...")
        deps = ["pygame>=2.5.0", "Pillow>=10.0.0"]
        for dep in deps:
            try:
                subprocess.run(
                    [pip_cmd, "install", dep],
                    check=True,
                    capture_output=True,
                    text=True,
                )
                log_success(f"  {dep} instalado ✓")
            except subprocess.CalledProcessError as e:
                log_error(f"  Falha ao instalar {dep}: {e.stderr}")
                sys.exit(1)

    # Instala o próprio projeto em modo editável (se pyproject.toml existir)
    pyproject = project_root / "pyproject.toml"
    if pyproject.exists():
        log_info("Instalando projeto em modo editável...")
        try:
            subprocess.run(
                [pip_cmd, "install", "-e", str(project_root)],
                check=True,
                capture_output=True,
                text=True,
            )
            log_success("Projeto instalado em modo editável ✓")
        except subprocess.CalledProcessError as e:
            log_warn(f"Instalação editável falhou (não crítico): {e.stderr[:200]}")


def validate_installation(os_info: dict) -> None:
    """Valida que pygame e dependências estão funcionando."""
    venv_python = os_info["venv_python"]

    log_info("Validando instalação do pygame...")

    # Testa import do pygame
    try:
        result = subprocess.run(
            [venv_python, "-c",
             "import pygame; print(f'pygame {pygame.ver}')"],
            check=True,
            capture_output=True,
            text=True,
        )
        version = result.stdout.strip()
        log_success(f"{version} ✓")
    except subprocess.CalledProcessError as e:
        log_error(f"pygame não funciona: {e.stderr}")
        sys.exit(1)

    # Testa import do Pillow
    try:
        result = subprocess.run(
            [venv_python, "-c",
             "from PIL import Image; print(f'Pillow OK')"],
            check=True,
            capture_output=True,
            text=True,
        )
        log_success("Pillow ✓")
    except subprocess.CalledProcessError:
        log_warn("Pillow não disponível (captura de screenshots pode ser limitada)")


def configure_headless(os_info: dict) -> None:
    """Configura ambiente headless se necessário."""
    if os_info["has_display"] and not os_info["is_ci"]:
        log_info("Display disponível — modo gráfico normal.")
        return

    log_info("Configurando modo headless...")

    # SDL_VIDEODRIVER=dummy para rodar sem janela
    os.environ["SDL_VIDEODRIVER"] = "dummy"
    log_success("SDL_VIDEODRIVER=dummy configurado ✓")

    if os_info["system"] == "Linux":
        # Verifica se Xvfb está disponível
        try:
            subprocess.run(
                ["which", "Xvfb"],
                check=True,
                capture_output=True,
            )
            log_success("Xvfb disponível (use para fidelidade visual em CI)")
            log_info("  Para usar: Xvfb :99 -screen 0 800x600x24 &")
            log_info("  export DISPLAY=:99")
        except (subprocess.CalledProcessError, FileNotFoundError):
            log_warn("Xvfb não encontrado. Para instalar:")
            log_warn("  sudo apt install xvfb")
            log_info("  O SDL_VIDEODRIVER=dummy será usado como fallback.")


def print_summary(project_root: Path, os_info: dict) -> None:
    """Imprime resumo final do setup."""
    print()
    print(f"{Colors.BOLD}{'='*60}{Colors.RESET}")
    print(f"{Colors.GREEN}{Colors.BOLD} ✓ GenreForge Arcade — Ambiente Configurado!{Colors.RESET}")
    print(f"{Colors.BOLD}{'='*60}{Colors.RESET}")
    print()
    print(f"  SO:         {os_info['system']} ({os_info['release']})")
    print(f"  Python:     {sys.version_info[0]}.{sys.version_info[1]}.{sys.version_info[2]}")
    print(f"  .venv:      {project_root / '.venv'}")
    print(f"  Headless:   {'Sim' if os_info['is_ci'] or not os_info['has_display'] else 'Não'}")
    print()

    if os_info["system"] == "Windows":
        activate = r".venv\Scripts\activate"
    else:
        activate = "source .venv/bin/activate"

    print(f"  {Colors.CYAN}Para ativar o ambiente:{Colors.RESET}")
    print(f"    {activate}")
    print()
    print(f"  {Colors.CYAN}Para gerar um jogo:{Colors.RESET}")
    print(f"    /pygame-genre-forge shooter \"nave espacial com tiros coloridos\"")
    print()


def main() -> None:
    """Fluxo principal do setup."""
    print()
    print(f"{Colors.BOLD}{Colors.CYAN}╔══════════════════════════════════════════════╗{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}║   GenreForge Arcade — Setup do Ambiente      ║{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}╚══════════════════════════════════════════════╝{Colors.RESET}")
    print()

    # 1. Detecta projeto root
    project_root = get_project_root()
    log_info(f"Diretório do projeto: {project_root}")

    # 2. Detecta SO
    os_info = detect_os()

    # 3. Verifica Python
    check_python_version()

    # 4. Cria .venv
    os_info = create_venv(project_root, os_info)

    # 5. Instala dependências
    install_dependencies(project_root, os_info)

    # 6. Valida instalação
    validate_installation(os_info)

    # 7. Configura headless (se necessário)
    configure_headless(os_info)

    # 8. Resumo
    print_summary(project_root, os_info)


if __name__ == "__main__":
    main()
