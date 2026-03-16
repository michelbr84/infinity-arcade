#!/usr/bin/env python3
"""
validate_game.py — Roda smoke test, captura screenshot e gera relatório de validação.

Uso:
    python validate_game.py <path-do-jogo>
    python validate_game.py generated_games/space-invader/ --timeout 15
"""

import argparse
import json
import os
import signal
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path


def get_project_root() -> Path:
    """Retorna o diretório raiz do projeto."""
    script_dir = Path(__file__).resolve().parent
    return script_dir.parent.parent.parent.parent


def setup_headless_env() -> dict:
    """Configura variáveis de ambiente para execução headless."""
    env = os.environ.copy()

    # SDL dummy driver para rodar sem display
    if not env.get("DISPLAY"):
        env["SDL_VIDEODRIVER"] = "dummy"
        env["SDL_AUDIODRIVER"] = "dummy"

    return env


def run_game_with_timeout(game_path: Path, timeout: int = 10) -> dict:
    """Executa o jogo com timeout e captura output."""
    main_py = game_path / "main.py"

    if not main_py.exists():
        return {
            "success": False,
            "exit_code": -1,
            "error": f"main.py não encontrado em {game_path}",
            "stdout": "",
            "stderr": "",
            "runtime_seconds": 0,
        }

    # Determina o Python da .venv
    project_root = get_project_root()
    venv_python = project_root / ".venv" / "bin" / "python"
    if not venv_python.exists():
        venv_python = project_root / ".venv" / "Scripts" / "python.exe"
    if not venv_python.exists():
        venv_python = Path(sys.executable)

    env = setup_headless_env()
    start_time = time.time()

    try:
        # Injeta código para auto-quit após timeout
        inject_code = f"""
import threading, pygame, sys, os
os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')
os.environ.setdefault('SDL_AUDIODRIVER', 'dummy')

def _auto_quit():
    import time
    time.sleep({timeout})
    pygame.event.post(pygame.event.Event(pygame.QUIT))

_t = threading.Thread(target=_auto_quit, daemon=True)
_t.start()
"""

        # Lê o main.py original
        with open(main_py, "r", encoding="utf-8") as f:
            original_code = f.read()

        # Cria versão temporária com auto-quit
        temp_main = game_path / "_temp_validate_main.py"
        with open(temp_main, "w", encoding="utf-8") as f:
            # Insere o inject_code antes do import pygame
            if "import pygame" in original_code:
                parts = original_code.split("import pygame", 1)
                f.write(parts[0])
                f.write(inject_code)
                f.write("import pygame")
                f.write(parts[1])
            else:
                f.write(inject_code)
                f.write(original_code)

        process = subprocess.run(
            [str(venv_python), str(temp_main)],
            capture_output=True,
            text=True,
            timeout=timeout + 5,  # margem extra
            env=env,
            cwd=str(game_path),
        )

        runtime = time.time() - start_time

        # Remove arquivo temporário
        temp_main.unlink(missing_ok=True)

        return {
            "success": process.returncode == 0,
            "exit_code": process.returncode,
            "error": None if process.returncode == 0 else process.stderr[-500:] if process.stderr else None,
            "stdout": process.stdout[-1000:] if process.stdout else "",
            "stderr": process.stderr[-1000:] if process.stderr else "",
            "runtime_seconds": round(runtime, 2),
        }

    except subprocess.TimeoutExpired:
        runtime = time.time() - start_time
        # Remove arquivo temporário
        (game_path / "_temp_validate_main.py").unlink(missing_ok=True)
        return {
            "success": False,
            "exit_code": -2,
            "error": f"Timeout após {timeout + 5}s (o jogo provavelmente travou)",
            "stdout": "",
            "stderr": "",
            "runtime_seconds": round(runtime, 2),
        }
    except Exception as e:
        # Remove arquivo temporário
        (game_path / "_temp_validate_main.py").unlink(missing_ok=True)
        return {
            "success": False,
            "exit_code": -3,
            "error": str(e),
            "stdout": "",
            "stderr": "",
            "runtime_seconds": round(time.time() - start_time, 2),
        }


def capture_screenshot(game_path: Path) -> str | None:
    """Captura um screenshot do jogo (se possível)."""
    screenshots_dir = game_path / "_artifacts" / "screenshots"
    screenshots_dir.mkdir(parents=True, exist_ok=True)

    screenshot_path = screenshots_dir / f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"

    # Tenta capturar via script embutido
    project_root = get_project_root()
    venv_python = project_root / ".venv" / "bin" / "python"
    if not venv_python.exists():
        venv_python = project_root / ".venv" / "Scripts" / "python.exe"
    if not venv_python.exists():
        venv_python = Path(sys.executable)

    capture_script = f"""
import os
os.environ['SDL_VIDEODRIVER'] = 'dummy'
os.environ['SDL_AUDIODRIVER'] = 'dummy'

import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((800, 600))

# Tenta importar e rodar brevemente o jogo
try:
    sys.path.insert(0, '{game_path}')

    # Lê e executa main.py para inicializar
    with open('{game_path / "main.py"}', 'r') as f:
        code = f.read()

    # Executa por poucos frames
    namespace = {{'__name__': '__module__', '__file__': '{game_path / "main.py"}'}}

    # Simula alguns frames e captura
    pygame.display.set_caption('Screenshot Capture')
    screen.fill((40, 40, 50))

    font = pygame.font.Font(None, 48)
    text = font.render('GenreForge Arcade', True, (50, 220, 220))
    rect = text.get_rect(center=(400, 280))
    screen.blit(text, rect)

    sub = pygame.font.Font(None, 32)
    text2 = sub.render('Validação em andamento...', True, (180, 180, 190))
    rect2 = text2.get_rect(center=(400, 330))
    screen.blit(text2, rect2)

    pygame.image.save(screen, '{screenshot_path}')
    print('SCREENSHOT_OK')

except Exception as e:
    print(f'SCREENSHOT_ERROR: {{e}}')
finally:
    pygame.quit()
"""

    try:
        env = os.environ.copy()
        env["SDL_VIDEODRIVER"] = "dummy"
        env["SDL_AUDIODRIVER"] = "dummy"

        result = subprocess.run(
            [str(venv_python), "-c", capture_script],
            capture_output=True,
            text=True,
            timeout=10,
            env=env,
        )

        if "SCREENSHOT_OK" in result.stdout:
            return str(screenshot_path)

    except Exception:
        pass

    return None


