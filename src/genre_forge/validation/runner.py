"""
runner.py — Executor controlado de jogos Pygame com timeout e headless.

Usado pela Validation Layer para rodar jogos em ambiente controlado.
"""

import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Optional


class GameRunner:
    """
    Executa um jogo Pygame com timeout e captura de output.

    Uso:
        runner = GameRunner(timeout=10, headless=True)
        result = runner.run(Path("generated_games/space-shooter/main.py"))

        if result.success:
            print(f"Jogo rodou por {result.runtime:.1f}s")
        else:
            print(f"Falha: {result.error}")
    """

    def __init__(
        self,
        timeout: int = 10,
        headless: bool = True,
        python_path: Optional[str] = None,
    ):
        """
        Args:
            timeout: Tempo máximo de execução em segundos
            headless: Se True, configura SDL_VIDEODRIVER=dummy
            python_path: Caminho para o Python da .venv (auto-detecta se None)
        """
        self.timeout = timeout
        self.headless = headless
        self.python_path = python_path or self._find_python()

    def _find_python(self) -> str:
        """Encontra o Python da .venv ou fallback para o atual."""
        # Tenta encontrar .venv no CWD ou parent dirs
        cwd = Path.cwd()
        for parent in [cwd] + list(cwd.parents):
            venv_python = parent / ".venv" / "bin" / "python"
            if venv_python.exists():
                return str(venv_python)
            venv_python_win = parent / ".venv" / "Scripts" / "python.exe"
            if venv_python_win.exists():
                return str(venv_python_win)
        return sys.executable

    def _build_env(self) -> dict:
        """Constrói variáveis de ambiente para execução."""
        env = os.environ.copy()
        if self.headless:
            env["SDL_VIDEODRIVER"] = "dummy"
            env["SDL_AUDIODRIVER"] = "dummy"
        return env

    def run(self, main_py: Path) -> "RunResult":
        """
        Executa o jogo e retorna resultado.

        Args:
            main_py: Caminho para o main.py do jogo

        Returns:
            RunResult com status, output e métricas
        """
        if not main_py.exists():
            return RunResult(
                success=False,
                exit_code=-1,
                runtime=0,
                stdout="",
                stderr=f"Arquivo não encontrado: {main_py}",
                error=f"Arquivo não encontrado: {main_py}",
            )

        env = self._build_env()
        start_time = time.time()

        try:
            process = subprocess.run(
                [self.python_path, str(main_py)],
                capture_output=True,
                text=True,
                timeout=self.timeout,
                env=env,
                cwd=str(main_py.parent),
            )

            runtime = time.time() - start_time

            return RunResult(
                success=process.returncode == 0,
                exit_code=process.returncode,
                runtime=runtime,
                stdout=process.stdout[-2000:] if process.stdout else "",
                stderr=process.stderr[-2000:] if process.stderr else "",
                error=None if process.returncode == 0 else process.stderr[-500:],
            )

        except subprocess.TimeoutExpired:
            return RunResult(
                success=False,
                exit_code=-2,
                runtime=self.timeout,
                stdout="",
                stderr="",
                error=f"Timeout: jogo excedeu {self.timeout}s",
            )

        except Exception as e:
            return RunResult(
                success=False,
                exit_code=-3,
                runtime=time.time() - start_time,
                stdout="",
                stderr=str(e),
                error=str(e),
            )


class RunResult:
    """Resultado da execução de um jogo."""

    def __init__(
        self,
        success: bool,
        exit_code: int,
        runtime: float,
        stdout: str,
        stderr: str,
        error: Optional[str] = None,
    ):
        self.success = success
        self.exit_code = exit_code
        self.runtime = round(runtime, 2)
        self.stdout = stdout
        self.stderr = stderr
        self.error = error

    def to_dict(self) -> dict:
        return {
            "success": self.success,
            "exit_code": self.exit_code,
            "runtime_seconds": self.runtime,
            "error": self.error,
        }

    def __repr__(self) -> str:
        status = "OK" if self.success else "FALHA"
        return f"RunResult({status}, code={self.exit_code}, runtime={self.runtime}s)"
