# This is a sample Python script.
# evolution 3d for Simon
import vpython as vp
import random
# Press Umschalt+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


#def print_hi(name):
#    # Use a breakpoint in the code line below to debug your script.
#    print(f'Hi, {name}')  # Press Strg+F8 to toggle the breakpoint.

class Game:
    grid_size = 1
    dt = 1/100
    grid_dim = 2
    cube_to_grid_ratio = 0.95
    max_swimmers = 100
    swimmers = {} # python objects
    cubes = {}
    cubelist = []  # for 3d grafik
    swimmlist = [] # spriteliste for representation


class Cube():
    """basically an aquarium for swimmies with own enviroment"""
    number = 0

    def __init__(self, pos, size, color, opacity):
        self.number = Cube.number
        Cube.number += 1
        Game.cubes[self.number] = self

        self.pos = pos
        self.size = size
        self.color = color
        self.opacity = opacity


    @property
    def amount_of_swimmies(self):
        amount = 0
        for swimmy in Game.swimmers.values():
            if abs(swimmy.pos.x - self.pos.x) < (self.size.x / 2):
                if abs(swimmy.pos.y - self.pos.y) < (self.size.y / 2):
                    if abs(swimmy.pos.z - self.pos.z) < (self.size.z / 2):
                        amount += 1
        return amount

    def change_color(self):
        # the more swimmies in me, the redder i become
        total = len(Game.swimmers)
        mine = self.amount_of_swimmies
        self.color = vp.vector(mine/total, self.color.y, self.color.z)

class Swimmer():
    number = 0

    def __init__(self):
        self.number = Swimmer.number
        Swimmer.number +=1
        Game.swimmers[self.number] = self
        self.hp = 100
        self.hp_max = 100
        self.speed = 5
        #self.hunger = 0
        self.energy = 100
        #self._color = 0
        self.pos = vp.vector(1,0,1)

    @property
    def color(self):
        return vp.vector(   1 - (self.hp / self.hp_max), self.hp / self.hp_max,  0 )

    @property
    def move(self):
        mx = random.uniform(-1,1)
        my = random.uniform(-1,1)
        mz = random.uniform(-1,1)
             #            ) # -1..1,  -1..1, -1..1
        #print(mx, my, mz, self.pos, self.speed, Game.dt)
        new_pos = self.pos + vp.vector(mx, my,mz)  * self.speed * Game.dt
        #         0                    1
        #    -0.5bis0.5          0.5 bis 1.5
        # bounce if reaching outer aquariums wall
        if (new_pos.x > Game.grid_dim * Game.grid_size  - Game.grid_size/2) or (new_pos.x < - Game.grid_size/2) :
            mx *= -1
        if (new_pos.y > Game.grid_dim * Game.grid_size  - Game.grid_size/2) or (new_pos.y < - Game.grid_size/2) :
            my *= -1
        if (new_pos.z > Game.grid_dim * Game.grid_size  - Game.grid_size/2) or (new_pos.z < - Game.grid_size/2):
            mz *= -1
        return vp.vector(mx, my, mz)


def create_world():
    xarrow = vp.arrow(pos=vp.vector(0,0,0), axis=vp.vector(1,0,0), color=vp.vector(1,0,0))  # red
    yarrow = vp.arrow(pos=vp.vector(0,0,0), axis=vp.vector(0,1,0), color=vp.vector(0,1,0))  # green
    zarrow = vp.arrow(pos=vp.vector(0, 0, 0), axis=vp.vector(0, 0, 1), color=vp.vector(0, 0, 1))  # blue
    xlabel = vp.label(pos= xarrow.pos + xarrow.axis, color=xarrow.color, text="spielend-programmmieren.at")

    for x in range(Game.max_swimmers):
        Swimmer()

def create_cubes():
    for x in range(0, Game.grid_dim, Game.grid_size):
        for y in range(0, Game.grid_dim, Game.grid_size):
            for z in range(0, Game.grid_dim, Game.grid_size):
                Cube(pos=vp.vector(x,y,z),
                       size=vp.vector(Game.grid_size * Game.cube_to_grid_ratio,
                                      Game.grid_size * Game.cube_to_grid_ratio,
                                      Game.grid_size * Game.cube_to_grid_ratio,
                       ),
                       color=vp.vector(0.5,0.5,0.5),
                       opacity=0.25,
                       )

    for cube in Game.cubes.values():
        Game.cubelist.append(vp.box(pos=cube.pos, size=cube.size, color=cube.color, opacity=cube.opacity))

def display():
    # clear spritelist
    for sprite in Game.swimmlist:
        sprite.visible = False
        sprite.delete()
    Game.swimmlist = [] # empty the list
    # wait display to have time for updates


    # update python objects
    for swimmy in Game.swimmers.values():
        swimmy.pos += swimmy.move * swimmy.speed * Game.dt

        Game.swimmlist.append(vp.simple_sphere(pos=swimmy.pos, color=swimmy.color, radius=0.01))
    for cube in Game.cubes.values():
        cube.change_color()
        Game.cubelist[cube.number].color = cube.color

    vp.sleep(Game.dt)



def main():
    create_world()
    create_cubes()

    # update swimmies
    while True:
        display()




# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()



# See PyCharm help at https://www.jetbrains.com/help/pycharm/