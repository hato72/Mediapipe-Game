import pygame
import random
import time
from env import *
from hand_tracking import Hand_tracking
from hand import Hand
import cv2
import draw_image
import sys

class Mole:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.visible = False
        self.appear_time = 0
        self.stay_duration = random.uniform(1.0, 3.0)
        self.image = pygame.image.load("img/mole.png")
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect(center=(x, y))
        self.state = "hidden"
        self.animation_progress = 0
        self.hit_effect_duration = 0.5  # モグラが当たったときのエフェクト表示時間
        self.hit_time = None  # 当たった時のタイムスタンプ
        self.hit_effect_image = pygame.image.load("img/hit_effect.png")  # 当たりエフェクト画像
        self.hit_effect_image = pygame.transform.scale(self.hit_effect_image, (100, 100))
        self.hole_radius = 60

    def draw_hole(self, surface):
        # 穴を描画する (黒い円)
        pygame.draw.circle(surface, (0, 0, 0), (self.x, self.y), self.hole_radius)

    def update(self, current_time):
        # if self.visible and current_time - self.appear_time > self.stay_duration:
        #     self.visible = False
        if self.state == "hidden" and current_time - self.appear_time > self.stay_duration:
            self.state = "appearing"
            self.animation_progress = 0
        elif self.state == "appearing":
            self.animation_progress += 0.05
            if self.animation_progress >= 1:
                self.state = "visible"
                self.appear_time = current_time
        elif self.state == "visible" and current_time - self.appear_time > self.stay_duration:
            self.state = "hiding"
            self.animation_progress = 1
        elif self.state == "hiding":
            self.animation_progress -= 0.05
            if self.animation_progress <= 0:
                self.state = "hidden"
                self.appear_time = current_time

        # ヒットエフェクトの表示時間を管理
        if self.hit_time and current_time - self.hit_time > self.hit_effect_duration:
            self.hit_time = None


    def draw(self, surface):
        # if self.visible:
        #     surface.blit(self.image, self.rect)
        if self.state == "appearing":
            visible_height = int(self.image.get_height() * self.animation_progress)
            visible_part = self.image.subsurface((0, 0, self.image.get_width(), visible_height))
            surface.blit(visible_part, (self.rect.x, self.rect.y + self.rect.height - visible_height))
        elif self.state == "visible":
            surface.blit(self.image, self.rect)
        elif self.state == "hiding":
            visible_height = int(self.image.get_height() * self.animation_progress)
            visible_part = self.image.subsurface((0, 0, self.image.get_width(), visible_height))
            surface.blit(visible_part, (self.rect.x, self.rect.y + self.rect.height - visible_height))

        # モグラに当たった時のエフェクトを描画
        if self.hit_time:
            surface.blit(self.hit_effect_image, self.rect)


    def hit(self):
        if self.state == "visible" or self.state == "appearing":
            self.state = "hiding"
            self.animation_progress = 1
            self.hit_time = time.time()
            return True
        return False

class MoleManager:
    def __init__(self, mole_count, screen_width, screen_height):
        self.moles = []
        self.spawn_interval = 2.0  # 初期は2秒ごとに1匹出現
        self.last_spawn_time = time.time()
        self.spawn_rate_increase = 0.95  # 徐々に出現間隔を短くする
        self.min_spawn_interval = 0.5  # 最短出現間隔
        for _ in range(mole_count):
            x = random.randint(50, screen_width - 50)
            y = random.randint(50, screen_height - 50)
            self.moles.append(Mole(x, y))

    def update(self, current_time):
        # 時間が経過するごとに出現ペースを早める
        if current_time - self.last_spawn_time > self.spawn_interval:
            # ランダムに1匹を出現させる
            hidden_moles = [mole for mole in self.moles if mole.state == "hidden"]
            if hidden_moles:
                mole_to_spawn = random.choice(hidden_moles)
                mole_to_spawn.state = "appearing"
                mole_to_spawn.appear_time = current_time
                self.last_spawn_time = current_time

            # 出現間隔を短縮（ただし最小間隔まで）
            if self.spawn_interval > self.min_spawn_interval:
                self.spawn_interval *= self.spawn_rate_increase

        # 全モグラの状態を更新
        for mole in self.moles:
            mole.update(current_time)

    def draw(self, surface):
        for mole in self.moles:
            mole.draw_hole(surface)
        for mole in self.moles:
            mole.draw(surface)

class Hammer:
    def __init__(self):
        self.image = pygame.image.load("img/hammer.png")
        self.image = pygame.transform.scale(self.image, (150, 150))
        self.rect = self.image.get_rect()
        #当たり判定を変えるときは以下を操作する
        self.rect = pygame.Rect(self.rect.x - 150, self.rect.y - 160, 100, 30)
        self.hitting = False
        self.hit_time = 0
        self.hit_duration = 0.2
        self.hit_angle = 0

    def update(self, x, y, current_time):
        self.rect.center = (x, y)
        # self.hitbox_rect.centerx = self.rect.centerx
        # self.hitbox_rect.centery = self.rect.bottom - (self.hitbox_height // 2) 
        # if self.hitting and current_time - self.hit_time > self.hit_duration:
        #     self.hitting = False
        if self.hitting:
            progress = (current_time - self.hit_time) / self.hit_duration
            self.hit_angle = -90 * min(progress, 1)
            if progress >= 1:
                self.hitting = False

    def hit(self, current_time):
        self.hitting = True
        self.hit_time = current_time

    def draw(self, surface):
        # if self.hitting:
        #     rotated_image = pygame.transform.rotate(self.image, -45)
        # else:
        #     rotated_image = self.image
        # surface.blit(rotated_image, self.rect)
        rotated_image = pygame.transform.rotate(self.image, self.hit_angle)
        new_rect = rotated_image.get_rect(center=self.rect.center)
        surface.blit(rotated_image, new_rect.topleft)

