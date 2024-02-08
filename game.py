import pygame
import random
import os
import torch
from PIL import Image
import shutil  
import numpy as np

def predict_number(truth,image_path,model_path='demo.pth')->bool:
    '''
    truth: int, the truth of the image
    model_path: str, the path of the model
    image_path: str, the path of the image 
    return: bool, if true, the prediction is correct, otherwise, the prediction is wrong
    '''
    model = torch.jit.load(model_path)
    model.eval()
    image = Image.open(image_path)
    # preprocess the image
    image = image.resize((28,28))
    image = image.convert('L')
    image = torch.tensor(np.array(image),dtype=torch.float32)
    image = image / 255
    image = image.view(1,1,28,28)
    # predict the number
    prediction = model(image)
    prediction = torch.argmax(prediction)
    # print(prediction,truth)
    return prediction.item() == truth
    
if os.path.exists('screenshots'):
    shutil.rmtree('screenshots')
os.makedirs('screenshots')

pygame.init()
# settint some variables
white = (255,255,255)
black = (0,0,0)
window_width = 560
window_height = 610
font_size = 30
countdown = 5 * 1000
# create some objects for future use
font = pygame.font.Font(None, font_size) # create a font object
font.set_bold(False) # make the font bold
window = pygame.display.set_mode((window_width, window_height)) # create a window
pygame.display.set_caption("MNIST Game") # set the title of the window

# initialize the window
window.fill((0,0,0)) # fill the window with black color
pygame.draw.line(window, white, (0, window_height-window_width-1), (window_width, window_height-window_width-1), 1) # draw a line to separate the top bar
start_ticks = pygame.time.get_ticks() # starter tick
number = random.randint(0,9) # get a random number
drawing = False
total_quest = 5
quest = 1
correct = 0

# game part
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            drawing = True
        elif event.type == pygame.MOUSEBUTTONUP:
            drawing = False

    elapsed_time = pygame.time.get_ticks() - start_ticks
    remaining_time = countdown - elapsed_time
    # calculate remaining seconds
    seconds = remaining_time // 1000

    if remaining_time > 0:
        timer_text = font.render("Seconds left {}".format(int(seconds)), True, white)
        number_text = font.render("Please draw {}".format(number), True, white)
        if drawing:
            pygame.draw.circle(window, (255,255,255), pygame.mouse.get_pos(), radius = 20)
    else:
        seconds = 0        
        screenshot_area = pygame.Rect(0,window_height-window_width,window_width,window_width) # Define the area of the screenshot
        screenshot = window.subsurface(screenshot_area) # Capture a screenshot of the specific section
        pygame.image.save(screenshot, os.path.join('screenshots', 'screenshot_{}.png'.format(quest))) # Save the screenshot
        correct += predict_number(number,os.path.join('screenshots', 'screenshot_{}.png'.format(quest)))
        start_ticks = pygame.time.get_ticks() # reset the timer
        number = random.randint(0,9) # reset the number
        quest += 1
        # initialize the window
        window.fill((0,0,0)) # fill the window with black color
        pygame.draw.line(window, white, (0, window_height-window_width-1), (window_width, window_height-window_width-1), 1) # draw a line to separate the top bar

    # set the place of the text
    timer_text_rect = timer_text.get_rect(topright = (window_width,0))
    number_text_rect = number_text.get_rect(topleft = (0,0))
    # remoove the top bar
    fill_ract = (0,0,window_width,window_height-window_width-1)
    window.fill(black, fill_ract)
    # draw the text
    window.blit(timer_text, timer_text_rect)
    window.blit(number_text, number_text_rect)
    #update the window
    pygame.display.update()
    
    # check if the game is over
    if quest == total_quest + 1:
        window.fill(black)
        finish_text = font.render("You get {} out of {}".format(correct,total_quest), True, white)
        finish_text_rect = finish_text.get_rect(center = (window_width/2, window_height/2))
        window.blit(finish_text, finish_text_rect)
        pygame.display.update()
        pygame.time.wait(2000)
        pygame.quit()
        quit()

