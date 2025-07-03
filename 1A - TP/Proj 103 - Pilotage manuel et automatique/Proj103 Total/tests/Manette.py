import pygame  
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

def manette():
    pygame.joystick.init()
    joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
    options = webdriver.ChromeOptions() 
    options.add_argument("--disable-blink-features=AutomationControlled") 
    options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
    options.add_experimental_option("useAutomationExtension", False)
    driver = webdriver.Chrome(options=options) 
    driver.execute_cdp_cmd("Network.setUserAgentOverride", {"userAgent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 OPR/105.0.0.0"})
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    driver.get("http://localhost:8000") #L'URL en question du webserver
    wait = WebDriverWait(driver, 10)
    try:
        span_element = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="axeptio_btn_acceptAll"]')))
        time.sleep(1)
        span_element.click()
    except TimeoutException:
        pass
    except NoSuchElementException:
        pass

"""
class Player(object):
    
    def __init__(self):
        self.player = pygame.rect.Rect((300, 400, 30, 30))
        self.color = "white"
        
    def move(self, x_speed, y_speed):
        self.player.move_ip((x_speed,y_speed))
        
    def change_color(self, color):
        self.color = color
        
    def draw(self, game_screen):
        pygame.draw.rect(game_screen, self.color, self.player)
        
pygame.init()

player = Player()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((800,600))

while(True):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            break
        if event.type == pygame.JOYBUTTONDOWN:
            if pygame.joystick.Joystick(0).get_button(0):
                player.change_color("Blue")
            elif pygame.joystick.Joystick(0).get_button(1):
                player.change_color("Red")
            elif pygame.joystick.Joystick(0).get_button(2):
                player.change_color("Yellow")
            elif pygame.joystick.Joystick(0).get_button(3):
                player.change_color("Green")
                
    x_speed = round(pygame.joystick.Joystick(0).get_axis(0))
    y_speed = round(pygame.joystick.Joystick(0).get_axis(1))
    player.move(x_speed,y_speed)
    screen.fill((0, 0, 0))
    player.draw(screen)
    pygame.display.update()
    clock.tick(100)"""