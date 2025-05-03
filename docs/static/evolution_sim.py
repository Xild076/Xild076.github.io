from browser import document, window, timer
import random, math

canvas = document["evoCanvas"]
ctx = canvas.getContext("2d")

def resize(ev=None):
    canvas.width = int(canvas.clientWidth * window.devicePixelRatio)
    canvas.height = int(canvas.clientHeight * window.devicePixelRatio)
    ctx.scale(window.devicePixelRatio, window.devicePixelRatio)

window.bind("resize", resize)
resize()

class Organism:
    MAX_VEL = 1.5
    RADIUS = 3.5
    def __init__(self, w, h):
        self.width, self.height = w, h
        self.x = random.uniform(0, w)
        self.y = random.uniform(0, h)
        self.vx = random.uniform(-0.5,0.5)*self.MAX_VEL
        self.vy = random.uniform(-0.5,0.5)*self.MAX_VEL
        self.fitness = 0
        self.target_radius = self.RADIUS
        self.current_radius = self.RADIUS
        self.hue = 240
        self.saturation = 70
        self.lightness = 60

    def move(self):
        self.x += self.vx
        self.y += self.vy
        self.vx += random.uniform(-0.05,0.05)
        self.vy += random.uniform(-0.05,0.05)
        speed = math.hypot(self.vx, self.vy)
        if speed > self.MAX_VEL:
            self.vx = self.vx/speed*self.MAX_VEL
            self.vy = self.vy/speed*self.MAX_VEL
        buf = self.RADIUS*2
        if self.x<buf and self.vx<0: self.vx*=-0.95; self.x=buf
        if self.x>self.width-buf and self.vx>0: self.vx*=-0.95; self.x=self.width-buf
        if self.y<buf and self.vy<0: self.vy*=-0.95; self.y=buf
        if self.y>self.height-buf and self.vy>0: self.vy*=-0.95; self.y=self.height-buf

    def eval_fitness(self):
        dx = abs(self.width/2 - self.x)
        norm = min(1, dx/(self.width/2))
        self.fitness = 1 - norm
        target_hue = 40 + (1 - self.fitness)*200
        self.hue += (target_hue - self.hue)*0.1
        self.target_radius = self.RADIUS + self.fitness*1.5
        self.current_radius += (self.target_radius - self.current_radius)*0.1

    def draw(self):
        glow = self.current_radius*1.8
        grad = ctx.createRadialGradient(self.x,self.y,self.current_radius*0.2,self.x,self.y,glow)
        base = f"hsla({int(self.hue)}, {self.saturation}%, {self.lightness}%, 0.4)"
        trans = f"hsla({int(self.hue)}, {self.saturation}%, {self.lightness}%, 0)"
        grad.addColorStop(0, base)
        grad.addColorStop(1, trans)
        ctx.fillStyle = grad
        ctx.beginPath()
        ctx.arc(self.x, self.y, glow, 0, 2*math.pi)
        ctx.fill()
        main_light = self.lightness + 10
        ctx.fillStyle = f"hsl({int(self.hue)}, {self.saturation}%, {main_light}%)"
        ctx.beginPath()
        ctx.arc(self.x, self.y, self.current_radius, 0, 2*math.pi)
        ctx.fill()

def step(pop, w, h):
    for o in pop:
        o.move(); o.eval_fitness()
    pop.sort(key=lambda x:x.fitness, reverse=True)
    n = len(pop)//2
    surv = pop[:n]
    kids = []
    if surv:
        for _ in range(len(pop)-n):
            p = random.choice(surv)
            c = Organism(w,h)
            c.x = min(w, max(0, p.x + random.uniform(-5,5)))
            c.y = min(h, max(0, p.y + random.uniform(-5,5)))
            c.vx = p.vx + random.uniform(-0.1,0.1)*Organism.MAX_VEL
            c.vy = p.vy + random.uniform(-0.1,0.1)*Organism.MAX_VEL
            c.hue = p.hue + random.uniform(-10,10)
            kids.append(c)
    else:
        kids = [Organism(w,h) for _ in pop]
    return surv + kids

population = [Organism(canvas.clientWidth, canvas.clientHeight) for _ in range(60)]

def animate(ts=0):
    w, h = canvas.clientWidth, canvas.clientHeight
    ctx.fillStyle = "rgba(10,15,30,0.12)"
    ctx.fillRect(0,0,w,h)
    global population
    population = step(population, w, h)
    for o in population:
        o.width, o.height = w, h
        o.draw()
    timer.request_animation_frame(animate)

timer.request_animation_frame(animate)
