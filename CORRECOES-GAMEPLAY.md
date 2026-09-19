# Last Ward — Correções de gameplay

Esta versão integra as correções da segunda auditoria:

- upgrades aplicados de verdade ao personagem e combos secretos condicionados ao upgrade;
- compra de upgrades no slot selecionado, com pré-requisitos e salvamento por mesclagem;
- segredos wall/door/npc/quick funcionais e persistentes;
- colecionáveis persistentes na galeria;
- rotas, flags, bosses e finais persistentes;
- controles de coop separados (P1 WASD, P2 setas/Numpad; setas continuam disponíveis ao P1 no solo);
- correção de soft-lock quando todos os jogadores ficam derrubados;
- Arcade com 3 vidas totais e continues realmente consumidos;
- desafios com objetivos e validação de sucesso;
- conquistas integradas a kills, combos, ranks, coop, armas, personagens, segredos, rotas, bosses, objetos, Arcade, Nightmare e Boss Rush;
- estatísticas de bosses, mortes, tempo por personagem, armas, objetos quebrados, agarrões, rotas, finais, desafios e Boss Rush;
- Boss Rush com sequência, conclusão, recompensa e recuperação parcial entre chefes;
- remoção correta do listener de visibilitychange;
- persistência das estatísticas também em Game Over;
- correção de contagem/persistência de vidas entre fases do Arcade.

Validação:

- motor do jogo: typecheck isolado aprovado;
- sintaxe TypeScript/TSX dos arquivos alterados: aprovada;
- suíte geral: 195 testes, 187 aprovados e 8 falhas preexistentes no plugin PWA/branding.
