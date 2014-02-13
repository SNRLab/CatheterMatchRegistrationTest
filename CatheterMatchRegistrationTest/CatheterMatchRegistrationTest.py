import os
import unittest
import EditorLib
from __main__ import vtk, qt, ctk, slicer


#
# NeedleDetection
#

# Fixed Volume
needleDetectionOutputFixedVolume = slicer.mrmlScene.CreateNodeByClass("vtkMRMLScalarVolumeNode")
needleDetectionOutputFixedVolume.SetName("NeedleDetectionOutputFixedVolume")
needleDetectionOutputFixedVolume.LabelMapOn()
slicer.mrmlScene.AddNode(needleDetectionOutputFixedVolume)

needleDetectionOutputFixedTransform = slicer.mrmlScene.CreateNodeByClass("vtkMRMLLinearTransformNode")
needleDetectionOutputFixedTransform.SetName("NeedleDetectionOutputFixedTransform")
slicer.mrmlScene.AddNode(needleDetectionOutputFixedTransform)

# Moving Volume
needleDetectionOutputMovingVolume = slicer.mrmlScene.CreateNodeByClass("vtkMRMLScalarVolumeNode")
needleDetectionOutputMovingVolume.SetName("NeedleDetectionOutputMovingVolume")
needleDetectionOutputMovingVolume.LabelMapOn()
slicer.mrmlScene.AddNode(needleDetectionOutputMovingVolume)

needleDetectionOutputMovingTransform = slicer.mrmlScene.CreateNodeByClass("vtkMRMLLinearTransformNode")
needleDetectionOutputMovingTransform.SetName("NeedleDetectionOutputMovingTransform")
slicer.mrmlScene.AddNode(needleDetectionOutputMovingTransform)

# Parameters
needleDetectionParameters = {}
needleDetectionParameters["sigma1"] = 1
needleDetectionParameters["positivecontrast"] = False
needleDetectionParameters["minsigma"] = 3
needleDetectionParameters["maxsigma"] = 3
needleDetectionParameters["stepsigma"] = 1
needleDetectionParameters["minlinemeasure"] = 150
needleDetectionParameters["alpha1"] = 0.5
needleDetectionParameters["alpha2"] = 2.0
needleDetectionParameters["anglethreshold"] = 35
needleDetectionParameters["normal"] = 0.0,0.0,1.0
needleDetectionParameters["numberOfBins"] = 128
needleDetectionParameters["minimumObjectSize"] = 500
needleDetectionParameters["minPrincipalAxisLength"] = 180.0
needleDetectionParameters["closestPoint"] = 0.0,0.0,0.0  

#
# Cylinder Mask Generator
#

# Fixed Volume Mask
fixedProstateMask = slicer.mrmlScene.CreateNodeByClass("vtkMRMLScalarVolumeNode")
fixedProstateMask.LabelMapOn()
fixedProstateMask.SetName("FixedProstateMask")
slicer.mrmlScene.AddNode(fixedProstateMask)

# Moving Volume Mask
movingProstateMask = slicer.mrmlScene.CreateNodeByClass("vtkMRMLScalarVolumeNode")
movingProstateMask.LabelMapOn()
movingProstateMask.SetName("MovingProstateMask")
slicer.mrmlScene.AddNode(movingProstateMask)

# Parameters
cylinderRadius = 35
cylinderLength = 40
cylinderOffset = 10

modelToLabelMapParameters = {}
modelToLabelMapParameters["sampleDistance"] = 1
modelToLabelMapParameters["labelValue"] = 255

# 
# Catheter Match Registration
#

# Output volume
catheterRegistrationOutputVolume = slicer.mrmlScene.CreateNodeByClass("vtkMRMLScalarVolumeNode")
catheterRegistrationOutputVolume.SetName("CatheterMatchRegistrationOutputVolume")
slicer.mrmlScene.AddNode(catheterRegistrationOutputVolume)

# Parameters
catheterRegistrationParameters = {}
catheterRegistrationParameters["FixedImageSmoothingFactor"] = 0
catheterRegistrationParameters["MovingImageSmoothingFactor"] = 0
catheterRegistrationParameters["TestingMode"] = False
catheterRegistrationParameters["HistogramBins"] = 50
catheterRegistrationParameters["SpatialSamples"] = 10000
catheterRegistrationParameters["Iterations"] = 1000,1000,500,200
catheterRegistrationParameters["LearningRate"] = 0.01,0.005,0.0005,0.0002
catheterRegistrationParameters["TranslationScale"] = 100.0
catheterRegistrationParameters["TestOffset"] = 0.0
catheterRegistrationParameters["TestAngleOffset"] = 0.0
catheterRegistrationParameters["ResampledImageFileName"] = catheterRegistrationOutputVolume.GetID()

