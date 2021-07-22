# evolution 3d for Simon
import vpython
import vpython as vp  # vpython must be installed from vpython.org
import random


# Press Umschalt+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


# def print_hi(name):
#    # Use a breakpoint in the code line below to debug your script.
#    print(f'Hi, {name}')  # Press Strg+F8 to toggle the breakpoint.

class Game:
    grid_size = 1  # should be 1 until we understand what it does
    fps = 60
    grid_dim = 2  # 1 = 1 cube, 2 = 2x2x2 cubes, 3=3x3x3 cubes...
    cube_to_grid_ratio = 0.95
    max_swimmers = 10
    friction = 0.93
    
    trails = True

    cubedict = {}
    plantdict = {}
    particledict = {}
    swimmidict = {}

    # TODO: compounds?


class Plant(vpython.simple_sphere):
    number = 0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.number = Plant.number
        Plant.number += 1

        self.spawn_rate = 0.01
        self.spawn_speed = random.uniform(0.4, 1.5)

        if "color" not in kwargs or kwargs["color"] is None:
            self.color = vp.vector(random.random(), random.random(), random.random())
        if "radius" not in kwargs or kwargs["radius"] is None:
            self.radius = random.random()

        Game.plantdict[self.number] = self

    def update(self):
        if random.random() < self.spawn_rate:
            Particle(pos=self.pos, color=self.color, radius=0.01, speed=self.spawn_speed)


class Particle(vpython.simple_sphere):
    number = 0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.number = Particle.number
        Particle.number += 1

        self.axis = vpython.vector.random()
        self.speed = kwargs["speed"]

        self.max_age = 10
        self.age = 0

        Game.particledict[self.number] = self

    def update(self):
        self.pos += self.axis * self.speed * 1 / Game.fps
        self.speed *= Game.friction

        self.age += 1 / Game.fps
        if self.age > self.max_age:
            self.visible = False


class Cube(vpython.box):
    """basically an aquarium for swimmies with own enviroment"""
    number = 0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.number = Cube.number
        Cube.number += 1

        Game.cubedict[self.number] = self

    @property
    def amount_of_swimmies(self):
        amount = 0
        for swimmy in Game.swimmidict.values():
            if abs(swimmy.pos.x - self.pos.x) < (self.size.x / 2):
                if abs(swimmy.pos.y - self.pos.y) < (self.size.y / 2):
                    if abs(swimmy.pos.z - self.pos.z) < (self.size.z / 2):
                        amount += 1
        return amount

    def change_color(self):
        if len(Game.swimmidict) > 0:
            # the more swimmies in me, the redder i become
            total = len(Game.swimmidict)
            mine = self.amount_of_swimmies
            self.color = vp.vector(mine / total, self.color.y, self.color.z)


