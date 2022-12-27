import tkinter as tk
from random import randint

Width = 300
Height = 240

    


class Ball:
    """Intialization of Ball"""
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
        """Move with speed (vx) on x-axis and (vy) on y axis and also check is ball cross borders or not """
        self.x += self.vx
        self.y += self.vy
        if self.x + self.r >= Width or self.x - self.r <= 0:
            self.vx = -self.vx
        if self.y + self.r  >= Height or self.y - self.r <= 0:
            self.vy = -self.vy
    
    def touch(self):
        """Check does ball touched the gollkeeper(red rectangle) or not
            PROBLEM IS HERE!!!"""
        if self.x - self.r <= gollkeeper_coords_x2 and self.x + self.r >= gollkeeper_coords_x:    
            if self.y + self.r >= 240:
                self.change_direct()   #<------------- when ball touches the gollkeeper, this function repeats until ball will touch gollkeeper again
            else:
                pass 
        else:
            pass
                        
    
    def change_direct(self):
        """Chenge moving or rebound"""
        self.vy =  -self.vy

    


        
        



class Gollkeeper:
    def __init__(self):
        self.x = 100
        self.y = 240
        self.x2 = 140
        self.y2 = 250
        self.vx = 12
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
        """announce coords of gollkeeper as global"""
        global gollkeeper_coords_x, gollkeeper_coords_x2, gollkeeper_coords_y
        gollkeeper_coords_x = self.x
        gollkeeper_coords_x2 = self.x2
        gollkeeper_coords_y = self.y
        
    
        
    
    

class Field:
    """Empty class"""
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