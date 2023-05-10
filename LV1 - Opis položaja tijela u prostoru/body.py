from vtkmodules.vtkFiltersSources import vtkCylinderSource, vtkCubeSource
from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkRenderingCore import vtkActor, vtkPolyDataMapper

class Body:
    def __init__(self):
        self.pose = vtkTransform()
        self.pose.PostMultiply()
        self.actor = None
        self.caption = None
        self.parts = []

    def CreateBox(self, a, b, c, red, green, blue):
        cubeSource = vtkCubeSource()
        cubeSource.SetXLength(a)
        cubeSource.SetYLength(b)
        cubeSource.SetZLength(c)

        mapper = vtkPolyDataMapper()
        mapper.SetInputConnection(cubeSource.GetOutputPort())
        self.actor = vtkActor()
        self.actor.SetMapper(mapper)
        self.actor.GetProperty().SetColor(red, green, blue)

    def CreateCylinder(self, r, h, res, red, green, blue):
        cylinderSource = vtkCylinderSource()
        cylinderSource.SetRadius(r)
        cylinderSource.SetHeight(h)
        cylinderSource.SetResolution(res)

        mapper = vtkPolyDataMapper()
        mapper.SetInputConnection(cylinderSource.GetOutputPort())
        self.actor = vtkActor()
        self.actor.SetMapper(mapper)
        self.actor.GetProperty().SetColor(red, green, blue)

    def AddPart(self, part):
        self.parts.append(part)

    def Transform(self, T):
        self.pose.SetMatrix(T)

    def AddToRenderer(self, renderer, TIn = None):
        if TIn:
            T = TIn
            if self.actor:
                t_ = T.GetPosition()
                self.actor.SetPosition(t_)
                q_ = T.GetOrientationWXYZ()
                self.actor.RotateWXYZ(q_[0], q_[1], q_[2], q_[3])
        else:
            T = vtkTransform()
            T.Identity()

        if self.actor:
            renderer.AddActor(self.actor)
        
        # if caption

        T_ = vtkTransform()

        for part in self.parts:
            T_.Identity()
            T_.Concatenate(T)
            T_.Concatenate(part.pose)

            part.AddToRenderer(renderer, T_)
    
    def AddToDisplay(self, window):
        self. AddToRenderer(window.GetRenderer())