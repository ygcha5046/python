import pygame
import random
import sys
import os

# 초기화
pygame.init()
pygame.mixer.init()

# 화면 설정
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("사이버펑크 RPG")

# 폰트 설정
font = pygame.font.Font("D:/온글잎 이빈나.ttf", 36)

# 색깔
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 150, 255)

# 배경 이미지 로드
background_path = "E:/cyberpunk_background.jpg"
if os.path.exists(background_path):
    background_img = pygame.image.load(background_path)
    background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))
else:
    background_img = None

# 배경 음악 재생
music_path = "E:/cyberpunk_bgm.mp3"
if os.path.exists(music_path):
    pygame.mixer.music.load(music_path)
    pygame.mixer.music.play(-1)  # 무한반복
else:
    print("배경 음악 파일이 없습니다!")

# 버튼 클래스
class Button:
    def __init__(self, text, x, y, width, height, callback=None):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.callback = callback

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, self.rect, 2)
        text_surf = font.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# 캐릭터 클래스
class Character:
    def __init__(self, name, role):
        self.name = name
        self.role = role
        self.hp = 100
        self.max_hp = 100
        self.level = 1
        self.attack_power = self.set_attack_power()
        self.items = []

    def set_attack_power(self):
        if self.role == "해커":
            return 8
        elif self.role == "용병":
            return 12
        elif self.role == "경찰":
            return 10
        elif self.role == "도둑":
            return 9
        else:
            return 5

    def attack(self, enemy, critical=False):
        base_damage = random.randint(self.attack_power - 2, self.attack_power + 2)
        if critical:
            base_damage *= 2
        enemy.hp -= base_damage
        return base_damage

    def heal(self):
        if "체력 포션" in self.items:
            self.hp = min(self.hp + 50, self.max_hp)
            self.items.remove("체력 포션")
            return True
        return False

    def buff_attack(self):
        if "공격력 증가 칩셋" in self.items:
            self.attack_power += 5
            self.items.remove("공격력 증가 칩셋")
            return True
        return False

# 적 클래스
class Enemy:
    def __init__(self, name, hp, attack_power):
        self.name = name
        self.hp = hp
        self.attack_power = attack_power

    def attack(self, player):
        if random.random() < 0.2:
            return 0
        damage = random.randint(self.attack_power - 2, self.attack_power + 2)
        player.hp -= damage
        return damage

# 텍스트 출력 함수
def draw_text(text, x, y, color=WHITE):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

# 적 리스트
def get_random_enemy(player_level):
    if player_level >= 5 and random.random() < 0.3:
        return Enemy("보스: 네온 파라오", 150 + player_level * 10, 18 + player_level // 2)
    else:
        enemies = [
            Enemy("경비 드론", 50 + player_level * 5, 8 + player_level),
            Enemy("사이버 암살자", 70 + player_level * 7, 10 + player_level),
            Enemy("악덕 경찰", 80 + player_level * 6, 12 + player_level)
        ]
        return random.choice(enemies)

# 보상 리스트
def get_random_reward():
    return random.choice(["체력 포션", "공격력 증가 칩셋", "방어구 강화"])

# 게임 메인 함수
def game():
    clock = pygame.time.Clock()

    player = Character("플레이어", "해커")
    enemy = get_random_enemy(player.level)

    attack_button = Button("공격하기", 50, 500, 150, 50)
    skill_button = Button("강력 공격", 250, 500, 150, 50)
    item_button = Button("아이템 사용", 450, 500, 150, 50)
    run_button = Button("도망가기", 650, 500, 100, 50)

    message = "전투 시작!"

    running = True
    while running:
        # 배경 설정
        if background_img:
            screen.blit(background_img, (0, 0))
        else:
            screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if attack_button.is_clicked(pos):
                    crit = random.random() < 0.2
                    damage = player.attack(enemy, critical=crit)
                    if crit:
                        message = f"💥 크리티컬! {damage} 데미지!"
                    else:
                        message = f"플레이어가 {enemy.name}에게 {damage} 데미지를 줬다!"
                    if enemy.hp > 0:
                        edamage = enemy.attack(player)
                        if edamage == 0:
                            message += f" {enemy.name}의 공격이 빗나갔다!"
                        else:
                            message += f" {enemy.name}이(가) {player.name}에게 {edamage} 데미지를 줬다!"
                if skill_button.is_clicked(pos):
                    damage = player.attack(enemy, critical=True)
                    message = f"⚡ 강력 공격! {enemy.name}에게 {damage} 데미지!"
                    if enemy.hp > 0:
                        edamage = enemy.attack(player)
                        if edamage == 0:
                            message += f" {enemy.name}의 공격이 빗나갔다!"
                        else:
                            message += f" {enemy.name}이(가) {player.name}에게 {edamage} 데미지를 줬다!"
                if item_button.is_clicked(pos):
                    if player.heal():
                        message = "🧪 체력 포션 사용! 체력 회복!"
                    elif player.buff_attack():
                        message = "🔧 공격력 증가 칩셋 사용! 공격력 상승!"
                    else:
                        message = "❗ 사용 가능한 아이템이 없습니다!"
                if run_button.is_clicked(pos):
                    message = "플레이어가 도망쳤습니다!"
                    running = False

        # 체력 및 레벨 출력
        draw_text(f"{player.name} HP: {player.hp}/{player.max_hp}  LV: {player.level}", 50, 50)
        draw_text(f"{enemy.name} HP: {enemy.hp}", 50, 100)

        # 아이템 출력
        draw_text(f"아이템: {', '.join(player.items) if player.items else '없음'}", 50, 150, BLUE)

        # 메시지 출력
        draw_text(message, 50, 300, YELLOW)

        # 버튼 출력
        attack_button.draw(screen)
        skill_button.draw(screen)
        item_button.draw(screen)
        run_button.draw(screen)

        # 승리/패배 판정
        if player.hp <= 0:
            message = "☠️ 플레이어가 쓰러졌습니다... 게임 오버"
            screen.fill(BLACK)
            draw_text(message, 150, 300, RED)
            pygame.display.update()
            pygame.time.delay(3000)
            running = False
        elif enemy.hp <= 0:
            if player.level >= 100:
                message = "🎉 축하합니다! 100레벨 달성! 사이버 세상의 지배자가 되었습니다!"
                screen.fill(BLACK)
                draw_text(message, 50, 250, GREEN)
                pygame.display.update()
                pygame.time.delay(5000)
                running = False
            else:
                reward = get_random_reward()
                player.items.append(reward)
                player.level += 1
                player.max_hp += 10
                player.hp = player.max_hp
                message = f"🏆 {enemy.name} 격파! 보상: {reward} 획득!"
                pygame.display.update()
                pygame.time.delay(2000)
                enemy = get_random_enemy(player.level)
                message = f"{enemy.name} 등장! 준비하세요!"

        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    game()