class MoleWhackGame:
    def __init__(self, surface):
        self.surface = surface
        self.hand_tracking = Hand_tracking()
        self.hammer = Hammer()
        self.moles = []
        self.score = 0
        self.game_duration = 60  # 60秒のゲーム
        self.start_time = time.time()
        self.game_start_time = time.time()
        self.cap = cv2.VideoCapture(0)
        self.difficulty = 1
        self.game_state = "playing"

        # モグラの穴の位置を設定
        hole_positions = [
            (200, 150), (400, 150), (600, 150),
            (200, 300), (400, 300), (600, 300),
            (200, 450), (400, 450), (600, 450)
        ]
        for pos in hole_positions:
            self.moles.append(Mole(pos[0], pos[1]))

    def draw(self):
        self.surface.fill((0, 150, 0))  # 緑色の背景
        for mole in self.moles:
            mole.draw(self.surface)
        self.hammer.draw(self.surface)

        # スコアと残り時間の表示
        # font = pygame.font.Font(None, 36)
        # score_text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        # self.surface.blit(score_text, (10, 10))

        # time_left = max(0, self.game_duration - (time.time() - self.start_time))
        # time_text = font.render(f"Time: {int(time_left)}", True, (255, 255, 255))
        # self.surface.blit(time_text, (screen_width - 150, 10))
        draw_image.draw_text(self.surface, f"Score : {self.score}", (5, 5), COLORS["score"], font=FONT["medium"],
                    shadow=True, shadow_color=(255,255,255))
        # draw the time left
        timer_text_color = (160, 40, 0) if self.time_left < 5 else COLORS["timer"] # change the text color if less than 5 s left
        draw_image.draw_text(self.surface, f"Time left : {self.time_left}", (screen_width//2, 5),  timer_text_color, font=FONT["medium"],
                    shadow=True, shadow_color=(255,255,255))

    def reset(self):
        self.score = 0
        self.hand_tracking = Hand_tracking()
        self.hand = Hand()
        self.start_time = time.time()
        self.difficulty = 1
        for mole in self.moles:
            #mole.visible = False
            mole.state = "hidden"

    def game_time_update(self):
        self.time_left = max(round(dulation - (time.time() - self.game_start_time), 1), 0)

    def update(self):
        current_time = time.time()
        game_time = current_time - self.start_time
        self.game_time_update()
        # ハンドトラッキングの更新
        _,self.frame = self.cap.read()
        self.frame = cv2.flip(self.frame, 1)

        self.frame = self.hand_tracking.hand_tracking(self.frame)
        self.draw()

        if self.time_left > 0:
            x, y = self.hand_tracking.get_hand_center()
            self.hammer.update(x, y, current_time)

            if self.hand_tracking.hand_close:
                self.hammer.hit(current_time)
                for mole in self.moles:
                    # if mole.visible and self.hammer.rect.colliderect(mole.rect):
                    #     mole.visible = False
                    #     self.score += 1
                    if mole.state in ["visible", "appearing"] and self.hammer.rect.colliderect(mole.rect):
                        if mole.hit():
                            self.score += 1


            # モグラの更新
            # for mole in self.moles:
            #     mole.update(current_time)
            #     if not mole.visible and random.random() < 0.02:  # 2%の確率でモグラが出現
            #         mole.visible = True
            #         mole.appear_time = current_time
            active_moles = sum(1 for mole in self.moles if mole.state != "hidden")
            if active_moles < self.difficulty and random.random() < 0.02 * self.difficulty:
                hidden_moles = [mole for mole in self.moles if mole.state == "hidden"]
                if hidden_moles:
                    random.choice(hidden_moles).state = "appearing"

            for mole in self.moles:
                mole.update(current_time)

            # 難易度の更新
            self.difficulty = min(5, 1 + int(game_time / 10))  # 10秒ごとに難易度が上がる、最大5
        else:
            #return "game_over"
            if draw_image.button(self.surface, 320, "Continue"):
                self.reset()
                return "playing"
            if draw_image.button(self.surface, 320+button_size[1]*1.5, "Quit"):
                pygame.quit()
                sys.exit()

        #return "playing"
        cv2.imshow("Frame", self.frame)
        cv2.waitKey(1)
        

    def draw_menu(self):
        # メニュー画面の表示
        font = pygame.font.Font(None, 36)
        continue_button = font.render("Continue", True, (255, 255, 255))
        quit_button = font.render("Quit", True, (255, 255, 255))

        # 続けるボタン
        continue_rect = continue_button.get_rect(center=(400, 250))
        self.surface.blit(continue_button, continue_rect)

        # Quitボタン
        quit_rect = quit_button.get_rect(center=(400, 350))
        self.surface.blit(quit_button, quit_rect)

        # マウスクリック処理
        mouse_pos = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:
            if continue_rect.collidepoint(mouse_pos):
                self.game_state = "playing"  # ゲーム再開
            elif quit_rect.collidepoint(mouse_pos):
                pygame.quit()
                sys.exit()



def game_loop():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()

    mole_manager = MoleManager(5, 800, 600)
    running = True

    while running:
        screen.fill((255, 255, 255))
        current_time = time.time()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        mole_manager.update(current_time)
        mole_manager.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    game_loop()