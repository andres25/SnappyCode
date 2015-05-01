import turtle
def dragoncurve(l,n): 
    def x(n): 
        if n==0: 
            return x(n-1) 
        turtle.rt(90) 
        y(n-1) 
        turtle.fd(l) 
    def y(n): 
        if n==0: 
            return turtle.fd(l) 
        x(n-1) 
        turtle.lt(90) 
        y(n-1) 
        turtle.fd(l) 
        x(n)
myWin = turtle.Screen()
dragoncurve(3,12)
myWin.exitonclick()
