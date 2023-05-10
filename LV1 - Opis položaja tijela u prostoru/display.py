from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkRenderingCore import vtkRenderWindow, vtkRenderWindowInteractor, vtkRenderer
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleTrackballCamera
from vtkmodules.vtkRenderingAnnotation import vtkAxesActor

class Display:
    def __init__(self, width, height, windowName, red, green, blue):
        self.renderer = vtkRenderer()
        self.renderWindow = vtkRenderWindow()
        self.renderWindow.AddRenderer(self.renderer)
        self.renderWindow.SetSize(width, height)
        self.renderWindow.SetWindowName(windowName)
        self.renderWindowInteractor = vtkRenderWindowInteractor()
        self.renderWindowInteractor.SetRenderWindow(self.renderWindow)
        style = vtkInteractorStyleTrackballCamera()
        self.renderWindowInteractor.SetInteractorStyle(style)
        self.renderer.SetBackground(red, green, blue)

        #Axes
        axes = vtkAxesActor()
        transform = vtkTransform()
        transform.Translate(-0.5, 0.0, 0.0)

        axes.SetUserTransform(transform)
        axes.SetTotalLength(0.2, 0.2, 0.2)
        axes.GetXAxisCaptionActor2D().GetTextActor().SetTextScaleModeToNone()
        axes.GetYAxisCaptionActor2D().GetTextActor().SetTextScaleModeToNone()
        axes.GetZAxisCaptionActor2D().GetTextActor().SetTextScaleModeToNone()

        self.renderer.AddActor(axes)

    def Run(self):
        self.renderWindow.Render()
        self.renderWindowInteractor.Start()

    def GetRenderer(self):
        return self.renderer