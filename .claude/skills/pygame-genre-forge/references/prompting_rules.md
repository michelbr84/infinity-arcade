# Regras de Geração — Pygame Genre Forge

Regras que devem ser seguidas ao gerar código de jogos Pygame.

---

## Regras Obrigatórias

### 1. Pygame Puro
- Usar **apenas `pygame`** como biblioteca gráfica/de jogo
- **Sem assets externos** (imagens, sons, fontes custom) no MVP
- Formas geométricas e `pygame.font.Font(None, size)` para texto

### 2. Resolução e Display
- Resolução padrão: **800×600**
- Modo janela (não fullscreen por padrão)
- Título da janela: nome do jogo

### 3. Loop e Eventos
- Game loop com **delta time** (`clock.tick(FPS) / 1000.0`)
- FPS padrão: **60**
- **Sempre** tratar `pygame.QUIT` e `pygame.K_ESCAPE`
- Chamar `pygame.quit()` e `sys.exit()` ao sair

### 4. HUD Mínimo
Todo jogo deve ter pelo menos:
- **Score** ou indicador de progresso
- **Vida/HP** (quando aplicável)
- **Tempo** (quando aplicável)
- Usar `pygame.font.Font(None, 36)` para HUD

### 5. Win/Lose
- Toda gameplay deve ter **condição de vitória** e **condição de derrota**
- Tela de **Game Over** com opção de reiniciar (tecla R)
- Tela de **Vitória** quando aplicável

### 6. Controles
- Documentar controles no README.md
- Usar padrão **WASD** ou **Setas** para movimento
- **SPACE** para ação principal
- **ESC** para sair
- **R** para reiniciar após game over

---

## Padrão de Código

### Estrutura do main.py
```python
#!/usr/bin/env python3
"""Descrição do jogo."""

import sys
import math
import random
import pygame

# Constantes
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Cores (usar nomes descritivos)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
# ...

class Game:
    def __init__(self):
        pygame.init()
        # setup

    def handle_events(self):
        # processar eventos

    def update(self, dt: float):
        # lógica (dt em segundos)

    def render(self):
        # desenhar

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0
            self.handle_events()
            self.update(dt)
            self.render()
        pygame.quit()
        sys.exit()

def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    main()
```

### Estilo
- **PEP 8** obedecido
- Comentários em **português**
- Docstrings em classes e funções públicas
- Nomes de variáveis descritivos

### Cores Recomendadas
Usar paleta vibrante e consistente:

| Nome | RGB | Uso sugerido |
|------|-----|------|
| `DARK_GRAY` | `(40, 40, 50)` | Background |
| `WHITE` | `(255, 255, 255)` | Texto principal |
| `CYAN` | `(50, 220, 220)` | Destaques, HUD |
| `GREEN` | `(50, 200, 50)` | Positivo (vida, score) |
| `RED` | `(220, 50, 50)` | Negativo (dano, perigo) |
| `YELLOW` | `(240, 220, 50)` | Alerta, power-ups |
| `BLUE` | `(50, 100, 220)` | Player, elementos neutros |
| `MAGENTA` | `(220, 50, 220)` | Especial, bônus |

---

## Anti-padrões (evitar)

- ❌ `time.sleep()` dentro do game loop
- ❌ Hardcoded pixel positions sem usar constantes
- ❌ Game loop sem delta time
- ❌ Não tratar `pygame.QUIT`
- ❌ Não chamar `pygame.quit()` ao sair
- ❌ Variáveis globais mutáveis (usar classe Game)
- ❌ Imports de bibliotecas não-padrão (além de pygame)