#
# CatheterMatchRegistrationTest
#

class CatheterMatchRegistrationTest:
  def __init__(self, parent):
    parent.title = "Catheter Match Registration Test" # TODO make this more human readable by adding spaces
    parent.categories = ["IGT"]
    parent.dependencies = []
    parent.contributors = ["Laurent Chauvin (BWH), Junichi Tokuda (BWH)"] # replace with "Firstname Lastname (Org)"
    parent.helpText = """
    This is an example of scripted loadable module bundled in an extension.
    """
    parent.acknowledgementText = """
    This file was originally developed by Jean-Christophe Fillion-Robin, Kitware Inc. and Steve Pieper, Isomics, Inc.  and was partially funded by NIH grant 3P41RR013218-12S1.
""" # replace with organization, grant and thanks.
    self.parent = parent

    # Add this test to the SelfTest module's list for discovery when the module
    # is created.  Since this module may be discovered before SelfTests itself,
    # create the list if it doesn't already exist.
    try:
      slicer.selfTests
    except AttributeError:
      slicer.selfTests = {}
    slicer.selfTests['CatheterMatchRegistrationTest'] = self.runTest

  def runTest(self):
    tester = CatheterMatchRegistrationTestTest()
    tester.runTest()

#
# qCatheterMatchRegistrationTestWidget
#

