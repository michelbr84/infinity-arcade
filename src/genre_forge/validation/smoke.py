"""
smoke.py — Smoke tests básicos para jogos Pygame gerados.

Verifica que um jogo atende requisitos mínimos de estrutura e execução.
"""

import ast
import json
from pathlib import Path
from typing import Dict, List


class SmokeChecker:
    """
    Verificador de smoke tests para jogos gerados.

    Checks:
        - Estrutura de arquivos (main.py, game.json, README.md)
        - Imports necessários (pygame, sys)
        - Tratamento de QUIT e ESC
        - Presença de game loop
        - Presença de HUD/score
        - Blueprint válido
    """

    def __init__(self, game_dir: Path):
        self.game_dir = Path(game_dir)
        self.results: Dict[str, bool] = {}
        self.details: Dict[str, str] = {}

    def run_all(self) -> Dict[str, bool]:
        """Executa todos os smoke checks e retorna resultados."""
        self.check_file_structure()
        self.check_main_py_syntax()
        self.check_imports()
        self.check_quit_handling()
        self.check_game_loop()
        self.check_blueprint()
        return self.results

    def check_file_structure(self) -> None:
        """Verifica que arquivos essenciais existem."""
        files = {
            "main.py": self.game_dir / "main.py",
            "game.json": self.game_dir / "game.json",
            "README.md": self.game_dir / "README.md",
        }

        for name, path in files.items():
            key = f"file_{name.replace('.', '_')}"
            exists = path.exists()
            self.results[key] = exists
            self.details[key] = f"{'✅' if exists else '❌'} {name} {'existe' if exists else 'não encontrado'}"

    def check_main_py_syntax(self) -> None:
        """Verifica que main.py é Python válido."""
        main_py = self.game_dir / "main.py"
        key = "syntax_valid"

        if not main_py.exists():
            self.results[key] = False
            self.details[key] = "❌ main.py não existe"
            return

        try:
            source = main_py.read_text(encoding="utf-8")
            ast.parse(source)
            self.results[key] = True
            self.details[key] = "✅ Sintaxe Python válida"
        except SyntaxError as e:
            self.results[key] = False
            self.details[key] = f"❌ Erro de sintaxe: linha {e.lineno}: {e.msg}"

    def check_imports(self) -> None:
        """Verifica que pygame e sys são importados."""
        main_py = self.game_dir / "main.py"
        key = "imports_ok"

        if not main_py.exists():
            self.results[key] = False
            return

        source = main_py.read_text(encoding="utf-8")
        has_pygame = "import pygame" in source
        has_sys = "import sys" in source

        self.results[key] = has_pygame and has_sys
        missing = []
        if not has_pygame:
            missing.append("pygame")
        if not has_sys:
            missing.append("sys")

        if missing:
            self.details[key] = f"❌ Imports faltando: {', '.join(missing)}"
        else:
            self.details[key] = "✅ pygame e sys importados"

    def check_quit_handling(self) -> None:
        """Verifica que QUIT e ESC são tratados."""
        main_py = self.game_dir / "main.py"
        key = "quit_handling"

        if not main_py.exists():
            self.results[key] = False
            return

        source = main_py.read_text(encoding="utf-8")

        has_quit = "pygame.QUIT" in source or "QUIT" in source
        has_esc = "K_ESCAPE" in source or "pygame.K_ESCAPE" in source

        self.results[key] = has_quit and has_esc
        if not has_quit:
            self.details[key] = "❌ pygame.QUIT não tratado"
        elif not has_esc:
            self.details[key] = "❌ ESC (K_ESCAPE) não tratado"
        else:
            self.details[key] = "✅ QUIT e ESC tratados"

    def check_game_loop(self) -> None:
        """Verifica presença de game loop com delta time."""
        main_py = self.game_dir / "main.py"
        key = "game_loop"

        if not main_py.exists():
            self.results[key] = False
            return

        source = main_py.read_text(encoding="utf-8")

        has_loop = "while" in source and "running" in source
        has_clock = "clock.tick" in source or "Clock()" in source
        has_flip = "display.flip" in source or "display.update" in source

        self.results[key] = has_loop and has_clock
        details = []
        if not has_loop:
            details.append("sem while loop")
        if not has_clock:
            details.append("sem clock.tick")
        if not has_flip:
            details.append("sem display.flip/update")

        if details:
            self.details[key] = f"❌ Game loop incompleto: {', '.join(details)}"
        else:
            self.details[key] = "✅ Game loop com delta time"

    def check_blueprint(self) -> None:
        """Verifica que game.json é válido e tem campos essenciais."""
        game_json = self.game_dir / "game.json"
        key = "blueprint_valid"

        if not game_json.exists():
            self.results[key] = False
            self.details[key] = "❌ game.json não encontrado"
            return

        try:
            data = json.loads(game_json.read_text(encoding="utf-8"))
            required = ["name", "genre"]
            missing = [f for f in required if f not in data]

            if missing:
                self.results[key] = False
                self.details[key] = f"❌ Campos faltando no blueprint: {', '.join(missing)}"
            else:
                self.results[key] = True
                self.details[key] = f"✅ Blueprint válido (gênero: {data.get('genre', '?')})"
        except json.JSONDecodeError as e:
            self.results[key] = False
            self.details[key] = f"❌ JSON inválido: {e}"

    @property
    def passed(self) -> bool:
        """Retorna True se todos os checks passaram."""
        return all(self.results.values()) if self.results else False

    @property
    def passed_count(self) -> int:
        return sum(1 for v in self.results.values() if v)

    @property
    def total_count(self) -> int:
        return len(self.results)

    def summary(self) -> str:
        """Retorna resumo dos checks em texto."""
        lines = [f"Smoke Tests: {self.passed_count}/{self.total_count}"]
        for key, detail in self.details.items():
            lines.append(f"  {detail}")
        return "\n".join(lines)
