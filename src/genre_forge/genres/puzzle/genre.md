# Puzzle — Definição do Gênero

## Core Loop
1. Jogador visualiza o grid/tabuleiro
2. Jogador faz uma ação (mover, empurrar, rotacionar)
3. Estado do puzzle é atualizado deterministicamente
4. Checar condição de vitória
5. Se venceu: próximo nível ou tela de vitória
6. R reinicia o nível atual

## Rubrica de Qualidade
- [ ] Regras claras e determinísticas
- [ ] Controles grid-based precisos
- [ ] Pelo menos 3 níveis jogáveis
- [ ] Condição de vitória verificável
- [ ] Contador de movimentos
- [ ] HUD mostra: nível, movimentos, tempo
- [ ] Opção de reiniciar nível (R)
- [ ] Feedback visual de vitória
- [ ] Níveis progressivamente mais difíceis
- [ ] ESC encerra o jogo

## Componentes do Engine Utilizados
- `core_loop.GameBase` — loop principal
- `input_map.InputMap` — teclado (grid movement)
- `ui.hud.HUD` — nível, movimentos
