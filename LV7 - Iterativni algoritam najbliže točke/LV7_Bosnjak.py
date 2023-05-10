import vtk
import time
import math
import multiprocessing
import numpy as np
import time

from vtkmodules.vtkRenderingCore import vtkRenderWindow, vtkRenderer, vtkRenderWindowInteractor, vtkPolyDataMapper, vtkActor, vtkTextActor
from vtkmodules.vtkIOPLY import vtkPLYReader
from vtkmodules.vtkCommonDataModel import vtkIterativeClosestPointTransform
from vtkmodules.vtkFiltersGeneral import vtkTransformPolyDataFilter, vtkDistancePolyDataFilter
from vtkmodules.vtkRenderingAnnotation import vtkScalarBarActor

maxIter=100
maxLandmarks=1000

def VisualizeModel(targetPath, sourcePath):

    start=time.time() #Početak računanja vremena

    plyReader = vtkPLYReader()
    plyReader.SetFileName(targetPath) #Putanja do željene datoteke
    plyReader.Update() #Učitaj  
    targetPD = plyReader.GetOutput() #Učitana geometrija se nalazi u vtkPolyData objektu

    plyReader_ = vtkPLYReader()
    plyReader_.SetFileName(sourcePath) #Putanja do željene datoteke
    plyReader_.Update() #Učitaj  
    sourcePD = plyReader_.GetOutput() #Učitana geometrija se nalazi u vtkPolyData objektu

    interactor = vtkRenderWindowInteractor()

    mapper_source = vtkPolyDataMapper()
    mapper_target = vtkPolyDataMapper()
    mapper_icp = vtkPolyDataMapper()

    renderer = vtkRenderer()
    renderer.SetBackground(1.0, 1.0, 1.0) #Bijela pozadina
    renderer.ResetCamera() #Centriraj kameru tako da obuhvaća objekte na sceni

    window = vtkRenderWindow()
    window.AddRenderer(renderer) #Moguće je dodati i više renderera na jedan prozor
    window.SetSize(800, 600) #Veličina prozora na ekranu
    window.SetWindowName("Scena") #Naziv prozora
    window.Render() #Renderaj scenu

    mapper_target.SetInputData(targetPD)

    actor_target = vtkActor()
    actor_target.SetMapper(mapper_target) #Povezujemo ga s mapperom za određeni tip podataka
    actor_target.GetProperty().SetColor(1.0, 0.0, 0.0) #Objekt će biti obojan u crveno
    actor_target.GetProperty().SetPointSize(5) #Veličina će biti 5x5 piksela po točci
    actor_target.GetProperty().SetOpacity(0.5)
    renderer.AddActor(actor_target) #Dodajemo ga na popis objekata na sceni

    icp = vtkIterativeClosestPointTransform()
    icp.SetSource(sourcePD) #Ulazni objekt (početna poza objekta)
    icp.SetTarget(targetPD) #Konačni objekt (željena poza objekta)
    icp.GetLandmarkTransform().SetModeToRigidBody() #Potrebni način rada je transformacija za kruta tijela
    icp.SetMaximumNumberOfIterations(maxIter) #Željeni broj iteracija
    icp.SetMaximumNumberOfLandmarks(maxLandmarks) #Koliko parova točaka da se koristi prilikom minimiziranja cost funkcije
    icp.Update() #Provedi algoritam

    icpTransformFilter = vtkTransformPolyDataFilter()
    icpTransformFilter.SetInputData(sourcePD) #Objekt s početnim koordinatama
    icpTransformFilter.SetTransform(icp) #transformiramo na novi položaj koristeći transformacijsku matricu
    icpTransformFilter.Update()
    icpResultPD = icpTransformFilter.GetOutput() #Transformirani (novi) objekt

    mapper_icp.SetInputData(icpResultPD)
    actor_output = vtkActor()
    actor_output.SetMapper(mapper_icp) #Povezujemo ga s mapperom za određeni tip podataka
    actor_output.GetProperty().SetColor(0.0, 0.0, 1.0) #Objekt će biti obojan u plavo
    actor_output.GetProperty().SetPointSize(5) #Veličina će biti 5x5 piksela po točci
    renderer.AddActor(actor_output) #Dodajemo ga na popis objekata na sceni

    end=time.time() #Kraj računanja vremena

    actor_time=vtkTextActor() #Stvaranje tekstualnog aktora
    actor_time.SetInput("Vrijeme izvršavana: " + str(end-start)) #Pridruživanje stringa njegovoj vrijednosti
    actor_time.SetPosition(10,40) #Postavljanje pozicije unutar window-a
    actor_time.GetTextProperty().SetFontSize(24) #Veličina fonta
    actor_time.GetTextProperty().SetColor(0,0,0) #Postavljanje boje 
    renderer.AddActor2D(actor_time) #Dodavanje aktora na scenu

    actor_maxIters=vtkTextActor()
    actor_maxIters.SetInput("Broj iteracija ICP algoritma: " + str(maxIter))
    actor_maxIters.SetPosition(10,70)
    actor_maxIters.GetTextProperty().SetFontSize(24)
    actor_maxIters.GetTextProperty().SetColor(0,0,0)
    renderer.AddActor2D(actor_maxIters)

    actor_maxLandmarks=vtkTextActor()
    actor_maxLandmarks.SetInput("Broj parova točaka: " + str(maxLandmarks))
    actor_maxLandmarks.SetPosition(10,100)
    actor_maxLandmarks.GetTextProperty().SetFontSize(24)
    actor_maxLandmarks.GetTextProperty().SetColor(0,0,0)
    renderer.AddActor2D(actor_maxLandmarks)

    window.Render()
    interactor.SetRenderWindow(window)
    interactor.Start() #Pokretanje interaktora, potrebno kako se vtk prozor ne bi odmah zatvorio


def main():
    targetPath="./LV/LV7/bunny.ply"
    sourcePaths=[   "./LV/LV7/bunny_t1.ply",
                    "./LV/LV7/bunny_t2.ply",
                    "./LV/LV7/bunny_t3.ply",
                    "./LV/LV7/bunny_t4_parc.ply",
                    "./LV/LV7/bunny_t5_parc.ply"
    ]
    for sourcePath in sourcePaths:
        VisualizeModel(targetPath,sourcePath)


if __name__=='__main__':
    main()



