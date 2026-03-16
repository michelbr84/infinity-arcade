# Shooter Minimal — Exemplo

Exemplo de prompt e output esperado para um jogo Shooter mínimo.

## Prompt
```
/pygame-genre-forge shooter "nave no espaço, tiros coloridos, ondas de aliens, powerups de velocidade"
```

## Blueprint esperado (game.json)
```json
{
  "name": "space-shooter",
  "genre": "shooter",
  "pitch": "nave no espaço, tiros coloridos, ondas de aliens, powerups de velocidade",
  "config": {
    "resolution": [800, 600],
    "fps": 60,
    "title": "Space Shooter"
  },
  "controls": {
    "movement": "WASD or Arrow Keys",
    "shoot": "SPACE",
    "quit": "ESC"
  },
  "params": {
    "player_speed": 300,
    "bullet_speed": 500,
    "fire_rate": 0.2,
    "enemy_speed": 100,
    "wave_count": 5,
    "enemies_per_wave": 8
  }
}
```

## Mecânicas essenciais
- Player (nave) se move em X na parte inferior
- Projéteis sobem ao pressionar SPACE
- Inimigos descem em padrão (ondas)
- Colisão projétil×inimigo = score + explosão
- Colisão inimigo×player = perda de vida
- HUD: score, vidas, wave atual
