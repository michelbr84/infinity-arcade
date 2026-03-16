"""
test_skill_smoke.py — Testes de smoke da estrutura da Skill.

Verifica que todos os arquivos essenciais existem e estão bem formados.
"""

import json
from pathlib import Path

import pytest


PROJECT_ROOT = Path(__file__).resolve().parent.parent
SKILL_DIR = PROJECT_ROOT / ".claude" / "skills" / "pygame-genre-forge"


class TestSkillStructure:
    """Verifica a estrutura da skill."""

    def test_skill_md_exists(self):
        """SKILL.md deve existir."""
        assert (SKILL_DIR / "SKILL.md").exists()

    def test_skill_md_has_frontmatter(self):
        """SKILL.md deve ter frontmatter YAML com name e description."""
        content = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
        assert content.startswith("---")
        assert "name:" in content
        assert "description:" in content

    def test_scripts_exist(self):
        """Scripts essenciais devem existir."""
        scripts = ["setup_env.py", "generate_game.py", "validate_game.py"]
        for script in scripts:
            path = SKILL_DIR / "scripts" / script
            assert path.exists(), f"Script não encontrado: {script}"

    def test_references_exist(self):
        """Referências devem existir."""
        refs = ["genre_catalog.md", "prompting_rules.md", "troubleshooting.md"]
        for ref in refs:
            path = SKILL_DIR / "references" / ref
            assert path.exists(), f"Referência não encontrada: {ref}"

    def test_examples_exist(self):
        """Exemplos mínimos devem existir."""
        examples = ["shooter_minimal.md", "puzzle_minimal.md", "sports_minimal.md"]
        for ex in examples:
            path = SKILL_DIR / "examples" / ex
            assert path.exists(), f"Exemplo não encontrado: {ex}"


class TestEngineStructure:
    """Verifica a estrutura do engine."""

    ENGINE_DIR = PROJECT_ROOT / "src" / "genre_forge" / "engine"

    def test_core_modules_exist(self):
        """Módulos core do engine devem existir."""
        modules = [
            "__init__.py", "core_loop.py", "input_map.py",
            "math2d.py", "collision.py", "scene_manager.py",
        ]
        for mod in modules:
            path = self.ENGINE_DIR / mod
            assert path.exists(), f"Módulo não encontrado: {mod}"

    def test_ui_exists(self):
        """Subpacote UI deve existir."""
        assert (self.ENGINE_DIR / "ui" / "__init__.py").exists()
        assert (self.ENGINE_DIR / "ui" / "hud.py").exists()

    def test_rendering_exists(self):
        """Subpacote rendering deve existir."""
        assert (self.ENGINE_DIR / "rendering" / "__init__.py").exists()
        assert (self.ENGINE_DIR / "rendering" / "effects.py").exists()


class TestGenreStructure:
    """Verifica a estrutura dos gêneros MVP."""

    GENRES_DIR = PROJECT_ROOT / "src" / "genre_forge" / "genres"

    @pytest.mark.parametrize("genre", ["shooter", "puzzle", "sports"])
    def test_genre_has_spec(self, genre):
        """Cada gênero MVP deve ter genre.md."""
        assert (self.GENRES_DIR / genre / "genre.md").exists()

    @pytest.mark.parametrize("genre", ["shooter", "puzzle", "sports"])
    def test_genre_has_blueprint_schema(self, genre):
        """Cada gênero MVP deve ter blueprint.schema.json válido."""
        schema_path = self.GENRES_DIR / genre / "blueprint.schema.json"
        assert schema_path.exists()
        data = json.loads(schema_path.read_text(encoding="utf-8"))
        assert "properties" in data
        assert data.get("type") == "object"


class TestValidationStructure:
    """Verifica a estrutura da camada de validação."""

    VALIDATION_DIR = PROJECT_ROOT / "src" / "genre_forge" / "validation"

    def test_validation_modules_exist(self):
        """Módulos de validação devem existir."""
        modules = ["__init__.py", "runner.py", "smoke.py", "capture.py", "report.py"]
        for mod in modules:
            path = self.VALIDATION_DIR / mod
            assert path.exists(), f"Módulo não encontrado: {mod}"
