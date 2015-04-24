import turtle


turtle.setup(800, 600)      
wn = turtle.Screen()        # establecer wn al objeto de la ventana
wn.bgcolor("lightgreen")    # establecer el color de fondo de la ventana
wn.title("Hola, Tess!")     
tess = turtle.Turtle()
tess.color("blue")          
tess.pensize(3)              
tess.forward(300)
tess.left(120)
tess.forward(300)

wn.exitonclick()