class CatheterMatchRegistrationTestWidget:
  def __init__(self, parent = None):
    if not parent:
      self.parent = slicer.qMRMLWidget()
      self.parent.setLayout(qt.QVBoxLayout())
      self.parent.setMRMLScene(slicer.mrmlScene)
    else:
      self.parent = parent
    self.layout = self.parent.layout()
    if not parent:
      self.setup()
      self.parent.show()

  def setup(self):
    # Instantiate and connect widgets ...

    #
    # Reload and Test area
    #
    reloadCollapsibleButton = ctk.ctkCollapsibleButton()
    reloadCollapsibleButton.text = "Reload && Test"
    self.layout.addWidget(reloadCollapsibleButton)
    reloadFormLayout = qt.QFormLayout(reloadCollapsibleButton)

    # reload button
    # (use this during development, but remove it when delivering
    #  your module to users)
    self.reloadButton = qt.QPushButton("Reload")
    self.reloadButton.toolTip = "Reload this module."
    self.reloadButton.name = "CatheterMatchRegistrationTest Reload"
    reloadFormLayout.addWidget(self.reloadButton)
    self.reloadButton.connect('clicked()', self.onReload)

    # reload and test button
    # (use this during development, but remove it when delivering
    #  your module to users)
    self.reloadAndTestButton = qt.QPushButton("Reload and Test")
    self.reloadAndTestButton.toolTip = "Reload this module and then run the self tests."
    reloadFormLayout.addWidget(self.reloadAndTestButton)
    self.reloadAndTestButton.connect('clicked()', self.onReloadAndTest)

    #
    # Parameters Area
    #
    parametersCollapsibleButton = ctk.ctkCollapsibleButton()
    parametersCollapsibleButton.text = "Parameters"
    self.layout.addWidget(parametersCollapsibleButton)

    # Layout within the dummy collapsible button
    parametersFormLayout = qt.QFormLayout(parametersCollapsibleButton)

    #
    # Fixed Volume to register
    #
    self.inputFixedSelector = slicer.qMRMLNodeComboBox()
    self.inputFixedSelector.nodeTypes = ( ("vtkMRMLScalarVolumeNode"), "" )
    self.inputFixedSelector.addAttribute( "vtkMRMLScalarVolumeNode", "LabelMap", 0 )
    self.inputFixedSelector.selectNodeUponCreation = True
    self.inputFixedSelector.addEnabled = False
    self.inputFixedSelector.removeEnabled = False
    self.inputFixedSelector.noneEnabled = False
    self.inputFixedSelector.showHidden = False
    self.inputFixedSelector.showChildNodeTypes = False
    self.inputFixedSelector.setMRMLScene( slicer.mrmlScene )
    self.inputFixedSelector.setToolTip( "Pick the fixed volume to register." )
    parametersFormLayout.addRow("Fixed Volume: ", self.inputFixedSelector)

    #
    # Moving Volume to register
    #
    self.inputMovingSelector = slicer.qMRMLNodeComboBox()
    self.inputMovingSelector.nodeTypes = ( ("vtkMRMLScalarVolumeNode"), "" )
    self.inputMovingSelector.addAttribute( "vtkMRMLScalarVolumeNode", "LabelMap", 0 )
    self.inputMovingSelector.selectNodeUponCreation = False
    self.inputMovingSelector.addEnabled = False
    self.inputMovingSelector.removeEnabled = False
    self.inputMovingSelector.noneEnabled = False
    self.inputMovingSelector.showHidden = False
    self.inputMovingSelector.showChildNodeTypes = False
    self.inputMovingSelector.setMRMLScene( slicer.mrmlScene )
    self.inputMovingSelector.setToolTip( "Pick the moving volume to register" )
    parametersFormLayout.addRow("Moving Volume: ", self.inputMovingSelector)

    #
    # Output registration matrix
    #
    self.outputTransformSelector = slicer.qMRMLNodeComboBox()
    self.outputTransformSelector.nodeTypes = ( ("vtkMRMLLinearTransformNode"), "")
    self.outputTransformSelector.selectNodeUponCreation = True
    self.outputTransformSelector.addEnabled = True
    self.outputTransformSelector.removeEnabled = True
    self.outputTransformSelector.renameEnabled = True
    self.outputTransformSelector.noneEnabled = False
    self.outputTransformSelector.showHidden = False
    self.outputTransformSelector.showChildNodeTypes = False
    self.outputTransformSelector.setMRMLScene( slicer.mrmlScene )
    self.outputTransformSelector.setToolTip( "Output registration matrix" )
    parametersFormLayout.addRow("Output Registration Transform: ", self.outputTransformSelector)

    #
    # Apply Button
    #
    self.applyButton = qt.QPushButton("Apply")
    self.applyButton.toolTip = "Run the algorithm."
    self.applyButton.enabled = False
    parametersFormLayout.addRow(self.applyButton)

    # connections
    self.applyButton.connect('clicked(bool)', self.onApplyButton)
    self.inputFixedSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)
    self.inputMovingSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)
    self.outputTransformSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)

    # Add vertical spacer
    self.layout.addStretch(1)

  def cleanup(self):
    pass

  def onSelect(self):
    self.applyButton.enabled = self.inputFixedSelector.currentNode() and self.inputMovingSelector.currentNode() and self.outputTransformSelector.currentNode()

  def onApplyButton(self):
    logic = CatheterMatchRegistrationTestLogic()
    print("Run the algorithm")
    logic.run(self.inputFixedSelector.currentNode(), self.inputMovingSelector.currentNode(), self.outputTransformSelector.currentNode())

  def onReload(self,moduleName="CatheterMatchRegistrationTest"):
    """Generic reload method for any scripted module.
    ModuleWizard will subsitute correct default moduleName.
    """
    globals()[moduleName] = slicer.util.reloadScriptedModule(moduleName)

  def onReloadAndTest(self,moduleName="CatheterMatchRegistrationTest"):
    try:
      self.onReload()
      evalString = 'globals()["%s"].%sTest()' % (moduleName, moduleName)
      tester = eval(evalString)
      tester.runTest()
    except Exception, e:
      import traceback
      traceback.print_exc()
      qt.QMessageBox.warning(slicer.util.mainWindow(), 
          "Reload and Test", 'Exception!\n\n' + str(e) + "\n\nSee Python Console for Stack Trace")


#
# CatheterMatchRegistrationTestLogic
#

