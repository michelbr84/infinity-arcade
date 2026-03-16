---
name: pygame-genre-forge
description: >
  Gera jogos em Pygame por gênero (ação, aventura, rpg, shooter, estratégia,
  puzzle, corrida, esportes, simulação, sandbox) usando templates e scaffold.
  Use quando o usuário pedir para criar/gerar um jogo Pygame, prototipar um
  gênero, criar um mini-game jogável, ou quando quiser validar automaticamente
  um jogo gerado (smoke test, screenshots).
license: MIT
compatibility: >
  Claude Code (project skill). Requer Python 3.10+ e pygame instalados.
  Para CI/headless, pode usar SDL_VIDEODRIVER=dummy ou Xvfb.
---

# Pygame Genre Forge

## Objetivo

Você é um gerador de jogos Pygame por gênero. Sempre produza:

1. Um mini GDD (Game Design Doc) curto e objetivo;
2. Um blueprint (JSON) com parâmetros do jogo;
3. Código Pygame jogável, aderente ao gênero, com loop completo e controles responsivos;
4. Uma validação automática (smoke test + 1 screenshot) e um relatório.

Siga a ordem: **(GDD) → (Blueprint) → (Código) → (Validação) → (Correções)**.

## Primeiro Passo: Setup do Ambiente

Antes de gerar qualquer jogo, **sempre** execute o setup do ambiente:

```bash
python .claude/skills/pygame-genre-forge/scripts/setup_env.py
```

Isso irá:
- Detectar o sistema operacional (Linux/Windows/macOS)
- Criar um ambiente virtual `.venv` se não existir
- Instalar todas as dependências necessárias (pygame, Pillow)
- Validar que tudo funciona corretamente

## Comandos (slash)

### /pygame-genre-forge \<genero\> \<pitch\>

Gera um jogo novo dentro de `generated_games/<slug>/`.

**Exemplos:**
- `/pygame-genre-forge shooter "nave no espaço, tiros coloridos, ondas, powerups simples"`
- `/pygame-genre-forge puzzle "um puzzle de empurrar caixas estilo sokoban em 10 fases pequenas"`
- `/pygame-genre-forge sports "pong com física simples e placar até 7"`

### /pygame-genre-forge remix \<path-do-projeto\> \<mudanca\>

Aplica mudanças ao jogo existente, mantendo estilo e estrutura.

### /pygame-genre-forge validate \<path-do-projeto\>

Roda validação (timeout, smoke, screenshot) e salva artefatos em `_artifacts/`.

## Perguntas mínimas (se faltarem dados)

Pergunte apenas o essencial, em no máximo 5 perguntas:

1. Qual é o **gênero** (um dos 10: action, adventure, rpg, shooter, strategy, puzzle, racing, sports, simulation, sandbox)?
2. **Tema/ambientação**?
3. **Objetivo** (win/lose)?
4. **Controles** (teclado/mouse) e plataforma alvo?
5. **Complexidade**: MVP (simples) / v1 (médio) / v2 (avançado)?

## Regras de geração (padrão)

- **Pygame puro**; evitar depender de imagens/sons externos no MVP.
- Resolução padrão: **800×600**.
- O jogo deve encerrar com **ESC** e tratar **QUIT**.
- Deve existir pelo menos: **HUD mínimo** (score/tempo/vida), **condição de vitória/derrota**, e **feedback visual claro**.
- Use **formas geométricas** (retângulos, círculos) e **cores vibrantes** ao invés de sprites externos.
- O código deve ser **bem comentado em português** e seguir PEP 8.
- Usar **delta time** para movimento e animação (independente de FPS).
- Tratar **colisões** adequadamente ao gênero.

## Estrutura esperada do output

```
generated_games/<slug>/
├── main.py            # ponto de entrada do jogo
├── game.json          # blueprint com parâmetros
├── README.md          # como jogar + descrição
└── _artifacts/        # gerado pela validação
    ├── screenshots/
    ├── video/
    └── validation_report.json
```

## Fluxo de geração passo a passo

1. **Setup**: Executar `setup_env.py` se `.venv` não existir
2. **GDD**: Criar mini Game Design Document com:
   - Nome, gênero, pitch, mecânicas, controles, win/lose condition
3. **Blueprint**: Criar `game.json` com parâmetros estruturados
4. **Código**: Gerar `main.py` usando templates e engine:
   - Importar componentes do engine (`src/genre_forge/engine/`)
   - Seguir padrão do gênero (`src/genre_forge/genres/<genero>/`)
   - Aplicar regras de geração
5. **Validação**: Executar `validate_game.py`:
   - Rodar jogo por 10s com timeout
   - Capturar screenshot
   - Gerar relatório
6. **Correção**: Se falhar, corrigir e revalidar uma vez

## Onde buscar templates e referências

- Templates por gênero: `src/genre_forge/templates/`
- Specs de gênero: `src/genre_forge/genres/`
- Catálogo de gêneros: `references/genre_catalog.md`
- Regras de geração: `references/prompting_rules.md`
- Troubleshooting: `references/troubleshooting.md`
- Exemplos mínimos: `examples/`

## Engine disponível

O engine em `src/genre_forge/engine/` oferece:

- `core_loop.py` — Game loop com delta time e hooks
- `input_map.py` — Mapeamento de teclas/mouse
- `collision.py` — Detecção de colisão (AABB, círculo)
- `math2d.py` — Vetores 2D e utilitários
- `scene_manager.py` — Stack de cenas (menu, jogo, pause, game over)
- `ui/` — HUD, menus, botões
- `rendering/` — Sprites, efeitos, câmera
