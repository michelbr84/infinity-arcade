# GenreForge Arcade 🎮

> Gere jogos Pygame por gênero via Claude Code — com templates, scaffold e validação automática.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Pygame](https://img.shields.io/badge/pygame-2.5+-green.svg)](https://www.pygame.org/)

## O que é?

GenreForge Arcade é uma **Skill de Claude Code** que gera jogos completos em Pygame orientados por gênero. Basta descrever o que você quer e a skill:

1. 📝 Cria um mini **Game Design Document**
2. 🔧 Gera um **blueprint** (JSON) com parâmetros
3. 🎮 Produz **código Pygame jogável**
4. ✅ Roda **validação automática** (smoke test + screenshots)

## Quickstart

### 1. Setup automático

```bash
# O script detecta seu SO e configura tudo automaticamente
python .claude/skills/pygame-genre-forge/scripts/setup_env.py
```

### 2. Ativar ambiente

```bash
source .venv/bin/activate        # Linux/macOS
# .venv\Scripts\activate          # Windows
```

### 3. Gerar um jogo

No Claude Code, use o comando:
```
/pygame-genre-forge shooter "nave no espaço com tiros coloridos e ondas de aliens"
```

Ou gere manualmente:
```bash
python .claude/skills/pygame-genre-forge/scripts/generate_game.py \
  --genre shooter --name "space-blaster" --pitch "nave contra aliens"
```

### 4. Jogar!

```bash
python generated_games/space-blaster/main.py
```

## Gêneros Suportados

| Gênero | Exemplo | Complexidade |
|--------|---------|:---:|
| 🔫 **Shooter** | Nave espacial, waves de inimigos | ⭐ |
| 🧩 **Puzzle** | Sokoban, empurrar caixas | ⭐ |
| ⚽ **Sports** | Pong, placar por rounds | ⭐ |
| ⚔️ **Action** | Combate, colisões, waves | ⭐⭐ |
| 🗺️ **Adventure** | Exploração, puzzles, narrativa | ⭐⭐ |
| ♟️ **Strategy** | Grid, turnos, AI simples | ⭐⭐ |
| 🏎️ **Racing** | Pista, voltas, tempo | ⭐⭐ |
| 🎲 **RPG** | Stats, itens, combate | ⭐⭐⭐ |
| 🏭 **Simulation** | Agentes, recursos, ticks | ⭐⭐⭐ |
| 🌍 **Sandbox** | Mundo editável, crafting | ⭐⭐⭐ |

⭐ = MVP (implementado) | ⭐⭐ = v1 | ⭐⭐⭐ = v2

## Arquitetura

```
┌─────────────────────────────────────────────┐
│  Skill Layer        (.claude/skills/)        │
│  SKILL.md + scripts + references             │
├─────────────────────────────────────────────┤
│  Genre Layer        (src/genre_forge/genres/) │
│  Blueprints + templates por gênero           │
├─────────────────────────────────────────────┤
│  Engine Layer       (src/genre_forge/engine/) │
│  Core loop + input + colisão + UI            │
├─────────────────────────────────────────────┤
│  Validation Layer   (src/genre_forge/validation/) │
│  Runner + smoke tests + screenshots          │
└─────────────────────────────────────────────┘
```

## Validação Automática

```bash
python .claude/skills/pygame-genre-forge/scripts/validate_game.py generated_games/space-blaster/
```

Gera:
- `_artifacts/screenshots/` — Screenshots do jogo
- `_artifacts/validation_report.json` — Relatório detalhado
- `_artifacts/validation_report.md` — Resumo legível

## Estrutura do Projeto

```
infinity-arcade/
├── .claude/skills/pygame-genre-forge/    # Skill Layer
│   ├── SKILL.md                          # Definição da skill
│   ├── scripts/                          # setup, geração, validação
│   ├── references/                       # catálogo, regras, troubleshooting
│   └── examples/                         # exemplos por gênero
├── src/genre_forge/                      # Núcleo do projeto
│   ├── engine/                           # Engine (loop, input, colisão)
│   ├── genres/                           # Specs por gênero
│   ├── validation/                       # Runner, smoke, captura
│   └── templates/                        # Templates preenchíveis
├── generated_games/                      # Output (gitignored)
├── tests/                                # Testes automatizados
└── .github/workflows/                    # CI/CD
```

## Desenvolvimento

```bash
# Setup completo para dev
python .claude/skills/pygame-genre-forge/scripts/setup_env.py
source .venv/bin/activate
pip install -e ".[dev]"

# Rodar testes
pytest tests/ -v
```

## Licença

MIT — veja [LICENSE](LICENSE) para detalhes.
