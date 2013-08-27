#!/usr/bin/env python

'''
Description:
    A collection of utility functions for deep playblasts:

    DeepPlayblastMakeNamespaceRenderLayer
        Prepare for deep playblast by making a namespace render layer

    DeepPlayblastHandleGpuMeshRenderLayer
        Handle gpu mesh nodes to treat them like they are in the render layer

    DeepPlayblastMakeXML
        Generate an xml string describing the deep playblast

Dependancies:
    getPath.mel
    parseXML.mel
    xml_parser plug-in
    fileQuery plug-in
    AnimSlicesUtilities.mel

Documentation:

Examples:

Notes:


Bugs:

Original:   02/29/12
Revisions:  05/22/12    Rev 1.0     mjefferies
            - added the specification of a filename to use as the alternate movie file with deep
              playblast tracks in it.

            05/24/12    Rev 1.1     mjefferies
            - modified to take a structure file rather than the seq/shot, so that an alternate
              structure file can be given.

            06/06/12    Rev 1.2     mjefferies
            - added support for deep playblasting gpumeshes and added the phase to the xml data

            07/19/12    Rev 1.3     mjefferies
            - added export of the assigned supervisor and artist usernames for each slice

            08/08/12    Rev 1.4     mjefferies
            - added a hack to get around an issue in maya when creating the namespaces render layer

            08/09/12    Rev 1.5        hmichalakeas
            - added a check to see if rfxAlembicMeshGpuCache type is present before ls -type ...

            08/16/12    Rev 1.6     mjefferies
            - added some robustness to deal with removing intermediate objects
              that have been assigned to the initialShadingGroup

            08/22/12    Rev 1.7        hmichalakeas
            - In DeepPlayblastMakeNamespaceRenderLayer, accounted for the possibility that lambert1 may have been mapped or otherwise adjusted.

            08/24/12    Rev 1.8       hmichalakeas
            - Switched fallback strategy for when maya gives a syntax error when assigning a shader. New approach switches layer back to the
            default render layer, unassigns then re-assigns the material assignments, switches to namespace layer and tries to assign the shader again.

            08/30/12    Rev 1.9       hmichalakeas
            - Further tweaks to fallback shader assignment strategy

            08/30/12    Rev 2.0       hmichalakeas
            - Switched to a more robust fallback shader assignment strategy (setup for shading group "hijacking" - see inline notes)

            09/19/12    Rev 2.1     mjefferies
            - Switched getting colors routine for deep playblast to use the same color for all props in a set.

            10/11/12    Rev 2.2       hmichalakeas
            - Switched to always using fallback shader assignment method (shading group hijack method)
'''

# Built-in
import json
import os
import hashlib
import random

