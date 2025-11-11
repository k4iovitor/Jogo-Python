import pygame
import variaveis
from random import randint

# Carrega os assets específicos da Fase 2
boss_superficie_f2_original = pygame.image.load(variaveis.CAMINHO_BOSS_FASE2)
boss_superficie_f2_original = pygame.transform.scale_by(boss_superficie_f2_original, 0.3)
boss_projetil_superficie_original = pygame.image.load(variaveis.CAMINHO_PROJETIL_BOSS)
laser_boss_original = pygame.image.load(variaveis.CAMINHO_LASER_BOSS)
bomba_superficie_original = pygame.image.load(variaveis.CAMINHO_BOMBA)
bomba_superficie_original = pygame.transform.scale_by(bomba_superficie_original, 1/6)
explosao_superficie_original = pygame.image.load(variaveis.CAMINHO_EXPLOSAO)
explosao_superficie_original = pygame.transform.scale_by(explosao_superficie_original, 2/6)

# Variáveis para guardar as superfícies otimizadas
boss_superficie_f2 = None
boss_projetil_superficie = None
laser_boss_superficie = None
bomba_superficie = None
explosao_superficie = None

def otimizar_assets_fase2():
    """Otimiza as imagens da Fase 2 depois que o display do Pygame foi iniciado."""
    global boss_superficie_f2, boss_projetil_superficie, laser_boss_superficie, bomba_superficie, explosao_superficie
    global boss_superficie_f2_original, boss_projetil_superficie_original, laser_boss_original, bomba_superficie_original, explosao_superficie_original

    boss_superficie_f2_original = boss_superficie_f2_original.convert_alpha()
    boss_projetil_superficie = boss_projetil_superficie_original.convert_alpha()
    laser_boss_original = laser_boss_original.convert_alpha()
    bomba_superficie = bomba_superficie_original.convert_alpha()
    explosao_superficie = explosao_superficie_original.convert_alpha()

    boss_superficie_f2 = pygame.transform.scale(boss_superficie_f2_original, (int(boss_superficie_f2_original.get_width() * 0.7), int(boss_superficie_f2_original.get_height() * 0.7)))
    laser_boss_superficie = pygame.transform.scale(laser_boss_original, (variaveis.TAMANHO_TELA[0], laser_boss_original.get_height()))


def inicializar_fase2(posicao_central_anterior):
    """Prepara e retorna um dicionário com o estado inicial do chefe na Fase 2."""
    boss_info = {
        'superficie': boss_superficie_f2,
        'retangulo': boss_superficie_f2.get_rect(center=posicao_central_anterior),
        'vida': variaveis.BOSS_VIDA_FASE2,
        'velocidade': variaveis.BOSS_VELOCIDADE, 'direcao': 1, 'intervalo_ataque': variaveis.BOSS_INTERVALO_ATAQUE,
        'lista_projeteis': [], 'projetil_superficie': boss_projetil_superficie, 'estado_ataque': 'normal',
        'proximo_especial': 1, 'contador_ataques': 0, 'delay_timer': -1,
        'intervalo_ondas_timer': 0, 'ondas_disparadas': 0, 'lista_lasers_horizontais': [],
        'lista_bombas': [], 'lista_explosoes': [], 'padrao_bomba': 0
    }
    return boss_info

