import os.path
from pdb import runcall
from re import T
import pygame
import neat
import sys
import random
import pickle
pygame.init()


paddle_imgs = [pygame.image.load(os.path.join('assets', 'pong-paddle-1.png')),
            pygame.image.load(os.path.join('assets', 'pong-paddle-2.png'))]


ball_img = pygame.image.load(os.path.join('assets', 'ball.png'))

bg_img = pygame.image.load(os.path.join('assets', 'Pong-background.png'))
FONT = pygame.font.SysFont("Bebas Neue", 42)



class Paddle:
    paddle_speed = 13

    def __init__(self, paddle):
        self.y = self.original_y = 240
        self.paddle_img = paddle_imgs[paddle]
        self.moving_up = False
        self.moving_down = False
        self.hits = 0
        if paddle == 0:
            self.x = self.original_x = 20
        else:
            self.x = self.original_x = 750
        self.rect = pygame.Rect(self.x, self.y, self.paddle_img.get_width(), self.paddle_img.get_height())

    def update(self):
        if self.moving_up:
            self.move_up()
        if self.moving_down:
            self.move_down()

    def manual_update(self):
        self.manual_imput()
        if self.moving_up:
            self.move_up()
        if self.moving_down:
            self.move_down()


    def manual_imput(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_UP]:
            self.moving_up = True
        if key[pygame.K_DOWN]:
            self.moving_down = True

    def move_up(self):
        if self.rect.y > 1:
            self.rect.y -= self.paddle_speed
            self.moving_up = False

    def move_down(self):
        if self.rect.y < 510:
            self.rect.y += self.paddle_speed
            self.moving_down = False

    def draw(self, WIN):
        paddle = WIN.blit(self.paddle_img, (self.rect.x, self.rect.y))

    def reset(self):
        self.rect.x = self.original_x
        self.rect.y = self.original_y


class Ball:

    def __init__(self):
        self.x = random.randrange(300,500)
        self.y = random.randrange(200,400)
        if random.random() < 0.5:
            self.pos_neg = 1
        else:
            self.pos_neg = -1
        self.x_vel = -4 * self.pos_neg
        self.y_vel = 2 * self.pos_neg
        self.ball_img = ball_img
        self.rect = pygame.Rect(self.x, self.y, self.ball_img.get_width(), self.ball_img.get_height())
        self.left_score = 0
        self.right_score = 0

    def movement(self):
        if self.rect.x <= 0 and self.rect.y >= 0 and self.rect.y <= 580:
            self.reset()
            self.right_score +=1

        if self.rect.x >= 780 and self.rect.y>= 0 and self.rect.y <= 580:
            self.reset()
            self.left_score +=1

        if self.rect.y <= 0 and self.rect.x >= 0 and self.rect.x <= 780:
            self.y_vel = -self.y_vel

        if self.rect.y>= 578 and self.rect.x >= 0 and self.rect.x <= 780:
            self.y_vel = -self.y_vel

        self.rect.x += self.x_vel
        self.rect.y += self.y_vel

        
        if -7 <= self.y_vel <= 10:
            self.y_vel *= 1.001
        if -9 <= self.x_vel <= 12:
            self.x_vel *= 1.001



    def reset(self):
        self.rect.x = random.randrange(300, 500)
        self.rect.y = random.randrange(100, 500)
        if random.random() < 0.5:
            self.pos_neg = 1
        else:
            self.pos_neg = -1
        self.x_vel = -4 * self.pos_neg
        self.y_vel = 2 * self.pos_neg

    def draw(self, WIN):
        paddle = WIN.blit(self.ball_img, (self.rect.x, self.rect.y))


