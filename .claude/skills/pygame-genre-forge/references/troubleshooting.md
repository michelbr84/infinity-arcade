# Troubleshooting — Pygame Genre Forge

Soluções para erros comuns durante geração e validação de jogos.

---

## Pygame sem Display (headless/CI)

**Erro:** `pygame.error: No available video device`

**Solução:**
```bash
# Opção 1: SDL dummy driver
export SDL_VIDEODRIVER=dummy
export SDL_AUDIODRIVER=dummy
python main.py

# Opção 2: Xvfb (Linux, melhor fidelidade)
sudo apt install xvfb
Xvfb :99 -screen 0 800x600x24 &
export DISPLAY=:99
python main.py
```

---

## Python venv não funciona

**Erro:** `No module named venv` ou `ensurepip is not available`

**Solução:**
```bash
# Ubuntu/Debian
sudo apt install python3.10-venv python3-pip

# Fedora
sudo dnf install python3-virtualenv

# macOS
brew install python@3.10
```

---

## pygame não instala

**Erro:** `Could not build wheels for pygame`

**Solução:**
```bash
# Ubuntu/Debian - instalar dependências de build
sudo apt install python3-dev libsdl2-dev libsdl2-image-dev \
    libsdl2-mixer-dev libsdl2-ttf-dev libfreetype6-dev

# Alternativa: usar pygame-ce (community edition)
pip install pygame-ce
```

---

## ImportError de módulos do projeto

**Erro:** `ModuleNotFoundError: No module named 'genre_forge'`

**Solução:**
```bash
# Instalar projeto em modo editável
pip install -e .

# Ou adicionar ao PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
```

---

## Jogo trava na validação

**Problema:** O jogo não responde ao evento QUIT e o timeout é atingido.

**Causa:** O game loop não trata `pygame.QUIT` corretamente.

**Solução:** Garantir que o loop principal tem:
```python
for event in pygame.event.get():
    if event.type == pygame.QUIT:
        self.running = False
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            self.running = False
```

---

## Screenshot não é capturado

**Problema:** A validação roda mas não gera screenshot.

**Soluções:**
1. Verificar que `SDL_VIDEODRIVER=dummy` está configurado
2. Verificar que o diretório `_artifacts/screenshots/` existe
3. Testar manualmente:
```python
import os
os.environ['SDL_VIDEODRIVER'] = 'dummy'
import pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
screen.fill((40, 40, 50))
pygame.image.save(screen, 'test_screenshot.png')
pygame.quit()
```

---

## Conflitos de versão

**Problema:** Diferentes versões de pygame entre sistema e .venv.

**Solução:**
```bash
# Sempre usar o pip da .venv
.venv/bin/pip install --upgrade pygame

# Verificar versão
.venv/bin/python -c "import pygame; print(pygame.ver)"
```

---

## Permissões de escrita

**Erro:** `PermissionError` ao criar arquivos em `generated_games/`

**Solução:**
```bash
# Verificar permissões
ls -la generated_games/

# Corrigir se necessário
chmod -R u+w generated_games/
```
