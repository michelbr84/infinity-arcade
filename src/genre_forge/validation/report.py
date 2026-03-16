"""
report.py — Geração de relatórios de validação em JSON e Markdown.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional


class ValidationReport:
    """
    Gera relatórios de validação para jogos gerados.

    Uso:
        report = ValidationReport(game_dir, genre="shooter")
        report.set_execution(success=True, exit_code=0, runtime=5.2)
        report.set_smoke_results(smoke_checker.results)
        report.set_screenshot("/path/to/screenshot.png")
        report.save()
    """

    def __init__(self, game_dir: Path, genre: str = "unknown", name: str = ""):
        self.game_dir = Path(game_dir)
        self.genre = genre
        self.name = name or game_dir.name
        self.timestamp = datetime.now().isoformat()

        self._execution: Dict[str, Any] = {}
        self._smoke_results: Dict[str, bool] = {}
        self._screenshot: Optional[str] = None
        self._video: Optional[str] = None
        self._notes: list = []

    def set_execution(
        self,
        success: bool,
        exit_code: int,
        runtime: float,
        error: Optional[str] = None,
    ) -> None:
        """Define resultados da execução."""
        self._execution = {
            "success": success,
            "exit_code": exit_code,
            "runtime_seconds": round(runtime, 2),
            "error": error,
        }

    def set_smoke_results(self, results: Dict[str, bool]) -> None:
        """Define resultados dos smoke tests."""
        self._smoke_results = results

    def set_screenshot(self, path: Optional[str]) -> None:
        """Define caminho do screenshot."""
        self._screenshot = path

    def set_video(self, path: Optional[str]) -> None:
        """Define caminho do vídeo."""
        self._video = path

    def add_note(self, note: str) -> None:
        """Adiciona nota ao relatório."""
        self._notes.append(note)

    def to_dict(self) -> dict:
        """Retorna relatório como dicionário."""
        smoke_passed = sum(1 for v in self._smoke_results.values() if v)
        smoke_total = len(self._smoke_results)
        exec_ok = self._execution.get("success", False)

        return {
            "validation": {
                "timestamp": self.timestamp,
                "game_path": str(self.game_dir),
                "game_name": self.name,
                "genre": self.genre,
            },
            "execution": self._execution,
            "smoke_tests": {
                "results": self._smoke_results,
                "passed": smoke_passed,
                "total": smoke_total,
            },
            "artifacts": {
                "screenshot": self._screenshot,
                "video": self._video,
            },
            "summary": {
                "overall_passed": exec_ok and smoke_passed >= (smoke_total * 0.6),
                "smoke_score": f"{smoke_passed}/{smoke_total}",
                "notes": self._notes,
            },
        }

    def save(self, output_dir: Optional[Path] = None) -> tuple:
        """
        Salva relatório em JSON e Markdown.

        Returns:
            Tupla (json_path, md_path)
        """
        if output_dir is None:
            output_dir = self.game_dir / "_artifacts"
        output_dir.mkdir(parents=True, exist_ok=True)

        data = self.to_dict()

        # JSON
        json_path = output_dir / "validation_report.json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        # Markdown
        md_path = output_dir / "validation_report.md"
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(self._to_markdown(data))

        return json_path, md_path

    def _to_markdown(self, data: dict) -> str:
        """Converte relatório para Markdown."""
        summary = data["summary"]
        execution = data["execution"]
        smoke = data["smoke_tests"]

        status = "✅ APROVADO" if summary["overall_passed"] else "❌ REPROVADO"

        lines = [
            f"# Relatório de Validação — {self.name}",
            "",
            f"**Gênero:** {self.genre}",
            f"**Data:** {self.timestamp[:19]}",
            f"**Status:** {status}",
            "",
            "## Execução",
            f"- Success: {execution.get('success', 'N/A')}",
            f"- Exit code: {execution.get('exit_code', 'N/A')}",
            f"- Runtime: {execution.get('runtime_seconds', 'N/A')}s",
        ]

        if execution.get("error"):
            lines.append(f"- Erro: {execution['error'][:300]}")

        lines.extend([
            "",
            f"## Smoke Tests ({smoke['passed']}/{smoke['total']})",
        ])

        for check, passed in smoke.get("results", {}).items():
            icon = "✅" if passed else "❌"
            lines.append(f"- {icon} {check}")

        if data["artifacts"]["screenshot"]:
            lines.extend([
                "",
                "## Screenshot",
                f"![screenshot]({data['artifacts']['screenshot']})",
            ])

        if self._notes:
            lines.extend(["", "## Notas"])
            for note in self._notes:
                lines.append(f"- {note}")

        return "\n".join(lines) + "\n"