class Game:
    WIN_HEIGHT = 600
    WIN_WIDTH = 800
    a = 0
    def __init__(self):
        self.right_paddle = Paddle(1)
        self.left_paddle = Paddle(0)
        self.ball = Ball()
        self.left_hits = 0
        self.right_hits = 0
        self.bg_img = bg_img
        self.WIN = pygame.display.set_mode((self.WIN_WIDTH, self.WIN_HEIGHT))
        self.FONT = pygame.font.SysFont("Bebas Neue", 42)

    def draw_score(self):
        left_score_display = FONT.render(str(self.ball.left_score), 0, (77, 77, 77))
        right_score_display = FONT.render(str(self.ball.right_score), 0, (77, 77, 77))
        self.WIN.blit(left_score_display, (250, 75))
        self.WIN.blit(right_score_display, (550, 75))


    def collision(self):
        if self.ball.rect.colliderect(self.right_paddle.rect):
            self.ball.rect.x = 727
            self.ball.x_vel *= -1
            self.right_hits += 1
        if self.ball.rect.colliderect(self.left_paddle.rect):
            self.ball.rect.x = 43
            self.ball.x_vel *= -1
            self.left_hits += 1

    def loop(self, draw =True):
        self.ball.movement()
        self.collision()
        self.left_paddle.update()
        self.right_paddle.update()
        if draw:
            self.WIN.blit(bg_img, (0, 0))
            self.ball.draw(self.WIN)
            self.right_paddle.draw(self.WIN)
            self.left_paddle.draw(self.WIN)
            self.draw_score()
        self.info = dict(ball_y = self.ball.y, ball_x = self.ball.x, left_paddle_y = self.left_paddle.y,
                            right_paddle_y = self.right_paddle.y, left_paddle_score = self.ball.left_score,
                            right_paddle_score = self.ball.right_score,left_paddle_hits = self.left_hits,
                            right_paddle_hits = self.right_hits)

    def reset(self):
        self.ball.reset()
        self.left_paddle.reset()
        self.right_paddle.reset()
        self.ball.right_score = 0
        self.ball.left_score = 0
        self.right_hits = 0
        self.left_hits = 0



def train_ai(genome1, genome2, config):

    net1 = neat.nn.FeedForwardNetwork.create(genome1, config)
    net2 = neat.nn.FeedForwardNetwork.create(genome2, config)
    old_vel = 0
    run = True
    game = Game()
    clock = pygame.time.Clock()
    standing_still = 0
    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        output1 = net1.activate((game.left_paddle.rect.y, game.ball.rect.y, abs(game.left_paddle.rect.x - game.ball.rect.x),  game.ball.x_vel, game.ball.y_vel))
        decision1 = output1.index(max(output1))
        if decision1 == 0:
            pass
        elif decision1 ==1:
            game.left_paddle.move_up()
        else:
            game.left_paddle.move_down()

        output2 = net2.activate((game.right_paddle.rect.y, game.ball.rect.y, abs(game.right_paddle.rect.x - game.ball.rect.x),  game.ball.x_vel, game.ball.y_vel))
        decision2 = output2.index(max(output2))
        if decision2 == 0:
            pass
        elif decision2 == 1:
            game.right_paddle.move_up()
        else:
            game.right_paddle.move_down()

        key = pygame.key.get_pressed()
        if key[pygame.K_6]:
            break
        if key[pygame.K_8]:
            game.loop(draw=True)
        else:
            game.loop(draw=False)

        pygame.display.update()

        if game.ball.left_score == 1 or game.ball.right_score == 1 or game.right_hits > 50:
            genome1.fitness += game.left_hits
            genome2.fitness += game.right_hits
            break
        if old_vel == game.ball.x:
            standing_still +=1
            if standing_still == 2000:
                print(standing_still)
                standing_still = 0
                break


        old_vel = game.ball.x
    return False





def eval_genomes(genomes, config):

    for i, (genome_id1,genome1) in enumerate(genomes):
        if i == len(genomes) - 1:
            break
        genome1.fitness = 0
        for genome_id2, genome2 in genomes[i+1:]:
            genome2.fitness = 0 if genome2.fitness == None else genome2.fitness
            train_ai(genome1, genome2, config)

#
def run_neat(config):
    # p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-85')
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)


    winner = p.run(eval_genomes,75)

    with open("best.pickle", "wb") as f:
        pickle.dump(winner, f)


def play_best(config):

    run = True
    game = Game()
    clock = pygame.time.Clock()

    with open("best.pickle", "rb") as f:
        winner = pickle.load(f)

    winner_net = neat.nn.FeedForwardNetwork.create(winner, config)

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        clock.tick(60)

        output = winner_net.activate((game.right_paddle.rect.y, game.ball.rect.y, abs(game.right_paddle.rect.x - game.ball.rect.x),  game.ball.x_vel, game.ball.y_vel))
        decision = output.index(max(output))

        if decision == 0:
            pass
        elif decision ==1:
            game.right_paddle.move_up()
        else:
            game.right_paddle.move_down()

        game.left_paddle.manual_imput()


        game.loop()

        pygame.display.update()
        key = pygame.key.get_pressed()
        if key[pygame.K_6]:
            game.reset()

if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'PongNeatConfig.txt')

    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)
    run_neat(config)
    play_best(config)