def atualizar_boss_fase2(boss_info, delta_tempo):
    """Atualiza toda a lógica do chefe na Fase 2."""
    
    if boss_info['estado_ataque'] != 'especial_bombas':
        boss_info['retangulo'].x += boss_info['velocidade'] * boss_info['direcao'] * delta_tempo
        if boss_info['retangulo'].right >= variaveis.TAMANHO_TELA[0]:
            boss_info['retangulo'].right = variaveis.TAMANHO_TELA[0]; boss_info['direcao'] *= -1
        elif boss_info['retangulo'].left <= 0:
            boss_info['retangulo'].left = 0; boss_info['direcao'] *= -1

    if boss_info['delay_timer'] > 0:
        boss_info['delay_timer'] -= delta_tempo
        if boss_info['delay_timer'] <= 0:
            if boss_info['proximo_especial'] == 1:
                boss_info['estado_ataque'] = 'especial_lasers'
                boss_info['proximo_especial'] = 2
            else:
                boss_info['estado_ataque'] = 'especial_bombas'
                boss_info['proximo_especial'] = 1
                boss_info['padrao_bomba'] = randint(1, 4)
            
            boss_info['ondas_disparadas'] = 0
            boss_info['contador_ataques'] = 0
            boss_info['delay_timer'] = -1
            boss_info['intervalo_ondas_timer'] = 0

    if boss_info['estado_ataque'] == 'normal':
        boss_info['intervalo_ataque'] -= 1
        if boss_info['intervalo_ataque'] <= 0:
            boss_info['intervalo_ataque'] = variaveis.BOSS_INTERVALO_ATAQUE
            pos_x1 = boss_info['retangulo'].centerx - boss_info['retangulo'].width / 4
            pos_x2 = boss_info['retangulo'].centerx + boss_info['retangulo'].width / 4
            proj_ret1 = boss_projetil_superficie.get_rect(midtop=(pos_x1, boss_info['retangulo'].bottom))
            proj_ret2 = boss_projetil_superficie.get_rect(midtop=(pos_x2, boss_info['retangulo'].bottom))
            boss_info['lista_projeteis'].extend([proj_ret1, proj_ret2])
            
            boss_info['contador_ataques'] += 1
            # --- CORREÇÃO AQUI: Alterado de '>=' para '==' ---
            if boss_info['delay_timer'] == -1 and boss_info['contador_ataques'] == variaveis.BOSS_ATAQUES_ATE_ESPECIAL_F2:
                boss_info['delay_timer'] = variaveis.BOSS_ESPECIAL_DELAY
    
    elif boss_info['estado_ataque'] == 'especial_lasers':
        boss_info['intervalo_ondas_timer'] -= delta_tempo
        if boss_info['intervalo_ondas_timer'] <= 0:
            if len(boss_info['lista_lasers_horizontais']) > 0:
                boss_info['lista_lasers_horizontais'].clear()
                boss_info['intervalo_ondas_timer'] = variaveis.LASER_FASE2_INTERVALO
            else:
                if boss_info['ondas_disparadas'] < len(variaveis.POSICOES_LASER_FASE2):
                    pos_y = variaveis.TAMANHO_TELA[1] * variaveis.POSICOES_LASER_FASE2[boss_info['ondas_disparadas']]
                    laser_ret = laser_boss_superficie.get_rect(topleft=(0, pos_y))
                    boss_info['lista_lasers_horizontais'].append({'retangulo': laser_ret})
                    boss_info['ondas_disparadas'] += 1
                    boss_info['intervalo_ondas_timer'] = variaveis.LASER_FASE2_DURACAO
                else: 
                    boss_info['estado_ataque'] = 'normal'
    
    elif boss_info['estado_ataque'] == 'especial_bombas':
        if not boss_info['lista_bombas'] and not boss_info['lista_explosoes']:
            b1 = bomba_superficie.get_rect(midbottom=boss_info['retangulo'].midbottom)
            b2 = bomba_superficie.get_rect(midbottom=boss_info['retangulo'].midbottom)
            b3 = bomba_superficie.get_rect(midbottom=boss_info['retangulo'].midbottom)
            boss_info['lista_bombas'] = [{'rect': b1}, {'rect': b2}, {'rect': b3}]

        # --- CORREÇÃO AQUI: O loop agora usa 'enumerate' para um índice seguro ---
        for i, bomba in enumerate(boss_info['lista_bombas'][:]):
            padrao = boss_info['padrao_bomba']
            if padrao == 1: # Padrão Diagonal 1
                bomba['rect'].y += variaveis.BOMBA_VELOCIDADE * delta_tempo
                if i == 1: bomba['rect'].x -= variaveis.BOMBA_VELOCIDADE * 0.5 * delta_tempo
                if i == 2: bomba['rect'].x += variaveis.BOMBA_VELOCIDADE * 0.5 * delta_tempo
            elif padrao == 2: # Padrão Diagonal 2
                bomba['rect'].y += variaveis.BOMBA_VELOCIDADE * delta_tempo
                if i == 1: bomba['rect'].x += variaveis.BOMBA_VELOCIDADE * 0.5 * delta_tempo
                if i == 2: bomba['rect'].x -= variaveis.BOMBA_VELOCIDADE * 0.5 * delta_tempo
            elif padrao == 3: # Padrão Horizontal (agora afeta todas as bombas)
                 bomba['rect'].y += variaveis.BOMBA_VELOCIDADE * 1.5 * delta_tempo
                 if i == 1: bomba['rect'].x -= variaveis.BOMBA_VELOCIDADE * 0.3 * delta_tempo
                 if i == 2: bomba['rect'].x += variaveis.BOMBA_VELOCIDADE * 0.3 * delta_tempo
            else: # Padrão Vertical (com velocidades diferentes)
                if i == 0: bomba['rect'].y += variaveis.BOMBA_VELOCIDADE * 0.8 * delta_tempo
                if i == 1: bomba['rect'].y += variaveis.BOMBA_VELOCIDADE * 1.2 * delta_tempo
                if i == 2: bomba['rect'].y += variaveis.BOMBA_VELOCIDADE * 1.5 * delta_tempo

            if bomba['rect'].top > variaveis.TAMANHO_TELA[1] - 20:
                exp_rect = explosao_superficie.get_rect(center=bomba['rect'].center)
                boss_info['lista_explosoes'].append({'rect': exp_rect, 'timer': 1.0}) 
                boss_info['lista_bombas'].remove(bomba)
        
        for explosao in boss_info['lista_explosoes'][:]:
            explosao['timer'] -= delta_tempo
            if explosao['timer'] <= 0:
                boss_info['lista_explosoes'].remove(explosao)
        
        if not boss_info['lista_bombas'] and not boss_info['lista_explosoes']:
            boss_info['estado_ataque'] = 'normal'

    # Atualiza projéteis normais
    for p in boss_info['lista_projeteis'][:]:
        p.y += variaveis.PROJETIL_VELOCIDADE * delta_tempo
        if p.top > variaveis.TAMANHO_TELA[1]:
            boss_info['lista_projeteis'].remove(p)

    return boss_info