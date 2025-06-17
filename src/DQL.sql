-- 1.localização do jogador
SELECT 
    estagiario.id_personagem,
    estagiario.andar_atual,
    estagiario.sala_atual,
    andar.numero,
    andar.nome,
    sala.nome,
    sala.descricao
FROM Estagiario estagiario
JOIN Andar andar ON estagiario.andar_atual = andar.id_andar
JOIN Sala sala ON estagiario.sala_atual = sala.id_sala;

-- 2.inventário do jogador
SELECT 
    item.nome,
    item.tipo,
    item.descricao,
    iteminventario.quantidade
FROM ItemInventario iteminventario
JOIN InstanciaItem instanciaitem ON iteminventario.id_instancia = instanciaitem.id_instancia
JOIN Item item ON instanciaitem.id_item = item.id_item
WHERE iteminventario.id_inventario = 1;

-- 3.NPCs suas missões
SELECT 
    npc.id_personagem,
    personagem.nome,
    npc.tipo,
    npc.andar_atual,
    npc.dialogo_padrao,
    missao.id_missao,
    missao.nome,
    missao.descricao,
    missao.tipo,
    missao.xp_recompensa,
    missao.moedas_recompensa
FROM NPC npc
JOIN Personagem personagem ON npc.id_personagem = personagem.id_personagem
LEFT JOIN Missao missao ON missao.npc_origem = npc.id_personagem;

-- 4.status das missões do jogador
SELECT 
    missao.id_missao,
    missao.nome,
    missao.descricao,
    missao.tipo,
    missao.xp_recompensa,
    missao.moedas_recompensa,
    missaostatus.status
FROM Missao missao
JOIN MissaoStatus missaostatus ON missao.id_missao = missaostatus.id_missao
WHERE missaostatus.id_estagiario = 1;

-- 5.itens da cafeteria
SELECT 
    item.id_item,
    item.nome,
    item.descricao,
    item.tipo,
    item.preco_base,
    instanciaitem.quantidade
FROM InstanciaItem instanciaitem
JOIN Item item ON instanciaitem.id_item = item.id_item
WHERE instanciaitem.local_atual = 'Loja'
ORDER BY item.tipo, item.preco_base;

-- 6. Status do Estagiário
SELECT 
    estagiario.id_personagem,
    estagiario.nome,
    estagiario.nivel,
    estagiario.xp,
    estagiario.coins,
    estagiario.status,
    estagiario.respeito
FROM Estagiario estagiario;


SELECT * FROM Inimigo;