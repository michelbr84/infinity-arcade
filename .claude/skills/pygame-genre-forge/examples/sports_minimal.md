# Sports Minimal — Exemplo

Exemplo de prompt e output esperado para um jogo Sports mínimo.

## Prompt
```
/pygame-genre-forge sports "pong com física simples e placar até 7"
```

## Blueprint esperado (game.json)
```json
{
  "name": "retro-pong",
  "genre": "sports",
  "pitch": "pong com física simples e placar até 7",
  "config": {
    "resolution": [800, 600],
    "fps": 60,
    "title": "Retro Pong"
  },
  "controls": {
    "player1": "W/S",
    "player2": "Arrow Up/Down (or AI)",
    "quit": "ESC"
  },
  "params": {
    "score_limit": 7,
    "ball_speed": 300,
    "paddle_speed": 400,
    "paddle_height": 80,
    "has_ai": true
  }
}
```

## Mecânicas essenciais
- Dois paddles (esquerda/direita)
- Bola com reflexão nas bordas e paddles
- Score incrementa quando bola passa do paddle
- Primeiro a 7 pontos ganha
- AI simples para player 2: seguir a bola
- HUD: placar de ambos os lados
