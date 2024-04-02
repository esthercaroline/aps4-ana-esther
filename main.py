import pygame
import numpy as np

def matriz_rotacao_x(angulo):
    # Retorna uma matriz de rotação 4x4 em torno do eixo x dado um ângulo em graus.

    angulo_radianos = np.radians(angulo)
    return np.array([
        [1, 0, 0, 0],
        [0, np.cos(angulo_radianos), -np.sin(angulo_radianos), 0],
        [0, np.sin(angulo_radianos), np.cos(angulo_radianos), 0], 
        [0, 0, 0, 1]
    ])

def matriz_rotacao_y(angulo):
    # Retorna uma matriz de rotação 4x4 em torno do eixo y dado um ângulo em graus.

    angulo_radianos = np.radians(angulo)
    return np.array([
        [np.cos(angulo_radianos), 0, np.sin(angulo_radianos), 0],
        [0, 1, 0, 0],
        [-np.sin(angulo_radianos), 0, np.cos(angulo_radianos), 0], 
        [0, 0, 0, 1]
    ])

def matriz_rotacao_z(angulo):
    # Retorna uma matriz de rotação 4x4 em torno do eixo z dado um ângulo em graus.

    angulo_radianos = np.radians(angulo)
    return np.array([
        [np.cos(angulo_radianos), -np.sin(angulo_radianos), 0, 0],
        [np.sin(angulo_radianos), np.cos(angulo_radianos), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])

def matriz_translacao(x, y, z):
    # Retorna uma matriz de translação 4x4 dadas as coordenadas x, y e z.

    return np.array([
        [1, 0, 0, x],
        [0, 1, 0, y],
        [0, 0, 1, z],
        [0, 0, 0, 1]
    ])

def projetar_pontos(pontos, dist_focal):
    # Projeta pontos 3D em um plano 2D usando um modelo de câmera pinhole.

    matriz_transformacao = np.array([[0,0,0,-dist_focal], [1,0,0,0], [0,1,0,0], [0,0,-1/dist_focal,0]])
    matriz_wp = matriz_transformacao @ pontos
    pontos_projetados = []
    for i, ponto in enumerate(matriz_wp.T):
        w = ponto[3]
        if pontos[2][i] > 0:
            pontos_projetados.append((ponto[1]/w, ponto[2]/w, pontos[2][i]))
        else:
            pontos_projetados.append((0, 0, 0))
    return np.array(pontos_projetados)

# Define as dimensões da tela
LARGURA, ALTURA = 800, 600
dist_focal = 250

# Define as coordenadas dos vértices do cubo de aresta 2*40 centrado na origem.
vertices = np.array([
    [-1, -1, -1],
    [-1, -1, 1],
    [-1, 1, -1],
    [-1, 1, 1],
    [1, -1, -1],
    [1, -1, 1],
    [1, 1, -1],
    [1, 1, 1],
])*40
vertices = vertices.T
vertices = np.vstack((vertices, np.ones((1, vertices.shape[1]))))

# Define as arestas do cubo
arestas = [
    (0, 1),
    (0, 2),
    (0, 4),
    (1, 3),
    (1, 5),
    (2, 3),
    (2, 6),
    (3, 7),
    (4, 5),
    (4, 6),
    (5, 7),
    (6, 7)
]

# Inicializa o pygame e cria uma janela com dimensões LARGURA x ALTURA.
pygame.init()
tela = pygame.display.set_mode((LARGURA, ALTURA))

# Define o título da janela.
pygame.display.set_caption("Cubo em 3D")

# Cria um objeto de relógio para controlar o framerate do jogo.
relogio = pygame.time.Clock()

# Define a velocidade de movimento e rotação do jogador.
VELOCIDADE_MOV = 3
VELOCIDADE_ROT = 2

# Define a variável 'executando' como True para iniciar o loop do jogo.
executando = True

# Inicializa a variável de ângulo como 0.
angulo = 0

# Define a posição e orientação inicial do jogador.
posicao_jogador = np.array([0, 0, 0, 1])
angulo_jogador = 0

# Define a direção inicial do jogador.
direcao_jogador = np.array([0, 0, 1, 1])

# Inicializa a variável 'posicao_mouse_previa' como None.
posicao_mouse_previa = None

# Inicializa o dicionário 'teclas_pressionadas' como um dicionário vazio.
teclas_pressionadas = {}

# Inicializa a variável de ângulo de rotação atual como 0.
angulo_rotacao_atual = 0

# Inicia o loop do jogo.
while executando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            executando = False

        # Captura as teclas pressionadas pelo usuário.
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                executando = False
            teclas_pressionadas[evento.key] = True
        elif evento.type == pygame.KEYUP:
            teclas_pressionadas[evento.key] = False
        
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 4: 
                dist_focal += 10
            elif evento.button == 5:
                if dist_focal > 10:
                    dist_focal -= 10

    # Atualiza a posição do jogador de acordo com o estado das teclas.
    if teclas_pressionadas.get(pygame.K_w):
        posicao_jogador[2] -= VELOCIDADE_MOV
    elif teclas_pressionadas.get(pygame.K_s):
        posicao_jogador[2] += VELOCIDADE_MOV

    if teclas_pressionadas.get(pygame.K_a):
        posicao_jogador[0] -= VELOCIDADE_MOV
    elif teclas_pressionadas.get(pygame.K_d):
        posicao_jogador[0] += VELOCIDADE_MOV
    
    if teclas_pressionadas.get(pygame.K_e):
        angulo_rotacao_atual += 0.1
    elif teclas_pressionadas.get(pygame.K_q):
        angulo_rotacao_atual -= 0.1

    # Captura os movimentos do mouse.
    if evento.type == pygame.MOUSEMOTION:
        if posicao_mouse_previa is not None:
            # Calcula a diferença entre a posição atual e a posição anterior do mouse.
            diff_mouse = np.array(pygame.mouse.get_pos()) - posicao_mouse_previa

            # Rotaciona o vetor direção_jogador em torno do eixo y.
            direcao_jogador[1] += diff_mouse[0]/3

            # Rotaciona o vetor direcao_jogador em torno do eixo x.
            direcao_jogador[0] -= diff_mouse[1]/3
        posicao_mouse_previa = np.array(pygame.mouse.get_pos())

    # Incrementa o ângulo de rotação do cubo.
    angulo += angulo_rotacao_atual

    # Aplica rotações e translações aos vértices do cubo para simular seu movimento.
    rotacao = (matriz_rotacao_x(direcao_jogador[0]) @ matriz_rotacao_y(direcao_jogador[1]))
    vertices_rotacionados = rotacao @ matriz_translacao(posicao_jogador[0],0, posicao_jogador[2]) @ matriz_translacao(0, 0, 200) @ matriz_rotacao_x(angulo) @ matriz_rotacao_y(angulo) @ matriz_rotacao_z(angulo) @ vertices
    
    # Projeta os vértices em um plano 2D usando o modelo de câmera pinhole.
    pontos_projetados = projetar_pontos(vertices_rotacionados, dist_focal)

    # Preenche a tela com preto.
    tela.fill((0, 0, 0))

    # Desenha linhas entre os pontos projetados para criar o wireframe do cubo.
    for aresta in arestas:
        # Obtém os pontos de início e fim da aresta no espaço 2D.
        inicio = (pontos_projetados[aresta[0]][0] + LARGURA/2, pontos_projetados[aresta[0]][1] + ALTURA/2)
        fim = (pontos_projetados[aresta[1]][0] + LARGURA/2, pontos_projetados[aresta[1]][1] + ALTURA/2)

        # Calcula a distância dos pontos de início e fim da câmera (ao longo do eixo z).
        distancia_z_inicio = pontos_projetados[aresta[0]][2]
        distancia_z_fim = pontos_projetados[aresta[1]][2]

        # Calcula a espessura da linha com base na distância dos pontos de início e fim da câmera.
        grossura_linha = 1/(distancia_z_inicio/1400 + distancia_z_fim/1400)

        # Desenha a linha apenas se os pontos de início e fim estiverem à frente da câmera.
        if pontos_projetados[aresta[0]][2] > 0 and pontos_projetados[aresta[1]][2] > 0 and grossura_linha < 30:
            pygame.draw.line(tela, (255, 255, 255), inicio, fim, int(grossura_linha))
        
    # Atualiza a tela e limita o framerate a 60 FPS.
    pygame.display.flip()
    relogio.tick(60)

# Encerra o pygame.
pygame.quit()