class CatheterMatchRegistrationTestLogic:
  """This class should implement all the actual 
  computation done by your module.  The interface 
  should be such that other python code can import
  this class and make use of the functionality without
  requiring an instance of the Widget
  """
  def __init__(self):
    pass

  def hasImageData(self,volumeNode):
    """This is a dummy logic method that 
    returns true if the passed in volume
    node has valid image data
    """
    if not volumeNode:
      print('no volume node')
      return False
    if volumeNode.GetImageData() == None:
      print('no image data')
      return False
    return True

  def delayDisplay(self,message,msec=1000):
    #
    # logic version of delay display
    #
    print(message)
    self.info = qt.QDialog()
    self.infoLayout = qt.QVBoxLayout()
    self.info.setLayout(self.infoLayout)
    self.label = qt.QLabel(message,self.info)
    self.infoLayout.addWidget(self.label)
    qt.QTimer.singleShot(msec, self.info.close)
    self.info.exec_()

  def run(self,inputFixedVolume,inputMovingVolume,outputTransform):
    """
    Run the actual algorithm
    """

    self.delayDisplay('Running the aglorithm')

    # Get NeedleDetectionCLI module
    needleDetectionCLI = slicer.modules.needledetection

    # Find needle for fixed volume
    needleDetectionParameters["inputVolume"] = inputFixedVolume.GetID()
    needleDetectionParameters["outputVolume"] = needleDetectionOutputFixedVolume.GetID()
    needleDetectionParameters["needleTransform"] = needleDetectionOutputFixedTransform.GetID()
    slicer.cli.run(needleDetectionCLI, None, needleDetectionParameters, wait_for_completion=True)

    # Find needle for moving volume
    needleDetectionParameters["inputVolume"] = inputMovingVolume.GetID()
    needleDetectionParameters["outputVolume"] = needleDetectionOutputMovingVolume.GetID()
    needleDetectionParameters["needleTransform"] = needleDetectionOutputMovingTransform.GetID()
    slicer.cli.run(needleDetectionCLI, None, needleDetectionParameters, wait_for_completion=True)
    
    # Generate cylinder mask for fixed volume
    self.GenerateCylinderLabelMap(needleDetectionOutputFixedTransform, inputFixedVolume, fixedProstateMask, cylinderRadius, cylinderLength, cylinderOffset, 4)
    
    # Generate cylinder mask for moving volume
    self.GenerateCylinderLabelMap(needleDetectionOutputMovingTransform, inputMovingVolume, movingProstateMask, cylinderRadius, cylinderLength, cylinderOffset, 4)

    # Replace label 255 by 1
#    replaceLabel = EditorLib.ChangeLabelEffectOptions()
#    parameterNode = replaceLabel.editUtil.getParameterNode()
#    parameterNode.SetDisableModifiedEvent(1)
#    parameterNode.SetParameter("ChangeLabelEffect,inputColor","255")
#    parameterNode.SetParameter("ChangeLabelEffect,outputColor","1")
#    parameterNode.InvokePendingModifiedEvent()
#
#    replaceLabel.editUtil.getCompositeNode().SetLabelVolumeID(fixedProstateMask.GetID())
#    replaceLabel.onApply()
#    replaceLabel.editUtil.getCompositeNode().SetLabelVolumeID(movingProstateMask.GetID())
#    replaceLabel.onApply()

    # Get CatheterMatchRegistrationCLI module
    catheterRegistrationCLI = slicer.modules.cathetermatchregistration

    # Register fixed and moving image
    catheterRegistrationParameters["FixedCatheterTransform"] = needleDetectionOutputFixedTransform.GetID()
    catheterRegistrationParameters["MovingCatheterTransform"] = needleDetectionOutputMovingTransform.GetID()
    catheterRegistrationParameters["FixedImageFileName"] = inputFixedVolume.GetID()
    catheterRegistrationParameters["MovingImageFileName"] = inputMovingVolume.GetID()
    catheterRegistrationParameters["FixedMaskImageFileName"] = fixedProstateMask.GetID()
    catheterRegistrationParameters["MovingMaskImageFileName"] = movingProstateMask.GetID()
    catheterRegistrationParameters["OutputTransform"] = outputTransform.GetID()
    slicer.cli.run(catheterRegistrationCLI, None, catheterRegistrationParameters, wait_for_completion=True)

    # Put the moving volume under registration transform
    inputMovingVolume.SetAndObserveTransformNodeID(outputTransform.GetID())

    return True


  def GenerateCylinderLabelMap(self,needleTransform, image, outputMask, radius, length, offset, refineRate = 3):

    # Get needle matrix
    needleMatrix = needleTransform.GetMatrixTransformToParent()
    
    # Create cylinder
    cylinderSource = vtk.vtkCylinderSource()
    cylinderSource.SetCenter(0.0, 0.0, 0.0)
    cylinderSource.SetRadius(radius)
    cylinderSource.SetHeight(length)
    cylinderSource.SetResolution(30)
    cylinderSource.Update()

    # Move cylinder to needleTransform
    transformCylinder = vtk.vtkTransform()
    transformCylinder.RotateX(90)
    transformCylinder.Translate(0.0, -length/2, 0.0)
    transformCylinder.PostMultiply()
    transformCylinder.Concatenate(needleMatrix)
    transformCylinder.Update()

    transformPolyData = vtk.vtkTransformPolyDataFilter()
    transformPolyData.SetInputConnection(cylinderSource.GetOutputPort())
    transformPolyData.SetTransform(transformCylinder)
    transformPolyData.Update()
    
    # Add nodes to the scene
    modelDisplayNode = slicer.mrmlScene.CreateNodeByClass("vtkMRMLModelDisplayNode")
    modelDisplayNode.SetColor(1.0,0.0,0.0)
    slicer.mrmlScene.AddNode(modelDisplayNode)

    modelNode = slicer.mrmlScene.CreateNodeByClass("vtkMRMLModelNode")
    modelNode.SetName("CylinderModel")
    modelNode.SetAndObservePolyData(transformPolyData.GetOutput())
    modelNode.SetAndObserveDisplayNodeID(modelDisplayNode.GetID())
    modelNode.Modified()
    slicer.mrmlScene.AddNode(modelNode)

    # Call ModelToLabelMap module
    cliNode = self.runModelToLabelMap(image, modelNode, outputMask, refineRate)

  def runModelToLabelMap(self,image, modelNode, outputMask, refineRate):

    # Make sure all polygons are triangles
    triangle = vtk.vtkTriangleFilter()
    triangle.SetInput(modelNode.GetPolyData())
    triangle.Update()
    modelNode.SetAndObservePolyData(triangle.GetOutput())

    # Increase number of polygons in the mesh to avoid having holes
    # in contour, which confuse ModelToLabelMap when flooding
    # (flooding the whole labelmap if contour is not closed)
    refine = vtk.vtkLoopSubdivisionFilter()
    refine.SetInput(modelNode.GetPolyData())
    refine.SetNumberOfSubdivisions(refineRate)
    refine.Update()
    modelNode.SetAndObservePolyData(refine.GetOutput())

    # Set ModelToLabelMap parameters
    modelToLabelMapParameters["InputVolume"] = image.GetID()
    modelToLabelMapParameters["surface"] = modelNode.GetID()
    modelToLabelMapParameters["OutputVolume"] = outputMask.GetID()

    # Run ModelToLabelMap
    modelToLabelMapCLI = slicer.modules.modeltolabelmap
    slicer.cli.run(modelToLabelMapCLI, None, modelToLabelMapParameters, wait_for_completion=True)


