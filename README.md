# PongBot
UTRA Beer Pong Robot - 2015

### Full stack overview
Broadly, the software for the project can be grouped into 4 components that go from an image of the table, to code interfacing the firing mechanism. These 4 components, and their responsibilities, are as follows: 

1. Computer Vision: Image -> circles (x, y) on image
2. Coordinate Transform: Circles (x, y) ->  Circles (r, theta) relative to bot
3. Physics: Circles (r, theta) -> Control/motor input
4. Control: Control/motor input -> Firing the ball

### Soon to Come:
* Trashtalking
* Trickshots
* Quality of toss will be dependent on robo-drunkedness 