class Swimmi(vpython.cone):
    number = 0
    max_speed = 0.75
    min_speed = 0.01
    turn_speed = 90  # degrees / second

    def __init__(self, **kwargs):
        # for k, v in kwargs.items():
        if "pos" not in kwargs or kwargs["pos"] is None:
            # if (newpos.x > Game.grid_dim * Game.grid_size - Game.grid_size / 2) or (newpos.x < - Game.grid_size / 2):
            kwargs["pos"] = vpython.vector(
                random.uniform(-Game.grid_size / 2, Game.grid_dim * Game.grid_size - Game.grid_size / 2),
                random.uniform(-Game.grid_size / 2, Game.grid_dim * Game.grid_size - Game.grid_size / 2),
                random.uniform(-Game.grid_size / 2, Game.grid_dim * Game.grid_size - Game.grid_size / 2),
                )
        if "axis" not in kwargs or kwargs["axis"] is None:
            kwargs["axis"] = vpython.norm(vpython.vector.random()) * 0.07
        # overwrite radius with 0.03
        kwargs["radius"] = 0.03
        
        # only make trail if Game.trails is True
        if Game.trails:
            kwargs["make_trail"] = True
            kwargs["trail_type"] = "curve"
            # use either interval or pps
            #kwargs["interval"] = 10
            kwargs["pps"] = 15 # for curve only, if no interval is given, add 15 trail points per second
            kwargs["retain"] = 15
            
        super().__init__(**kwargs)

        print("Ich bin ein Swimmi")
        self.number = Swimmi.number
        Swimmi.number += 1
        Game.swimmidict[self.number] = self
        self.age = 0
        self.angle = 0
        self.max_age = random.uniform(500, 500)
        self.speed = random.uniform(Swimmi.min_speed, Swimmi.max_speed)
        self.nervousness = random.random() + 0.01
        self.iwanttogothere = vpython.vector.random()

    def update(self):
        # change speed
        self.speed += random.uniform(-0.01, 0.01)
        self.speed = max(Swimmi.min_speed, self.speed)
        self.speed = min(self.speed, Swimmi.max_speed)
        self.reflect()
        self.pos += vpython.norm(self.axis) * self.speed * 1 / Game.fps
        # aging
        self.age += 1 / Game.fps
        if self.age > self.max_age:
            # kill correctly
            self.visible = False
        # rotating randomly
        self.pitchaxis = vpython.cross(self.axis, self.up)
        rot_axis = random.choice([self.axis, self.up, self.pitchaxis])
        self.angle += random.uniform(-0.1, 0.1)
        if random.random() < self.nervousness:
            self.iwanttogothere = vpython.vector.random()
        diff_angle = vpython.diff_angle(self.axis, self.iwanttogothere)
        if diff_angle > 0:
            for axis in [self.axis, self.up, self.pitchaxis]:
                axisleft = self.axis.rotate(angle=vpython.radians(self.turn_speed * 1 / 60), axis=axis)
                resultleft = vpython.diff_angle(axisleft, self.iwanttogothere)
                axisright = self.axis.rotate(angle=vpython.radians(-self.turn_speed * 1 / 60), axis=axis)
                resultright = vpython.diff_angle(axisright, self.iwanttogothere)

                if resultleft < resultright:
                    angle = 1
                elif resultleft > resultright:
                    angle = -1
                else:
                    angle = 0
                if angle != 0:
                    self.rotate(angle=vpython.radians(angle * self.turn_speed * 1 / 60), axis=axis)

    def reflect(self):
        m = self.axis
        mx = m.x
        my = m.y
        mz = m.z
        newpos = self.pos + vpython.norm(self.axis) * self.speed * 1 / Game.fps
        # reflect from edge of universe
        if (newpos.x > Game.grid_dim * Game.grid_size - Game.grid_size / 2) or (newpos.x < - Game.grid_size / 2):
            mx *= -1
        if (newpos.y > Game.grid_dim * Game.grid_size - Game.grid_size / 2) or (newpos.y < - Game.grid_size / 2):
            my *= -1
        if (newpos.z > Game.grid_dim * Game.grid_size - Game.grid_size / 2) or (newpos.z < - Game.grid_size / 2):
            mz *= -1
        # reflect from plant
        for p in Game.plantdict.values():
            distance = self.pos - p.pos
            if distance.mag < p.radius:
                mx *= -1
                my *= -1
                mz *= -1
                break
        self.axis = vpython.vector(mx, my, mz)


def create_world():
    xarrow = vp.arrow(pos=vp.vector(0, 0, 0), axis=vp.vector(1, 0, 0), color=vp.vector(1, 0, 0))  # red
    yarrow = vp.arrow(pos=vp.vector(0, 0, 0), axis=vp.vector(0, 1, 0), color=vp.vector(0, 1, 0))  # green
    zarrow = vp.arrow(pos=vp.vector(0, 0, 0), axis=vp.vector(0, 0, 1), color=vp.vector(0, 0, 1))  # blue
    xlabel = vp.label(pos=xarrow.pos + xarrow.axis, color=xarrow.color, text="x")
    ylabel = vp.label(pos=yarrow.pos + yarrow.axis, color=yarrow.color, text="y")
    zlabel = vp.label(pos=zarrow.pos + zarrow.axis, color=zarrow.color, text="z")

    for x in range(Game.max_swimmers):
        Swimmi()


def create_cubes():
    for x in range(0, Game.grid_dim, Game.grid_size):
        for y in range(0, Game.grid_dim, Game.grid_size):
            for z in range(0, Game.grid_dim, Game.grid_size):
                Cube(pos=vp.vector(x, y, z),
                     size=vp.vector(Game.grid_size * Game.cube_to_grid_ratio,
                                    Game.grid_size * Game.cube_to_grid_ratio,
                                    Game.grid_size * Game.cube_to_grid_ratio,
                                    ),
                     color=vp.vector(0.75, 0.75, 0.75),
                     opacity=0.15,
                     )
                Plant(pos=vp.vector(x, y, z), radius=Game.grid_size * Game.cube_to_grid_ratio / 10)


def display():
    for swimmi in Game.swimmidict.values():
        swimmi.update()
    for particili in Game.particledict.values():
        particili.update()
    for plant in Game.plantdict.values():
        plant.update()
    for cube in Game.cubedict.values():
        cube.change_color()

    # kill dead stuff
    for mydict in [Game.swimmidict, Game.particledict]:
        for dead_thing in [item for item in mydict.values() if item.age > item.max_age]:
            del mydict[dead_thing.number]
            del dead_thing


def main():
	# toggle all trails with this variable
    Game.trails = False
	
    create_world()
    create_cubes()
    
    # update swimmies
    while True:
        vp.rate(Game.fps)
        display()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
