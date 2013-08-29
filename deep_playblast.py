#!/usr/bin/env python


#----------------------------------------------------------------------------#
#------------------------------------------------------------ HEADER_START --#
"""
@newField description: Description
@newField category: Category
@newField application: Application

@author:
    slu

@organization:
    ReelFX

@description:
    Utility to create a Deep Playblast Render Layer to distinguish
    animation slices.

@category:
    - Animation

@application:
    - Maya
"""

# Built-in
import hashlib
import json
import os
import random
import sys

# Maya
from pymel.all import *
import pymel.core as pm

# ReelFX
from pipe_utils.sequence import FrameRange

# ----------------------------------------------------------------------------
# source statements
#
# ----------------------------------------------------------------------------
# global variables
# ----------------------------------------------------------------------------

# ----------------------------------------------------------------------------
# CLASSES
# ----------------------------------------------------------------------------

# Lets hope I can make this beautiful class.. I dunno
class DeepPlayblastRenderLayer(object):

    def __init__(self, metadata_path='', filename= '', camera='',
                 frame_range='', format='', compression='', widthHeight=''):
        """
        .. class:: DeepPlayblastRenderLayer

        This is the object to create a deep playblast render layer.
        """
        self.metadata_path = metadata_path
        self.camera = camera
        self.frame_range = FrameRange.parse(frame_range)
        self.format = format
        self.compression = compression
        self.widthHeight = widthHeight
        self.filename = filename
        self.input_pb_args = {'filename' : self.filename,
                              'frame' : self.frame_range.get_frames(),
                              'format' : self.format,
                              'compression' : self.compression,
                              'widthHeight' : self.widthHeight}
        self.gpu_meshes = []
        self.namespaces = []
        self.colors = []
        self.meshes_with_color = []
        self.old_render_layer = None
        self.playblast_panel = pm.modelPanel(replacePanel='modelPanel4')
        self.old_bkg_color = pm.displayRGBColor("background", query=True)
        self.old_bkg_top_color = pm.displayRGBColor("backgroundTop", query=True)
        self.old_bkg_bottom_color = pm.displayRGBColor(
            "backgroundBottom",
            query=True
        )

    def _getRandomColors(self, combineSetColors = None):
        for namespace in self.namespaces:
            if combineSetColors:
                if mel.gmatch(namespace, "*[:]*"):
                    namespace=str(mel.getNamespaceFromString(namespace))

            m = hashlib.sha1()
            m.update(namespace)
            checksum = int(m.hexdigest(), 16)
            random.seed(checksum)
            r = random.uniform(1, 25) / 25.0
            g = random.uniform(1, 25) / 25.0
            b = random.uniform(1, 25) / 25.0
            # mel.seed("DeepPlayblast", checksum)
            # r=float(mel.rand("DeepPlayblast", 1, 25) / 25.0)
            # g=float(mel.rand("DeepPlayblast", 1, 25) / 25.0)
            # b=float(mel.rand("DeepPlayblast", 1, 25) / 25.0)
            self.colors.append([r,g,b])

    def write_metadata(self):
        colors = []
        namespace_color_map = dict(zip(self.namespaces, self.colors))
        metadata = json.dumps(namespace_color_map)
        try:
            with open(self.metadata_path, 'w') as f:
                json.dump(metadata, f)
        except IOError:
            print "Unable to write metadata path: %s" % self.metadata_path

    def read_metadata(self):
        try:
            with open(self.metadata_path, 'r') as f:
                metadata = json.load(f)
        except IOError:
            print "Unable to read metadata path: %s" % self.metadata_path
        self.metadata = eval(metadata)

    def get_namespace_colors(self):
        self._getRandomColors()

    def get_meshes_with_color(self):
        """ Retrieve a list of all the meshes that need to display color. """
        allmeshes = pm.ls(type="mesh")
        for obj in allmeshes:
            display_colors = obj.getAttr('displayColors')
            if display_colors:
                self.meshes_with_color.append(obj)

    def handle_gpu_mesh(self, switch):
        lighting = switch
        colorsMode = switch
        for obj in self.gpu_meshes:
            obj.setAttr('lighting', lighting)
            obj.setAttr('colorsMode', colorsMode)

    def playblast(self):
        # Set up the camera
        pm.modelEditor(self.playblast_panel, edit=True, camera=self.camera)
        pm.playblast(**self.playblast_args)

    def push_namespace_materials(self):
        """ Connected the outColor attribute of the namespace
        shaders to the surface shader.
        """
        shadingGroups = pm.ls(type="shadingEngine")
        for shader in shadingGroups:
            try:
                namespace_shader = shader.attr("namespaceShader")
            except MayaAttributeError:
                continue
            ns_connections = namespace_shader.listConnections(s=True, d=False)
            surface_shader = shader.attr('surfaceShader')
            ns_is_connected = pm.isConnected(
                ns_connections[0].attr("outColor"),
                shader.attr("surfaceShader")
            )
            if ns_connections and not ns_is_connected:
                ns_connections[0].connectAttr(
                    "outColor",
                    shader.attr('surfaceShader'),
                    f=True
                )

    def pop_namespace_materials(self):
        """ Connect the outColor to the default shader to the surface
        shader.
        """
        shadingGroups = pm.ls(type="shadingEngine")
        for shader in shadingGroups:
            try:
                default_shader = shader.attr("defaultShader")
            except MayaAttributeError:
                continue
            ds_connections = default_shader.listConnections(s=True, d=False)
            ds_is_connected = pm.isConnected(
                ds_connections[0].attr("outColor"),
                shader.attr("surfaceShader")
            )
            if ds_connections and not ds_is_connected:
                ds_connections[0].connectAttr("outColor", shader.attr("surfaceShader"), f=True)

    def push(self):
        self.old_render_layer = pm.editRenderLayerGlobals(query=True,
                                        currentRenderLayer=True)
        editor = pm.modelEditor(self.playblast_panel, edit=True,
                               displayTextures=False, displayAppearance='smoothShaded')
        # pm.modelEditor(editor, edit=True, displayTextures=False)
        pm.editRenderLayerGlobals(currentRenderLayer=self.layer.name())
        # pm.modelEditor('modelPanel4', query=True, displayTextures=False)
        # Change the background color
        pm.displayRGBColor("background", 0, 0, 0)
        pm.displayRGBColor("backgroundTop", 0, 0, 0)
        pm.displayRGBColor("backgroundBottom", 0, 0, 0)
        self.get_meshes_with_color()
        for obj in self.meshes_with_color:
            obj.setAttr('displayColors', 0)
        self.handle_gpu_mesh(True)
        self.push_namespace_materials()

    def pop(self):
        # Set back tot he old render layer
        pm.editRenderLayerGlobals(currentRenderLayer=self.old_render_layer)
        editor = pm.modelEditor(self.playblast_panel, edit=True,
                               displayTextures=True)
        # Reset the background colors
        pm.displayRGBColor("background", *self.old_bkg_color)
        pm.displayRGBColor("backgroundTop", *self.old_bkg_top_color)
        pm.displayRGBColor("backgroundBottom", *self.old_bkg_bottom_color)
        # Change the attributes on the meshes
        for obj in self.meshes_with_color:
            obj.setAttr('displayColors', 1)
        self.handle_gpu_mesh(False)
        self.pop_namespace_materials()

    def get_namespaces(self):
        namespaces = []
        nodes = pm.ls(visible=True, type=['mesh', 'nurbsSurface'])
        for node in nodes:
            name = node.name()
            if '|' in name:
                name = name.rpartition('|')[-1]
            if ':' in name:
                namespaces.append(name.rpartition(':')[0])
            else:
                continue
        self.namespaces = list(set(namespaces))

    def create(self):
        _loadPlugins()
        # Query for the shading group set
        assigned = pm.sets("initialShadingGroup", query=True)
        if assigned:
            # Create new lambert shader
            default_lambert = pm.shadingNode("lambert", asShader=True)
            attrs = default_lambert.listAttr(scalar=True, read=True, settable=True, keyable=True)
            for attr in attrs:
                num_child_attrs = pm.attributeQuery(
                    attr.name(includeNode=False),
                    node="lambert1",
                    numberOfChildren=True
                )
                plug = attr.listConnections(plugs=True, destination=False, source=True)

                if plug:
                    attr.connectAttr(plug[0])

                elif num_child_attrs:
                    attr_val = pm.getAttr('lambert1.{0}'.format(attr))
                    default_lambert.setAttr(attr_val)
                    # Add parent attribute if there are any
                    parent_attr = pm.attributeQuery(attr, lp=True, n="lambert1")
                    if parent_attr and parent_attr[0] not in attrs:
                        attrs.append(parent_attr[0])

            shading_group = pm.sets(renderable=True, noSurfaceShader=True)
            default_lambert.connectAttr(
                'outColor',
                '{0}.surfaceShader'.format(shading_group.name()),
                f=True
            )
            for item in assigned:
                is_object = pm.ls(item, o=True)
                if is_object:
                    try:
                        shade_remove = pm.sets(item.name(),
                                               rm='initialShadingGroup',
                                               e=True)
                        pm.sets(item, e=True, fe=shading_group)
                    except RuntimeError:
                        shade_remove = None
                        print "Problem remove " + str(item) + " from the initialShadingGroup"
        # Get namespaces and generate colors based on those namespaces
        self.get_namespaces()
        self.get_namespace_colors()
        # Must replace with internal object function
        # _getNamespaceInfoFromStructureFile(self.struc, self.namespaces,
        #                                    [], [], [], [], [])

        # _getColors(self.namespaces, self.colors)
        old_namespace = pm.namespaceInfo(currentNamespace=True)
        old_render_layer = pm.editRenderLayerGlobals(q=True, currentRenderLayer=True)
        layer = ""
        for i, cur_namespace in enumerate(self.namespaces):
            # Will probably need to remove
            if cur_namespace == 'stereoCam':
                continue

            if layer == '':
                layer = pm.createRenderLayer(makeCurrent=True, name="namespaceLayer")

            if not pm.namespace(set=(":" + str(cur_namespace))):
                continue

            (red, green, blue) = self.colors[i]
            dag_namespace = pm.namespaceInfo(dp=1, lod=True)
            pm.select(dag_namespace, replace=True)
            geom = pm.ls(visible=True, type=['mesh', 'nurbsSurface'], dag=True, ni=True, selection=True)
            gpu_mesh = []
            if pm.objectType(tagFromType="rfxAlembicMeshGpuCache"):
                gpu_mesh = pm.ls(selection=True, visible=True, dag=True,
                                 type="rfxAlembicMeshGpuCache", long=True)

            pm.select(clear=True)
            if len(geom)>0:
                material=str(shadingNode('surfaceShader', asShader=True))
                setAttr((material + ".outColor"),
                    red,green,blue,
                    type='double3')
                shader=str(cmds.sets(renderable=True,
                                     noSurfaceShader=True, empty=True))
                connectAttr((material + ".outColor"),(shader + ".surfaceShader"),
                    f=True)
                for j in range(0,len(geom)):
                    existingShaders=listConnections(geom[j],
                        source=False,
                        plugs=False,
                        destination=True,
                        type="shadingEngine")
                    if len(existingShaders)>0:
                        editRenderLayerMembers(layer,geom[j])
                        retry=0
                        # first try to set the shader in object mode
                        retry=1
                        # Use shading group hijack method for everything...
                        #if (catch(`sets -noWarnings -forceElement $shader $geom[$j]`)) {
                        #    $retry = 1;
                        #}
                        if retry == 1:
                            # Couldn't assign shader. Various alternative approaches to assigning the shader have not worked 100% of the time.
                            # So add a couple of extra attributes to the shadingGroup - defaultShader and namespaceShader, and connect the respective
                            # shaders to these. During pushRenderLayer (PlayblastTool), check for the existence of the namespaceShader, and if present,
                            # find it's connection and plug it into the surfaceShader attribute, thus "hijacking" the shading group. During popRenderLayer,
                            # connect the attribute plugged into defaultShader and plug this back into the surfaceShader attribute. This is messy, but it
                            # sidesteps material assignment alltogether.
                            for k in range(0,len(existingShaders)):
                                if not objExists(existingShaders[k] + ".defaultShader"):
                                    addAttr(existingShaders[k],
                                        ln="defaultShader",at="message")
                                    defaultMat=listConnections((existingShaders[k] + ".surfaceShader"),
                                        s=1,d=0)
                                    if len(defaultMat):
                                        connectAttr((defaultMat[0] + ".message"),(existingShaders[k] + ".defaultShader"))

                                    addAttr(existingShaders[k],
                                        ln="namespaceShader",at="message")
                                    connectAttr((material + ".message"),(existingShaders[k] + ".namespaceShader"))


                            retry=0
                            # temp until we feel confident retiring the next section of code

                        if retry == 1:
                            print "DeepPlayblastUtilities: Using alternate shader assignment strategy on " + geom[j] + "\n"
                            # couldn't assign shader. Emergency fall-back: Switch back to defaultRenderLayer, unassign and re-assign the existing shaders, then
                            # switch back to namespace layer and try again.
                            existingShaders = self.stringArrayReverse(existingShaders)
                            """
                            To-do: Add an explanation about why reversing the shaders array is necessary once we've confirmed that we are good. -HM
                            """
                            # store the existing material assignments
                            comps=[]
                            indices=[]
                            for k in range(1,len(existingShaders)):
                                indices[k - 1]=len(comps)
                                assigned=cmds.sets(existingShaders[k],
                                    q=1)
                                for m in range(0,len(assigned)):
                                    obj=ls(o=assigned[m])
                                    if obj[0] == geom[j]:
                                        comps.append(assigned[m])



                            # unassign the existing materials
                            for k in range(0,len(existingShaders)):
                                cmds.sets(geom[j],
                                    rm=existingShaders[k],e=1)

                            if catch( lambda: cmds.sets(geom[j],
                                noWarnings=1,forceElement=shader) ):
                                mel.warning("DeepPlayblastUtilities: Couldn't assign namespace shader to " + geom[j])
                                continue


                            else:
                                print "DeepPlayblastUtilities: Alternate shader assignment worked for " + geom[j] + ".\n"

                            editRenderLayerGlobals(currentRenderLayer="defaultRenderLayer")
                            # switch back to defaultRenderLayer
                            # and re-assign (assign first shader to whole object, then component assign subsequent shaders)
                            cmds.sets(geom[j],
                                e=1,fe=existingShaders[0])
                            for k in range(0,len(indices)):
                                end=int((k<len(indices) - 1) and indices[k + 1] or (len(comps)))
                                for m in range(indices[k],end):
                                    cmds.sets(comps[m],
                                        e=1,fe=existingShaders[k + 1])


                            # switch to namespace layer
                            editRenderLayerGlobals(currentRenderLayer=layer)

            if len(gpu_mesh)>0:
                # end if size($existingShaders)
                for j in range(0,len(gpuMesh)):
                    pm.editRenderLayerMembers(layer,gpuMesh[j])
                    pm.setAttr((gpuMesh[j] + ".defaultColor"),
                        red,green,blue,
                        type='double3')
                    gpuMeshes.append(gpuMesh[j])



        if layer != "":
            pm.namespace(set=old_namespace)
            pm.editRenderLayerGlobals(currentRenderLayer=old_render_layer)

        self.layer = layer

    def stringArrayReverse(self, array):
        result=[]
        s=len(array) - 1
        for i in range(0,s+1):
            result[i]=array[s - i]

        return result

    @property
    def playblast_args(self):
        playblast_args = {
            'showOrnaments' : False,
            'rawFrameNumbers' : True,
            'viewer' : False,
            'offScreen' : True,
            'forceOverwrite' : True,
            'percent' : 100,
            'quality' : 100,
        }
        # Only if the input playblast arguments are specified do we add them
        for arg, value in self.input_pb_args.iteritems():
            if value:
                playblast_args[arg] = value
        return playblast_args

