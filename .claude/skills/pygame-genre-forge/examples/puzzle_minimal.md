# Puzzle Minimal — Exemplo

Exemplo de prompt e output esperado para um jogo Puzzle mínimo.

## Prompt
```
/pygame-genre-forge puzzle "puzzle de empurrar caixas estilo sokoban em 5 fases pequenas"
```

## Blueprint esperado (game.json)
```json
{
  "name": "box-pusher",
  "genre": "puzzle",
  "pitch": "puzzle de empurrar caixas estilo sokoban em 5 fases pequenas",
  "config": {
    "resolution": [800, 600],
    "fps": 60,
    "title": "Box Pusher"
  },
  "controls": {
    "movement": "WASD or Arrow Keys",
    "reset": "R",
    "quit": "ESC"
  },
  "params": {
    "grid_size": [10, 8],
    "level_count": 5,
    "tile_size": 64,
    "puzzle_type": "sokoban"
  }
}
```

## Mecânicas essenciais
- Grid com tiles: parede, chão, alvo, caixa, player
- Player se move em 4 direções (grid-based)
- Caixas empurradas na direção do movimento
- Vitória: todas as caixas nos alvos
- R reinicia o nível atual
- HUD: nível atual, movimentos, tempo
