# LAST WARD

Beat ’em up 2.5D original ambientado em **Porto Vésper**. Quatro lutadores, rotas ramificadas, chefes com fases e campanha arcade.

Jogo original — personagens, inimigos, estágios e história próprios.

## Jogar

```bash
npm install
npm run dev
```

Abre em `http://localhost:8080`.

## Controles

| Ação | Teclado | Gamepad |
| --- | --- | --- |
| Mover | WASD / setas | Analógico / D-pad |
| Correr | Shift (ou duplo toque na direção) | RT |
| Soco / leve | J / Z | X |
| Chute / pesado | K / X | Y |
| Especial | L / C | B |
| Super | I / V | RB |
| Agarrar | U / G | LB |
| Esquiva / guarda | O / F | LT |
| Pular | Espaço | A |
| Taunt | T | — |
| Pausa | Esc / P | Start |

No celular: stick analógico à esquerda e botões à direita.

## Personagens

- **Kael Morrow** — boxer do cais, equilibrado
- **Vyra Quill** — rápida, strings longas
- **Rutger Kane** — pesado, agarrões
- **Sien Park** — técnica, especiais precisos

## Modos

História, Arcade, Treinamento, Desafios, Boss Rush, Cooperativo local (P1 WASD, P2 setas/numpad).

Progresso (slots, upgrades, conquistas, rotas) fica no `localStorage` do navegador.

## Stack

React 19 + TanStack Start + Canvas 2D, timestep fixo 60 Hz.

## Licença

Conteúdo original do projeto Last Ward. Código publicado para o dono do repositório.
