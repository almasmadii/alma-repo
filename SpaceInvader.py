import turtle
import time
import random
#SET-UP
screen=turtle.Screen()
screen.title("Space Invaders Game")
screen.bgcolor("black")
screen.setup(width=800,height=600)
screen.tracer(0)
#PLAYER
player=turtle.Turtle()
player.shape("triangle")
player.color("white")
player.penup()
player.goto(0, -250)
player.speed(0)
player.setheading(90)
#ALIENS
aliens=[]
for row in range(3):
    for col in range(10):
        alien=turtle.Turtle()
        alien.shape("square")
        alien.color("green")
        alien.penup()
        alien.goto(-270 + col * 60, 150 + row * 40)
        alien.speed(0)
        aliens.append(alien)
#BULLETS
bullet=turtle.Turtle()
bullet.shape("circle")
bullet.color("yellow")
bullet.shapesize(0.3,0.3)
bullet.penup()
bullet.hideturtle()
bullet.speed(0)
bullet_active=False

#SCORE
score=0
score_display=turtle.Turtle()
score_display.color("white")
score_display.penup()
score_display.hideturtle()
score_display.goto(-25,250)
score_display.write(f"Score: {score}",font=("Arial",14,"normal"))

#MOVEMENT

def move_left():
    x=player.xcor()
    if x > -350:
        player.setx(x-20)

def move_right():
    x=player.xcor()
    if x < 350:
        player.setx(x+20)
def shoot():
    global bullet_active
    if not bullet_active:
        bullet.goto(player.xcor(),player.ycor()+20)
        bullet.showturtle()
        bullet_active=True


screen.onkey(move_left,"Left")
screen.onkey(move_right,"Right")
screen.onkey(shoot,"space")
screen.listen()

#ALIEN MOVEMENT
alien_direction=1
alien_speed=2
last_alien_move=time.time()

#GAME LOOP
game_over=False
while not game_over:
    screen.update()

    if bullet_active:
        bullet.sety(bullet.ycor() + 15)
        if bullet.ycor()>300:
            bullet.hideturtle()
            bullet_active=False
    for alien in aliens[:]:

        if bullet_active:
            if abs(bullet.xcor()-alien.xcor()) <20 and \
                abs(bullet.ycor() - alien.ycor()) < 20:
                alien.hideturtle()
                aliens.remove(alien)
                bullet.hideturtle()
                bullet_active=False
                score+=10
                score_display.clear()
                score_display.write(f"Score: {score}", font=("Arial",14,"normal"))

    if time.time()-last_alien_move>1:
        for alien in aliens:
            alien.setx(alien.xcor() + alien_speed * alien_direction)

        for alien in aliens:
            if alien.xcor() >350 or alien.xcor() <-350:
                alien_direction*=-1
                for a in aliens:
                    a.sety(a.ycor()-20)
                break
        last_alien_move=time.time()

    for alien in aliens:
        if alien.ycor()<-220:
            game_over=True
            break
    if len (aliens)==0:
        score_display.goto(0,0)
        score_display.write("YOU WIN!!",align="center",font=("Arial",24,"normal"))
        game_over=True
    time.sleep(0.02)

go=turtle.Turtle()
go.color("red")
go.penup()
go.hideturtle()
go.goto(0,25)
go.write("GAME OVER",align="center",font=("Arial",36,"bold"))


turtle.done()

# hamodeh was here