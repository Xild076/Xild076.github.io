from browser import document, window, timer
import random, math

canvas = document["evoCanvas"]
ctx    = canvas.getContext("2d")

def resize(ev=None):
    w, h = canvas.clientWidth, canvas.clientHeight
    ratio = window.devicePixelRatio
    canvas.width  = int(w * ratio)
    canvas.height = int(h * ratio)
    ctx.scale(ratio, ratio)

window.bind("resize", resize)
resize()

class Organism:
    MAX_VEL = 1.5
    RADIUS  = 3.5
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.x = random.uniform(0, w)
        self.y = random.uniform(0, h)
        self.vx = random.uniform(-0.5,0.5)*self.MAX_VEL
        self.vy = random.uniform(-0.5,0.5)*self.MAX_VEL
        self.hue, self.sat, self.lum = 240,70,60
        self.curr_r = self.RADIUS
        self.tgt_r  = self.RADIUS

    def move(self):
        self.x += self.vx; self.y += self.vy
        self.vx += random.uniform(-.05,.05)
        self.vy += random.uniform(-.05,.05)
        sp = math.hypot(self.vx,self.vy)
        if sp>self.MAX_VEL:
            self.vx, self.vy = (self.vx/sp*self.MAX_VEL,
                                self.vy/sp*self.MAX_VEL)
        buf = self.RADIUS*2
        if self.x<buf and self.vx<0: self.vx*=-.95; self.x=buf
        if self.x>self.w-buf and self.vx>0: self.vx*=-.95; self.x=self.w-buf
        if self.y<buf and self.vy<0: self.vy*=-.95; self.y=buf
        if self.y>self.h-buf and self.vy>0: self.vy*=-.95; self.y=self.h-buf

    def eval_fitness(self):
        dx = abs(self.w/2-self.x)
        norm = min(1, dx/(self.w/2))
        fit  = 1-norm
        tgt_hue = 40 + (1-fit)*200
        self.hue += (tgt_hue-self.hue)*.1
        self.tgt_r = self.RADIUS + fit*1.5
        self.curr_r += (self.tgt_r-self.curr_r)*.1

    def draw(self):
        glow = self.curr_r*1.8
        grad = ctx.createRadialGradient(
            self.x,self.y,self.curr_r*.2, self.x,self.y,glow
        )
        c0 = f"hsla({int(self.hue)},{self.sat}%,{self.lum}%,.4)"
        c1 = f"hsla({int(self.hue)},{self.sat}%,{self.lum}%,0)"
        grad.addColorStop(0,c0); grad.addColorStop(1,c1)
        ctx.fillStyle=grad
        ctx.beginPath(); ctx.arc(self.x,self.y,glow,0,2*math.pi); ctx.fill()
        mlum = self.lum+10
        ctx.fillStyle = f"hsl({int(self.hue)},{self.sat}%,{mlum}%)"
        ctx.beginPath(); ctx.arc(self.x,self.y,self.curr_r,0,2*math.pi); ctx.fill()

def step(pop,w,h):
    for o in pop: o.move(); o.eval_fitness()
    pop.sort(key=lambda x:x.fitness if hasattr(x,'fitness') else 0,
             reverse=True)
    half = len(pop)//2
    surv = pop[:half]
    kids = []
    if surv:
        for _ in range(len(pop)-half):
            p = random.choice(surv)
            c = Organism(w,h)
            c.x = max(0,min(w, p.x+random.uniform(-5,5)))
            c.y = max(0,min(h, p.y+random.uniform(-5,5)))
            c.vx = p.vx + random.uniform(-.1,.1)*Organism.MAX_VEL
            c.vy = p.vy + random.uniform(-.1,.1)*Organism.MAX_VEL
            c.hue= p.hue+random.uniform(-10,10)
            kids.append(c)
    else:
        kids = [Organism(w,h) for _ in pop]
    return surv + kids

population = [Organism(canvas.clientWidth,canvas.clientHeight)
              for _ in range(60)]

def animate(ts=0):
    w,h = canvas.clientWidth,canvas.clientHeight
    ctx.fillStyle="rgba(10,15,30,0.12)"
    ctx.fillRect(0,0,w,h)
    global population
    population = step(population,w,h)
    for o in population:
        o.w, o.h = w, h
        o.draw()
    timer.request_animation_frame(animate)

timer.request_animation_frame(animate)