# Maya
from pymel.all import *
import pymel.core as pm

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
    def __init__(self, gpu_meshes=[]):
        self.gpu_meshes = gpu_meshes
        self.namespaces = []
        self.colors = []
        self.meshes_with_color = []
        self.old_render_layer = None
        self.playblast_panel = pm.paneLayout('modelPanel4',p1=True)
        self.old_bkg_color = pm.displayRGBColor("background", query=True)
        self.old_bkg_top_color = pm.displayRGBColor("backgroundTop", query=True)
        self.old_bkg_bottom_color = pm.displayRGBColor("backgroundBottom",
                                                       query=True)
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

    def push_namespace_materials(self):
        shadingGroups = pm.ls(type="shadingEngine")
        for shader in shadingGroups:
            try:
                namespace_shader = shader.attr("namespaceShader")
            except MayaAttributeError:
                continue
            ns_connections = namespace_shader.listConnections(s=True, d=False)
            surface_shader = shader.attr('surfaceShader')
            if (ns_connections and not
                    pm.isConnected(ns_connections[0].attr("outColor"),
                                  shader.attr('surfaceShader'))):
                ns_connections[0].connectAttr("outColor", shader.attr('surfaceShader'),
                                              f=True)

    def pop_namespace_materials(self):
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

    def push_layer(self):
        self.old_render_layer = pm.editRenderLayerGlobals(query=True,
                                        currentRenderLayer=True)
        panel=pm.modelPanel(replacePanel='modelPanel4')
        editor = pm.modelEditor(panel, query=True,
                               displayTextures=False)
        pm.modelEditor('modelPanel4', edit=True, displayTextures=False)
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

    def pop_layer(self):
        # Set back tot he old render layer
        pm.editRenderLayerGlobals(currentRenderLayer=self.old_render_layer)
        panel=pm.modelPanel(replacePanel='modelPanel4')
        editor = pm.modelEditor(panel, edit=True,
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
            import pdb; pdb.set_trace()
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
                            existingShaders=stringArrayReverse(existingShaders)
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

# ----------------------------------------------------------------------------
# load all plug-ins required for this mel script
# ----------------------------------------------------------------------------
def _loadPlugins():
    if not pluginInfo("xml_parser",
        q=1,l=1):
        loadPlugin("xml_parser")

    # if not pluginInfo("fileQuery",
    #     q=1,l=1):
    #     loadPlugin("fileQuery")

    mel.eval("source \"parseXML.mel\";")
    # mel.eval("source \"AnimSlicesUtilities.mel\";")


# ----------------------------------------------------------------------------
def stringArrayReverse(array):
    result=[]
    s=len(array) - 1
    for i in range(0,s+1):
        result[i]=array[s - i]

    return result


# ----------------------------------------------------------------------------
# XXX TODO: This function will either no longer exist or will exist to query
# the db.
def _getNamespaceInfoFromStructureFile(strucfile,namespaces,paths,
                                       versions,types,phases,masterCam):
    # namespaces=[]
    # paths=[]
    # versions=[]
    # types=[]
    # phases=[]
    # masterCam=[]
    if os.path.exists( strucfile ) and os.path.getsize( strucfile ):
        xml=str(mel.readXML(strucfile, 0))
        assetXML=mel.xml_getTag(xml, "Asset")
        for i in range(0,len(assetXML)):
            namespaces.append(str(mel.xml_getVar(assetXML[i], "Namespace")))
            paths.append(str(mel.xml_getVar(assetXML[i], "Path")))
            versions.append(str(mel.xml_getVar(assetXML[i], "Version")))
            types.append(str(mel.xml_getVar(assetXML[i], "AssetType")))
            phases.append(str(mel.xml_getVar(assetXML[i], "Phase")))
            masterCam.append(str(mel.xml_getVar(assetXML[i], "MasterCamera")))



    else:
        print "Structure file " + strucfile + " is missing.\n"



# ----------------------------------------------------------------------------
def _getRandomColors(namespaces,colors,combineSetColors):
    # colors=[]
    for i in range(0,len(namespaces)):
        namespace=namespaces[i]
        if combineSetColors:
            if mel.gmatch(namespace, "*[:]*"):
                namespace=str(mel.getNamespaceFromString(namespace))

        # PROBLEM TO SOLVE TODAY
        # fq=fileQuery(namespace,
        #     checksum=1,fromString=1)
        # checksum=fq[0]
        m = hashlib.sha1()
        m.update(namespace)
        checksum = int(m.hexdigest(), 16)
        mel.seed("DeepPlayblast", checksum)
        r=float(mel.rand("DeepPlayblast", 1, 25) / 25.0)
        g=float(mel.rand("DeepPlayblast", 1, 25) / 25.0)
        b=float(mel.rand("DeepPlayblast", 1, 25) / 25.0)
        colors.append([r,g,b])



# ----------------------------------------------------------------------------
def _getColors(namespaces,colors):
    combineSetColors=1
    _getRandomColors(namespaces, colors, combineSetColors)


# ----------------------------------------------------------------------------
# Switch to namespace materials for objects that needed the fallback method of
# material assignment (see notes in DeepPlayblastMakeNamespaceRenderLayer)
# ----------------------------------------------------------------------------
def DeepPlayblastPushNamespaceMaterials():
    shadingGroups=ls(type="shadingEngine")
    for i in range(0,len(shadingGroups)):
        if objExists(shadingGroups[i] + ".namespaceShader"):
            nsShader=listConnections((shadingGroups[i] + ".namespaceShader"),
                s=1,d=0)
            if len(nsShader) and not isConnected((nsShader[0] + ".outColor"),
                                                 (shadingGroups[i] +
                                                  ".surfaceShader")):
                connectAttr((nsShader[0] + ".outColor"),
                            (shadingGroups[i] + ".surfaceShader"),
                            f=True)

# ----------------------------------------------------------------------------
# Switch to normal materials for objects that needed the fallback method of
# material assignment (see notes in DeepPlayblastMakeNamespaceRenderLayer)
# ----------------------------------------------------------------------------
def DeepPlayblastPopNamespaceMaterials():
    shadingGroups=ls(type="shadingEngine")
    for i in range(0,len(shadingGroups)):
        if objExists(shadingGroups[i] + ".defaultShader"):
            defaultShader=listConnections((shadingGroups[i] + ".defaultShader"),
                s=1,d=0)
            if len(defaultShader) and not isConnected((defaultShader[0] +
                                                       ".outColor"),
                                                      (shadingGroups[i] +
                                                       ".surfaceShader")):
                connectAttr((defaultShader[0] + ".outColor"),
                            (shadingGroups[i] + ".surfaceShader"),
                            f=True)

# ----------------------------------------------------------------------------
# Prepare for deep playblast by making a namespace render layer
# ----------------------------------------------------------------------------
def DeepPlayblastMakeNamespaceRenderLayer(strucfile,gpuMeshes):
    _loadPlugins()
    import pdb; pdb.set_trace()
    # this code is a hack to get around a problem with render layers in maya
    assigned = sets("initialShadingGroup", q=True)
    if assigned:
        defaultLambert=str(shadingNode("lambert", asShader=True))
        # account for the possibility of lambert1 having been adjusted, mapped
        attrs=listAttr("lambert1", s=1,r=True,k=1,se=1)
        for i in range(0,len(attrs)):
            numChildAttrs=attributeQuery(attrs[i], nc=1,n="lambert1")
            plug=listConnections(("lambert1." + attrs[i]),
                p=1,s=1,d=0)

            if len(plug):
                connectAttr((defaultLambert + "." + attrs[i]), plug[0])

            elif numChildAttrs:
                val=float(getAttr("lambert1." + attrs[i]))
                setAttr((defaultLambert + "." + attrs[i]),
                    val)
                # add parent attribute if any
                parentAttr=attributeQuery(attrs[i],
                    lp=1,n="lambert1")
                if len(parentAttr) and mel.stringArrayFindIndex(parentAttr[0], attrs) == -1:
                    attrs.append(parentAttr[0])

        shadingGroup=str(cmds.sets(renderable=True,noSurfaceShader=True))
        connectAttr((defaultLambert + ".outColor"),
                    (shadingGroup + ".surfaceShader"), f=True)
        for i in range(0,len(assigned)):
            isObject=len(ls(assigned[i], o=True))
            if isObject:
                import pdb; pdb.set_trace()
                if catch( lambda: cmds.sets(assigned[i],
                    rm="initialShadingGroup",e=1) ):
                    print "Problem removing " + assigned[i] + " from the initialShadingGroup\n"

                else:
                    cmds.sets(assigned[i],
                        e=1,fe=shadingGroup)

    namespaces=[]
    colors=[]
    # XXX TODO: This will need to be changed to use the database
    _getNamespaceInfoFromStructureFile(strucfile, namespaces, [], [], [], [], [])
    _getColors(namespaces, colors)
    # gpuMeshes=[]
    oldNamespace=str(namespaceInfo(currentNamespace=True))
    oldRenderLayer=str(editRenderLayerGlobals(q=1,currentRenderLayer=1))
    layer=""
    import pdb; pdb.set_trace()
    for i, cur_namespace in enumerate(namespaces):
        if cur_namespace == "stereoCam":
            continue

        if layer == "":
            layer=str(createRenderLayer(makeCurrent=1,name="namespaceLayer"))

        if catch( lambda: namespace(set=(":" + cur_namespace)) ):
            continue
        (red, green, blue) = colors[i]
        select(namespaceInfo(dp=1, lod=True), replace=True)
        import pdb; pdb.set_trace()
        geom=ls(visible=1,type=['mesh', 'nurbsSurface'],dag=1,ni=1,sl=1)
        gpuMesh=[]
        if objectType(tagFromType="rfxAlembicMeshGpuCache") != 0:
            gpuMesh=ls(selection=True, visible=1,dag=1,
                       type='rfxAlembicMeshGpuCache',long=1)

        select(clear=True)
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
                        existingShaders=stringArrayReverse(existingShaders)
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
        # With gpu meshes, we cannot set the shader.  We must change the default color for them
        if len(gpuMesh)>0:
            # end if size($existingShaders)
            for j in range(0,len(gpuMesh)):
                editRenderLayerMembers(layer,gpuMesh[j])
                setAttr((gpuMesh[j] + ".defaultColor"),
                    red,green,blue,
                    type='double3')
                gpuMeshes.append(gpuMesh[j])



    if layer != "":
        namespace(set=oldNamespace)
        editRenderLayerGlobals(currentRenderLayer=oldRenderLayer)

    return layer


# ---------------------------------------------------------------------------------------------------
# Handle gpu mesh nodes to treat them like they are in the render layer
# ---------------------------------------------------------------------------------------------------
def DeepPlayblastHandleGpuMeshRenderLayer(gpuMeshes,on):
    lighting=(on and 0 or 1)
    colorsMode=(on and 0 or 1)
    for i in range(0,len(gpuMeshes)):
        setAttr((gpuMeshes[i] + ".lighting"),
            lighting)
        setAttr((gpuMeshes[i] + ".colorsMode"),
            colorsMode)



# ---------------------------------------------------------------------------------------------------
def _getUserNameFromID(userID,idCache,usernameCache):
    index=int(mel.stringArrayFindIndex(userID, idCache))
    if index>=0:
        return usernameCache[index]

    username=""
    xml=str(mel.insightRequest("get", "http://insightcore.reelfx.com", "users/" + userID + ".xml", []))
    usernameNode=mel.xml_getTag(xml, "user-name")
    if len(usernameNode)>0:
        username=str(mel.xml_getCharacterData(usernameNode[0]))

    idCache.append(userID)
    usernameCache.append(username)
    return username


# ---------------------------------------------------------------------------------------------------
def _getSliceUserNames(strucfile,slices,supervisors,artists):
    supervisors=[]
    artists=[]
    for i in range(0,len(slices)):
        supervisors[i]=""
        artists[i]=""

    seq=str(mel.getPath("SequenceFromFilename", [strucfile]))
    shot=str(mel.getPath("ShotFromFilename", [strucfile]))
    xml=str(mel.insightGetTaskStatus(seq, shot, "Animation", ""))
    tasks=mel.xml_getTag(xml, "Task")
    idCache=[]
    usernameCache=[]
    for i in range(0,len(tasks)):
        taskName=str(mel.xml_getVar(tasks[i], "TaskName"))
        slice=str(mel.AnimSlicesGetSliceFromTaskName(taskName))
        index=int(mel.stringArrayFindIndex(slice, slices))
        if index != -1:
            supervisorID=str(mel.xml_getVar(tasks[i], "SupervisorID"))
            supervisors[index]=str(_getUserNameFromID(supervisorID, idCache, usernameCache))
            artistID=str(mel.xml_getVar(tasks[i], "WorkerID"))
            artists[index]=str(_getUserNameFromID(artistID, idCache, usernameCache))




# ---------------------------------------------------------------------------------------------------
# Build an xml string with information about the deep playblast
# ---------------------------------------------------------------------------------------------------
def DeepPlayblastMakeXML(strucfile,deepPlayblastFile,namespaceTrack):
    _loadPlugins()
    result=""
    result+="<DeepPlayblast "
    if deepPlayblastFile != "":
        result+="File=\"" + deepPlayblastFile + "\""

    result+=">\n"
    if namespaceTrack != "":
        namespaces=[]
        paths=[]
        versions=[]
        types=[]
        phases=[]
        masterCam=[]
        sliceNames=[]
        sliceSupervisors=[]
        sliceArtists=[]
        sliceNamespaces=[]
        namespacesInSlice=[]
        reserved=[]
        colors=[]
        _getNamespaceInfoFromStructureFile(strucfile, namespaces, paths, versions, types, phases, masterCam)
        mel.AnimSlicesGetSlicesFromStructureFile(strucfile, sliceNames, namespacesInSlice, sliceNamespaces, reserved)
        _getColors(namespaces, colors)
        _getSliceUserNames(strucfile, sliceNames, sliceSupervisors, sliceArtists)
        result+="\t<Namespaces Track=\"" + namespaceTrack + "\">\n"
        pos=0
        for s in range(0,len(sliceNames)):
            prefix="\t\t"
            if sliceNames[s] != "":
                result+="\t\t<Slice Name=\"" + sliceNames[s] + "\""
                if sliceSupervisors[s] != "":
                    result+=" Supervisor=\"" + sliceSupervisors[s] + "\""

                if sliceArtists[s] != "":
                    result+=" Artist=\"" + sliceArtists[s] + "\""

                result+=">\n"
                prefix+="\t"

            for n in range(0,namespacesInSlice[s]):
                i=int(mel.stringArrayFindIndex(sliceNamespaces[pos], namespaces))
                pos+=1
                if i>=0:
                    color=colors[i]
                    r=int(int(color.x * 255))
                    g=int(int(color.y * 255))
                    b=int(int(color.z * 255))
                    result+=prefix
                    result+="<Namespace"
                    result+=" Name=\"" + namespaces[i] + "\""
                    result+=" Color=\"" + str(r) + "," + str(g) + "," + str(b) + "\""
                    result+=" AssetPath=\"" + paths[i] + "\""
                    result+=" AssetVersion=\"" + versions[i] + "\""
                    result+=" AssetType=\"" + types[i] + "\""
                    if phases[i] != "":
                        result+=" Phase=\"" + phases[i] + "\""

                    if masterCam[i] != "":
                        result+=" MasterCamera=\"" + masterCam[i] + "\""

                    result+=" />\n"


            if sliceNames[s] != "":
                result+="\t\t</Slice>\n"


        result+="\t</Namespaces>\n"

    result+="</DeepPlayblast>\n"
    return result

def pushRenderLayer(renderLayer):
    import pdb; pdb.set_trace()
    melGlobals.initVar( 'string', 'gRFXPlayblastModelPanel' )
    melGlobals.initVar( 'string[]', 'gMeshesWithColorsOn' )
    melGlobals.initVar( 'string[]', 'gGpuMeshes' )
    # saved settings
    melGlobals.initVar( 'string', 'gOldRenderLayer' )
    melGlobals.initVar( 'int', 'gOldDisplayTextures' )
    melGlobals.initVar( 'float[]', 'gOldBackgroundColor' )
    melGlobals.initVar( 'float[]', 'gOldBackgroundTopColor' )
    melGlobals.initVar( 'float[]', 'gOldBackgroundBottomColor' )
    melGlobals['gOldRenderLayer']=str(editRenderLayerGlobals(q=1,currentRenderLayer=1))
    melGlobals['gOldDisplayTextures']=int(modelEditor(melGlobals['gRFXPlayblastModelPanel'],
        q=1,displayTextures=1))
    melGlobals['gOldBackgroundColor']=displayRGBColor("background",
        q=1)
    melGlobals['gOldBackgroundTopColor']=displayRGBColor("backgroundTop",
        q=1)
    melGlobals['gOldBackgroundBottomColor']=displayRGBColor("backgroundBottom",
        q=1)
    editRenderLayerGlobals(currentRenderLayer=renderLayer)
    modelEditor(melGlobals['gRFXPlayblastModelPanel'],
        edit=1,displayTextures=False)
    displayRGBColor("background",0,0,0)
    displayRGBColor("backgroundTop",0,0,0)
    displayRGBColor("backgroundBottom",0,0,0)
    for obj in melGlobals['gMeshesWithColorsOn']:
        setAttr((str(obj) + ".displayColors"),
            0)

    DeepPlayblastHandleGpuMeshRenderLayer(melGlobals['gGpuMeshes'], 1)
    DeepPlayblastPushNamespaceMaterials()


def popRenderLayer():
    melGlobals.initVar( 'string', 'gRFXPlayblastModelPanel' )
    melGlobals.initVar( 'string[]', 'gMeshesWithColorsOn' )
    melGlobals.initVar( 'string[]', 'gGpuMeshes' )
    # saved settings
    melGlobals.initVar( 'string', 'gOldRenderLayer' )
    melGlobals.initVar( 'int', 'gOldDisplayTextures' )
    melGlobals.initVar( 'float[]', 'gOldBackgroundColor' )
    melGlobals.initVar( 'float[]', 'gOldBackgroundTopColor' )
    melGlobals.initVar( 'float[]', 'gOldBackgroundBottomColor' )
    editRenderLayerGlobals(currentRenderLayer=melGlobals['gOldRenderLayer'])
    modelEditor(melGlobals['gRFXPlayblastModelPanel'],
        edit=1,displayTextures=melGlobals['gOldDisplayTextures'])
    displayRGBColor("background",melGlobals['gOldBackgroundColor'][0],melGlobals['gOldBackgroundColor'][1],melGlobals['gOldBackgroundColor'][2])
    displayRGBColor("backgroundTop",melGlobals['gOldBackgroundTopColor'][0],melGlobals['gOldBackgroundTopColor'][1],melGlobals['gOldBackgroundTopColor'][2])
    displayRGBColor("backgroundBottom",melGlobals['gOldBackgroundBottomColor'][0],melGlobals['gOldBackgroundBottomColor'][1],melGlobals['gOldBackgroundBottomColor'][2])
    for obj in melGlobals['gMeshesWithColorsOn']:
        setAttr((str(obj) + ".displayColors"),
            1)

    DeepPlayblastHandleGpuMeshRenderLayer(melGlobals['gGpuMeshes'], 0)
    DeepPlayblastPopNamespaceMaterials()