class CatheterMatchRegistrationTestTest(unittest.TestCase):
  """
  This is the test case for your scripted module.
  """

  def delayDisplay(self,message,msec=1000):
    """This utility method displays a small dialog and waits.
    This does two things: 1) it lets the event loop catch up
    to the state of the test so that rendering and widget updates
    have all taken place before the test continues and 2) it
    shows the user/developer/tester the state of the test
    so that we'll know when it breaks.
    """
    print(message)
    self.info = qt.QDialog()
    self.infoLayout = qt.QVBoxLayout()
    self.info.setLayout(self.infoLayout)
    self.label = qt.QLabel(message,self.info)
    self.infoLayout.addWidget(self.label)
    qt.QTimer.singleShot(msec, self.info.close)
    self.info.exec_()

  def setUp(self):
    """ Do whatever is needed to reset the state - typically a scene clear will be enough.
    """
    slicer.mrmlScene.Clear(0)

  def runTest(self):
    """Run as few or as many tests as needed here.
    """
    self.setUp()
    self.test_CatheterMatchRegistrationTest1()

  def test_CatheterMatchRegistrationTest1(self):
    """ Ideally you should have several levels of tests.  At the lowest level
    tests sould exercise the functionality of the logic with different inputs
    (both valid and invalid).  At higher levels your tests should emulate the
    way the user would interact with your code and confirm that it still works
    the way you intended.
    One of the most important features of the tests is that it should alert other
    developers when their changes will have an impact on the behavior of your
    module.  For example, if a developer removes a feature that you depend on,
    your test should break so they know that the feature is needed.
    """

    self.delayDisplay("Starting the test")
    #
    # first, get some data
    #
    import urllib
    downloads = (
        ('http://slicer.kitware.com/midas3/download?items=5767', 'FA.nrrd', slicer.util.loadVolume),
        )

    for url,name,loader in downloads:
      filePath = slicer.app.temporaryPath + '/' + name
      if not os.path.exists(filePath) or os.stat(filePath).st_size == 0:
        print('Requesting download %s from %s...\n' % (name, url))
        urllib.urlretrieve(url, filePath)
      if loader:
        print('Loading %s...\n' % (name,))
        loader(filePath)
    self.delayDisplay('Finished with download and loading\n')

    volumeNode = slicer.util.getNode(pattern="FA")
    logic = CatheterMatchRegistrationTestLogic()
    self.assertTrue( logic.hasImageData(volumeNode) )
    self.delayDisplay('Test passed!')
