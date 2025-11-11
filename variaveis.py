# ===============================
# CONFIGURAÇÕES GERAIS DA TELA
# ===============================
TAMANHO_TELA = (517, 690)
FPS = 60

# ===============================
# CONFIGURAÇÕES DE VIDA
# ===============================
PLAYER_VIDA_INICIAL = 30
BOSS_VIDA_INICIAL = 100
BOSS_VIDA_FASE2 = 200 # Vida extra para a segunda fase

# ===============================
# CONFIGURAÇÕES DO PLAYER
# ===============================
PLAYER_VELOCIDADE = 300
PLAYER_INTERVALO_TIRO = 8
PLAYER_ALTURA_MAXIMA_BUFFER = 100

# ===============================
# CONFIGURAÇÕES DO BOSS
# ===============================
BOSS_VELOCIDADE = 200
BOSS_POSICAO_Y_INICIAL = 100
BOSS_INTERVALO_ATAQUE = 120 

# ===============================
# CONFIGURAÇÕES DO ATAQUE ESPECIAL
# ===============================
BOSS_ATAQUES_ATE_ESPECIAL = 2 
BOSS_ATAQUES_ATE_ESPECIAL_F2 = 3
BOSS_ESPECIAL_DELAY = 3 
INTERVALO_ONDAS_F1 = 3
MISSEL_VELOCIDADE = 350
POSICOES_LASER_FASE2 = [7/20, 12/20, 17/20] 
LASER_FASE2_DURACAO = 2.0 
LASER_FASE2_INTERVALO = 1.5

# ===============================
# CONFIGURAÇÕES DOS PROJÉTEIS
# ===============================
PROJETIL_VELOCIDADE = 600
BOMBA_VELOCIDADE = 400

# ===============================
# CONFIGURAÇÕES DA FONTE E TEXTO
# ===============================
FONTE_TAMANHO = 32
COR_TEXTO = (255, 255, 255) 

# ===============================
# CAMINHOS DOS ARQUIVOS (ASSETS)
# ===============================
# FASE 1
CAMINHO_NAVE = 'graficos/nave.png'
CAMINHO_BOSS = 'graficos/Boss.png'

# FASE 2
CAMINHO_NAVE_FASE2 = 'graficos/Player_mecha.png'
CAMINHO_BOSS_FASE2 = 'graficos/Boss_mecha.png'
CAMINHO_LASER_BOSS = 'graficos/laser_boss.png'

# PROJÉTEIS
CAMINHO_PROJETIL_PLAYER = 'graficos/projetil_p.png'
CAMINHO_PROJETIL_BOSS = 'graficos/Tiro_boss.png'
CAMINHO_LASER = 'graficos/laser.png'
CAMINHO_PROJETIL_B_ESQUERDA = 'graficos/projetil_b_esquerda.png' 
CAMINHO_PROJETIL_B_DIREITA = 'graficos/projetil_b_direita.png'

# BOMBAS (NOVOS)
CAMINHO_BOMBA = 'graficos/Granade_b.png'
CAMINHO_EXPLOSAO = 'graficos/Granade_Boom.png'