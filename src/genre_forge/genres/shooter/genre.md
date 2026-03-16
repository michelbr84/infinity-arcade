# Shooter — Definição do Gênero

## Core Loop
1. Player se move (horizontal ou 2D)
2. Player atira (projéteis)
3. Inimigos spawnam em padrões/ondas
4. Colisão projétil × inimigo = destruição + score
5. Colisão inimigo × player = dano
6. Power-ups aparecem aleatoriamente
7. Ondas progressivamente mais difíceis
8. Game over quando HP = 0

## Rubrica de Qualidade
- [ ] Controles responsivos (sem input lag perceptível)
- [ ] Projéteis visíveis e rápidos
- [ ] Spawn de inimigos em padrões variados
- [ ] Score incrementa corretamente
- [ ] HUD mostra: score, vida, wave atual
- [ ] Condição de vitória ou loop infinito com dificuldade crescente
- [ ] Game over com opção de reiniciar
- [ ] Feedback visual de hit (flash, explosão)
- [ ] Pelo menos 2 tipos de inimigos
- [ ] ESC encerra o jogo

## Componentes do Engine Utilizados
- `core_loop.GameBase` — loop principal
- `input_map.InputMap` — teclado/mouse
- `collision.check_groups` — projétil × inimigo
- `collision.check_aabb` — inimigo × player
- `rendering.effects.ParticleEmitter` — explosões
- `ui.hud.HUD` — score, vida, wave
