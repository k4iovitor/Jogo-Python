import pygame
import variaveis 
import fase2 

# --- FUNÇÃO DE INICIALIZAÇÃO GERAL ---
def inicializar_jogo():
    pygame.init()
    pygame.mixer.init() 
    pygame.display.set_caption('Cosmic Fury')
    tela = pygame.display.set_mode(variaveis.TAMANHO_TELA)
    relogio = pygame.time.Clock()
    fonte_hud = pygame.font.Font(None, variaveis.FONTE_TAMANHO)
    fonte_botao = pygame.font.Font(None, 50)
    
    fase2.otimizar_assets_fase2()
    
    return tela, relogio, fonte_hud, fonte_botao

# --- FUNÇÃO PRINCIPAL ---
def rodar_jogo():
    tela, relogio, fonte_hud, fonte_botao = inicializar_jogo()

    # --- ESTADOS GERAIS DO JOGO ---
    running = True
    estado_jogo = 'titulo' 
    fase_atual = 1
    
    # --- MÚSICAS ---
    stranger_song = pygame.mixer.Sound('Stranger.mp3')
    stranger_song.set_volume(0.15)
    red_sun_song = pygame.mixer.Sound('Red Sun.mp3')
    red_sun_song.set_volume(0.15)
    titulo_song = pygame.mixer.Sound('Tittle.mp3')
    titulo_song.set_volume(0.15)
    grito_transformacao = pygame.mixer.Sound('scream.mp3')
    grito_transformacao.set_volume(0.15)
    tiro_som = pygame.mixer.Sound('laser_shot.mp3')
    tiro_som.set_volume(0.15)
    
    musica_tocando = None
    timer_transicao = 0

    # --- ASSETS GERAIS E TELA DE TÍTULO ---
    bg_surf = pygame.image.load('graficos/bg.png').convert()
    titulo_surf = pygame.transform.scale_by(pygame.image.load('graficos/Titulo.png').convert_alpha(), 1/2)
    botao_surf = pygame.transform.scale_by(pygame.image.load('graficos/Botão.png').convert_alpha(), 1/6)
    botao_surf.set_colorkey('black')
    botao_rect_play = botao_surf.get_rect(center=(tela.get_width() * 3/4, 450))
    botao_rect_quit = botao_surf.get_rect(center=(tela.get_width() * 3/4, 520))
    texto_play_surf = fonte_botao.render('Play', False, 'white')
    texto_quit_surf = fonte_botao.render('Quit', False, 'white')

    # --- ASSETS DO PLAYER (AMBAS AS FASES) ---
    player_superficie_f1 = pygame.image.load(variaveis.CAMINHO_NAVE).convert_alpha()
    player_superficie_f1 = pygame.transform.scale_by(player_superficie_f1,1/8)
    player_superficie_f1 = pygame.transform.rotate(player_superficie_f1,180)
    player_superficie_f1.set_colorkey('black')
    player_superficie_f2 = pygame.image.load(variaveis.CAMINHO_NAVE_FASE2).convert_alpha()
    player_superficie_f2 = pygame.transform.scale_by(player_superficie_f2, 1/8)
    player_superficie_f2.set_colorkey('black')
    player_superficie = player_superficie_f1
    player_retangulo = player_superficie.get_rect(center=(tela.get_width()/2, tela.get_height() * (7/8)))
    player_vida = variaveis.PLAYER_VIDA_INICIAL
    player_intervalo_tiro = 0
    player_lista_projeteis = []
    player_dano_cooldown = 0
    player_projetil_superficie = pygame.image.load(variaveis.CAMINHO_PROJETIL_PLAYER).convert_alpha()
    player_projetil_superficie = pygame.transform.scale_by(player_projetil_superficie, 1/16)

    # --- ASSETS DO BOSS (FASE 1) ---
    boss_superficie_f1_original = pygame.image.load(variaveis.CAMINHO_BOSS).convert_alpha()
    t_f1 = boss_superficie_f1_original.get_size()
    boss_superficie_f1 = pygame.transform.scale_by(boss_superficie_f1_original, 1/3)
    
    # --- DICIONÁRIO DE DADOS DO BOSS (COMEÇA NA FASE 1) ---
    boss_info = {
        'superficie': boss_superficie_f1,
        'retangulo': boss_superficie_f1.get_rect(center=(tela.get_width() / 2, variaveis.BOSS_POSICAO_Y_INICIAL)),
        'vida': variaveis.BOSS_VIDA_INICIAL, 'velocidade': variaveis.BOSS_VELOCIDADE, 'direcao': 1, 'intervalo_ataque': variaveis.BOSS_INTERVALO_ATAQUE,
        'lista_projeteis': [], 'projetil_superficie': pygame.image.load(variaveis.CAMINHO_PROJETIL_BOSS).convert_alpha(),
        'estado_ataque': 'normal', 'proximo_especial': 1, 'pronto_para_especial_2': False, 'contador_ataques': 0,
        'delay_timer': -1, 'intervalo_ondas_timer': 0, 'ondas_disparadas': 0,
        'lista_misseis': [], 'lista_bombas': [], 'lista_explosoes': []
    }

    # Assets Especiais (Fase 1)
    missel_esq_superficie = pygame.image.load(variaveis.CAMINHO_PROJETIL_B_ESQUERDA).convert_alpha()
    missel_dir_superficie = pygame.image.load(variaveis.CAMINHO_PROJETIL_B_DIREITA).convert_alpha()
    laser_superficie = pygame.transform.scale(pygame.image.load(variaveis.CAMINHO_LASER).convert_alpha(), (40, variaveis.TAMANHO_TELA[1]))
    laser_esq_retangulo = laser_superficie.get_rect(midtop=boss_info['retangulo'].midbottom)
    laser_dir_retangulo = laser_superficie.get_rect(midtop=boss_info['retangulo'].midbottom)
    posicoes_y_misseis = [frac * variaveis.TAMANHO_TELA[1] for frac in [10/20, 14/20, 18/20, 12/20, 16/20, 8/20, 18/20, 15/20, 11/20, 17/20]]
    indice_posicao_missel = 0
    bomba_f1_surf = pygame.image.load(variaveis.CAMINHO_BOMBA).convert_alpha()
    bomba_f1_surf = pygame.transform.scale_by(bomba_f1_surf, 2/10)
    explosao_f1_surf = pygame.image.load(variaveis.CAMINHO_EXPLOSAO).convert_alpha()
    explosao_f1_surf = pygame.transform.scale_by(explosao_f1_surf, 3/10)

    # ===============================
    # LOOP PRINCIPAL DO JOGO
    # ===============================
    while running:
        eventos = pygame.event.get()
        for evento in eventos:
            if evento.type == pygame.QUIT: running = False

        tela.blit(bg_surf, (0,0))
        delta_tempo = relogio.tick(variaveis.FPS) / 1000

        if estado_jogo == 'titulo':
            if musica_tocando != 'titulo': titulo_song.play(-1); musica_tocando = 'titulo'
            tela.blit(titulo_surf, (0, 89))
            tela.blit(botao_surf, botao_rect_play); tela.blit(texto_play_surf, (botao_rect_play.x + 65, botao_rect_play.y + 18))
            tela.blit(botao_surf, botao_rect_quit); tela.blit(texto_quit_surf, (botao_rect_quit.x + 65, botao_rect_quit.y + 18))
            if pygame.mouse.get_pressed()[0]:
                if botao_rect_play.collidepoint(pygame.mouse.get_pos()): estado_jogo = 'batalha'; titulo_song.stop(); musica_tocando = None
                if botao_rect_quit.collidepoint(pygame.mouse.get_pos()): running = False
        
        elif estado_jogo == 'transicao':
            if int(timer_transicao * 10) % 2 == 0: tela.fill((150, 0, 0))
            timer_transicao -= delta_tempo
            if timer_transicao <= 0:
                fase_atual = 2
                player_superficie = player_superficie_f2
                player_retangulo = player_superficie.get_rect(center=player_retangulo.center)
                boss_info = fase2.inicializar_fase2(boss_info['retangulo'].center)
                estado_jogo = 'batalha'

        elif estado_jogo == 'batalha':
            if fase_atual == 1 and musica_tocando != 'fase1': red_sun_song.play(-1); musica_tocando = 'fase1'
            elif fase_atual == 2 and musica_tocando != 'fase2':
                if not pygame.mixer.get_busy(): stranger_song.play(-1); musica_tocando = 'fase2'

            teclas = pygame.key.get_pressed()
            
            altura_limite = boss_info['retangulo'].bottom + variaveis.PLAYER_ALTURA_MAXIMA_BUFFER
            if teclas[pygame.K_UP] and player_retangulo.top > altura_limite: player_retangulo.y -= variaveis.PLAYER_VELOCIDADE * delta_tempo
            if teclas[pygame.K_DOWN] and player_retangulo.bottom < variaveis.TAMANHO_TELA[1]: player_retangulo.y += variaveis.PLAYER_VELOCIDADE * delta_tempo
            if teclas[pygame.K_LEFT] and player_retangulo.left > 0: player_retangulo.x -= variaveis.PLAYER_VELOCIDADE * delta_tempo
            if teclas[pygame.K_RIGHT] and player_retangulo.right < variaveis.TAMANHO_TELA[0]: player_retangulo.x += variaveis.PLAYER_VELOCIDADE * delta_tempo
            
            if teclas[pygame.K_z] and player_intervalo_tiro <= 0:
                tiro_som.play()
                if fase_atual == 1: player_lista_projeteis.append(player_projetil_superficie.get_rect(midbottom=player_retangulo.midtop))
                else:
                    player_lista_projeteis.append(player_projetil_superficie.get_rect(midbottom=(player_retangulo.centerx - player_retangulo.width / 4, player_retangulo.top)))
                    player_lista_projeteis.append(player_projetil_superficie.get_rect(midbottom=(player_retangulo.centerx + player_retangulo.width / 4, player_retangulo.top)))
                player_intervalo_tiro = variaveis.PLAYER_INTERVALO_TIRO
            player_intervalo_tiro -= 1
            for p in player_lista_projeteis[:]:
                p.y -= variaveis.PROJETIL_VELOCIDADE * delta_tempo
                if p.bottom < 0: player_lista_projeteis.remove(p)

            if boss_info['vida'] > 0:
                
                if fase_atual == 1:
                    boss_info['retangulo'].x += boss_info['velocidade'] * boss_info['direcao'] * delta_tempo
                    
                    if boss_info['retangulo'].right >= variaveis.TAMANHO_TELA[0]: 
                        boss_info['retangulo'].right = variaveis.TAMANHO_TELA[0]; 
                        boss_info['direcao'] *= -1
                    elif boss_info['retangulo'].left <= 0: boss_info['retangulo'].left = 0; boss_info['direcao'] *= -1
                    
                    if boss_info['delay_timer'] > 0:
                        boss_info['delay_timer'] -= delta_tempo
                        
                        if boss_info['delay_timer'] <= 0:
                            if boss_info['proximo_especial'] == 1: boss_info['estado_ataque'] = 'especial_1'; boss_info['proximo_especial'] = 2
                            elif boss_info['proximo_especial'] == 2: boss_info['estado_ataque'] = 'carregando_especial_2'; boss_info['proximo_especial'] = 3
                            else: boss_info['estado_ataque'] = 'especial_bombas'; boss_info['proximo_especial'] = 1
                            boss_info['ondas_disparadas'] = 0; boss_info['contador_ataques'] = 0; boss_info['lista_projeteis'].clear(); boss_info['delay_timer'] = -1; indice_posicao_missel = 0; boss_info['intervalo_ondas_timer'] = 0; boss_info['lista_misseis'].clear(); boss_info['lista_bombas'].clear(); boss_info['lista_explosoes'].clear()
                    
                    if boss_info['estado_ataque'] == 'normal':
                        boss_info['intervalo_ataque'] -= 1
                        if boss_info['intervalo_ataque'] <= 0:
                            boss_info['intervalo_ataque'] = variaveis.BOSS_INTERVALO_ATAQUE
                            boss_info['lista_projeteis'].append(boss_info['projetil_superficie'].get_rect(midtop=boss_info['retangulo'].midbottom))
                            boss_info['contador_ataques'] += 1
                            if boss_info['delay_timer'] == -1 and boss_info['contador_ataques'] == variaveis.BOSS_ATAQUES_ATE_ESPECIAL:
                                if boss_info['proximo_especial'] == 2: boss_info['pronto_para_especial_2'] = True
                                else: boss_info['delay_timer'] = variaveis.BOSS_ESPECIAL_DELAY
                        if boss_info.get('pronto_para_especial_2') and player_retangulo.centerx > boss_info['retangulo'].left and player_retangulo.centerx < boss_info['retangulo'].right:
                            boss_info['delay_timer'] = variaveis.BOSS_ESPECIAL_DELAY; boss_info['pronto_para_especial_2'] = False
                    
                    elif boss_info['estado_ataque'] == 'especial_bombas':
                        if not boss_info['lista_bombas'] and not boss_info['lista_explosoes']:
                            bomba_rect = bomba_f1_surf.get_rect(midbottom=boss_info['retangulo'].midbottom)
                            boss_info['lista_bombas'].append({'rect': bomba_rect, 'target_y': player_retangulo.y})
                        for bomba in boss_info['lista_bombas'][:]:
                            if bomba['rect'].y < bomba['target_y']: bomba['rect'].y += variaveis.BOMBA_VELOCIDADE * delta_tempo
                            else:
                                exp_rect = explosao_f1_surf.get_rect(center=bomba['rect'].center)
                                boss_info['lista_explosoes'].append({'rect': exp_rect, 'timer': 1.0}); boss_info['lista_bombas'].remove(bomba)
                        for exp in boss_info['lista_explosoes'][:]:
                            exp['timer'] -= delta_tempo
                            if exp['timer'] <= 0: boss_info['lista_explosoes'].remove(exp)
                        if not boss_info['lista_bombas'] and not boss_info['lista_explosoes']: boss_info['estado_ataque'] = 'normal'
                    
                    elif boss_info['estado_ataque'] == 'carregando_especial_2':
                        player_retangulo.centerx = variaveis.TAMANHO_TELA[0] / 2; boss_info['estado_ataque'] = 'especial_2'
                    
                    if boss_info['estado_ataque'] in ['especial_1', 'especial_2']:
                        boss_info['intervalo_ondas_timer'] -= delta_tempo
                        
                        if boss_info['intervalo_ondas_timer'] <= 0:
                            num_posicoes = len(posicoes_y_misseis)
                            if boss_info['ondas_disparadas'] == 0:
                                pos_y = posicoes_y_misseis[indice_posicao_missel % num_posicoes]; 
                                boss_info['lista_misseis'].append({'retangulo': missel_dir_superficie.get_rect(centery=pos_y, right=0), 'direcao': 1, 'superficie': missel_dir_superficie}); indice_posicao_missel += 1
                                for _ in range(2): 
                                    pos_y = posicoes_y_misseis[indice_posicao_missel % num_posicoes]; 
                                    boss_info['lista_misseis'].append({'retangulo': missel_esq_superficie.get_rect(centery=pos_y, left=variaveis.TAMANHO_TELA[0]), 'direcao': -1, 'superficie': missel_esq_superficie}); indice_posicao_missel += 1
                                boss_info['ondas_disparadas'] = 1; boss_info['intervalo_ondas_timer'] = variaveis.INTERVALO_ONDAS_F1
                            
                            elif boss_info['ondas_disparadas'] == 1:
                                for _ in range(2): 
                                    pos_y = posicoes_y_misseis[indice_posicao_missel % num_posicoes]; 
                                    boss_info['lista_misseis'].append({'retangulo': missel_dir_superficie.get_rect(centery=pos_y, right=0), 'direcao': 1, 'superficie': missel_dir_superficie}); indice_posicao_missel += 1
                                pos_y = posicoes_y_misseis[indice_posicao_missel % num_posicoes]; 
                                boss_info['lista_misseis'].append({'retangulo': missel_esq_superficie.get_rect(centery=pos_y, left=variaveis.TAMANHO_TELA[0]), 'direcao': -1, 'superficie': missel_esq_superficie}); indice_posicao_missel += 1
                                boss_info['ondas_disparadas'] = 2; boss_info['intervalo_ondas_timer'] = variaveis.INTERVALO_ONDAS_F1
                            
                            elif boss_info['ondas_disparadas'] == 2:
                                for _ in range(2): 
                                    pos_y = posicoes_y_misseis[indice_posicao_missel % num_posicoes]; 
                                    boss_info['lista_misseis'].append({'retangulo': missel_dir_superficie.get_rect(centery=pos_y, right=0), 'direcao': 1, 'superficie': missel_dir_superficie}); indice_posicao_missel += 1
                                for _ in range(2): 
                                    pos_y = posicoes_y_misseis[indice_posicao_missel % num_posicoes]; 
                                    boss_info['lista_misseis'].append({'retangulo': missel_esq_superficie.get_rect(centery=pos_y, left=variaveis.TAMANHO_TELA[0]), 'direcao': -1, 'superficie': missel_esq_superficie}); indice_posicao_missel += 1
                                
                                boss_info['ondas_disparadas'] = 3; boss_info['intervalo_ondas_timer'] = variaveis.INTERVALO_ONDAS_F1

                            elif boss_info['ondas_disparadas'] == 3:    
                                boss_info['estado_ataque'] = 'normal'
                
                else: # fase_atual == 2
                    boss_info = fase2.atualizar_boss_fase2(boss_info, delta_tempo)
            
            # Atualização de Projéteis
            for p in boss_info['lista_projeteis']: p.y += variaveis.PROJETIL_VELOCIDADE * delta_tempo
            if fase_atual == 1: 
                for m in boss_info['lista_misseis']: m['retangulo'].x += variaveis.MISSEL_VELOCIDADE * m['direcao'] * delta_tempo
            
            if fase_atual == 1 and boss_info['estado_ataque'] in ['carregando_especial_2', 'especial_2']:
                pos_laser_esq_x = boss_info['retangulo'].centerx - boss_info['retangulo'].width / 4
                pos_laser_dir_x = boss_info['retangulo'].centerx + boss_info['retangulo'].width / 4
                laser_esq_retangulo.midtop = (pos_laser_esq_x, boss_info['retangulo'].centery)
                laser_dir_retangulo.midtop = (pos_laser_dir_x, boss_info['retangulo'].centery)
                if player_retangulo.left < laser_esq_retangulo.right: player_retangulo.left = laser_esq_retangulo.right
                if player_retangulo.right > laser_dir_retangulo.left: player_retangulo.right = laser_dir_retangulo.left

            # Lógica de Colisão
            if player_dano_cooldown > 0: player_dano_cooldown -= delta_tempo
            for p in player_lista_projeteis[:]:
                if boss_info['vida'] > 0 and p.colliderect(boss_info['retangulo']):
                    is_invencivel = (fase_atual == 1 and boss_info['estado_ataque'] in ['carregando_especial_2', 'especial_2'])
                    if not is_invencivel: boss_info['vida'] -= 1
                    player_lista_projeteis.remove(p)
                    
                    if boss_info['vida'] <= 0:
                        if fase_atual == 1:
                            estado_jogo = 'transicao'; timer_transicao = 3
                            red_sun_song.stop(); grito_transformacao.play(); musica_tocando = 'fase2_intro'
                        elif fase_atual == 2:
                            print("BOSS DERROTADO! VOCÊ VENCEU!"); stranger_song.stop(); running = False
            
            for p in boss_info['lista_projeteis']:
                if p.colliderect(player_retangulo): player_vida -= 1; boss_info['lista_projeteis'].remove(p); break
            
            if player_dano_cooldown <= 0:
                if fase_atual == 1:
                    if boss_info['estado_ataque'] in ['especial_1', 'especial_2']:
                        for m in boss_info['lista_misseis'][:]:
                            if m['retangulo'].colliderect(player_retangulo): player_vida -= 1; player_dano_cooldown = 0.5; boss_info['lista_misseis'].remove(m); break
                    if boss_info['estado_ataque'] == 'especial_bombas':
                        for exp in boss_info['lista_explosoes']:
                            if exp['rect'].colliderect(player_retangulo): player_vida -= 1; player_dano_cooldown = 0.5; break
                    if boss_info['estado_ataque'] == 'especial_2':
                        if laser_esq_retangulo.colliderect(player_retangulo) or laser_dir_retangulo.colliderect(player_retangulo): player_vida -= 1; player_dano_cooldown = 0.5
                elif fase_atual == 2:
                    for l in boss_info.get('lista_lasers_horizontais', []):
                        if l['retangulo'].colliderect(player_retangulo): player_vida -= 2; player_dano_cooldown = 0.5; break
                    if boss_info['estado_ataque'] == 'especial_bombas':
                        for exp in boss_info.get('lista_explosoes', []):
                            if exp['rect'].colliderect(player_retangulo): player_vida -= 2; player_dano_cooldown = 0.5; break
            
            if player_vida <= 0: print("PLAYER DERROTADO! FIM DE JOGO!"); pygame.mixer.stop(); running = False
            
            # --- RENDERIZAÇÃO DA BATALHA ---
            for p in player_lista_projeteis: tela.blit(player_projetil_superficie, p)
            for p in boss_info['lista_projeteis']: tela.blit(boss_info['projetil_superficie'], p)
            if fase_atual == 1:
                if boss_info['estado_ataque'] in ['especial_1', 'especial_2']:
                    for m in boss_info['lista_misseis']: tela.blit(m['superficie'], m['retangulo'])
                if boss_info['estado_ataque'] == 'especial_2':
                    tela.blit(laser_superficie, laser_esq_retangulo); tela.blit(laser_superficie, laser_dir_retangulo)
                if boss_info['estado_ataque'] == 'especial_bombas':
                    for b in boss_info['lista_bombas']: tela.blit(bomba_f1_surf, b['rect'])
                    for e in boss_info['lista_explosoes']: tela.blit(explosao_f1_surf, e['rect'])
            elif fase_atual == 2:
                if boss_info['estado_ataque'] == 'especial_lasers':
                    for l in boss_info.get('lista_lasers_horizontais', []): tela.blit(fase2.laser_boss_superficie, l['retangulo'])
                elif boss_info['estado_ataque'] == 'especial_bombas':
                    for b in boss_info['lista_bombas']: tela.blit(fase2.bomba_superficie, b['rect'])
                    for e in boss_info['lista_explosoes']: tela.blit(fase2.explosao_superficie, e['rect'])
            tela.blit(player_superficie, player_retangulo)
            if boss_info['vida'] > 0: tela.blit(boss_info['superficie'], boss_info['retangulo'])

            # Renderização da Interface
            texto_vida_player = f"VIDA: {player_vida}"; superficie_texto_player = fonte_hud.render(texto_vida_player, True, variaveis.COR_TEXTO)
            posicao_vida_player = (10, variaveis.TAMANHO_TELA[1] - superficie_texto_player.get_height() - 10); tela.blit(superficie_texto_player, posicao_vida_player)
            texto_vida_boss = f"VIDA: {boss_info['vida']}"; superficie_texto_boss = fonte_hud.render(texto_vida_boss, True, variaveis.COR_TEXTO)
            posicao_vida_boss = (variaveis.TAMANHO_TELA[0] - superficie_texto_boss.get_width() - 10, 10); tela.blit(superficie_texto_boss, posicao_vida_boss)

        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    rodar_jogo()