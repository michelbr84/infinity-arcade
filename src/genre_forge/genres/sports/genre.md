# Sports — Definição do Gênero

## Core Loop
1. Partida inicia (bola no centro)
2. Jogadores se movem (teclado ou AI)
3. Bola se move com física simples (reflexão)
4. Colisão bola × paddle = rebote
5. Bola passa do paddle = ponto para oponente
6. Checar condição de vitória (score limit)
7. Reset e próximo round

## Rubrica de Qualidade
- [ ] Física da bola realista (ângulo de rebote)
- [ ] Controles responsivos para ambos jogadores
- [ ] AI funcional para player 2
- [ ] Placar visível e atualizado
- [ ] Condição de vitória (primeiro a N pontos)
- [ ] Reset automático após ponto
- [ ] Feedback visual de ponto marcado
- [ ] Linha divisória e decoração do campo
- [ ] Game over com vencedor declarado
- [ ] ESC encerra o jogo

## Componentes do Engine Utilizados
- `core_loop.GameBase` — loop principal
- `input_map.InputMap` — teclado (W/S e Up/Down)
- `collision.check_aabb` — bola × paddle
- `ui.hud.HUD` — placar
