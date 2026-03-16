# Catálogo de Gêneros — Pygame Genre Forge

Referência completa dos 10 gêneros suportados, com definição de core loop, parâmetros chave e complexidade.

---

## 1. Action

**Core loop:** Movimento contínuo → combate → colisões → feedback de hit → waves curtas
**Controles:** WASD/Setas + SPACE (ataque)
**Win/Lose:** Sobreviver N waves / HP chega a zero
**Entidades:** Player, inimigos, projéteis, power-ups
**Complexidade MVP:** Média

**Parâmetros chave:**
- `player_speed`, `player_hp`, `wave_count`, `enemy_types`, `spawn_rate`

---

## 2. Adventure

**Core loop:** Exploração → gatilhos/eventos → puzzles simples → narrativa
**Controles:** WASD/Setas (movimento) + E (interagir)
**Win/Lose:** Completar objetivos / sem condição de derrota explícita (ou timer)
**Entidades:** Player, NPCs, objetos interativos, portas/gatilhos
**Complexidade MVP:** Média

**Parâmetros chave:**
- `map_size`, `npc_count`, `has_dialogue`, `quest_count`

---

## 3. RPG

**Core loop:** Exploração → combate (turno ou action-lite) → progressão → itens
**Controles:** WASD + SPACE/ENTER (confirmar) + I (inventário)
**Win/Lose:** Derrotar boss / HP chega a zero
**Entidades:** Player (com stats), inimigos, NPCs, itens, inventário
**Complexidade MVP:** Alta → simplificar para "RPG-lite" (combate básico + 3 stats)

**Parâmetros chave:**
- `player_stats`, `level_cap`, `inventory_size`, `combat_type`, `enemy_types`

---

## 4. Shooter ★ MVP

**Core loop:** Movimento → tiro → spawn de inimigos → score → power-ups
**Controles:** WASD/Setas (movimento) + SPACE (tiro) ou Mouse (mira+tiro)
**Win/Lose:** Score máximo / ondas completas / HP chega a zero
**Entidades:** Player (nave/personagem), projéteis, inimigos, power-ups
**Complexidade MVP:** Baixa

**Parâmetros chave:**
- `player_speed`, `bullet_speed`, `fire_rate`, `enemy_speed`, `wave_count`, `powerup_types`

**Exemplo de prompt:**
> "nave no espaço, tiros coloridos, ondas de aliens, powerups de velocidade e escudo"

---

## 5. Strategy

**Core loop:** Grid → turnos → ações por unidade → AI simples → condição de vitória
**Controles:** Mouse (seleção) + teclado (ações)
**Win/Lose:** Eliminar todas unidades inimigas / perder todas as suas
**Entidades:** Unidades (diferentes tipos), grid/mapa, cursor
**Complexidade MVP:** Média

**Parâmetros chave:**
- `grid_size`, `unit_types`, `ai_difficulty`, `turn_limit`

---

## 6. Puzzle ★ MVP

**Core loop:** Regras determinísticas → ações do jogador → checagem de vitória → próximo nível
**Controles:** WASD/Setas (movimento) + R (reset do nível)
**Win/Lose:** Completar todos os níveis / sem condição de derrota (ou moves limitados)
**Entidades:** Player, caixas/blocos, alvos, paredes
**Complexidade MVP:** Baixa

**Parâmetros chave:**
- `level_count`, `grid_size`, `puzzle_type`, `max_moves`

**Exemplo de prompt:**
> "puzzle de empurrar caixas estilo sokoban em 10 fases pequenas"

---

## 7. Racing

**Core loop:** Física simplificada → limites de pista → contagem de voltas/tempo
**Controles:** Setas (aceleração, frenagem, direção)
**Win/Lose:** Completar N voltas em tempo limite
**Entidades:** Veículo, pista, obstáculos, checkpoint
**Complexidade MVP:** Média

**Parâmetros chave:**
- `track_length`, `lap_count`, `vehicle_speed`, `has_obstacles`, `time_limit`

---

## 8. Sports ★ MVP

**Core loop:** Regras de partida simples → placar → rounds → reset
**Controles:** WASD (player 1) + Setas (player 2 ou AI)
**Win/Lose:** Primeiro a atingir score limite
**Entidades:** Bola, jogadores/paddles, placar, campo
**Complexidade MVP:** Baixa

**Parâmetros chave:**
- `score_limit`, `ball_speed`, `player_speed`, `has_ai`, `field_type`

**Exemplo de prompt:**
> "pong com física simples e placar até 7"

---

## 9. Simulation

**Core loop:** Ticks de tempo → atualização de agentes → UI de inspeção → estado global
**Controles:** Mouse (inspeção, construção) + teclado (velocidade do tempo)
**Win/Lose:** Sem condição explícita (sandbox com métricas) ou meta de prosperidade
**Entidades:** Agentes, recursos, construções, indicadores
**Complexidade MVP:** Alta → "sim-lite" (3-5 agentes, 2 recursos)

**Parâmetros chave:**
- `agent_count`, `resource_types`, `tick_speed`, `world_size`

> ⚠️ No MVP, tratar como "simulação-lite" focando no ciclo mínimo.

---

## 10. Sandbox

**Core loop:** Mundo editável → inventário → construção/crafting → loop criativo
**Controles:** WASD (movimento) + Mouse (construir/destruir) + I (inventário)
**Win/Lose:** Sem condição (criativo) ou objetivos opcionais
**Entidades:** Player, blocos/tiles, itens, inventário
**Complexidade MVP:** Alta → "sandbox-lite" (grid pequeno, 5 materiais)

**Parâmetros chave:**
- `world_size`, `material_types`, `has_crafting`, `inventory_size`

> ⚠️ No MVP, tratar como "sandbox-lite" focando em grid editável básico.
