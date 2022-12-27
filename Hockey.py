import tkinter as tk
from random import randint

Width = 300
Height = 240

    


class Ball:
    def __init__(self):
        self.r = randint(19,20)
        self.x = randint(self.r, Width - self.r)
        self.y = randint(self.r, Height - self.r)
        self.vx, self.vy = (+5, 5)
        self.ball_id = canvas.create_oval(self.x - self.r, self.y - self.r, 
                                        self.x + self.r, self.y + self.r, 
                                        fill='green')
    
    def show(self):
        canvas.move(self.ball_id, self.vx, self.vy)

    def move(self):
        self.x += self.vx
        self.y += self.vy
        if self.x + self.r >= Width or self.x - self.r <= 0:
            self.vx = -self.vx
        if self.y + self.r  >= Height or self.y - self.r <= 0:
            self.vy = -self.vy
    
    def touch(self):
        if self.x - self.r <= gollkeeper_coords_x2 and self.x + self.r >= gollkeeper_coords_x:    
            if self.y + self.r >= 240:
                self.change_direct()  #<------ Problem is here 
            else:
                pass 
        else:
            pass
                        
    
    def change_direct(self):
        self.vy =  -self.vy

    


        
        



class Gollkeeper:
    def __init__(self):
        self.x = 50
        self.y = 230
        self.x2 = 250
        self.y2 = 240
        self.vx = 0
        self.vy = 0
        self.gollkeeper_id = canvas.create_rectangle(self.x, self.y, 
                                               self.x2, self.y2, fill='Red')
    
    def show(self):
        canvas.move(self.gollkeeper_id, self.vx, self.vy)

    def move(self):
        self.x += self.vx
        self.x2 += self.vx
        self.y += self.vy
        if self.x <= 0 or self.x2 >=  Width:
            self.vx = -self.vx
    
    def get_coords(self):
        global gollkeeper_coords_x, gollkeeper_coords_x2, gollkeeper_coords_y
        gollkeeper_coords_x = self.x
        gollkeeper_coords_x2 = self.x2
        gollkeeper_coords_y = self.y
        
    
        
    
    

class Field:
    def __init__(self):
        pass

def tick():
    gollkeeper.show()
    gollkeeper.move()
    gollkeeper.get_coords()
    ball.move()
    ball.show()
    ball.touch()
    root.after(50, tick)



def main():
    global root, canvas, ball, gollkeeper
    root = tk.Tk(className='Game')
    root.geometry(str(Width) + 'x' + str(Height))
    canvas = tk.Canvas(root)
    canvas.pack(anchor= 'nw' )
    ball = Ball()
    gollkeeper = Gollkeeper()
    tick()



main()
root.mainloop()