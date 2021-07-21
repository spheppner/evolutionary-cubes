# evolution 3d for Simon
import vpython
import vpython as vp   # vpython must be installed from vpython.org
import random
# Press Umschalt+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


#def print_hi(name):
#    # Use a breakpoint in the code line below to debug your script.
#    print(f'Hi, {name}')  # Press Strg+F8 to toggle the breakpoint.

class Game:
    grid_size = 1 # should be 1 until we understand what it does
    dt = 1/100
    grid_dim = 4 # 1 = 1 cube, 2 = 2x2x2 cubes, 3=3x3x3 cubes...
    cube_to_grid_ratio = 0.95
    max_swimmers = 10
    swimmers = {} # python objects
    cubes = {}
    cubelist = []  # for 3d grafik
    plantlist = []
    particledict = {}
    particlelist = []
    swimmlist = [] # spriteliste for representation


class Plant():
    number = 0

    def __init__(self, startpos, color=None, radius=None):
        self.number = Plant.number
        Plant.number += 1

        self.spawn_rate = 0.1
        self.spawn_speed = random.uniform(0.1,1.5)

        self.startpos = startpos
        self.color = color if color is not None else vp.vector(random.random(), random.random(), random.random())
        self.radius = radius if radius is not None else random.random()

        Game.plantlist.append(self)

        vp.simple_sphere(pos=self.startpos, color=self.color, radius=self.radius)
        # TODO: age

    def update(self):
        if random.random() < self.spawn_rate:
            Particle(startpos=self.startpos, color=self.color, radius=0.01, speed=self.spawn_speed)

class Particle():
    number = 0

    def __init__(self, startpos, color=None, radius=None, speed=None):
        self.number = Particle.number
        Particle.number += 1

        self.move = vp.vector.random()
        self.startpos = startpos
        self.speed = speed if speed is not None else random.random()
        self.color = color if color is not None else vp.vector(random.random(), random.random(), random.random())
        self.radius = radius if radius is not None else random.random()

        self.friction = 0.93

        self.max_age = 500
        self.age = 0

        Game.particledict[self.number] = self

    def update(self):
        self.startpos += self.move * self.speed * Game.dt
        self.speed *= self.friction

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
        self.pos = vp.vector(0.5,0.5,0.5)

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
    xlabel = vp.label(pos= xarrow.pos + xarrow.axis, color=xarrow.color, text="x")
    ylabel = vp.label(pos=yarrow.pos + yarrow.axis, color=yarrow.color, text="y")
    zlabel = vp.label(pos=zarrow.pos + zarrow.axis, color=zarrow.color, text="z")

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
                       color=vp.vector(0.75,0.75,0.75),
                       opacity=0.15,
                       )
                Plant(startpos=vp.vector(x,y,z), radius = Game.grid_size * Game.cube_to_grid_ratio/10)

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

        Game.swimmlist.append(vp.simple_sphere(pos=swimmy.pos, color=swimmy.color, radius=0.02))
    for cube in Game.cubes.values():
        cube.change_color()
        Game.cubelist[cube.number].color = cube.color

    for sprite in Game.particlelist:
        sprite.visible = False
        sprite.delete()
    Game.particlelist = [] # empty the list

    marked_to_kill = []
    for particle in Game.particledict.values():
        particle.age += 1
        if particle.age > particle.max_age:
            #del Game.particledict[particle.number]
            marked_to_kill.append(particle.number)
        else:
            particle.update()
            Game.particlelist.append(vp.simple_sphere(pos=particle.startpos, color=particle.color, radius=particle.radius))
    for nr in marked_to_kill:
        del Game.particledict[nr]

    for plant in Game.plantlist:
        plant.update()

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
