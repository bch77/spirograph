#to do: add "res +/-" button

import pygame
import random
import math
import time

pygame.init()

# Set up the display
screen_width = 1200
screen_height = 1200
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Spirograph")

# Set up the clock
clock = pygame.time.Clock()
pygame.key.set_repeat(300, 10)

try:
    font = pygame.font.SysFont('Courier', 14, True)
except:
    font = pygame.font.Font(None,14)
    
input_text = ""
screen_copy_alpha = 255
clear_flag = False
value_changed_flag =  False
stop_flag = False


# Set up the colors 
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
light_blue = (0, 128, 255)
gray = (50, 50, 50)
yellow = (255, 255, 0)
magenta = (255, 0, 255)
bright_blue = (128, 192, 255)
bright_green = (160, 255, 64)
bright_red = (255, 160, 160)
bright_yellow = (255, 255, 192)

level_colors = (light_blue, green, red, yellow, gray)
level_button_colors = (bright_blue, bright_green, bright_red, bright_yellow)




def safe_float(text):
    i = len(text)
    j = i
    value = 0
    while j > 0:
        try:
            str = text[:j]
            if str == "-" or str == ".":
                str = "0"
            value = float(str)
            return value
        except ValueError as e:
            j -= 1

class TextBox(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, text, active):
        super().__init__()
        self.color = (255, 255, 255)
        self.rect = pygame.Rect(x, y, w, h)
        self.font = font
        self.text = text
        self.selected = False
        self.text_selected = False
        self.selection_start = 0
        self.selection_end = len(self.text)
        self.cursor_pos = len(self.text)
        self.blink_counter = 0
        self.active = active
        self.update()

    def update(self):
        self.image = pygame.Surface((self.rect.width, self.rect.height))
        self.image.fill(self.color)
        self.image.set_alpha(255)
               
        if self.selected:
            if self.text_selected:
                if self.selection_start < self.selection_end:
                    size_of_selection = self.font.size(self.text[self.selection_start:self.selection_end])
                    size_before_selection = self.font.size(self.text[:self.selection_start])
                    selection_rect = pygame.Rect(size_before_selection[0], 2, size_of_selection[0]+4, self.rect.height-8)
                    pygame.draw.rect(self.image, magenta, selection_rect)
            else:
                self.blink_counter += 1
            
                cursor_x = self.font.size(self.text[:self.cursor_pos])[0]
                if self.blink_counter % 120 < 60:
                    pygame.draw.line(self.image, (0, 0, 0), (cursor_x, 6), (cursor_x, self.rect.height - 6), 2)
            
        rendered_text = self.font.render(self.text, True, (0, 0, 0))            
        self.image.blit(rendered_text, (2, (self.rect.height - rendered_text.get_height()) // 2))
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                if self.selected == False:
                    self.text_selected = True
                self.selected = True
                self.selection_start = 0
                self.selection_end = len(self.text)
                self.cursor_pos = self.selection_end
                self.update()
            else:
                self.selected = False
                self.update()

        if self.selection_start == self.selection_end:
            self.text_selected = False
        
        if self.selected and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DELETE or event.key == pygame.K_BACKSPACE:
                if self.text_selected:
                    self.text = self.text[:self.selection_start] + self.text[self.selection_end:]
                    self.cursor_pos = self.selection_start
                    self.text_selected = False
                else:
                    if event.key == pygame.K_DELETE:
                        if self.cursor_pos < len(self.text):
                            self.text = self.text[:self.cursor_pos] + self.text[self.cursor_pos + 1:]
                            self.cursor_pos = 0
                    elif event.key == pygame.K_BACKSPACE and self.cursor_pos > 0:
                        if self.cursor_pos > 0:
                            self.text = self.text[:self.cursor_pos-1] + self.text[self.cursor_pos:]
                            self.cursor_pos -= 1
                       
            elif event.key == pygame.K_LEFT:
                if self.text_selected == True:
                    self.cursor_pos = 0
                self.text_selected = False
                if self.cursor_pos > 0:
                    self.cursor_pos -= 1
            elif event.key == pygame.K_RIGHT:
                self.text_selected = False
                if self.cursor_pos < len(self.text):
                    self.cursor_pos += 1
            else:
                if event.unicode.isdigit() or event.unicode in {'.', '-'}:
                    if self.text_selected == False:
                        self.text = self.text[:self.cursor_pos] + event.unicode + self.text[self.cursor_pos:]
                        self.cursor_pos += len(event.unicode)
                    else: 
                        self.text = event.unicode
                        self.text_selected == False
                        self.cursor_pos = len(event.unicode)
                    self.selection_start = self.cursor_pos
                    self.selection_end = self.cursor_pos
            self.update()
            
    def get_text(self):
        return self.text
        
    def set_text(self, text): 
        self.text = text
        
    def get_status(self):
        return self.selected
        
    def set_status(self, status):
        self.selected = status
        
    def set_color(self, color):
        self.color = color


# ===================================== end TextBox definition =====================================


            
class OrbitingObject:
    def __init__(self, x, y, radius1, speed1, angle1):
        if x == 0:
            self.reset_random()
        else:
            self.reset(x, y, radius1, speed1, angle1)

        
    def setotherattributes(self):
        self.kill = False
        self.obj_radius = 2 
        self.radius2 = 100
        self.radius3 = 100
        self.radius4 = 100
        self.speed2 = 3
        self.speed3 = 3
        self.speed4 = 3
        self.angle2 = 0
        self.angle3 = 0
        self.angle4 = 0
        self.radius1_inc = 0
        self.radius2_inc = 0
        self.radius3_inc = 0
        self.radius4_inc = 0
        self.speed1_inc = 0
        self.speed2_inc = 0
        self.speed3_inc = 0
        self.speed4_inc = 0
        self.angle1_inc = 0
        self.angle2_inc = 0
        self.angle3_inc = 0
        self.angle4_inc = 0
        
        
    def setpoint(self):
        if self.levels == 1:
            self.x = self.center_x + int(self.radius1 * math.cos(math.radians(self.angle1)))
            self.y = self.center_y + int(self.radius1 * math.sin(math.radians(self.angle1)))
        elif self.levels == 2:
            self.x = self.center_x + int(self.radius1 * math.cos(math.radians(self.angle1)) + self.radius2 * math.cos(math.radians(self.angle2)))
            self.y = self.center_y + int(self.radius1 * math.sin(math.radians(self.angle1)) + self.radius2 * math.sin(math.radians(self.angle2)))   
        elif self.levels ==3:
            self.x = self.center_x + int(self.radius1 * math.cos(math.radians(self.angle1)) + self.radius2 * math.cos(math.radians(self.angle2)) + self.radius3 * math.cos(math.radians(self.angle3)))
            self.y = self.center_y + int(self.radius1 * math.sin(math.radians(self.angle1)) + self.radius2 * math.sin(math.radians(self.angle2)) + self.radius3 * math.sin(math.radians(self.angle3)))
        else: # self.levels ==4:
            self.x = self.center_x + int(self.radius1 * math.cos(math.radians(self.angle1)) + self.radius2 * math.cos(math.radians(self.angle2)) + self.radius3 * math.cos(math.radians(self.angle3)) + self.radius4 * math.cos(math.radians(self.angle4)))
            self.y = self.center_y + int(self.radius1 * math.sin(math.radians(self.angle1)) + self.radius2 * math.sin(math.radians(self.angle2)) + self.radius3 * math.sin(math.radians(self.angle3)) + self.radius4 * math.sin(math.radians(self.angle4)))       

    def reset_random(self):
        self.speed1 = random.uniform(-5, 5)
        self.radius1 = random.randint(30, 150)
        self.setotherattributes()
        self.levels = random.choice([1,2,3])
        margin = self.radius1 + self.obj_radius + 2
        self.center_x = random.randint(margin, screen_width-margin)
        self.center_y = random.randint(margin, screen_height-margin)
        self.angle1 = random.randint(0, 360)
        self.setpoint()
        self.oldpos = (self.x, self.y)
    
    def reset(self, x, y, radius1, speed1, angle1):
        self.speed1 = speed1
        self.radius1 = radius1
        self.setotherattributes()
        self.levels = 1
        self.obj_radius=random.randint(5, 15)
        self.center_x = x
        self.center_y = y
        self.angle1 = 0
        self.setpoint()
        
    def reset_default(self):
        self.speed1 = 3
        self.radius1 = 100
        self.angle1 = 0
        self.setotherattributes()
        self.setpoint()
        self.update_fields_from_values()
    
    def update(self):
        self.angle1 = (self.angle1 + self.speed1) % 360
        self.angle2 = (self.angle2 + self.speed2) % 360
        self.angle3 = (self.angle3 + self.speed3) % 360
        self.angle4 = (self.angle4 + self.speed4) % 360
        self.oldpos = (self.x, self.y)
        if self.levels == 1:
            self.x = self.center_x + int(self.radius1 * math.cos(math.radians(self.angle1)))
            self.y = self.center_y + int(self.radius1 * math.sin(math.radians(self.angle1)))
        elif self.levels == 2:
            self.x = self.center_x + int(self.radius1 * math.cos(math.radians(self.angle1)) + self.radius2 * math.cos(math.radians(self.angle2)))
            self.y = self.center_y + int(self.radius1 * math.sin(math.radians(self.angle1)) + self.radius2 * math.sin(math.radians(self.angle2)))   
        elif self.levels ==3:
            self.x = self.center_x + int(self.radius1 * math.cos(math.radians(self.angle1)) + self.radius2 * math.cos(math.radians(self.angle2)) + self.radius3 * math.cos(math.radians(self.angle3)))
            self.y = self.center_y + int(self.radius1 * math.sin(math.radians(self.angle1)) + self.radius2 * math.sin(math.radians(self.angle2)) + self.radius3 * math.sin(math.radians(self.angle3)))
        else: # self.levels ==4:
            self.x = self.center_x + int(self.radius1 * math.cos(math.radians(self.angle1)) + self.radius2 * math.cos(math.radians(self.angle2)) + self.radius3 * math.cos(math.radians(self.angle3)) + self.radius4 * math.cos(math.radians(self.angle4)))
            self.y = self.center_y + int(self.radius1 * math.sin(math.radians(self.angle1)) + self.radius2 * math.sin(math.radians(self.angle2)) + self.radius3 * math.sin(math.radians(self.angle3)) + self.radius4 * math.sin(math.radians(self.angle4)))
        if value_changed_flag == True:
            self.oldpos = (self.x, self.y)
        
    def update_values_from_fields(self):
        for i, field in enumerate(fields):
            if field.text == "-" or field.text == "":
                fields[i].text = "0"
        self.speed1 = safe_float(fields[0].get_text())
        self.speed2 = safe_float(fields[1].get_text())
        self.speed3 = safe_float(fields[2].get_text())
        self.speed4 = safe_float(fields[3].get_text()) 
        self.radius1 = safe_float(fields[4].get_text())    
        self.radius2 = safe_float(fields[5].get_text())
        self.radius3 = safe_float(fields[6].get_text())
        self.radius4 = safe_float(fields[7].get_text())
        self.angle1 = safe_float(fields[8].get_text())
        self.angle2 = safe_float(fields[9].get_text())
        self.angle3 = safe_float(fields[10].get_text())
        self.angle4 = safe_float(fields[11].get_text())
        self.speed1_inc = safe_float(fields[12].get_text())
        self.radius1_inc = safe_float(fields[13].get_text())
        self.angle1_inc = safe_float(fields[14].get_text())
        self.speed2_inc = safe_float(fields[15].get_text())
        self.radius2_inc = safe_float(fields[16].get_text())
        self.angle2_inc = safe_float(fields[17].get_text())
        self.speed3_inc = safe_float(fields[18].get_text())
        self.radius3_inc = safe_float(fields[19].get_text())
        self.angle3_inc = safe_float(fields[20].get_text())
        self.speed4_inc = safe_float(fields[21].get_text()) 
        self.radius4_inc = safe_float(fields[22].get_text()) 
        self.angle4_inc = safe_float(fields[23].get_text())

    def update_fields_from_values(self):
        fields[0].set_text(str(round(spirograph_object.speed1,3)))
        fields[1].set_text(str(round(spirograph_object.speed2,3))) 
        fields[2].set_text(str(round(spirograph_object.speed3,3)))
        fields[3].set_text(str(round(spirograph_object.speed4,3)))
        fields[4].set_text(str(round(spirograph_object.radius1,3)))      
        fields[5].set_text(str(round(spirograph_object.radius2,3)))
        fields[6].set_text(str(round(spirograph_object.radius3,3)))
        fields[7].set_text(str(round(spirograph_object.radius4,3))) 
        fields[8].set_text(str(round(spirograph_object.angle1,3)))      
        fields[9].set_text(str(round(spirograph_object.angle2,3)))
        fields[10].set_text(str(round(spirograph_object.angle3,3)))
        fields[11].set_text(str(round(spirograph_object.angle4,3)))
        fields[12].set_text(str(round(spirograph_object.speed1_inc,3)))
        fields[13].set_text(str(round(spirograph_object.radius1_inc,3)))
        fields[14].set_text(str(round(spirograph_object.angle1_inc,3)))
        fields[15].set_text(str(round(spirograph_object.speed2_inc,3)))
        fields[16].set_text(str(round(spirograph_object.radius2_inc,3)))
        fields[17].set_text(str(round(spirograph_object.angle2_inc,3)))
        fields[18].set_text(str(round(spirograph_object.speed3_inc,3)))
        fields[19].set_text(str(round(spirograph_object.radius3_inc,3)))
        fields[20].set_text(str(round(spirograph_object.angle3_inc,3)))
        fields[21].set_text(str(round(spirograph_object.speed4_inc,3)))
        fields[22].set_text(str(round(spirograph_object.radius4_inc,3)))
        fields[23].set_text(str(round(spirograph_object.angle4_inc,3)))

    def auto_increment(self):
        self.speed1 += self.speed1_inc
        self.speed2 += self.speed2_inc
        self.speed3 += self.speed3_inc
        self.speed4 += self.speed4_inc
        self.radius1 += self.radius1_inc
        self.radius2 += self.radius2_inc
        self.radius3 += self.radius3_inc
        self.radius4 += self.radius4_inc
        self.angle1 += self.angle1_inc
        self.angle2 += self.angle2_inc
        self.angle3 += self.angle3_inc
        self.angle4 += self.angle4_inc
        cp.px += color_vector
        cp.px = cp.px % 360

    def change_speed(self, factor):
        self.speed1 *= factor
        self.speed2 *= factor
        self.speed3 *= factor
        self.speed4 *= factor
        
                       
    def draw(self):
        #pygame.draw.circle(screen, red, (self.x, self.y), self.obj_radius)
        if (self.x - (self.obj_radius + 1) > 0) and (self.x + (self.obj_radius + 1) < screen_width) and (self.y - (self.obj_radius + 1) > 0) and (self.y + (self.obj_radius + 1) < screen_height):
            pygame.draw.circle(screen, light_blue, (self.x, self.y), self.obj_radius+1)
            pygame.draw.circle(screen, self.color, (self.x, self.y), self.obj_radius)
            #draw center point
            # pygame.draw.circle(screen, gray, (self.center_x, self.center_y), 2)
        else:
            self.kill = True
            
# ===================================== end OrbitingObject definition =====================================            



class ColorPicker:
    def __init__(self, x, y):
        self.width = color_picker_width   
        self.height = color_picker_height   # in this example we're using 10 degrees of luminance at 3 pixels high each
        self.thumbsize = 20
        self.location = (x,y)
        self.border = color_picker_border
        self.bgrect = pygame.Rect(x,y, self.width + 2 * self.border, self.height + 2 * self.border)
        self.rect = pygame.Rect(x + self.border, y + self.border, self.width, self.height)

        self.image = pygame.Surface((self.width + 2 * self.border, self.height + 2 * self.border))
        self.image.fill((255, 255, 255))

        for j in range(10):  
            for i in range(self.width):
                color = pygame.Color(0)
                color.hsla = (i, 100, 10*j + 10, 100)
                pygame.draw.rect(self.image, color, (i + self.border, 3 * j + self.border, 1, 3))
        self.px = 200
        self.py = 15

    def get_color(self):
        color = pygame.Color(255)
        color.hsla = (int(self.px), 100, int(self.py/3 * 10), 100)
        return color

    def update(self):
        mouse_buttons = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        if mouse_buttons[0] and self.bgrect.collidepoint(mouse_pos):
            self.px = mouse_pos[0] - self.location[0] - self.border
            self.py = mouse_pos[1] - self.location[1] - self.border
            self.px = (max(0, min(self.px, 360)))
            self.py = (max(0, min(self.py, 30)))

    def draw(self, surf):
        surf.blit(self.image, self.location)
        therect = (self.px + self.location[0] + self.border-self.thumbsize / 2,self.py + self.location[1] + self.border-self.thumbsize / 2, self.thumbsize, self.thumbsize)
        pygame.draw.rect(surf, self.get_color(), pygame.Rect(therect), 0, 4)
        pygame.draw.rect(surf, black, pygame.Rect(therect), 1, 4)

# ===================================== end ColorPicker definition ====================================


# Set up the UI

# UI constants
num_fields = 25
field_width = 60
field_height = 32
shorter_field_difference = 12
field_spacing = 8
field_offset_x = 10
field_offset_y = 20

button_height = 20
button_width = 28
button_spacing = 6
other_button_width = field_width + 8
other_button_height = field_height + 6

lbutton_width = field_width - 2
lbutton_height = 5
lbutton_spacing = field_spacing + 2
lbutton_offset_x = field_offset_x + 1
lbutton_offset_y = field_height + field_offset_y - lbutton_height - 1
lbuttons = []

fields = []
textlabels = []
speed_field = 12
radius_field = 13
angle_field = 14
color_vector = 2
color_picker_width = 360  # 360 degrees of hue
color_picker_height = 30
color_picker_border = 4

color_picker_yloc = field_offset_y + field_height + field_spacing + button_height + button_spacing  
last_buttons_start_x = color_picker_width + 2 * color_picker_border + field_spacing


labeltexts = ("--------------SPEED--------------","--------------RADIUS-------------","--------------ANGLE-------------","---INCREMENTS (S,R,A)---", "RESOL.")

for i in range(4):
    text_rect = pygame.Rect(field_offset_x + (field_width + field_spacing) * 4 * i,
                             0,
                             field_width + field_spacing * 4,
                             20)
    textlabels.append((text_rect, labeltexts[i])) 
text_rect = (pygame.Rect(last_buttons_start_x + 5*(other_button_width + field_spacing) + 5, color_picker_yloc, other_button_width, other_button_height)) 
textlabels.append((text_rect, labeltexts[4])) 

for i in range(12):   #  the second set of 12 fields are different
    field_rect = pygame.Rect(field_offset_x + (field_width + field_spacing) * i,
                             field_offset_y,
                             field_width,
                             field_height)
    field_text = "1"
    field_active = False
    fields.append(TextBox(field_rect[0], field_rect[1], field_rect[2], field_rect[3], field_text, field_active))
    
    
for i in range(12):
    field_rect = pygame.Rect(field_offset_x + (field_width + field_spacing) * (12 + (i % 3)),
                             field_offset_y + (field_height - shorter_field_difference + field_spacing) * (i // 3) ,
                             field_width,
                             field_height - shorter_field_difference) 
    field_text = "1"
    field_active = False
    fields.append(TextBox(field_rect[0], field_rect[1], field_rect[2], field_rect[3], field_text, field_active)) 



    
for i in range(1): #color vector field
    field_rect = pygame.Rect(last_buttons_start_x, color_picker_yloc, field_width, field_height - shorter_field_difference)
    field_text = "2"
    field_active = False
    fields.append(TextBox(field_rect[0], field_rect[1], field_rect[2], field_rect[3], field_text, field_active))
    
                      

# set up the increment/decrement buttons
button_offset_x = 10
button_offset_y = field_offset_y + field_height + button_spacing
buttons = []
for i in range(24):
    button_rect = pygame.Rect(button_offset_x + (button_width + button_spacing) * i,
                              button_offset_y,
                              button_width,
                              button_height)
    if i%2 == 0:
        button_text = " -"
    else:
        button_text = " +"
    buttons.append((button_rect, button_text))
    
                        
    
# set up color increment button

buttons.append((pygame.Rect(last_buttons_start_x, color_picker_yloc + 18, field_width, field_height - shorter_field_difference), "COLOR>"))

#setup Auto button
buttons.append((pygame.Rect(last_buttons_start_x + other_button_width + field_spacing, color_picker_yloc, other_button_width + 5, other_button_height), "AUTO INC"))

#setup Reset Button
buttons.append((pygame.Rect(last_buttons_start_x + 2*(other_button_width + field_spacing) +5, color_picker_yloc, other_button_width, other_button_height), " RESET"))

#setup Clear Button
buttons.append((pygame.Rect(last_buttons_start_x + 3*(other_button_width + field_spacing) + 5, color_picker_yloc, other_button_width, other_button_height), " CLEAR"))

#setup Stop/Start Button
buttons.append((pygame.Rect(last_buttons_start_x + 4*(other_button_width + field_spacing) + 5, color_picker_yloc, other_button_width, other_button_height), " ||/>"))

#inc/dec buttons for resolution:
for i in range(2):
    button_rect = pygame.Rect(last_buttons_start_x + 5* (other_button_width + field_spacing) + 5 + i * (button_width + button_spacing) - 3,
                              color_picker_yloc + 18, 
                              button_width,
                              button_height) 
    if i%2 == 0:
        button_text = " -"
    else:
        button_text = " +" 
    buttons.append((button_rect, button_text))    
# set up the level buttons

for i in range(12):
    lbutton_rect = pygame.Rect(lbutton_offset_x + (lbutton_width + lbutton_spacing) * i,
                               lbutton_offset_y, lbutton_width, lbutton_height)

    lbutton_active = (i % 4 == 0)
    lbuttons.append((lbutton_rect, lbutton_active))
    
        

# set up the trail
trail_color = (0, 0, 0)
trail_alpha = 32
trail_surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA, trail_alpha)
trail_surface.fill((0, 0, 0, trail_alpha), special_flags=pygame.BLEND_RGBA_MULT)


spirograph_object = OrbitingObject(screen_width // 2, screen_height // 2, 100, 3, 0)

spirograph_object.obj_radius = 2
spirograph_object.color = blue
spirograph_object.levels = 1

#initialize text fields:
spirograph_object.update_fields_from_values()

# set initial values for increment fields - NOTE: reset clears them to 0
for i, field in enumerate(fields):
    if i >= 12:
        j = i % 3
        match (j):
            case 0:
                field.set_text(str(round(.1,3)))
            case 1:
                field.set_text(str(round(10,3)))
            case 2:
                field.set_text(str(round(5,3)))
        if i == 24:
            field.set_text(str(round(2, 3)))

cp = ColorPicker(field_offset_x, color_picker_yloc)

sprites = pygame.sprite.Group()  
for i in range(25):
    sprites.add(fields[i]) 

# Main loop
running = True
while running:
    # Handle events
    a_field_is_selected = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # check if a field was clicked
            for i, field in enumerate(fields):
                field.handle_event(event)
                a_field_is_selected = field.selected
                
            # check if a button was clicked
            for j, button in enumerate(buttons):
                if button[0].collidepoint(event.pos):
                    # update the field values based on the last 2 fields
                    value_changed_flag =  True
                    if j%2 == 0: # -
                        i = j//2
                        if j < 8:   
                            try:
                                delta = safe_float(fields[speed_field + (i%4) * 3].get_text())
                                fields[i].set_text(str(round(safe_float(fields[i].get_text()) - delta,3)))
                            except ValueError:
                                pass
                        elif j < 16:
                            try:
                                delta = safe_float(fields[radius_field  + (i%4) * 3].get_text())
                                fields[i].set_text(str(round(safe_float(fields[i].get_text()) - delta,3)))
                            except ValueError:
                                pass
                        elif j < 24:
                            try:
                                delta = safe_float(fields[angle_field  + (i%4) * 3].get_text())
                                fields[i].set_text(str(round(safe_float(fields[i].get_text()) - delta,3)))
                            except ValueError:
                                pass
                        elif j == 24:
                            cp.px += color_vector
                            cp.px = cp.px % 360
                        elif j == 26: # reset button
                            spirograph_object.reset_default()
                            value_changed_flag = True
                        elif j == 28: #  stop/start  button
                            stop_flag = not stop_flag
                            value_changed_flag = True
                        elif j == 30: #  resolution + button
                            spirograph_object.change_speed(.5)
                            spirograph_object.update_fields_from_values()
        
                    else: #  j%2 = 1 (+)
                        i = (j-1)//2
                        if j < 8:   
                            try:
                                delta = safe_float(fields[speed_field + (i%4) * 3].get_text())
                                fields[i].set_text(str(round(safe_float(fields[i].get_text()) + delta,3)))
                            except ValueError:
                                pass
                        elif j < 16:
                            try:
                                delta = safe_float(fields[radius_field  + (i%4) * 3].get_text())
                                fields[i].set_text(str(round(safe_float(fields[i].get_text()) + delta,3)))
                            except ValueError:
                                pass
                        elif j < 24:
                            try:
                                delta = safe_float(fields[angle_field  + (i%4) * 3].get_text())
                                fields[i].set_text(str(round(safe_float(fields[i].get_text()) + delta,3)))
                            except ValueError:
                                pass
                        elif j == 25: # j == 25:   auto-increment button
                            spirograph_object.auto_increment()
                            spirograph_object.update_fields_from_values()
                        elif j == 27: # clear button
                            clear_flag = True
                            value_changed_flag = True
                        elif j == 29: #  resolution - button
                            spirograph_object.change_speed(2)  
                            spirograph_object.update_fields_from_values() 
                    if j < 24:
                        spirograph_object.update_values_from_fields()
            for k, lbutton in enumerate(lbuttons):
                if lbutton[0].collidepoint(event.pos):
                    lbuttons[k] = (lbutton[0],not lbutton[1])
                    for m, matching_button in enumerate(lbuttons):
                        if k % 4 == m % 4 and k != m:
                            lbuttons[m]= (matching_button[0],not lbutton[1])
                    spirograph_object.levels = lbuttons[0][1] + lbuttons[1][1] + lbuttons[2][1] +lbuttons[3][1]
                    value_changed_flag = True

                            
        elif event.type == pygame.KEYDOWN:
            # update the active field text
            for i, field in enumerate(fields):
                a_field_is_selected = field.selected
                    
                if event.key == pygame.K_RETURN:
                    if i < 13:  # don't flag value changed for increment fields
                        value_changed_flag = True;
                    if i != 24:
                        spirograph_object.update_values_from_fields()
                    else:
                        color_vector = safe_float(fields[24].get_text())    
                    fields[i].set_status(False)
                else:
                    field.handle_event(event)
            
            if a_field_is_selected == False: # no field active
                if event.key == pygame.K_SPACE:
                    if screen_copy_alpha == 255:
                        screen_copy_alpha = 251
                    else:
                        screen_copy_alpha = 255
    
    cp.update()

    # Update the player object
    if not stop_flag:
        spirograph_object.update()
    
    # Draw the objects
    screen_copy = trail_surface.copy()
    screen_copy.set_alpha(screen_copy_alpha)
    if clear_flag == True:
        screen_copy.fill(black)
        clear_flag = False
    screen.fill(black)
    trail_surface.fill((0,0,0,255))
    trail_surface.blit(screen_copy, (0,0))

    if value_changed_flag == False:
        pygame.draw.line(trail_surface, spirograph_object.color, spirograph_object.oldpos,(spirograph_object.x, spirograph_object.y), 2)
    value_changed_flag = False

    screen.blit(trail_surface, (0, 0))
    
    spirograph_object.color = cp.get_color()
    spirograph_object.draw()
    
    cp.draw(screen)
 
    # draw the text fields
    for i, field in enumerate(fields):
        if i < 12:
            field.set_color(level_colors[i % 4])
        elif i < 24:
            field.set_color(level_colors[(i - 12) // 3])
        else:
            field.set_color(white)
        
        field.update()
       
    sprites.update()  # this line updates the blinking cursor
    sprites.draw(screen)
    
    # draw the increment/decrement buttons
    for i, button in enumerate(buttons):
        button_rect, button_text = button
        pygame.draw.rect(screen, white, button_rect, 1,4)
        pygame.draw.rect(screen, blue, pygame.Rect(button_rect[0]+2, button_rect[1]+2, button_rect[2]-4, button_rect[3]-4), 0, 4)
        button_surface = font.render(button_text, True, white)
        if i > 24 and i < 29:  # the last four buttons except for the res increment buttons
            button_text_y_spacer = 13
        else:
            button_text_y_spacer = 3 
        screen.blit(button_surface, (button_rect.x + 5, button_rect.y + button_text_y_spacer))
        
    # draw the level buttons
    for i, lbutton in enumerate(lbuttons):
        lbutton_rect, lbutton_active = lbutton
        if lbutton_active:
            color = level_button_colors[i % 4]
        else:
            color = level_colors[4] 
        pygame.draw.rect(screen, color, lbutton_rect, 0)    

    #draw the labels
    for i in range(5):
        text_surface = font.render(textlabels[i][1], True, white)
        screen.blit(text_surface, (textlabels[i][0][0], textlabels[i][0][1]))   

    pygame.display.flip()

    # Set the frame rate
    clock.tick(240)

# Quit Pygame
pygame.quit()
