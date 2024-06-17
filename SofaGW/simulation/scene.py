import Sofa
import Sofa.SofaGL

import os
import numpy as np
import pygame
from scipy.spatial.transform import Rotation as R
import time
import PIL.Image

import OpenGL.GL
import OpenGL.GLU


# For using SOFA.
class SOFA():
    def __init__(self, vessel_filename):
        self.display_size = (640, 480)
        self.vessel_filename = vessel_filename
        self.start_scene()

    def start_scene(self):
        self.root = Sofa.Core.Node("root")
        self.createScene()
        Sofa.Simulation.init(self.root)
        self.init_display()
        for _ in range(10): self.step(realtime=False)
    
    def createScene(self):
        self.root.gravity = [0,0,0]
        self.root.dt = 0.01
        self.root.addObject('RequiredPlugin', pluginName=['BeamAdapter',
                                                        'SofaMiscCollision',
                                                        'SofaConstraint',
                                                        'SofaImplicitOdeSolver',
                                                        'SofaGeneralLinearSolver',
                                                        'SofaBoundaryCondition',
                                                        'SofaDeformable',
                                                        'SofaTopologyMapping',
                                                        'SofaOpenglVisual',
                                                        'SofaMeshCollision',
                                                        'Sofa.Component.Collision.Detection.Algorithm',
                                                        'Sofa.Component.IO.Mesh',
                                                        'Sofa.GL.Component.Rendering3D',
                                                        'Sofa.GL.Component.Shader'
                                                        ])
        self.root.addObject('FreeMotionAnimationLoop') # All the scenes in SOFA must include an AnimationLoop.
        self.root.addObject('VisualStyle', displayFlags=['showVisualModels',
                                                    # 'showCollisionModels',
                                                    'hideCollisionModels',
                                                    'hideMappings',
                                                    'hideForceFields',
                                                    ])
        self.root.addObject('LCPConstraintSolver', mu='0.1', tolerance='1e-10', maxIt='1000', build_lcp='false')
        self.root.addObject('DefaultPipeline', draw='0', depth='6', verbose='1')
        self.root.addObject('BruteForceBroadPhase', name='N2')
        self.root.addObject('BVHNarrowPhase')
        self.root.addObject('LocalMinDistance', contactDistance='1', alarmDistance='3', name='localmindistance', angleCone='0.02')
        self.root.addObject('DefaultContactManager', name='Response', response='FrictionContactConstraint')



        ####################### >>> Make Instrument combining catheter, guidewire and coils. >>>
        ## Catheter
        '''
        # numEdges: The number of beams.
        # length : The limit of how long catheter can be pulled.
        '''
        topoLines_cath = self.root.addChild('topoLines_cath')
        topoLines_cath.addObject('WireRestShape', template='Rigid3d', printLog=False, name='catheterRestShape', length=1000.0, straightLength=600, spireDiameter=4000.0, spireHeight=0.0,
                    densityOfBeams=[40, 10], numEdges=200, numEdgesCollis=[40, 20], youngModulus=20000, youngModulusExtremity=10000)
        topoLines_cath.addObject('EdgeSetTopologyContainer', name='meshLinesCath')
        topoLines_cath.addObject('EdgeSetTopologyModifier', name='Modifier')
        topoLines_cath.addObject('EdgeSetGeometryAlgorithms', name='GeomAlgo', template='Rigid3d')
        topoLines_cath.addObject('MechanicalObject', template='Rigid3d', name='dofTopo1')
        ## Guide
        topoLines_guide = self.root.addChild('topoLines_guide')
        topoLines_guide.addObject('WireRestShape', template='Rigid3d', printLog=False, name='GuideRestShape', length=1000.0, straightLength=950.0, spireDiameter=30, spireHeight=0.0,
                        densityOfBeams=[60, 10], numEdges=200, numEdgesCollis=[100, 20], youngModulus=1200, youngModulusExtremity=120)
        topoLines_guide.addObject('EdgeSetTopologyContainer', name='meshLinesGuide')
        topoLines_guide.addObject('EdgeSetTopologyModifier', name='Modifier')
        topoLines_guide.addObject('EdgeSetGeometryAlgorithms', name='GeomAlgo', template='Rigid3d')
        topoLines_guide.addObject('MechanicalObject', template='Rigid3d', name='dofTopo2')
        ## Coils
        topoLines_coils = self.root.addChild('topoLines_coils')
        topoLines_coils.addObject('WireRestShape', template='Rigid3d', printLog=False, name='CoilRestShape', length=600.0, straightLength=540.0, spireDiameter=7, spireHeight=5.0,
                        densityOfBeams=[40, 20], numEdges=400, numEdgesCollis=[30, 30], youngModulus=168000, youngModulusExtremity=168000)
        topoLines_coils.addObject('EdgeSetTopologyContainer', name='meshLinesCoils')
        topoLines_coils.addObject('EdgeSetTopologyModifier', name='Modifier')
        topoLines_coils.addObject('EdgeSetGeometryAlgorithms', name='GeomAlgo', template='Rigid3d')
        topoLines_coils.addObject('MechanicalObject', template='Rigid3d', name='dofTopo3')

        ## Combined Instrument
        startingPos=[0,0,0] + list(R.from_euler('Y',-90,True).as_quat())
        InstrumentCombined = self.root.addChild('InstrumentCombined')
        InstrumentCombined.addObject('EulerImplicitSolver', rayleighStiffness=0.2, rayleighMass=0.1, printLog=False)
        InstrumentCombined.addObject('BTDLinearSolver', subpartSolve=False, verification=False, verbose=False)
        InstrumentCombined.addObject('RegularGridTopology', name='meshLinesCombined', nx=60, ny=1, nz=1, xmin=0.0, xmax=1.0, ymin=0, ymax=0, zmin=1, zmax=1)
        InstrumentCombined.addObject('MechanicalObject', template='Rigid3d', name='DOFs', showIndices=False, 
                                    translation=startingPos[:3], 
                                    ry=-90
                                    #rotation=R.from_quat(startingPos[3:]).as_euler('XYZ', degrees=True)
                                    )
        # Combine catheter
        InstrumentCombined.addObject('WireBeamInterpolation', name='InterpolCatheter', WireRestShape='@../topoLines_cath/catheterRestShape', radius=1, printLog=False)
        InstrumentCombined.addObject('AdaptiveBeamForceFieldAndMass', name='CatheterForceField', interpolation='@InterpolCatheter', massDensity=0.00000155)	
        # Combine guidewire
        InstrumentCombined.addObject('WireBeamInterpolation', name='InterpolGuide', WireRestShape='@../topoLines_guide/GuideRestShape', radius=0.9, printLog=False)
        InstrumentCombined.addObject('AdaptiveBeamForceFieldAndMass', name='GuideForceField', interpolation='@InterpolGuide', massDensity=0.00000155)
        # Combine coils
        InstrumentCombined.addObject('WireBeamInterpolation', name='InterpolCoils', WireRestShape='@../topoLines_coils/CoilRestShape', radius=0.1, printLog=False)
        InstrumentCombined.addObject('AdaptiveBeamForceFieldAndMass', name='CoilsForceField', interpolation='@InterpolCoils', massDensity=0.000021)	
        # Controller of instrument
        InstrumentCombined.addObject('InterventionalRadiologyController', template='Rigid3d', name='m_ircontroller', printLog=False, xtip=[1, 21, 0], step=3, rotationInstrument=[0, 0, 0],
                            controlledInstrument=0, startingPos=startingPos, 
                            speed=0, instruments=['InterpolCatheter', 'InterpolGuide', 'InterpolCoils'])
        # Fix the hole.
        InstrumentCombined.addObject('LinearSolverConstraintCorrection', printLog=False, wire_optimization=True)
        InstrumentCombined.addObject('FixedConstraint', name='FixedConstraint', indices=0)
        InstrumentCombined.addObject('RestShapeSpringsForceField', points='@m_ircontroller.indexFirstNode', stiffness=1e8, angularStiffness=1e8)
        # Set collision model.
        Collis = InstrumentCombined.addChild('Collis', activated=True)
        Collis.addObject('EdgeSetTopologyContainer', name='collisEdgeSet')
        Collis.addObject('EdgeSetTopologyModifier', name='colliseEdgeModifier')
        Collis.addObject('MechanicalObject', name='CollisionDOFs')
        Collis.addObject('MultiAdaptiveBeamMapping', controller='../m_ircontroller', useCurvAbs=True, printLog=False, name='collisMap')
        Collis.addObject('LineCollisionModel', proximity=0.0, group=1)
        Collis.addObject('PointCollisionModel', proximity=0.0, group=1)
        
        ## Visualize catheter
        VisuCatheter = InstrumentCombined.addChild('VisuCatheter', activated=True)
        VisuCatheter.addObject('MechanicalObject', name='Quads')
        VisuCatheter.addObject('QuadSetTopologyContainer', name='ContainerCath')
        VisuCatheter.addObject('QuadSetTopologyModifier', name='Modifier')
        VisuCatheter.addObject('QuadSetGeometryAlgorithms', name='GeomAlgo', template='Vec3d')
        VisuCatheter.addObject('Edge2QuadTopologicalMapping', nbPointsOnEachCircle=10, radius=2, input='@../../topoLines_cath/meshLinesCath', output='@ContainerCath', flipNormals=True)
        VisuCatheter.addObject('AdaptiveBeamMapping', name='VisuMapCath', useCurvAbs=True, printLog=False, interpolation='@../InterpolCatheter', input='@../DOFs', output='@Quads', isMechanical=False)
        VisuCatheterOgl = VisuCatheter.addChild('VisuOgl', activated=True)
        VisuCatheterOgl.addObject('OglModel', name='Visual', color=[0.7, 0.7, 0.7, 0.9], quads='@../ContainerCath.quads', material='texture Ambient 1 0.2 0.2 0.2 0.0 Diffuse 1 1.0 1.0 1.0 1.0 Specular 1 1.0 1.0 1.0 1.0 Emissive 0 0.15 0.05 0.05 0.0 Shininess 1 20')
        VisuCatheterOgl.addObject('IdentityMapping', input='@../Quads', output='@Visual')
        ## Visualize guidewire
        VisuGuide = InstrumentCombined.addChild('VisuGuide', activated=True)
        VisuGuide.addObject('MechanicalObject', name='Quads')
        VisuGuide.addObject('QuadSetTopologyContainer', name='ContainerGuide')
        VisuGuide.addObject('QuadSetTopologyModifier', name='Modifier')
        VisuGuide.addObject('QuadSetGeometryAlgorithms', name='GeomAlgo', template='Vec3d')
        VisuGuide.addObject('Edge2QuadTopologicalMapping', nbPointsOnEachCircle=10, radius=1, input='@../../topoLines_guide/meshLinesGuide', output='@ContainerGuide', flipNormals=True, listening=True)
        VisuGuide.addObject('AdaptiveBeamMapping', name='visuMapGuide', useCurvAbs=True, printLog=False, interpolation='@../InterpolGuide', input='@../DOFs', output='@Quads', isMechanical=False)
        VisuGuideOgl = VisuGuide.addChild('VisuOgl')
        VisuGuideOgl.addObject('OglModel', name='Visual', color=[0.2, 0.2, 0.8, 0.9], material='texture Ambient 1 0.2 0.2 0.2 0.0 Diffuse 1 1.0 1.0 1.0 1.0 Specular 1 1.0 1.0 1.0 1.0 Emissive 0 0.15 0.05 0.05 0.0 Shininess 1 20', quads='@../ContainerGuide.quads')
        VisuGuideOgl.addObject('IdentityMapping', input='@../Quads', output='@Visual')
        ## Visualize coils
        VisuCoils = InstrumentCombined.addChild('VisuCoils', activated=True)
        VisuCoils.addObject('MechanicalObject', name='Quads')
        VisuCoils.addObject('QuadSetTopologyContainer', name='ContainerCoils')
        VisuCoils.addObject('QuadSetTopologyModifier', name='Modifier')
        VisuCoils.addObject('QuadSetGeometryAlgorithms', name='GeomAlgo', template='Vec3d')
        VisuCoils.addObject('Edge2QuadTopologicalMapping', nbPointsOnEachCircle=10, radius=0.3, input='@../../topoLines_coils/meshLinesCoils', output='@ContainerCoils', flipNormals=True, listening=True)
        VisuCoils.addObject('AdaptiveBeamMapping', name='visuMapCoils', useCurvAbs=True, printLog=False, interpolation='@../InterpolCoils', input='@../DOFs', output='@Quads', isMechanical=False)
        VisuCoilsOgl = VisuCoils.addChild('VisuOgl')
        VisuCoilsOgl.addObject('OglModel', name='Visual', color=[0.2, 0.8, 0.2, 0.9], material='texture Ambient 1 0.2 0.2 0.2 0.0 Diffuse 1 1.0 1.0 1.0 1.0 Specular 1 1.0 1.0 1.0 1.0 Emissive 0 0.15 0.05 0.05 0.0 Shininess 1 20', quads='@../ContainerCoils.quads')
        VisuCoilsOgl.addObject('IdentityMapping', input='@../Quads', output='@Visual')
        




        # rootNode/CollisionModel
        Vessels = self.root.addChild('Vessels')
        ####### 이것만 바꾸면 됨
        
        Vessels.addObject('MeshObjLoader', filename=self.vessel_filename, flipNormals='1',
                                        triangulate='true', name='meshLoader')
        #######################
        Vessels.addObject('Mesh', position='@meshLoader.position', triangles='@meshLoader.triangles')
        Vessels.addObject('MechanicalObject', position='0 0 400', scale='3', name='DOFs1', ry='90')
        Vessels.addObject('TriangleCollisionModel', moving='0', simulated='0')
        Vessels.addObject('LineCollisionModel', moving='0', simulated='0')
        Vessels.addObject('PointCollisionModel', moving='0', simulated='0')
        #Vessels.addObject('OglModel', color='1 0 0 0.3', scale='3', fileMesh='phantom.obj',
        #                                 ry='90', name='Visual')
        Vessels.addObject('OglModel', color='1 0 0 0.3', scale='3', src='@meshLoader',
                                        ry='90', name='Visual')



        
        # Set camera.
        source = [-600,0,300]
        lookAt = source+np.array([1,0,0])
        orientation = [ 0, -0.70710678, 0, 0.70710678]
        self.root.addObject("LightManager")
        self.root.addObject("DirectionalLight", direction=[-1,0,0])
        self.root.addObject('InteractiveCamera', name='camera', position=source,
                        lookAt=lookAt, orientation=orientation)
        # self.root.camera.findData('position').value = []
        # self.root.camera.findData('lookAt').value = []
        # self.root.camera.findData('orientation').value = []
    
    def init_display(self):
        """Initialize OpenGL and pygame.
        """
        display_size = self.display_size
        pygame.display.init()
        pygame.display.set_mode(display_size, pygame.DOUBLEBUF | pygame.OPENGL)

        OpenGL.GL.glClear(OpenGL.GL.GL_COLOR_BUFFER_BIT | OpenGL.GL.GL_DEPTH_BUFFER_BIT)
        OpenGL.GL.glEnable(OpenGL.GL.GL_LIGHTING)
        OpenGL.GL.glEnable(OpenGL.GL.GL_DEPTH_TEST)
        Sofa.SofaGL.glewInit()
        Sofa.Simulation.initVisual(self.root)
        Sofa.Simulation.initTextures(self.root)
        OpenGL.GL.glMatrixMode(OpenGL.GL.GL_PROJECTION)
        OpenGL.GL.glLoadIdentity()
        OpenGL.GLU.gluPerspective(45, (display_size[0] / display_size[1]), 0.1, 50.0)

        OpenGL.GL.glMatrixMode(OpenGL.GL.GL_MODELVIEW)
        OpenGL.GL.glLoadIdentity()
        
    def step(self, realtime=True):
        """Calculate simulator one step.
        """
        target_time = time.time() + self.root.dt.value
        Sofa.Simulation.animate(self.root, self.root.dt.value)
        Sofa.Simulation.updateVisual(self.root)
        if realtime:
            current_time = time.time()
            if target_time - current_time > 0:
                time.sleep(target_time - current_time)
        self.simple_render()

    def simple_render(self):
        """Render camera of root onto pygame.
        Get the OpenGL Context to render an image (snapshot) of the simulation state.
        """
        zNear = 0.1; zFar = 0 # For penetrate infinite view.
        OpenGL.GL.glClear(OpenGL.GL.GL_COLOR_BUFFER_BIT | OpenGL.GL.GL_DEPTH_BUFFER_BIT)
        OpenGL.GL.glEnable(OpenGL.GL.GL_LIGHTING)
        OpenGL.GL.glEnable(OpenGL.GL.GL_DEPTH_TEST)
        OpenGL.GL.glMatrixMode(OpenGL.GL.GL_PROJECTION)
        OpenGL.GL.glLoadIdentity()
        OpenGL.GLU.gluPerspective(45, (self.display_size[0] / self.display_size[1]), zNear, zFar)
        OpenGL.GL.glMatrixMode(OpenGL.GL.GL_MODELVIEW)
        OpenGL.GL.glLoadIdentity()

        cameraMVM = self.root.camera.getOpenGLModelViewMatrix()
        OpenGL.GL.glMultMatrixd(cameraMVM)
        Sofa.SofaGL.draw(self.root)

        pygame.display.flip()


    def action(self, translation=0, rotation=0):
        self.root.InstrumentCombined.m_ircontroller.findData('xtip').value =\
            self.root.InstrumentCombined.m_ircontroller.findData('xtip').value \
            + np.array([0,translation,0], dtype=float)
        self.root.InstrumentCombined.m_ircontroller.findData('rotationInstrument').value =\
            self.root.InstrumentCombined.m_ircontroller.findData('rotationInstrument').value \
            + np.array([0,rotation,0], dtype=float)
        

    def visualize(self):
        """Render camera of root onto pygame.
        Get the OpenGL Context to render an image (snapshot) of the simulation state.
        """
        zNear = 0.1; zFar = 0 # For penetrate infinite view.
        OpenGL.GL.glClear(OpenGL.GL.GL_COLOR_BUFFER_BIT | OpenGL.GL.GL_DEPTH_BUFFER_BIT)
        OpenGL.GL.glEnable(OpenGL.GL.GL_LIGHTING)
        OpenGL.GL.glEnable(OpenGL.GL.GL_DEPTH_TEST)
        OpenGL.GL.glMatrixMode(OpenGL.GL.GL_PROJECTION)
        OpenGL.GL.glLoadIdentity()
        OpenGL.GLU.gluPerspective(45, (self.display_size[0] / self.display_size[1]), zNear, zFar)
        OpenGL.GL.glMatrixMode(OpenGL.GL.GL_MODELVIEW)
        OpenGL.GL.glLoadIdentity()

        cameraMVM = self.root.camera.getOpenGLModelViewMatrix()
        OpenGL.GL.glMultMatrixd(cameraMVM)
        Sofa.SofaGL.draw(self.root)

        pygame.display.flip()
        
    def GetImage(self):
        """
        Get frame image as numpy.

        Parameters:
        ----------
            None

        Returns:
        -------
            image: np.ndarray

        """
        buffer = OpenGL.GL.glReadPixels(0, 0, *self.display_size, OpenGL.GL.GL_RGB, OpenGL.GL.GL_UNSIGNED_BYTE)
        image_array = np.frombuffer(buffer, np.uint8)
        if image_array.shape != (0,):
            image = image_array.reshape(self.display_size[1], self.display_size[0], 3)
        else:
            image = np.zeros((self.display_size[1], self.display_size[0], 3))
        image = np.flipud(image)
        return image


# # Make custom environment with gymnasium
# # https://gymnasium.farama.org/tutorials/gymnasium_basics/environment_creation/ 
# # https://colab.research.google.com/github/araffin/rl-tutorial-jnrr19/blob/master/5_custom_gym_env.ipynb#scrollTo=PQfLBE28SNDr 
# # https://stable-baselines3.readthedocs.io/en/master/guide/custom_env.html 
# # 나중에 sofa github에 ubuntu server에서 soaf interactiva camera로 이미지 저장할 수 있는 방법 묻기.






    