# menu.py
import pygame
import settings

class GameMenu:
    def __init__(self, font_large, font_medium, font_small, bg_image):
        self.font_large = font_large
        self.font_medium = font_medium
        self.font_small = font_small
        self.bg_image = bg_image
        self.main_options = ["START GAME", "DIFFICULTY", "CONTROLS", "EXIT"]
        self.selected = 0
        self.show_controls = False
        self.show_difficulty = False
        self.difficulty_index = {"easy":0, "normal":1, "hard":2}[settings.difficulty]

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if self.show_controls:
                if event.key == pygame.K_ESCAPE:
                    self.show_controls = False
                return None
            elif self.show_difficulty:
                if event.key == pygame.K_UP:
                    self.difficulty_index = (self.difficulty_index - 1) % 3
                elif event.key == pygame.K_DOWN:
                    self.difficulty_index = (self.difficulty_index + 1) % 3
                elif event.key == pygame.K_RETURN:
                    settings.difficulty = ["easy", "normal", "hard"][self.difficulty_index]
                    self.show_difficulty = False
                elif event.key == pygame.K_ESCAPE:
                    self.show_difficulty = False
                return None
            else:
                if event.key == pygame.K_UP:
                    self.selected = (self.selected - 1) % len(self.main_options)
                elif event.key == pygame.K_DOWN:
                    self.selected = (self.selected + 1) % len(self.main_options)
                elif event.key == pygame.K_RETURN:
                    return self.selected
        return None

    def draw(self, surface):
        surface.blit(self.bg_image, (0, 0))
        overlay = pygame.Surface((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        overlay.set_alpha(100)
        overlay.fill(settings.BLACK)
        surface.blit(overlay, (0, 0))

        title = self.font_large.render("EMMA IN DANGER", True, settings.GOLD)
        surface.blit(title, (settings.SCREEN_WIDTH//2 - title.get_width()//2, 80))

        subtitle = self.font_small.render("Escape from the Haunted Forest", True, settings.WHITE)
        surface.blit(subtitle, (settings.SCREEN_WIDTH//2 - subtitle.get_width()//2, 140))

        if self.show_controls:
            self.draw_controls(surface)
        elif self.show_difficulty:
            self.draw_difficulty(surface)
        else:
            for i, opt in enumerate(self.main_options):
                color = settings.WHITE if i == self.selected else settings.GRAY
                text = self.font_medium.render(opt, True, color)
                surface.blit(text, (settings.SCREEN_WIDTH//2 - text.get_width()//2, 250 + i*60))
                if i == self.selected:
                    pygame.draw.polygon(surface, settings.WHITE,
                        [(settings.SCREEN_WIDTH//2 - 80, 270 + i*60),
                         (settings.SCREEN_WIDTH//2 - 100, 275 + i*60),
                         (settings.SCREEN_WIDTH//2 - 80, 280 + i*60)])
            diff_text = self.font_small.render(f"Current difficulty: {settings.difficulty.upper()}", True, settings.GREEN)
            surface.blit(diff_text, (settings.SCREEN_WIDTH//2 - diff_text.get_width()//2, 500))

    def draw_controls(self, surface):
        panel = pygame.Rect(settings.SCREEN_WIDTH//2 - 200, 150, 400, 300)
        pygame.draw.rect(surface, (30,30,30), panel)
        pygame.draw.rect(surface, settings.GOLD, panel, 3)
        title = self.font_medium.render("CONTROLS", True, settings.GOLD)
        surface.blit(title, (settings.SCREEN_WIDTH//2 - title.get_width()//2, 170))

        controls = [("← →", "Move"), ("SPACE", "Jump"), ("Z", "Shoot"), ("ESC", "Menu")]
        for i, (key, action) in enumerate(controls):
            key_text = self.font_small.render(key, True, settings.GREEN)
            action_text = self.font_small.render(action, True, settings.WHITE)
            surface.blit(key_text, (settings.SCREEN_WIDTH//2 - 120, 220 + i*40))
            surface.blit(action_text, (settings.SCREEN_WIDTH//2 + 20, 220 + i*40))

        back_text = self.font_small.render("Press ESC to return", True, settings.GRAY)
        surface.blit(back_text, (settings.SCREEN_WIDTH//2 - back_text.get_width()//2, 420))

    def draw_difficulty(self, surface):
        panel = pygame.Rect(settings.SCREEN_WIDTH//2 - 200, 150, 400, 300)
        pygame.draw.rect(surface, (30,30,30), panel)
        pygame.draw.rect(surface, settings.GOLD, panel, 3)
        title = self.font_medium.render("DIFFICULTY", True, settings.GOLD)
        surface.blit(title, (settings.SCREEN_WIDTH//2 - title.get_width()//2, 170))

        diffs = ["EASY", "NORMAL", "HARD"]
        for i, d in enumerate(diffs):
            color = settings.GREEN if i == self.difficulty_index else settings.GRAY
            text = self.font_medium.render(d, True, color)
            surface.blit(text, (settings.SCREEN_WIDTH//2 - text.get_width()//2, 240 + i*50))

        hint = self.font_small.render("Press ENTER to select, ESC to cancel", True, settings.GRAY)
        surface.blit(hint, (settings.SCREEN_WIDTH//2 - hint.get_width()//2, 420))