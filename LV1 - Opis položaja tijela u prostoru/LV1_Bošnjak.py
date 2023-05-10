import math
import vtkmodules.vtkInteractionStyle
import vtkmodules.vtkRenderingOpenGL2

from vtkmodules.vtkCommonMath import vtkMatrix4x4
from body import Body
from display import Display

def RotZ(q):
    cq=math.cos(q)
    sq=math.sin(q)
    T = [cq, -sq, 0, 0,
         sq, cq, 0, 0,
         0, 0, 1, 0,
         0, 0, 0, 1]
    return T

def main():

	theta1=float(input("Unesite željeni kut prvog zgloba: ")) # castanje stringa u float
	theta2=float(input("Unesite željeni kut drugog zgloba: "))
	theta3=float(input("Unesite željeni kut trećeg zgloba: "))
	TR1=RotZ(theta1 * math.pi / 180) # math.pi / 180 --> iz stupnjeva u radijane
	TR2=RotZ(theta2 * math.pi / 180)
	TR3=RotZ(theta3 * math.pi / 180)

	scene=Body()

	base=Body()
	base.CreateBox(0.4,0.4,0.15,0.1,0.2,0.5)

	scene.AddPart(base)

	#Prvi koordinatni sustav S1

	T1F = [ 1, 0, 0, 0,
			0, 1, 0, 0,
			0, 0, 1, 0.1,
			0, 0, 0, 1]

	T10 = [0] * 16

	vtkMatrix4x4.Multiply4x4(T1F, TR1, T10)

	#Drugi koordinatni sustav S2

	T2F = [ 1, 0, 0, 0.275,
			0, 1, 0, 0,
			0, 0, 1, 0.15,
			0, 0, 0, 1]

	T21 = [0] * 16
	T20 = [0] * 16

	vtkMatrix4x4.Multiply4x4(T2F, TR2, T21)
	vtkMatrix4x4.Multiply4x4(T10, T21, T20)

	#Treći koordinatni sustav S3

	T3F = [ 1, 0, 0, 0.275,
			0, 1, 0, 0,
			0, 0, 1, 0.15,
			0, 0, 0, 1]

	T32 = [0] * 16
	T31 = [0] * 16
	T30 = [0] * 16

	vtkMatrix4x4.Multiply4x4(T3F, TR3, T32)
	vtkMatrix4x4.Multiply4x4(T21, T32, T31)
	vtkMatrix4x4.Multiply4x4(T10, T31, T30)

	#Joint 1

	cyl1=Body()
	cyl1.CreateCylinder(0.025, 0.05, 36, 0.1, 0.2, 0.3)
	scene.AddPart(cyl1)

	TJ11 = [1, 0, 0, 0,
			0, 0, -1, 0,
			0, 1, 0, 0,
			0, 0, 0, 1]
	TJ10=[0] * 16

	vtkMatrix4x4.Multiply4x4(T10, TJ11, TJ10)

	cyl1.Transform(TJ10)

	#Link 1

	link1=Body()
	link1.CreateBox(0.4, 0.1, 0.1, 0.2, 0.1, 0.3)
	scene.AddPart(link1)

	TL11 = [1, 0, 0, 0.2-0.05-0.025,
			0, 1, 0, 0,
			0, 0, 1, 0.075,
			0, 0, 0, 1]
		
	TL10 = [0] * 16

	vtkMatrix4x4.Multiply4x4(T10, TL11, TL10)

	link1.Transform(TL10)

	#Joint 2

	cyl2=Body()
	cyl2.CreateCylinder(0.025, 0.05, 36, 0.1, 0.2, 0.3)
	scene.AddPart(cyl2)

	TJ21 = [1, 0, 0, 0,
			0, 0, -1, 0,
			0, 1, 0, 0,
			0, 0, 0, 1]
	TJ20=[0] * 16

	vtkMatrix4x4.Multiply4x4(T20, TJ21, TJ20)

	cyl2.Transform(TJ20)

	#Link 2

	link2=Body()
	link2.CreateBox(0.4, 0.1, 0.1, 0.2, 0.1, 0.3)
	scene.AddPart(link2)

	TL21 = [1, 0, 0, 0.2-0.05-0.025,
			0, 1, 0, 0,
			0, 0, 1, 0.075,
			0, 0, 0, 1]
		
	TL20 = [0] * 16

	vtkMatrix4x4.Multiply4x4(T20, TL21, TL20)

	link2.Transform(TL20)

	#Joint 3

	cyl3=Body()
	cyl3.CreateCylinder(0.025, 0.05, 36, 0.1, 0.2, 0.3)
	scene.AddPart(cyl3)

	TJ32 = [1, 0, 0, 0,
			0, 0, -1, 0,
			0, 1, 0, 0,
			0, 0, 0, 1]
	TJ30=[0] * 16

	vtkMatrix4x4.Multiply4x4(T30, TJ32, TJ30)

	cyl3.Transform(TJ30)

	#Link 3

	link3=Body()
	link3.CreateBox(0.4, 0.1, 0.1, 0.2, 0.1, 0.3)
	scene.AddPart(link3)

	TL31 = [1, 0, 0, 0.2-0.05-0.025,
			0, 1, 0, 0,
			0, 0, 1, 0.075,
			0, 0, 0, 1]
		
	TL30 = [0] * 16

	vtkMatrix4x4.Multiply4x4(T30, TL31, TL30)

	link3.Transform(TL30)

	#Prikaži na display

	display = Display(600, 600, "Hello", 10, 10, 10)

	scene.AddToDisplay(display)

	display.Run()


if __name__=='__main__':
    main()







