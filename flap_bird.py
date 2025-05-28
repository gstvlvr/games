import pygame
import os
import random


TELA_LARGURA = 500
TELA_ALTURA = 800

imagem_do_cano = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))
imagem_do_chao = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))
imagem_do_background = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))
imagens_passaros = [
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))), 
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png")))
] 
pygame.font.init()
fonte_pontos = pygame.font.SysFont("arial", 50)

class Passaro:
    IMGS = imagens_passaros
    #animaçoes da rotaçao
    rotaçao_maxima = 25
    velocidade_rotaçao = 20
    tempo_animaçao = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angulo = 0
        self.velocidade = 0
        self.altura = self.y
        self.tempo = 0
        self.contagem_imagem = 0
        self.image = self.IMGS[0]
    
    def pular(self):
        self.velocidade = -10.5
        self.tempo = 0
        self.altura = self.y
    
    def mover(self):
        #calcular deslocamento
        self.tempo += 1
        deslocamento = 1.5 * (self.tempo**2) + self.velocidade * self.tempo
        #restringir o deslocamneto
        if deslocamento > 16:
            deslocamento = 16
        elif deslocamento < 0:
            deslocamento -= 2
        
        self.y += deslocamento
        #angulo do passaro
        if deslocamento < 0 or self.y < (self.altura + 50):
            if self.angulo < self.rotaçao_maxima:
                self.angulo = self.rotaçao_maxima
        else:
            if self.angulo > -90:
                self.altura -= self.velocidade_rotaçao

    def desenhar(self, tela):
        # definir qual imagem do passaro usar
        self.contagem_imagem += 1

        if self.contagem_imagem < self.tempo_animaçao:
            self.image = self.IMGS[0]
        elif self.contagem_imagem < self.tempo_animaçao*2:
            self.image = self.IMGS[1]
        elif self.contagem_imagem < self.tempo_animaçao*3:
            self.image = self.IMGS[2]
        elif self.contagem_imagem < self.tempo_animaçao*4:
            self.image = self.IMGS[1]
        elif self.contagem_imagem >= self.tempo_animaçao*4 + 1:
            self.image = self.IMGS[0]
            self.contagem_imagem = 0    

        # se po passaro estiver caindo ele nao bate asa
        if self.angulo <= -80:
            self.image = self.IMGS[1]
            self.contagem_imagem = self.tempo_animaçao*2

        # desenhar a imagem
        imagem_rotacionada = pygame.transform.rotate(self.image, self.altura)
        pos_centro_imagem = self.image.get_rect(topleft=(self.x, self.y)).center 
        retangulo = imagem_rotacionada.get_rect(center= pos_centro_imagem)
        tela.blit(imagem_rotacionada, retangulo.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.image)

class Cano:
    distacia = 200
    velocidade = 5

    def __init__(self, x):
        self.x = x
        self.altura = 0
        self.pos_topo = 0
        self.base = 0
        self.cano_topo = pygame.transform.flip(imagem_do_cano, False, True) 
        self.cano_base = imagem_do_cano
        self.passou = False
        self.definir_altura()
    def definir_altura(self):
        self.altura = random.randrange(50, 450)
        self.pos_topo = self.altura - self.cano_topo.get_height()
        self.pos_base = self.altura + self.distacia
    def mover(self):
        self.x -= self.velocidade
    def desenhar(self, tela):
        tela.blit(self.cano_topo, (self.x, self.pos_topo))
        tela.blit(self.cano_base, (self.x, self.pos_base))
    def colidir(self, passaro):
        passaro_mask = passaro.get_mask()
        topo_mask = pygame.mask.from_surface(self.cano_topo)
        base_mask = pygame.mask.from_surface(self.cano_base)

        distancia_topo = (self.x - passaro.x, self.pos_topo - round(passaro.y))
        distancia_base = (self.x - passaro.x, self.pos_base - round(passaro.y))
        
        base_ponto = passaro_mask.overlap(base_mask, distancia_base)
        topo_ponto = passaro_mask.overlap(topo_mask, distancia_topo)

        if base_ponto or topo_ponto:
            return True
        else:
            return False

class chao:
    velocidade = 5
    largura = imagem_do_chao.get_width()
    imagem = imagem_do_chao

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.largura

    def mover(self):
        self.x1 -= self.velocidade
        self.x2 -= self.velocidade

        if self.x1 + self.largura < 0:
            self.x1 = self.x2 + self.largura
        if self.x2 + self.largura < 0:
            self.x2 + self.x1 + self.largura 

    def desenhar(self, tela):
        tela.blit(self.imagem, (self.x1, self.y))
        tela.blit(self.imagem, (self.x2, self.y))  

def desenhar_tela(tela, passaros, canos, chao, pontos):
    tela.blit(imagem_do_background, (0, 0))  
    for passaro in passaros:
        passaro.desenhar(tela)
    for cano in canos:
        cano.desenhar(tela)
    
    texto = fonte_pontos.render(f"pontuação: {pontos}", 1, (255, 255, 255))
    tela.blit(texto, (TELA_LARGURA - 10 - texto.get_width(), 10))
    chao.desenhar(tela)
    pygame.display.update()
def main():
    passaros = [Passaro(230, 350)]
    Chao = chao(730)
    canos = [Cano(700)]
    tela = pygame.display.set_mode((TELA_LARGURA, TELA_ALTURA))
    pontos = 0
    relogio = pygame.time.Clock()

    rodando = True
    while rodando:
        relogio.tick(30)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
                pygame.quit()
                quit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    for passaro in passaros:
                        passaro.pular()
            
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    for passaro in passaros:
                        passaro.pular()
        
                        
        for passaro in passaros:
            passaro.mover()
        Chao.mover()

        adicionar_cano = False
        remover_canos = []
        for cano in canos:
            for i, passaro in enumerate(passaros):
                if cano.colidir(passaro):
                    passaros.pop(i)
                if not cano.passou and passaro.x > cano.x:
                    cano.passou = True
                    adicionar_cano = True
                cano.mover()
                if cano.x + cano.cano_topo.get_width() < 0:
                    remover_canos.append(cano)
        if adicionar_cano:
            pontos += 1
            canos.append(Cano(600))
        for cano in remover_canos:
            canos.remove(cano)
        for i, passaro in enumerate(passaros):
            if (passaro.y + passaro.image.get_height()) > Chao.y or passaro.y < 0:
                passaros.pop(i)
        
        desenhar_tela(tela, passaros, canos, Chao, pontos)
        
if __name__ == "__main__":
    main()






            