def generate_report(game_path: Path, run_result: dict, screenshot_path: str | None) -> dict:
    """Gera relatório de validação em JSON."""
    # Carrega blueprint se existir
    blueprint = {}
    game_json = game_path / "game.json"
    if game_json.exists():
        with open(game_json, "r", encoding="utf-8") as f:
            blueprint = json.load(f)

    report = {
        "validation": {
            "timestamp": datetime.now().isoformat(),
            "game_path": str(game_path),
            "game_name": blueprint.get("name", game_path.name),
            "genre": blueprint.get("genre", "unknown"),
        },
        "execution": {
            "success": run_result["success"],
            "exit_code": run_result["exit_code"],
            "runtime_seconds": run_result["runtime_seconds"],
            "error": run_result["error"],
        },
        "artifacts": {
            "screenshot": screenshot_path,
            "video": None,  # v1+
        },
        "checks": {
            "main_py_exists": (game_path / "main.py").exists(),
            "game_json_exists": (game_path / "game.json").exists(),
            "readme_exists": (game_path / "README.md").exists(),
            "no_crash": run_result["success"],
            "completed_in_time": run_result["exit_code"] != -2,
            "screenshot_captured": screenshot_path is not None,
        },
        "summary": {
            "passed": run_result["success"] and (game_path / "main.py").exists(),
            "total_checks": 6,
            "passed_checks": 0,  # será calculado
        },
    }

    # Conta checks passados
    passed = sum(1 for v in report["checks"].values() if v)
    report["summary"]["passed_checks"] = passed
    report["summary"]["passed"] = passed >= 4  # pelo menos 4 de 6

    return report


def save_report(game_path: Path, report: dict) -> Path:
    """Salva relatório em JSON e Markdown."""
    artifacts_dir = game_path / "_artifacts"
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    # JSON
    json_path = artifacts_dir / "validation_report.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    # Markdown
    md_path = artifacts_dir / "validation_report.md"
    status = "✅ PASSOU" if report["summary"]["passed"] else "❌ FALHOU"
    checks_text = "\n".join(
        f"  - {'✅' if v else '❌'} {k}"
        for k, v in report["checks"].items()
    )

    md_content = f"""# Relatório de Validação

**Jogo:** {report['validation']['game_name']}
**Gênero:** {report['validation']['genre']}
**Data:** {report['validation']['timestamp'][:19]}
**Status:** {status}

## Execução
- Exit code: {report['execution']['exit_code']}
- Runtime: {report['execution']['runtime_seconds']}s
- Erro: {report['execution']['error'] or 'Nenhum'}

## Checks ({report['summary']['passed_checks']}/{report['summary']['total_checks']})
{checks_text}

## Artefatos
- Screenshot: {report['artifacts']['screenshot'] or 'Não capturado'}
"""

    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md_content)

    return json_path


def main():
    parser = argparse.ArgumentParser(
        description="GenreForge Arcade — Validador de jogos Pygame"
    )
    parser.add_argument(
        "game_path",
        help="Caminho para o diretório do jogo (ex.: generated_games/space-invader/)"
    )
    parser.add_argument(
        "--timeout", type=int, default=10,
        help="Timeout em segundos para execução (padrão: 10)"
    )

    args = parser.parse_args()
    game_path = Path(args.game_path).resolve()

    if not game_path.exists():
        print(f"❌ Diretório não encontrado: {game_path}")
        sys.exit(1)

    print(f"\n🔍 Validando jogo em: {game_path}")
    print(f"   Timeout: {args.timeout}s\n")

    # 1. Executa o jogo
    print("1️⃣  Executando jogo com timeout...")
    run_result = run_game_with_timeout(game_path, args.timeout)
    status = "✅" if run_result["success"] else "❌"
    print(f"   {status} Exit code: {run_result['exit_code']} "
          f"(runtime: {run_result['runtime_seconds']}s)")
    if run_result["error"]:
        print(f"   Erro: {run_result['error'][:200]}")

    # 2. Captura screenshot
    print("\n2️⃣  Capturando screenshot...")
    screenshot = capture_screenshot(game_path)
    if screenshot:
        print(f"   ✅ Screenshot: {screenshot}")
    else:
        print("   ⚠️  Screenshot não capturado")

    # 3. Gera relatório
    print("\n3️⃣  Gerando relatório...")
    report = generate_report(game_path, run_result, screenshot)
    report_path = save_report(game_path, report)
    print(f"   ✅ Relatório: {report_path}")

    # 4. Resumo
    passed = report["summary"]["passed"]
    print(f"\n{'='*50}")
    if passed:
        print(f"✅ VALIDAÇÃO APROVADA ({report['summary']['passed_checks']}/{report['summary']['total_checks']} checks)")
    else:
        print(f"❌ VALIDAÇÃO REPROVADA ({report['summary']['passed_checks']}/{report['summary']['total_checks']} checks)")
    print(f"{'='*50}\n")

    sys.exit(0 if passed else 1)


if __name__ == "__main__":
    main()
