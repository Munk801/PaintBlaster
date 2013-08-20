# script created by pymel.tools.mel2py from mel file:
# /mounts/elmo/people/slu/color_blast/PlayblastTool.mel

from pymel.all import *
import shutil,os,os.path
# PlayblastTool.mel (c) 2006 ReelFX Creative Studios
# Verision 1.0
# author: Harry Michalakeas
'''

Description:

	Automated Playblast mechanism. Recieves an xml instruction file, reads it, opens the shot, and playblasts it. Designed to be run as a process submitted by qube.

Use:

	PlayblastTool args

Options:

	args (string)	- semi-colon delimited argument string in the form arg1=val1;arg2=val2



Dependancies:



	parseXML.mel

	xml_parser plug-in

	rfxOverlay plug-in

	argList.mel

	fileIO.mel

	getPath

	stringArrayFindIndex

	createRfxOverlayFromTemplate

	padNumber

	getFileSize

	AnimSlicesUtilities.mel





Documentation:



Examples:



Notes:



	source "/data/film/apps/reelfx/maya/scripts/pipelineScripts/playblast/wip/PlayblastTool.6.10.mel"

Bugs:



Original:	09/18/06

Revisions:	09/22/06	Rev 1.0

		- Added temporary code to ensure that nearClippingPlane is not below 0.01 (due to problems with rfxOverlay node)

		- Added movie generation code.



		10/02/06	Rev 1.1

		- Added handling of mencoder audio as well as video options

		- Removed temporary clipping plane code.



		10/09/06	Rev 1.4

		- Added support for ffmpeg

		- Adding checking of frames and movie after creation

		- Added start and end message with time stamps.

		- Added the -useDefaultMaterial off flag in the modelEditor setup proc



		10/18/06	Rev 1.5

		- Re-organized so that the process occurs in two steps. Perform all the set up. Then evalDeferred -lp everything from the playblast on. This is so that control

		will briefly be returned to maya so that it can finish initializing the graphics



		10/23/06	Rev 1.6

		- Hooking up qt fast start

		- Hooking up export of overlay. This is a cheap and dirty way of letting the movie robot know that the frames in a given directory already have an overlay, so one

		doesn't need to be created.



		11/08/06	Rev 1.7

		- Switching to a more robust method of getting a start time to compare newly created images against (from the file system instead of system time - this allows the system

		to continue working even if the system time is off from the file system time)



		11/30/06	Rev 1.8

		- Propogating resulting movie to locations for Movie robot, and check that it made it.



		12/01/06	Rev 1.9

		- Propogating movie to edit_supervisor as well.



		12/12/06	Rev 2.0

		- Added deferred per frame playblasting, to solve the texture loading issue (only textures which are in frame at initial frame being loaded)



		12/14/06	Rev 2.1

		- Modified PlayblastToolHideLocators to catch snapshotShape's as well.



		??/??/??	Rev 2.2

		- Changes made by Kevin M.



		02/22/07	Rev 2.3

		- Check for 0k audio files, and treat them as "no audio"



		03/21/07	Rev 2.4

		- Enabling the display of imageplanes

		- ROLLBACK to 2.3



		03/26/07	Rev 2.5

		- Enabling display of imagePlanes (fix has been done to rfxOverlay node)



		03/29/07	Rev 2.6

		- Hiding cameras which don't have an imagePlane attached.



		05/24/07	Rev 3.0

		- Added PlayblastToolPropogateFrames() and PlayblastToolBuildSequenceMovies()



		06/06/07	Rev 3.1

		- Added check for project version of rfxBuildMoviesPath.py



		06/15/07	Rev 3.2

		- ?



		09/14/07	Rev 3.3		KM

		- PlayblastPreCallback and PlayblastPostCallback functions added previously, but not versioned

		- Folder archiving now includes tga files



		10/24/07	Rev 3.4		KM

		- Put catch statements around system calls to /bin/mv



		11/05/07	Rev 3.5		KM

		- Added check for existing active jobs.  If active jobs exist we may decide to not submit new jobs.



		11/20/07	Rev 3.6		KM

		- Implemented versioned frames and mov files on /render to match the Insight movie files on /data.



		11/26/07	Rev 3.7		KM

		- Deleted obsolete proc PlayblastToolDoPlayblast()

		- Removed unused instances of variable PlayblastToolDoPlayblast

		- Removed archiving of edit_supervisor



		11/27/07	Rev 3.8		KM

		- Added check to prevent the creation of /archive and /playblast subfolders in the /playblasts folders on /data



		12/05/07	Rev 3.9		KM

		- Added code to delete gOutputfmt frames from pre-existing playblast folders

		- Clean up of code previously commented out



		02/12/08	Rev 4.0		HM

		- Made PlayblastToolHideLocators more robust



		02/15/08	Rev 4.1		HM

		- Fixing a bug that appears in PlayblastToolHideLocators when underworld objects are encountered



		04/11/08	Rev 4.2		KM

		- Added full path to call for /usr/bin/python



		06/20/08	Rev 4.3		HM

		- Fixed a typo that was causing everything to be in textured mode regardless of value of gShadingMode



		07/14/08	Rev 4.4		KM

		- Re-wrote the python timer wrapping the qt-faststart call

		- Started changing Python calls made via system() to calls made via python()



		08/12/08	Rev 4.5		KM

		- Added xargs for deleting large numbers of files



		10/16/08	Rev 4.6		KM

		- Added game setting of 15 fps



		12/30/08	Rev 4.7		HM	(commited by KM)

		- Changes made to support new directory structure.



		01/20/09	Rev 4.8		KM

		- Changes made to support creation of FLV movies



		03/02/09	Rev 4.9		KM

		- Replaced the hardcoded flv resolution with the playblast resolution

		- Replaced flvmeta with flvtool++



		03/30/09	Rev 5.0		GD

		- Added support to playblast through a stereo camera in anaglyph mode



		05/01/09	Rev 5.1		GD

		- Rather than skipping the hiding of cameras with imagePlanes we now set the locator scale to 0.



		09/24/09	Rev 5.2		KM

		- Moved checks for existing sequence movie jobs into rfxBuildMovies.py

		- Updated name of rfxBuildMovies jobs to match format of the rfxBuildSequenceMovie jobs



		09/29/09	Rev 5.3		HM

		- Added support for open gl lit mode, and the open gl high quality renderer



		10/08/09	Rev 5.4		HM

		- Check for presense of lights when lighting is turned on, and turn it off if none are present



		10/20/09	Rev 5.5		HM

		- Adding ability to switch all rigs to render res if requested.



		11/19/09	Rev 5.6		HM

		- Putting ignore version in file opens



		02/12/10	Rev 5.7		HM

		- During setSmoothing, respect overrideSmooth if on



		03/25/10	Rev 5.8		HM

		- Reading John's media_file_id stuff (undocumented) for insight from instruction xml

		- Adding support for separate movie res from frame res



		04.28.2010	5.9	janderholm

		- Removes _ani/_lay from the live link name to be compatible with movie maker.

		e.g. versioned files are seq_shot_dep_ver.####.png, live files are seq_shot.####.png



		06/07/2010	6.0		HM

		- Suppressing error message when removing old frames from edit_supervisor directory and when removing temp flv file

		- Commented out the disabling of render res for layout rigs - there is no control in outsight by task



		06/15/2010	6.1		HM

		- If the project is stereo, apply the stereo overrides



		07.14.2010	6.2	janderholm

		- The filmFit is set to overscan, and the overscan is set to 1.0 on $gCameraShape

		to ensure proper framing.



		07.22.2010 6.3 mfortner

		- commenting out the block of code checking to see if frames are less than 1000

		in PlayblastToolCheckFrames



		09.30.2010	6.4	janderholm

		- Updated camera check looking for multiples to look based on name.



		10.13.2010	6.5	jcarey

		- Added $gWireframeOnShaded for future use of enabling wireframe on shaded in playblasts



		10.28.2010	6.6	janderholm

		- Make sure to set active stereo cameras to overscan @ 1.0.

		- Disables all zeroParallaxPlanes.

		- Uses findAssetsByName to track down the stereo camera.

		- Now just always calls maximize function.



		12.16.2010	6.7 jbarrett

		- Because stereo camera references may now be locked out of layout,

		the camera's lock state is checked, and toggled if necessary



		01.25.2011	6.8	hmichalakeas

		- Upping texture res if universal eye is found.

		- Adding smoothing to NURBS objects



		02.05.2011	6.9	kmacphail

		- Removed vframes from mov creation, was causing last frame to drop audio



		02.08.2011	6.10	kmacphail

		- Merged Rockettes version back into main branch



		03.04.2011	6.11	jbarrett

		- Disabled loading of saved UI configuration



		03.24.2011	6.12	janderholm

		- Updated imagePlane/camera hiding to skip the hiding process after scaling

		the camera's locator scale to 0.0001.



		05.10.2011	6.13	jbarrett

		- Modified window maximization to work around a hiccup in KDE 4 for local playblasts



		05.16.2011	6.14	jmorrison

		- Added a check for exTraFramesAtHead in the instructions file as well as the associated

		actions that should be performed.



		05.17.2011	6.15	janderholm

		- Now explicitly sets hardware renderer.



		05.26.2011  6.16    jbarrett

		- More tweaks to window sizing to undo Linux window maximization from previous playblast



		06.14.2011  6.17    jbarrett

		- added PlayblastToolSetLogState proc for logging Maya's script editor output



		07.11.2011	6.18	jmorrison

		- Added a test for pixel_separation_info locators to hide them (line 2102)



		09.12.2011 6.19     dmcatavey

		- Added "PNG" in defaultRenderGlobals list in an attempt to produce

		compatability with Maya 2012



		09.14.2011 6.20		dmcatavey

		- Added if statement to check if output images were .iff's, and convert them to

		.png's if necessary.



		10.03.2011 6.21		dmcatavey

		- Added support for ntsc field (60 fps) frame rate.



		10.07.2011 6.22		dmcatavey

		- ntsc field was not the correct name. ntscf was.



		10.20.2011 6.23		dmcatavey

		- Removed logic to check for iff files. Amazing how well things work

		when you implement the proper commands!



		10.28.2011 6.24		janderholm

		- Preroll now executes before each run.  So if force reload is off and

		stereo is on, preroll will run before each eye.

		- Software rendering support added.

		- Added ability to import light rig.

		- Distribution has been implemented.

			- The post process can be bypassed for subjobs.

			- The post process can be invoked exclusively for a post job.

		- Added ability to load render globals preset.



		11.01.2011	6.25	janderholm

		- Updated distribution handling to use farm tag in Playblast.xml



		11.18.2011	6.26	janderholm

		- Explicitly set the renderer to mayaSoftware to prevent problems

		when loading globals.



		12.08.2011	6.27	janderholm

		- Use temp_unlock_camera to circumnavigate python util issues.



		12.14.2011	6.28	janderholm

		- Patch: Diable viewport update in attempt to speed up preroll for traditional playblast.



		12.07.2011  	6.3	jneumann

		- Now checking highQualityRendering setting and setting up the machines

		viewport properly.



		12.08.2011  	6.4	jneumann

		- In PlayblastToolGetStereoCamera we first check if gDoStereo is active before

		trying to run that call since it was erroring out with mono shots over an iterator.



		01.14.2012 	6.41	jneumann

		- Combined dave and underground playblast code.



		01.24.2012 	6.42    cpenny

		- set enableUniversalEye to on at same time as render switch



		03.23.2012	6.43	hmichalakeas

		- Fixed a bug in the logic which occured when the show is stereo, but we do not wish to do a stereo playblast.

		Previously, either gIsStereo (the show), OR gDoStereo (the playblast) being off would cause us to not retrieve the stereo cam info

		This was not correct, since if the show is stereo, but we are not doing a stereo playblast, we would still want to playblast through

		the left stereo cam and therefore need that info.

		- Updated PlayblastToolPrintOptions to print additional options that have been added in recent months.



		04.05.2012 6.45		mjefferies

		- Add support for animation slices and deep playblast



		04.24.2012 6.46		mjefferies

		- Added a call to movutils during deep playblast to make sure the quicktime player

		  shows track 0 (the regular playblast) over track 1 (the deep playblast)



		04.27.2012 6.47		mjefferies

		- Bug fix for more robust handling of a failure to create the deep playblast render layer



        04.27.2012 6.48     mjefferies

        - Add a flag to ffmpeg to include the target filename as metadata in the mov file.



        - Change deep playblast behavior to export a completely separate file with namespace track.

          So now in deep playblast mode you get the normal file, and the deep playblast file with two video tracks



        05.24.2012 6.50     mjefferies

        - Modified deep playblast to generate a temp structure file during layout in order to

          build the namespace info.



        06.06.2012 6.51     mjefferies

        - Added support for deep playblast of gpu meshes



        06.13.2012 6.52	   hmichalakeas

        - Placed a catch around the file -lr which is called when load all references is turned on



        08.02.2012 6.53     mjefferies

        - Added making backup copy of deep playblast xml file if it contains slices



        08.21.2012 6.54    hmichalakeas

        - Adjusted PlayblastToolGetStereoCamera so that it sets the overscan to 1.0 on the left and right stereo cams as well as the master.



        08.29.2012 6.55     mjefferies

        - Added call to re-sync anim slices after forcing the visibilty of all caches, so that visibility of set props will match the cache.



        08.30.2012 6.56	   hmichalakeas

        - Added calls to DeepPlayblastPushNamespaceMaterials and DeepPlayblastPopNamespaceMaterials in push/pop render layers (Deep Playblast related)



        11.15.2012 6.57     mjefferies

        - Force HQ Graphics for anim slices mesh gpu caches during playblast



        01.28.2013 6.58     mjefferies

        - Added call to clear settings that could be altered by the AnimSlicesDashboard



To-do's:

		- Handling of display layers. Do we want to preserve them?

		- Per shot callbacks

		- Resolution check for movies (width must be multiple of 4)

		- Image format check. Make sure that we are playblasting a format that the encoder can handle.

'''
# ---------------------------------------------------------------------------------------------------
# source statements
#
# ---------------------------------------------------------------------------------------------------
# global variables
#
# ---------------------------------------------------------------------------------------------------
# load all plug-ins required for this mel script
def _loadPlugins():
	mel.eval("source \"AnimSlicesUtilities.mel\";")
	mel.eval("source \"AnimSlicesDashboard.mel\";")
	if not pluginInfo("xml_parser",
		q=1,l=1):
		loadPlugin("xml_parser")
		
	if not pluginInfo("rfxOverlay",
		q=1,l=1):
		loadPlugin("rfxOverlay")
		
	if not pluginInfo("timeQuery",
		q=1,l=1):
		loadPlugin("timeQuery")
		
	if not pluginInfo("Mayatomr",
		q=1,l=1):
		loadPlugin("Mayatomr")
		
	

def _temp_unlock_camera():
	refs=cmds.file(q=1,r=1)
	for ref in refs:
		asset_name=str(mel.getPath("AssetNameFromFilename", [ref]))
		if asset_name == "stereoCam":
			rfn=str(referenceQuery(rfn=ref))
			if not cmds.file(ref,
				q=1,dr=1):
				cmds.file(ur=rfn)
				setAttr(rfn + ".locked",0)
				cmds.file(lr=rfn)
				
			
		
	

# ---------------------------------------------------------------------------------------------------
# PlayblastToolSetLogState - Turns script editor logging on/off
# ---------------------------------------------------------------------------------------------------
def PlayblastToolSetLogState(state):
	melGlobals.initVar( 'string', 'gInputScene' )
	# The scene to playblast
	if not about():
		if state:
			if scriptEditorInfo(q=1,writeHistory=1):
				scriptEditorInfo(writeHistory=False)
				# Is logging already turned on?  If so, disable it before starting a new log
				
			logfile=str(mel.dirname(mel.dirname(melGlobals['gInputScene']))) + "/td/playblastLog.txt"
			# For now, only save a single log file for the shot
			# In the future, versioned logs might be helpful
			mel.PlayblastToolMessage("Opening script editor log file: " + logfile)
			scriptEditorInfo(historyFilename=logfile,writeHistory=True)
			
		
		elif scriptEditorInfo(q=1,writeHistory=1):
			mel.PlayblastToolMessage("Closing script editor log file.")
			scriptEditorInfo(writeHistory=False)
			
		
		else:
			mel.PlayblastToolWarning("No script editor log file to close.")
			
		
	

# ---------------------------------------------------------------------------------------------------
# PlayblastToolMultipleOfTwo - Increments odd intergers by 1
# ---------------------------------------------------------------------------------------------------
def PlayblastToolMultipleOfTwo(val):
	if val % 2:
		val+=1
		
	return val
	

# ---------------------------------------------------------------------------------------------------
# Quit - leave lock file to indicate failure to wrapper
# ---------------------------------------------------------------------------------------------------
def PlayblastToolQuitError(msg):
	melGlobals.initVar( 'int', 'DEBUG' )
	melGlobals.initVar( 'int', 'gTempLocHandle' )
	melGlobals.initVar( 'int', 'gInsightMediaFileId' )
	mel.PlayblastToolMessage("[1;31mError:[0;31m " + msg + "[0m")
	# Stop the script editor log
	PlayblastToolSetLogState(0)
	batch_mode=int(about())
	if melGlobals['DEBUG'] or os.environ[ "PLAYBLASTING" ] == "" and not batch_mode:
		print "$DEBUG: " + str(melGlobals['DEBUG']) + "\n"
		print "ENV PLAYBLASTING: " + os.environ[ "PLAYBLASTING" ] + "\n"
		mel.error("")
		
	
	elif melGlobals['gTempLocHandle']:
		melGlobals['gTempLocHandle'].close()
		
	mel.PlayblastToolInsightCallback(2, msg)
	qube_job_id=int(mel.getThisQubeJobId())
	if batch_mode and qube_job_id:
		cmds.quit(a=1,ec=1)
		mel.error("abort")
		return 
		
	pid=int(mel.getpid())
	# harsh, but quit -f errors, and evalDeferred("quit -f") leaves maya running until you touch the mouse
	#		system("killall -9 maya.bin >& /dev/null");
	internal.shellOutput("kill -9 " + str(str(pid)) + " >& /dev/null", convertNewlines=False, stripTrailingNewline=False)
	

# ---------------------------------------------------------------------------------------------------
# Quit - remove lock file to indicate success to wrapper
# ---------------------------------------------------------------------------------------------------
def PlayblastToolQuitSuccess():
	melGlobals.initVar( 'int', 'DEBUG' )
	melGlobals.initVar( 'string', 'gLockFile' )
	melGlobals.initVar( 'int', 'gTempLocHandle' )
	if melGlobals['gTempLocHandle']:
		melGlobals['gTempLocHandle'].close()
		
	mel.PlayblastToolMessage("DONE.")
	if not melGlobals['DEBUG'] and os.environ[ "PLAYBLASTING" ] != "":
		if os.path.exists( melGlobals['gLockFile'] ) and os.path.getsize( melGlobals['gLockFile'] ):
			os.remove( melGlobals['gLockFile'] )
			# remove lock file to indicate success to wrapper
			# harsh, but quit -f errors, and evalDeferred("quit -f") leaves maya running until you touch the mouse
			
		pid=int(mel.getpid())
		internal.shellOutput("kill -9 " + str(str(pid)) + " >& /dev/null", convertNewlines=False, stripTrailingNewline=False)
		
	

# ---------------------------------------------------------------------------------------------------
def PlayblastToolMessage(msg):
	melGlobals.initVar( 'int', 'gTempLocHandle' )
	melGlobals.initVar( 'int', 'DEBUG' )
	prefix="[1;30mPlayblastTool [[0;33m" + str(date()) + "[1;30m]:[0m "
	buffer=msg.split("\n")
	line=""
	for i in range(0,len(buffer)):
		line+=prefix + buffer[i] + "\n"
		
	if line == "":
		line+=prefix + "\n"
		# output message to a temporary log. This will be cat'd by the wrapper process, so that our messages will show up in the qberr log.
		# 04.15.2010 - Attempt to use eprint which will output to stderr in interactive mode.
		
	if not melGlobals['DEBUG'] and os.environ[ "PLAYBLASTING" ] != "":
		if not melGlobals['gTempLocHandle']:
			melGlobals['gTempLocHandle']=open("/usr/tmp/PlayblastTempLog.txt","w")
			
		if not mel.eprint(line):
			melGlobals['gTempLocHandle'].write(line)
			
		
	
	else:
		mel.eprint(line)
		
	

def PlayblastToolWarning(msg):
	PlayblastToolMessage("[1;35mWarning:[0;35m " + msg + "[0m")
	

def PlayblastToolSeparator():
	PlayblastToolMessage("________________________________________________________________________________")
	PlayblastToolMessage("")
	

# ---------------------------------------------------------------------------------------------------
# PlayblastToolGetTagError - wrapper for xml_getTag - throw an error if the tag is not found
# ---------------------------------------------------------------------------------------------------
def _PlayblastToolGetTagError(xml,tagName):
	melGlobals.initVar( 'string', 'gInstructionFile' )
	# xml instructions for playblast
	node=mel.xml_getTag(xml, tagName)
	if not len(node):
		PlayblastToolQuitError("Problems occured reading " + melGlobals['gInstructionFile'] + ". Found no " + tagName + " node.")
		
	return node
	

# ---------------------------------------------------------------------------------------------------
# PlayblastToolGetVarError - wrapper for xml_getVar - throw an error if the var is not found
# ---------------------------------------------------------------------------------------------------
def _PlayblastToolGetVarError(xml,tagName,varName):
	melGlobals.initVar( 'string', 'gInstructionFile' )
	# xml instructions for playblast
	val=str(mel.xml_getVar(xml, varName))
	if val == "":
		PlayblastToolQuitError("Problems occured reading " + melGlobals['gInstructionFile'] + ". Found no attribute " + varName + " in node " + tagName + ".")
		
	return val
	

# ---------------------------------------------------------------------------------------------------
# PlayblastToolGetStereoCamera - finds the reference who's .name attr matches $gPlayblastStereoCamera
# ---------------------------------------------------------------------------------------------------
def PlayblastToolGetStereoCamera():
	melGlobals.initVar( 'string', 'gCamera' )
	# Cam to playblast thru
	melGlobals.initVar( 'string', 'gPlayblastStereoCamera' )
	# the .name attr value - the name of the stereo camera to use
	melGlobals.initVar( 'int', 'gIsStereo' )
	melGlobals.initVar( 'string', 'gPlayblastStereoCameraLeft' )
	melGlobals.initVar( 'string', 'gPlayblastStereoCameraRight' )
	melGlobals.initVar( 'int', 'gDoStereo' )
	melGlobals.initVar( 'int', 'gDoStereoPlayblast' )
	if melGlobals['gPlayblastStereoCamera'] == "":
		melGlobals['gPlayblastStereoCamera']="stereoCam"
		
	melGlobals['gDoStereoPlayblast']=0
	# note - do not check for gDoStereo at this point.
	"""
	
			The meaning of the variables is a little confusing.
	
			gIsStereo - tells whether the show is stereo
	
			gDoStereo - do a stereo playblast for this shot
	
	
	
			It's valid to have a stereo show, but elect not to do stereo playblasts for a given phase. In that case,
	
			we still need to get the stereo camera info, since we will be using it to playblast through - we'll just be only doing one eye.
	
	
	
		"""
	if melGlobals['gIsStereo']:
		_temp_unlock_camera()
		#string $allProps[] = findAssetsByType("p", 0);
		#string $stereoCam = "";
		#for($i = 0; $i < size($allProps); $i+= 1)
		#	if(getAttr($allProps[$i] + ".name") == $gPlayblastStereoCamera)
		#		$stereoCam = $allProps[$i];
		# Update 12/16/10: Because stereo camera references may now be locked out of layout,
		# check the camera's lock state and unlock it before doing anything else
		# python("import layoutUtils");
		# if(python("layoutUtils.is_shot_camera_locked()"))
		# 	python("layoutUtils.toggle_shot_camera_lock()");
		stereo_cams=mel.findAssetsByName(melGlobals['gPlayblastStereoCamera'])
		stereoCam=stereo_cams[0]
		if stereoCam != "":
			all_nodes=[stereoCam] + listRelatives(pa=stereoCam,ad=1)
			stereoCamRig=ls(all_nodes,
				type="stereoRigTransform")
			if objExists(stereoCamRig[0]):
				PlayblastToolMessage("Found stereo camera rig.")
				melGlobals['gCamera']=stereoCamRig[0]
				#PlayblastToolMessage("Setting $gCamera to " + $stereoCamRig[0]);
				frustum=listRelatives(stereoCamRig[0],
					s=1,pa=1,type="stereoRigFrustum")
				if objExists(frustum[0]):
					cons=listConnections((frustum[0] + ".leftCamera"),
						p=0,s=1,c=0,d=0)
					melGlobals['gPlayblastStereoCameraLeft']=cons[0]
					cons=listConnections((frustum[0] + ".rightCamera"),
						p=0,s=1,c=0,d=0)
					melGlobals['gPlayblastStereoCameraRight']=cons[0]
					PlayblastToolMessage("Assigning eyes:")
					PlayblastToolMessage("L -> " + melGlobals['gPlayblastStereoCameraLeft'])
					PlayblastToolMessage("R -> " + melGlobals['gPlayblastStereoCameraRight'])
					offset_plug=stereoCamRig[0] + ".offset"
					if objExists(offset_plug):
						cons=listConnections(offset_plug,
							p=1,s=1,c=0,d=0)
						if len(cons):
							disconnectAttr(cons[0],offset_plug)
							# This controls how the horizontal film offset is applied to the left and right
							# cameras.
							# 0 - Disabled -> horizontal film offset is set to 0 on both cameras.
							# 1 - Uniform -> hfo is equal but opposite on both cameras.
							# 2 - Proportional -> if one camera is fixed, its hfo is set to 0, and the other
							#					   is set to 2x the amount.  If neither camera is fixed, the
							#					   hfo is uniform.
							#
							# In talks with Nick Ilyin, proportional is what should be used.  We will probably
							# end up locking the left camera, and rendering it at res.  The right camera will
							# have its hfo disabled for rendering purposes, but will be rendered with overscan
							# and the hfo will be applied in comp.
							# For the most part, the interaxial separation should remain at 6.35.
							# The general concensus is that toe-in should be completely avoided.
							#setAttr $offset_plug 2;
							# More updates:
							# It now appears with Troy's brief conversations with the Phil McNally at Dreamworks
							# that the backplane shifting is indeed the way to go.  Toe-in is verifiably an
							# abomination.
							#
							# Seeing that renderMan allows us some render savings when rendering left and
							# right images simultaneously, it makes the most sense to just render out the
							# left and the right images with overscan, and apply a proportional shift in post.
							# In order to match up between animation and lighting seamlessly, we will
							# force the proportional setting in the playblast.
							#
							# Note that the backplane shift correlates to the zeroParallax setting.  The
							# interaxial separation actually moves the (right) camera.  If the interaxial separation
							# changes, there would actually need to be a rerender of the right eye.
							# If only the parallax changes, the update should be reflected in the translate node
							# in Nuke.  McNally has been using phrases like, "shift this by 6 pixels", so hopefully
							# this ends up being the majority of changes (a.k.a. no rerendering).
							
						setAttr(offset_plug,1)
						
					camShapes=listRelatives(melGlobals['gCamera'],
						pa=1,type="camera",ad=1)
					# Force the camera into overscan.
					for i in range(0,len(camShapes)):
						cons=listConnections((camShapes[i] + ".renderable"),
							p=1,s=1,c=0,d=0)
						# Set the renderable to Overscan.
						if len(cons):
							catch( lambda: disconnectAttr((cons[0]),(camShapes[i])) )
							
						catch( lambda: setAttr((camShapes[i] + ".renderable"),
							1) )
						# Set the filmFit to Overscan.
						cons=listConnections((camShapes[i] + ".filmFit"),
							p=1,s=1,c=0,d=0)
						if len(cons):
							catch( lambda: disconnectAttr((cons[0]),(camShapes[i])) )
							
						catch( lambda: setAttr((camShapes[i] + ".filmFit"),
							3) )
						# Set the overscan to 1.0.
						cons=listConnections((camShapes[0] + ".overscan"),
							p=1,s=1,c=0,d=0)
						if len(cons):
							catch( lambda: disconnectAttr((cons[0]),(camShapes[i])) )
							
						catch( lambda: setAttr((camShapes[i] + ".overscan"),
							1.0) )
						
					
				
			stereo_cams=ls(type="stereoRigCamera")
			# Disable all zero parallax planes.
			for cam in stereo_cams:
				cons=listConnections((str(cam) + ".zeroParallaxPlane"),
					p=1,s=1,c=0,d=0)
				if len(cons):
					catch( lambda: disconnectAttr((cons[0]),
						cam) )
					
				catch( lambda: setAttr((str(cam) + ".zeroParallaxPlane"),
					0) )
				
			
		
		else:
			melGlobals['gIsStereo']=0
			PlayblastToolMessage("Turning off stereo for this playblast. Unable to find stereo camera.")
			
		if melGlobals['gIsStereo'] and melGlobals['gDoStereo'] and objExists(melGlobals['gPlayblastStereoCameraLeft']) and objExists(melGlobals['gPlayblastStereoCameraRight']):
			melGlobals['gDoStereoPlayblast']=1
			
		
	

# ---------------------------------------------------------------------------------------------------
# PlayblastToolPrintOptions - Print out all the options given after instructions file has been parsed
# ---------------------------------------------------------------------------------------------------
def PlayblastToolPrintOptions():
	melGlobals.initVar( 'string', 'gInstructionFile' )
	# xml instructions for playblast
	melGlobals.initVar( 'string', 'gInputScene' )
	# The scene to playblast
	melGlobals.initVar( 'int', 'gFramePreRollStart' )
	# The frame on which the preroll should start.
	melGlobals.initVar( 'int', 'gFrameRangeStart' )
	# Start frame to playblast
	melGlobals.initVar( 'int', 'gFrameRangeEnd' )
	# End frame (inclusive) to playblast
	melGlobals.initVar( 'int', 'gExtraFramesAtHead' )
	# Preroll frames for dynamics, etc
	melGlobals.initVar( 'string', 'gCamera' )
	# Cam to playblast thru
	melGlobals.initVar( 'int', 'gRefSwitchProxyToFull' )
	# Use selective preload to switch proxy refs to full
	melGlobals.initVar( 'int', 'gRefLoadAllRefs' )
	# Load all references
	melGlobals.initVar( 'int', 'gExecutePerAssetCallbacks' )
	# Execute per asset callbacks if any exist
	melGlobals.initVar( 'int', 'gSwitchAssetsToRender' )
	# if rigs have a res attribute, set it to render
	melGlobals.initVar( 'string', 'gTargetImagePath' )
	# Where to write images. Path, plus base name
	melGlobals.initVar( 'string', 'gTargetMoviePath' )
	# Where to write movies, if desired
	melGlobals.initVar( 'string', 'gShadingMode' )
	# wireframe, shaded, or textured.
	#	global int $gWireframeOnShaded;	// wireframe on shaded
	melGlobals.initVar( 'int', 'gLighting' )
	# Open GL lighting
	melGlobals.initVar( 'int', 'gHighQualityRendering' )
	# Hi Quality GL renderer
	melGlobals.initVar( 'int', 'gSetSmoothing' )
	# Smooth all the assets - if they have built in smoothing?
	melGlobals.initVar( 'int', 'gSmoothDivisions' )
	# How many divisions to smooth to.
	melGlobals.initVar( 'int', 'gDoStereo' )
	# Override to disable Stereo Playblasts
	melGlobals.initVar( 'int', 'gDoDeepPlayblast' )
	# Override to disable Deep Playblasts
	melGlobals.initVar( 'int', 'gDoReload' )
	# Override to disable texture reloads
	melGlobals.initVar( 'int', 'gDoHires' )
	# Override to default to Movie Resolution
	melGlobals.initVar( 'int', 'gSoftwareRender' )
	# Use the software renderer instead of playblast.
	melGlobals.initVar( 'string', 'gRenderGlobalsPreset' )
	# Render globals preset.
	melGlobals.initVar( 'int', 'gResWidth' )
	# x resolution to playblast at
	melGlobals.initVar( 'int', 'gResHeight' )
	# y resolution to playblast at
	melGlobals.initVar( 'float', 'gResAspect' )
	# aspect ratio
	melGlobals.initVar( 'int', 'gMovieResWidth' )
	# x resolution of movie, may be different than frame size
	melGlobals.initVar( 'int', 'gMovieResHeight' )
	# y resolution of movie, may be different than frame size
	melGlobals.initVar( 'float', 'gMovieResAspect' )
	# aspect ratio of movie, may be different than for frames
	melGlobals.initVar( 'string', 'gOutputFmt' )
	# Output format for frames.
	melGlobals.initVar( 'int', 'gDoMovie' )
	# Make a movie?
	melGlobals.initVar( 'int', 'gDoAudio' )
	# If we are making a movie, include audio?
	melGlobals.initVar( 'string', 'gMovieFPS' )
	# fps for movie
	melGlobals.initVar( 'string', 'gMovieType' )
	# mov or avi
	melGlobals.initVar( 'int', 'gFastStart' )
	# run qt fast start on movie?
	melGlobals.initVar( 'string', 'gEncoder' )
	# encoder to use "ffmpeg" or "mencoder"
	melGlobals.initVar( 'string', 'gEncoderVideoOptions' )
	# option string to send to mencoder for creating movies
	melGlobals.initVar( 'string', 'gEncoderAudioOptions' )
	# option string to send to mencoder for audio options
	melGlobals.initVar( 'string', 'gAudioPath' )
	# Path to audio for the shot
	melGlobals.initVar( 'int', 'gDoOverlay' )
	# Comp an overlay on top of the images.
	melGlobals.initVar( 'string', 'gOverlayTemplate' )
	# Template xml for creating overlay
	melGlobals.initVar( 'string', 'gPlayblastStereoCamera' )
	# the .name attr value - the name of the stereo camera to use
	melGlobals.initVar( 'int', 'gIsStereo' )
	# If 1 then playblast through the stereo camera
	melGlobals.initVar( 'string', 'gHost' )
	# Who submitted? "maya" or "insight"
	melGlobals.initVar( 'string', 'gInsightCallbackPath' )
	# Referer for the webservice
	melGlobals.initVar( 'string', 'gInsightCallbackArgs' )
	# Webservice arguments
	melGlobals.initVar( 'int', 'gInsightMediaFileId' )
	# Media file id for insight playblast.
	melGlobals.initVar( 'int', 'gBypassPostPlayblast' )
	# Skip the post playblast process (will be handled elsewhere).
	melGlobals.initVar( 'int', 'gPostPlayblastOnly' )
	# Just run the post playblast process.
	melGlobals.initVar( 'string', 'gLightRigName' )
	melGlobals.initVar( 'string', 'gPlayblastPreCallback' )
	# if it exists, this will be the path to the pre playblast callback
	melGlobals.initVar( 'string', 'gPlayblastPostCallback' )
	# if it exists, this will be the path to the post playblast callback
	# find the pre and post callback scripts if they exist
	#
	mel.PlayblastToolCheckPreCallback()
	mel.PlayblastToolCheckPostCallback()
	PlayblastToolMessage("Options:")
	PlayblastToolMessage("Instructions file: " + melGlobals['gInstructionFile'])
	PlayblastToolMessage("Input Scene: " + melGlobals['gInputScene'])
	PlayblastToolMessage("Pre-roll Start: " + str(melGlobals['gFramePreRollStart']))
	PlayblastToolMessage("Frame Range Start: " + str(melGlobals['gFrameRangeStart']))
	PlayblastToolMessage("Frame Range End: " + str(melGlobals['gFrameRangeEnd']))
	PlayblastToolMessage("Camera: " + melGlobals['gCamera'])
	PlayblastToolMessage("Switch Proxy References to Full: " + str(melGlobals['gRefSwitchProxyToFull']))
	PlayblastToolMessage("Execute Per Asset Callbacks: " + str(melGlobals['gExecutePerAssetCallbacks']))
	PlayblastToolMessage("Switch Res to Render: " + str(melGlobals['gSwitchAssetsToRender']))
	PlayblastToolMessage("Target Image Path: " + melGlobals['gTargetImagePath'])
	PlayblastToolMessage("Shading Mode: " + melGlobals['gShadingMode'])
	#	PlayblastToolMessage("Wireframe on Shaded Mode: " + $gWireframeOnShaded);
	PlayblastToolMessage("Lighting: " + str(melGlobals['gLighting']))
	PlayblastToolMessage("Light Rig: " + melGlobals['gLightRigName'])
	PlayblastToolMessage("High Quality Rendering: " + str(melGlobals['gHighQualityRendering']))
	PlayblastToolMessage("Software Render: " + str(melGlobals['gSoftwareRender']))
	PlayblastToolMessage("Render Globals Preset: " + melGlobals['gRenderGlobalsPreset'])
	PlayblastToolMessage("Set Smoothing: " + str(melGlobals['gSetSmoothing']))
	PlayblastToolMessage("Smooth Divisions: " + str(melGlobals['gSmoothDivisions']))
	PlayblastToolMessage("Resolution Width: " + str(melGlobals['gResWidth']))
	PlayblastToolMessage("Resolution Height: " + str(melGlobals['gResHeight']))
	PlayblastToolMessage("Aspect Ratio: " + str(melGlobals['gResAspect']))
	PlayblastToolMessage("Output Format: " + melGlobals['gOutputFmt'])
	PlayblastToolMessage("Do Movie: " + str(melGlobals['gDoMovie']))
	PlayblastToolMessage("Target Movie Path: " + melGlobals['gTargetMoviePath'])
	PlayblastToolMessage("Movie Frame Rate: " + melGlobals['gMovieFPS'])
	PlayblastToolMessage("Movie Type: " + melGlobals['gMovieType'])
	PlayblastToolMessage("Movie Resolution Width: " + str(melGlobals['gMovieResWidth']))
	PlayblastToolMessage("Movie Resolution Height: " + str(melGlobals['gMovieResHeight']))
	PlayblastToolMessage("Fast Start: " + str(melGlobals['gFastStart']))
	PlayblastToolMessage("Encoder: " + melGlobals['gEncoder'])
	PlayblastToolMessage("Encoder video options: " + melGlobals['gEncoderVideoOptions'])
	PlayblastToolMessage("Encoder audio options: " + melGlobals['gEncoderAudioOptions'])
	PlayblastToolMessage("Do Audio: " + str(melGlobals['gDoAudio']))
	PlayblastToolMessage("Audio Path: " + melGlobals['gAudioPath'])
	PlayblastToolMessage("Do Overlay: " + str(melGlobals['gDoOverlay']))
	PlayblastToolMessage("Pre Callback: " + melGlobals['gPlayblastPreCallback'])
	PlayblastToolMessage("Post Callback: " + melGlobals['gPlayblastPostCallback'])
	PlayblastToolMessage("Stereo camera name: " + melGlobals['gPlayblastStereoCamera'])
	PlayblastToolMessage("Stereo Show: " + str(melGlobals['gIsStereo']))
	PlayblastToolMessage("Stereo Playblast: " + str(melGlobals['gDoStereo']))
	PlayblastToolMessage("Deep Playblast: " + str(melGlobals['gDoDeepPlayblast']))
	PlayblastToolMessage("Callback host: " + melGlobals['gHost'])
	PlayblastToolMessage("Callback path: " + melGlobals['gInsightCallbackPath'])
	PlayblastToolMessage("Callback args: " + melGlobals['gInsightCallbackArgs'])
	PlayblastToolMessage("Insight Media Field ID: " + str(melGlobals['gInsightMediaFileId']))
	PlayblastToolMessage("Bypass Post Playblast: " + str(melGlobals['gBypassPostPlayblast']))
	PlayblastToolMessage("Post Playblast Only: " + str(melGlobals['gPostPlayblastOnly']))
	

# ---------------------------------------------------------------------------------------------------
# PlayblastToolParseInstructions - Parse the instructions xml
# ---------------------------------------------------------------------------------------------------
def PlayblastToolParseInstructions():
	melGlobals.initVar( 'string', 'gInstructionFile' )
	# global vars
	# xml instructions for playblast
	melGlobals.initVar( 'string', 'gInputScene' )
	# The scene to playblast
	melGlobals.initVar( 'int', 'gFramePreRollStart' )
	# The frame on which the preroll should start.
	melGlobals.initVar( 'int', 'gFrameRangeStart' )
	# Start frame to playblast
	melGlobals.initVar( 'int', 'gFrameRangeEnd' )
	# End frame (inclusive) to playblast
	melGlobals.initVar( 'int', 'gExtraFramesAtHead' )
	# Preroll frames for dynamics, etc
	melGlobals.initVar( 'string', 'gCamera' )
	# Cam to playblast thru
	melGlobals.initVar( 'int', 'gRefSwitchProxyToFull' )
	# Use selective preload to switch proxy refs to full
	melGlobals.initVar( 'int', 'gRefLoadAllRefs' )
	# Load all references
	melGlobals.initVar( 'int', 'gExecutePerAssetCallbacks' )
	# Execute per asset callbacks if any exist
	melGlobals.initVar( 'int', 'gSwitchAssetsToRender' )
	# if rigs have a res attribute, set it to render
	melGlobals.initVar( 'string', 'gTargetImagePath' )
	# Where to write images. Path, plus base name
	melGlobals.initVar( 'string', 'gTargetMoviePath' )
	# Where to write movies, if desired
	melGlobals.initVar( 'string', 'gShadingMode' )
	# wireframe, shaded, or textured.
	#	global int $gWireframeOnShaded;	// wireframe on shaded
	melGlobals.initVar( 'int', 'gLighting' )
	# Open GL lighting
	melGlobals.initVar( 'int', 'gHighQualityRendering' )
	# Hi Quality GL renderer
	melGlobals.initVar( 'int', 'gSetSmoothing' )
	# Smooth all the assets - if they have built in smoothing?
	melGlobals.initVar( 'int', 'gSmoothDivisions' )
	# How many divisions to smooth to.
	melGlobals.initVar( 'int', 'gDoStereo' )
	# Override to disable Stereo Playblasts
	melGlobals.initVar( 'int', 'gDoReload' )
	# Override to disable texture reloads
	melGlobals.initVar( 'int', 'gDoHires' )
	# Override to default to Movie Resolution
	melGlobals.initVar( 'int', 'gSoftwareRender' )
	# Use the software renderer instead of playblast.
	melGlobals.initVar( 'string', 'gRenderGlobalsPreset' )
	# Render globals preset.
	melGlobals.initVar( 'int', 'gResWidth' )
	# x resolution to playblast at
	melGlobals.initVar( 'int', 'gResHeight' )
	# y resolution to playblast at
	melGlobals.initVar( 'float', 'gResAspect' )
	# aspect ratio
	melGlobals.initVar( 'int', 'gMovieResWidth' )
	# x resolution of movie, may be different than frame size
	melGlobals.initVar( 'int', 'gMovieResHeight' )
	# y resolution of movie, may be different than frame size
	melGlobals.initVar( 'float', 'gMovieResAspect' )
	# aspect ratio of movie, may be different than for frames
	melGlobals.initVar( 'string', 'gOutputFmt' )
	# Output format for frames.
	melGlobals.initVar( 'int', 'gDoMovie' )
	# Make a movie?
	melGlobals.initVar( 'int', 'gDoAudio' )
	# If we are making a movie, include audio?
	melGlobals.initVar( 'string', 'gMovieFPS' )
	# fps for movie
	melGlobals.initVar( 'string', 'gMovieType' )
	# mov or avi
	melGlobals.initVar( 'int', 'gFastStart' )
	# run qt fast start on movie?
	melGlobals.initVar( 'string', 'gEncoder' )
	# encoder to use "ffmpeg" or "mencoder"
	melGlobals.initVar( 'string', 'gEncoderVideoOptions' )
	# option string to send to mencoder for creating movies
	melGlobals.initVar( 'string', 'gEncoderAudioOptions' )
	# option string to send to mencoder for audio options
	melGlobals.initVar( 'string', 'gAudioPath' )
	# Path to audio for the shot
	melGlobals.initVar( 'int', 'gDoOverlay' )
	# Comp an overlay on top of the images.
	melGlobals.initVar( 'string', 'gOverlayTemplate' )
	# Template xml for creating overlay
	melGlobals.initVar( 'string', 'gPlayblastStereoCamera' )
	# the .name attr value - the name of the stereo camera to use
	melGlobals.initVar( 'int', 'gIsStereo' )
	# If 1 then playblast through the stereo camera
	melGlobals.initVar( 'string', 'gHost' )
	# Who submitted? "maya" or "insight"
	melGlobals.initVar( 'string', 'gInsightCallbackPath' )
	# Referer for the webservice
	melGlobals.initVar( 'string', 'gInsightCallbackArgs' )
	# Webservice arguments
	melGlobals.initVar( 'int', 'gInsightMediaFileId' )
	# Media file id for insight playblast.
	melGlobals.initVar( 'int', 'gBypassPostPlayblast' )
	# Skip the post playblast process (will be handled elsewhere).
	melGlobals.initVar( 'int', 'gPostPlayblastOnly' )
	# Just run the post playblast process.
	melGlobals.initVar( 'string', 'gLightRigName' )
	melGlobals.initVar( 'int', 'gDoDeepPlayblast' )
	qube_id=int(mel.getThisQubeJobId())
	qube_frame=int(mel.getThisQubeFrameNumber())
	PlayblastToolMessage("Qube: " + str(str(qube_id)) + ":" + str(str(qube_frame)))
	# make sure the instructions file exists
	if not os.path.exists( melGlobals['gInstructionFile'] ) and os.path.getsize( melGlobals['gInstructionFile'] ):
		PlayblastToolQuitError("Instructions file " + melGlobals['gInstructionFile'] + " doesn't exist.")
		# parse the xml
		
	xml=str(mel.readXML(melGlobals['gInstructionFile'], 0))
	farmNode=mel.xml_getTag(xml, "farm")
	sceneNode=_PlayblastToolGetTagError(xml, "scene")
	outputNode=_PlayblastToolGetTagError(xml, "output")
	# -------------------
	# scene
	# -------------------
	# input file
	fileNode=_PlayblastToolGetTagError(sceneNode[0], "file")
	melGlobals['gInputScene']=str(_PlayblastToolGetVarError(fileNode[0], "file", "name"))
	melGlobals['gInputScene']=str(mel.getPath("ConformPath", [melGlobals['gInputScene']]))
	if not os.path.exists( melGlobals['gInputScene'] ) and os.path.getsize( melGlobals['gInputScene'] ):
		PlayblastToolQuitError("Input scene " + melGlobals['gInputScene'] + " does not exist.")
		# camera
		
	cameraNode=_PlayblastToolGetTagError(sceneNode[0], "camera")
	melGlobals['gCamera']=str(_PlayblastToolGetVarError(cameraNode[0], "camera", "name"))
	# stereo camera
	stereoCameraNode=mel.xml_getTag(sceneNode[0], "stereoCamera")
	melGlobals['gPlayblastStereoCamera']=str(mel.xml_getVar(stereoCameraNode[0], "name"))
	melGlobals['gIsStereo']=int(mel.xml_getVar(stereoCameraNode[0], "isStereoShow"))
	# light rig
	light_rig_node=mel.xml_getTag(sceneNode[0], "lightRig")
	if len(light_rig_node):
		melGlobals['gLightRigName']=str(mel.xml_getVar(light_rig_node[0], "name"))
		
	InsightCallbackNode=mel.xml_getTag(sceneNode[0], "callback")
	# insight callback
	melGlobals['gHost']=str(mel.xml_getVar(InsightCallbackNode[0], "host"))
	melGlobals['gInsightCallbackPath']=str(mel.xml_getVar(InsightCallbackNode[0], "path"))
	melGlobals['gInsightCallbackArgs']=str(mel.xml_getVar(InsightCallbackNode[0], "arguments"))
	val=str(mel.xml_getVar(InsightCallbackNode[0], "media_file_id"))
	melGlobals['gInsightMediaFileId']=int((val != ""))
	melGlobals['gInsightMediaFileId'] and int(val) or 0
	#if($gIsStereo)
	#{
	# It's a stereo show so find the stereo camera and set $gCamera to be the stereo camera.
	#
	#PlayblastToolGetStereoCamera();
	#}
	# reference options
	referenceNode=mel.xml_getTag(sceneNode[0], "references")
	if not len(referenceNode):
		PlayblastToolMessage("Warning. Instructions file " + melGlobals['gInstructionFile'] + " contains no references node.")
		melGlobals['gRefSwitchProxyToFull']=int(False)
		melGlobals['gRefLoadAllRefs']=int(False)
		melGlobals['gExecutePerAssetCallbacks']=int(False)
		
	
	else:
		refSwitchProxyToFull=str(mel.xml_getVar(referenceNode[0], "switchProxyToFull"))
		refLoadAllRefs=str(mel.xml_getVar(referenceNode[0], "loadAllReferences"))
		executePerAssetCallbacks=str(mel.xml_getVar(referenceNode[0], "executePerAssetCallbacks"))
		switchAssetsToRender=str(mel.xml_getVar(referenceNode[0], "switchToRenderRes"))
		melGlobals['gRefSwitchProxyToFull']=int((refSwitchProxyToFull == ""))
		melGlobals['gRefSwitchProxyToFull'] and False or int(refSwitchProxyToFull)
		melGlobals['gRefLoadAllRefs']=int((refLoadAllRefs == ""))
		melGlobals['gRefLoadAllRefs'] and False or int(refLoadAllRefs)
		melGlobals['gExecutePerAssetCallbacks']=int((executePerAssetCallbacks == ""))
		melGlobals['gExecutePerAssetCallbacks'] and False or int(executePerAssetCallbacks)
		melGlobals['gSwitchAssetsToRender']=int((switchAssetsToRender == ""))
		melGlobals['gSwitchAssetsToRender'] and False or int(switchAssetsToRender)
		
	targetNode=_PlayblastToolGetTagError(outputNode[0], "target")
	# -------------------
	# output
	# -------------------
	# target
	melGlobals['gTargetImagePath']=str(_PlayblastToolGetVarError(targetNode[0], "target", "imagePath"))
	melGlobals['gTargetImagePath']=str(mel.getPath("ConformPath", [melGlobals['gTargetImagePath']]))
	melGlobals['gTargetMoviePath']=str(mel.xml_getVar(targetNode[0], "moviePath"))
	# quality
	qualityNode=mel.xml_getTag(outputNode[0], "quality")
	if not len(qualityNode):
		PlayblastToolMessage("Warning. Instructions file " + melGlobals['gInstructionFile'] + " contains no quality node.")
		# use defaults
		melGlobals['gShadingMode']="shaded"
		#		$gWireframeOnShaded = 0;
		melGlobals['gSetSmoothing']=int(False)
		melGlobals['gSmoothDivisions']=0
		melGlobals['gLighting']=0
		melGlobals['gHighQualityRendering']=0
		melGlobals['gDoStereo']=1
		melGlobals['gDoReload']=1
		melGlobals['gDoHires']=1
		melGlobals['gSoftwareRender']=0
		
	
	else:
		shadingMode=str(mel.xml_getVar(qualityNode[0], "shadingMode"))
		lighting=str(mel.xml_getVar(qualityNode[0], "lighting"))
		highQualityRendering=str(mel.xml_getVar(qualityNode[0], "highQualityRendering"))
		setSmoothing=str(mel.xml_getVar(qualityNode[0], "setSmoothing"))
		divisions=str(mel.xml_getVar(qualityNode[0], "divisions"))
		doStereo=str(mel.xml_getVar(qualityNode[0], "doStereo"))
		doReload=str(mel.xml_getVar(qualityNode[0], "doReload"))
		doHires=str(mel.xml_getVar(qualityNode[0], "doHires"))
		softwareRender=str(mel.xml_getVar(qualityNode[0], "softwareRender"))
		renderGlobalsPreset=str(mel.xml_getVar(qualityNode[0], "renderGlobalsPreset"))
		if shadingMode == "wireframe" or shadingMode == "textured":
			melGlobals['gShadingMode']=shadingMode
			
		
		else:
			melGlobals['gShadingMode']="shaded"
			
		melGlobals['gLighting']=int((lighting == ""))
		melGlobals['gLighting'] and 0 or int(lighting)
		melGlobals['gHighQualityRendering']=int((highQualityRendering == ""))
		melGlobals['gHighQualityRendering'] and 0 or int(highQualityRendering)
		melGlobals['gSetSmoothing']=int((setSmoothing == ""))
		melGlobals['gSetSmoothing'] and False or int(setSmoothing)
		melGlobals['gSmoothDivisions']=int((divisions == ""))
		melGlobals['gSmoothDivisions'] and 0 or (min(int(divisions), 2))
		# No more than 2 smooth divisions
		melGlobals['gDoStereo']=int((doStereo == ""))
		melGlobals['gDoStereo'] and 1 or int(doStereo)
		# default to True
		melGlobals['gDoReload']=int((doReload == ""))
		melGlobals['gDoReload'] and 1 or int(doReload)
		# default to True
		melGlobals['gDoHires']=int((doHires == ""))
		melGlobals['gDoHires'] and 1 or int(doHires)
		# default to True
		melGlobals['gSoftwareRender']=int((softwareRender == ""))
		melGlobals['gSoftwareRender'] and 0 or int(softwareRender)
		# default to false.
		melGlobals['gRenderGlobalsPreset']=renderGlobalsPreset
		
	resolutionNode=_PlayblastToolGetTagError(outputNode[0], "resolution")
	# resolution
	melGlobals['gResWidth']=int(int(_PlayblastToolGetVarError(resolutionNode[0], "resolution", "width")))
	# ### To-do: Playblast width and height must be divisible by 4
	melGlobals['gResHeight']=int(int(_PlayblastToolGetVarError(resolutionNode[0], "resolution", "height")))
	aspect=str(mel.xml_getVar(resolutionNode[0], "aspectRatio"))
	melGlobals['gResAspect']=float((aspect == ""))
	melGlobals['gResAspect'] and (float(melGlobals['gResWidth']) / float(melGlobals['gResHeight'])) or float(aspect)
	# output format (for frames, not movie)
	formatNode=mel.xml_getTag(outputNode[0], "format")
	if not len(formatNode):
		PlayblastToolMessage("Warning. Instructions file " + melGlobals['gInstructionFile'] + " contains no format node. Defaulting to \"jpg\"")
		melGlobals['gOutputFmt']="jpg"
		
	
	else:
		outputFormat=str(mel.xml_getVar(formatNode[0], "imageFormat"))
		if outputFormat == "":
			PlayblastToolMessage("Warning. Instructions file " + melGlobals['gInstructionFile'] + " contains no format node. Defaulting to \"jpg\"")
			melGlobals['gOutputFmt']="jpg"
			
		
		else:
			melGlobals['gOutputFmt']=outputFormat
			# ### To-do: Validate format.
			
		
	melGlobals['gDoDeepPlayblast']=0
	# deep playblast
	deepPlayblastNode=mel.xml_getTag(outputNode[0], "deepPlayblast")
	if len(deepPlayblastNode):
		melGlobals['gDoDeepPlayblast']=int(int(mel.xml_getVar(deepPlayblastNode[0], "doNamespaces")))
		
	distro_enabled=int(False)
	# --------------------------------------------------------------------- //
	# Distribution.
	# --------------------------------------------------------------------- //
	subjob_count=0
	if len(farmNode):
		distro_tag=mel.xml_getTag(farmNode[0], "distribution")
		distro_en_str=str(mel.xml_getVar(distro_tag[0], "enabled"))
		if distro_en_str != "":
			distro_enabled=int(int(distro_en_str))
			
		subjob_str=str(mel.xml_getVar(farmNode[0], "subjobs"))
		subjob_count=int((subjob_str != ""))
		subjob_count and int(subjob_str) or 0
		
	is_subjob=(distro_enabled and qube_frame>=0)
	is_post=(distro_enabled and qube_frame<0)
	PlayblastToolMessage("$is_subjob " + str(is_subjob))
	PlayblastToolMessage("$is_post " + str(is_post))
	# --------------------------------------------------------------------- //
	# Frame range
	# --------------------------------------------------------------------- //
	frameRangeNode=_PlayblastToolGetTagError(sceneNode[0], "frameRange")
	start_frame=int(int(_PlayblastToolGetVarError(frameRangeNode[0], "frameRange", "start")))
	end_frame=int(int(_PlayblastToolGetVarError(frameRangeNode[0], "frameRange", "end")))
	preroll_str=str(mel.xml_getVar(frameRangeNode[0], "extraFramesAtHead"))
	preroll=int((preroll_str != "") and int(preroll_str) or 0)
	preroll=int(max(1, preroll))
	# Start the preroll on this frame.
	melGlobals['gFramePreRollStart']=start_frame - preroll
	# Determine the renderable frame range.
	if is_subjob:
		index=qube_frame
		# If we're a software render and we have chunks, we are distributed.
		# Get the frame range per subjob.
		frame_range=end_frame - start_frame + 1
		sub_range=frame_range / subjob_count
		if frame_range % subjob_count != 0:
			sub_range+=1
			
		offset=sub_range * index
		# Get the offset based on the subjob range and the current subjob.
		# Get the start and end frame of the subjob.
		sub_start_frame=start_frame + offset
		sub_end_frame=sub_start_frame + sub_range - 1
		# Restrict the values to the overall range of the shot.
		melGlobals['gFrameRangeStart']=int(max(start_frame, min(end_frame, sub_start_frame)))
		melGlobals['gFrameRangeEnd']=int(max(start_frame, min(end_frame, sub_end_frame)))
		# We will want to bypass the post process.
		melGlobals['gBypassPostPlayblast']=1
		
	
	else:
		melGlobals['gFrameRangeStart']=start_frame
		# Otherwise we're just a normal one shot.
		melGlobals['gFrameRangeEnd']=end_frame
		# See if we're a post job.
		if is_post:
			melGlobals['gPostPlayblastOnly']=1
			# If so, just execute the post process.
			
		
	PlayblastToolMessage("This playblast job will render frames: " + str(str(melGlobals['gFrameRangeStart'])) + "-" + str(str(melGlobals['gFrameRangeEnd'])) + ".")
	# movie options - to grow once we have a better idea from implementing this
	movieNode=mel.xml_getTag(outputNode[0], "movie")
	if not len(movieNode):
		PlayblastToolMessage("Warning. Instructions file " + melGlobals['gInstructionFile'] + " contains no movie node. No movie will be generated.")
		melGlobals['gDoMovie']=int(False)
		
	
	else:
		makeMovie=str(mel.xml_getVar(movieNode[0], "makeMovie"))
		if makeMovie == "":
			PlayblastToolMessage("Warning. Instructions file " + melGlobals['gInstructionFile'] + " contains no attribute makeMovie in node movie. No movie will be generated.")
			melGlobals['gDoMovie']=int(False)
			
		
		else:
			melGlobals['gDoMovie']=int(int(makeMovie))
			if melGlobals['gDoMovie']:
				if melGlobals['gTargetMoviePath'] == "":
					PlayblastToolMessage("Warning. Instructions file " + melGlobals['gInstructionFile'] + " contains no attribute moviePath in node target. No movie will be generated.")
					melGlobals['gDoMovie']=int(False)
					
				
				else:
					melGlobals['gTargetMoviePath']=str(mel.getPath("ConformPath", [melGlobals['gTargetMoviePath']]))
					doAudio=str(mel.xml_getVar(movieNode[0], "includeAudio"))
					audioPath=str(mel.xml_getVar(movieNode[0], "audioPath"))
					if audioPath != "":
						audioPath=str(mel.getPath("ConformPath", [audioPath]))
						
					melGlobals['gMovieType']=str(mel.xml_getVar(movieNode[0], "type"))
					# not doing anything with this yet.
					fastStart=str(mel.xml_getVar(movieNode[0], "faststart"))
					melGlobals['gFastStart']=int((fastStart == ""))
					melGlobals['gFastStart'] and 0 or int(fastStart)
					movieResWidth=str(mel.xml_getVar(movieNode[0], "width"))
					melGlobals['gMovieResWidth']=int((movieResWidth != ""))
					melGlobals['gMovieResWidth'] and int(movieResWidth) or melGlobals['gResWidth']
					movieResHeight=str(mel.xml_getVar(movieNode[0], "height"))
					melGlobals['gMovieResHeight']=int((movieResHeight != ""))
					melGlobals['gMovieResHeight'] and int(movieResHeight) or melGlobals['gResHeight']
					# aspect not implemented for movies
					# make sure movie res is divisible by 2 (required by ffmpeg)
					if melGlobals['gMovieResWidth'] != melGlobals['gResWidth'] and melGlobals['gMovieResHeight'] != melGlobals['gResHeight']:
						melGlobals['gMovieResWidth']-=melGlobals['gMovieResWidth'] % 2
						melGlobals['gMovieResHeight']-=melGlobals['gMovieResHeight'] % 2
						
					melGlobals['gDoAudio']=int((doAudio == ""))
					melGlobals['gDoAudio'] and False or int(doAudio)
					if melGlobals['gDoAudio']:
						if audioPath == "":
							PlayblastToolMessage("Warning. Instructions file " + melGlobals['gInstructionFile'] + " contains no audioPath attribute. No audio will be added to movie.")
							melGlobals['gDoAudio']=int(False)
							
						
						elif not os.path.exists( audioPath ) and os.path.getsize( audioPath ):
							PlayblastToolMessage("Warning. Audio file " + audioPath + " does not exist. No audio will be added to movie.")
							melGlobals['gDoAudio']=int(False)
							
						
						elif mel.getFileSize(audioPath) == 0:
							PlayblastToolMessage("Warning. Audio file " + audioPath + " is 0k. No audio will be added to movie.")
							# check for 0k audio file
							melGlobals['gDoAudio']=int(False)
							
						
						else:
							melGlobals['gAudioPath']=audioPath
							
						
					fps=str(mel.xml_getVar(movieNode[0], "fps"))
					# frame rate of movie
					if fps != "film" and fps != "ntsc" and fps != "pal" and fps != "game" and fps != "ntscf":
						PlayblastToolMessage("Warning. Invalid frame rate for movie \"" + fps + "\". Defaulting to \"film\".")
						melGlobals['gMovieFPS']="film"
						
					
					else:
						melGlobals['gMovieFPS']=fps
						
					encoderNode=mel.xml_getTag(movieNode[0], "encoding")
					# encoder options
					# $gEncoder
					melGlobals['gEncoder']=str(mel.xml_getVar(encoderNode[0], "encoder"))
					if melGlobals['gEncoder'] == "":
						PlayblastToolMessage("Warning. Instructions file " + melGlobals['gInstructionFile'] + " specifies no encoder. No movie will be generated.")
						melGlobals['gDoMovie']=int(False)
						
					
					elif melGlobals['gEncoder'] != "ffmpeg" and melGlobals['gEncoder'] != "mencoder":
						PlayblastToolMessage("Warning. Instructions file " + melGlobals['gInstructionFile'] + " specifies an invalid encoder (" + melGlobals['gEncoder'] + "). No movie will be generated.")
						melGlobals['gDoMovie']=int(False)
						
					if melGlobals['gEncoder'] != "ffmpeg" and melGlobals['gFastStart'] != 0:
						PlayblastToolMessage("Warning. Fast Start is specified, but encoder is not ffmpeg. Fast Start is currently only supported with movies made with ffmpeg. Disabling Fast Start.")
						melGlobals['gFastStart']=0
						
					options=str(mel.xml_getVar(encoderNode[0], "video_options"))
					if options == "":
						PlayblastToolMessage("Warning. Instructions file " + melGlobals['gInstructionFile'] + " contains no encoder options. No movie will be made.")
						melGlobals['gDoMovie']=int(False)
						
					
					else:
						melGlobals['gEncoderVideoOptions']=options
						
					if melGlobals['gDoMovie'] and melGlobals['gDoAudio']:
						audio_options=str(mel.xml_getVar(encoderNode[0], "audio_options"))
						if audio_options == "":
							PlayblastToolMessage("Warning. Instructions file " + melGlobals['gInstructionFile'] + " contains no encoder audio options. No audio will be added to movie.")
							melGlobals['gDoAudio']=int(False)
							
						
						else:
							melGlobals['gEncoderAudioOptions']=audio_options
							
						
					
				
			
		
	overlayNode=mel.xml_getTag(outputNode[0], "overlay")
	# overlay
	if not len(overlayNode):
		PlayblastToolMessage("Warning. Instructions file " + melGlobals['gInstructionFile'] + " contains no overlay node. No overlay will be generated.")
		melGlobals['gDoOverlay']=int(False)
		
	
	else:
		doOverlay=str(mel.xml_getVar(overlayNode[0], "doOverlay"))
		melGlobals['gDoOverlay']=int((doOverlay == ""))
		melGlobals['gDoOverlay'] and False or int(doOverlay)
		if melGlobals['gDoOverlay']:
			overlayTemplate[0=str(mel.xml_getTag(overlayNode[0], "overlayTemplate"))
			if not len(overlayTemplate):
				PlayblastToolMessage("Warning. Instructions file " + melGlobals['gInstructionFile'] + " contains no overlay template. No overlay will be generated.")
				melGlobals['gDoOverlay']=int(False)
				
			
			else:
				melGlobals['gOverlayTemplate']=str(overlayTemplate[0])
				
			
		
	

# Example Instruction file:
'''

<job>

	<scene>

		<file name="/data/entertainment/15374_socom/animation/showWork/seq004/sg0001/004_0001_ani.ma" />

		<frameRange start="1" end="160" />

		<camera name="cameraMain" />

		<references switchProxyToFull="1" loadAllReferences="0" executePerAssetCallbacks="0" />

	</scene>

	<output>

		<target imagePath="/renders/entertainment/15374_socom/show/seq004/sg0001/animation/004_0001_ani" moviePath="/data/entertainment/15374_socom/animation/showWork/seq004/sg0001/playblasts/003_0001.0003.avi" />

		<quality shadingMode="shaded" setSmoothing="1" divisions="1" />

		<resolution width="720" height="486" aspectRatio="1.33" />

		<format imageFormat="jpg" />

		<movie makeMovie="1" includeAudio="1" audioPath="/data/entertainment/15374_socom/animation/showWork/seq004/sg0001/audio/004_0001.aiff" />

		<overlay doOverlay="1" artist="John Doe" displayArtistName="1" version="004_0001_ani_12.ma" />

	</output>



</job>

'''
# ---------------------------------------------------------------------------------------------------
def _getLoadSettingsRFNs():
	rfns=[]
	numLoadSettings=int(selLoadSettings(q=1,numSettings=1))
	rfns[0]=""
	for i in range(1,numLoadSettings):
		loadSettingID=[]
		loadSettingID[0]=str(str(i))
		refs=selLoadSettings(loadSettingID,
			q=1,rfn=1)
		rfns[i]=refs[0]
		
	return rfns
	

# ---------------------------------------------------------------------------------------------------
# PlayblastToolOpenScene - open the scene. If switch proxy to full or load all references is set, do a selective preload
# ---------------------------------------------------------------------------------------------------
def PlayblastToolOpenScene():
	melGlobals.initVar( 'string', 'gInputScene' )
	# The scene to playblast
	melGlobals.initVar( 'int', 'gRefSwitchProxyToFull' )
	# Use selective preload to switch proxy refs to full
	melGlobals.initVar( 'int', 'gRefLoadAllRefs' )
	# Load all references
	melGlobals.initVar( 'string', 'gPlayblastPreCallback' )
	# if it exists, this will be the path to the pre playblast callback
	melGlobals.initVar( 'string', 'gPlayblastPostCallback' )
	# if it exists, this will be the path to the post playblast callback
	#Cycle check test - 01/19/07 - JSA
	cycleCheck(e=False)
	# Disable loading of saved UI configuration - 03.04.2011 - JBarrett
	melGlobals.initVar( 'int', 'gUseScenePanelConfig' )
	melGlobals['gUseScenePanelConfig']=int(False)
	cmds.file(uc=False)
	# get the ref nodes and namespaces in the file
	avail_namespaces=[]
	avail_refNodes=[]
	mel.assetListFromMa(melGlobals['gInputScene'], avail_namespaces, avail_refNodes, [], [])
	if melGlobals['gRefSwitchProxyToFull'] or melGlobals['gRefLoadAllRefs']:
		cmds.file(buildLoadSettings=melGlobals['gInputScene'],ignoreVersion=1,o=1,f=1)
		# selective preload
		numLoadSettings=int(selLoadSettings(q=1,numSettings=1))
		# loop through references...0 is the parent scene, so leave this alone
		for i in range(1,numLoadSettings):
			loadSettingID[1=str([str(i)])
			if melGlobals['gRefSwitchProxyToFull']:
				proxyTags=selLoadSettings(loadSettingID,
					q=1,proxySetTags=1)
				print proxyTags
				if len(proxyTags):
					if mel.stringArrayFindIndex("Full", proxyTags) != -1:
						PlayblastToolMessage("selLoadSettings -e -activeProxy \"Full\" " + loadSettingID[0])
						selLoadSettings(loadSettingID,
							activeProxy="Full",e=1)
						
					
				
			
		cmds.file(melGlobals['gInputScene'],
			pmt=False,ignoreVersion=1,loadSettings="implicitLoadSettings",o=1,f=1)
		# Now load the scene
		# Delete the cached rigs that are in the file
		mel.AnimSlicesDeleteCachedRigs(avail_namespaces, avail_refNodes)
		if melGlobals['gRefLoadAllRefs']:
			# now load all references
			for i in range(0,len(avail_refNodes)):
				catch( lambda: cmds.file(lr=avail_refNodes[i]) )
				
			
		
	
	else:
		cmds.file(pmt=False,ignoreVersion=1,o=melGlobals['gInputScene'],f=1)
		
	mel.AnimSlicesDashboard.clearAllSettings()
	# turn cache visiblity, colors and HQ graphics on and then resync
	cacheVisibility=1
	cacheColorFromFile=1
	mel.AnimSlicesForceAllCaches(cacheVisibility, cacheColorFromFile)
	mel.AnimSlicesSetHQGraphicsAllCaches(1)
	mel.AnimSlicesUpdateAllCaches()
	

# ---------------------------------------------------------------------------------------------------
# PlayblastToolLookupImageFormat - look up the number for the given image format key, and print a warning if a supported one is not found (switch to jpg in this case)
# ---------------------------------------------------------------------------------------------------
def PlayblastToolLookupImageFormat(key):
	lookup=["jpg","8",
		"jpeg","8",
		"iff","7",
		"rla","2",
		"sgi","5",
		"tga","19",
		"tif","3",
		"tiff","3",
		"png","32",
		"PNG",
		"32"]
	# image type lookup
	'''
	
		Alias PIX (als) - 6
	
		Cineon (cin) - 11
	
		DDS (dds) - 35
	
		EPS (eps) - 9
	
		GIF (gif) - 0
	
		JPEG (jpg) - 8
	
		Maya IFF (iff) - 7
	
		Maya16 IFF (iff) - 10
	
		PSD (psd) - 31
	
		PSD Layered (psd) - 36
	
		PNG (png) - 32
	
		Quantel (yuv) - 12
	
		RLA (rla) - 2
	
		SGI (sgi) - 5
	
		SGI16 (sgi) - 13
	
		SoftImage (pic) - 1
	
		Targa (tga) - 19
	
		Tiff (tif) - 3
	
		Tiff16 (tif) - 4
	
		Windows Bitmap (bmp) - 20
	
	
	
		The playblast tool will only support the following -
	
		jpg, iff, rla, sgi, tga, tif
	
	
	
		For future versions of Maya, that have changed values - the following will spit them out:
	
	
	
		string $items[] = `optionMenuGrp -q -itemListShort imageMenuMayaSW`;
	
		for($i = 0; $i < size($items); $i += 1)
	
		{
	
			int $val = `menuItem -q -data $items[$i]`;
	
			string $label = `menuItem -q -label $items[$i]`;
	
	
	
			print($label + " - " + $val + "\n");
	
	
	
		}
	
	
	
		'''
	# include a couple of alternative representations - such as jpeg in addition to jpg, tiff as well as tif, just so we don't not find our format for trivial reasons!
	index=int(mel.stringArrayFindIndex(key.lower(), lookup))
	if index == -1:
		PlayblastToolMessage("Warning. Unsupported output format " + key + ". Defaulting to \"jpg\"")
		index=int(mel.stringArrayFindIndex("jpg", lookup))
		
	return int(lookup[index + 1])
	

def _PlayblastTool.setCurrentRenderer(renderer):
	setAttr("defaultRenderGlobals.currentRenderer",renderer,
		type="string")
	"""
	
			Set the given renderer in the render globals.
	
	
	
			@param renderer: The renderer to use.
	
			@type renderer: string
	
	
	
			@returns: 1 if successful.
	
			@rtype: int
	
	
	
		"""
	PlayblastToolMessage("Current renderer: " + str(getAttr("defaultRenderGlobals.currentRenderer")))
	return 1
	

def _PlayblastTool.loadRenderGlobalsPreset(preset_name):
	PlayblastToolMessage("Loading render globals preset '" + preset_name + "'.")
	"""
	
			Load the render globals with the given preset name.
	
	
	
			@param preset_name: The name of the render globals preset.
	
			@type preset_name: string
	
	
	
			@returns: 1 if successful.
	
			@rtype: int
	
	
	
		"""
	path=str(mel.getPath("ProjectPresetDir", [])) + "/renderGlobals"
	# Iterate over the render globals nodes.
	# string $renderer = currentRenderer();
	renderer="mayaSoftware"
	setAttr("defaultRenderGlobals.currentRenderer","mayaSoftware",
		type="string")
	nodes=renderer(renderer,
		q=1,globalsNodes=1)
	for node in nodes:
		node_type=str(nodeType(node))
		# Derive the path to the preset file.
		basename=node_type + "Preset_" + preset_name + ".mel"
		preset=path + "/" + basename
		if os.path.exists( preset ) and os.path.getsize( preset ):
			select(r=node)
			# If it exists, select the node and apply the preset.
			PlayblastToolMessage(preset)
			mel.eval("source \"" + preset + "\";")
			
		
	return 1
	

def _PlayblastTool.unlockAllAttrs(node):
	attrs=listAttr(node)
	"""
	
			Unlock all attributes on the given node.
	
	
	
			@param node: The node to unlock.
	
			@type node: string
	
	
	
		"""
	for attr in attrs:
		plug=node + "." + str(attr)
		setAttr(plug,
			lock=False)
		
	

# ---------------------------------------------------------------------------------------------------
# PlayblastToolSetupRenderGlobals - setup the render globals
# ---------------------------------------------------------------------------------------------------
def PlayblastToolSetupRenderGlobals():
	melGlobals.initVar( 'string', 'gOutputFmt' )
	# Output format for frames.
	melGlobals.initVar( 'int', 'gResWidth' )
	# x resolution to playblast at
	melGlobals.initVar( 'int', 'gResHeight' )
	# y resolution to playblast at
	melGlobals.initVar( 'float', 'gResAspect' )
	# aspect ratio
	melGlobals.initVar( 'int', 'gFrameRangeStart' )
	# Start frame to playblast
	melGlobals.initVar( 'int', 'gFrameRangeEnd' )
	# End frame (inclusive) to playblast
	melGlobals.initVar( 'int', 'gSoftwareRender' )
	# Whether or not to do a software render.
	melGlobals.initVar( 'string', 'gRenderGlobalsPreset' )
	# The render globals preset to load.
	val=int(PlayblastToolLookupImageFormat(melGlobals['gOutputFmt']))
	# lookup the number
	# Unlock the render globals nodes.
	_PlayblastTool.unlockAllAttrs("defaultRenderGlobals")
	_PlayblastTool.unlockAllAttrs("defaultResolution")
	# renderer
	if melGlobals['gSoftwareRender']:
		_PlayblastTool.setCurrentRenderer("mayaSoftware")
		
	if len(melGlobals['gRenderGlobalsPreset']):
		_PlayblastTool.loadRenderGlobalsPreset(melGlobals['gRenderGlobalsPreset'])
		# globals preset
		
	setAttr("defaultRenderGlobals.animation",
		True)
	# render globals
	setAttr("defaultRenderGlobals.endFrame",melGlobals['gFrameRangeEnd'])
	setAttr("defaultRenderGlobals.extensionPadding",4)
	setAttr("defaultRenderGlobals.imageFormat",val)
	setAttr("defaultRenderGlobals.outFormatControl",0)
	setAttr("defaultRenderGlobals.periodInExt",
		True)
	setAttr("defaultRenderGlobals.putFrameBeforeExt",
		True)
	setAttr("defaultRenderGlobals.startFrame",melGlobals['gFrameRangeStart'])
	setAttr("defaultRenderGlobals.useFrameExt",
		True)
	#multi processing
	#get num of local cpus
	buffer=internal.shellOutput("grep \"model name\" /proc/cpuinfo", convertNewlines=False, stripTrailingNewline=False).split("\n")
	#force software render to use all cpus
	setAttr("defaultRenderGlobals.numCpusToUse",
		(len(buffer)))
	#
	# resolution
	setAttr("defaultResolution.aspectLock",
		True)
	setAttr("defaultResolution.deviceAspectRatio",melGlobals['gResAspect'])
	setAttr("defaultResolution.height",melGlobals['gResHeight'])
	setAttr("defaultResolution.width",melGlobals['gResWidth'])
	# workspace
	tmp_dir=str(mel.getPath("TempFile", []))
	workspace(rt=("images", tmp_dir))
	

# ---------------------------------------------------------------------------------------------------
# PlayblastToolCheckCamera - check camera a) that it's there, b) that there are no multiples, and pop the shape name into a global variable
# ---------------------------------------------------------------------------------------------------
def PlayblastToolCheckCamera():
	melGlobals.initVar( 'string', 'gCamera' )
	# Cam to playblast thru
	melGlobals.initVar( 'string', 'gCameraShape' )
	# check to see if it's a stereo camera show
	PlayblastToolGetStereoCamera()
	# does it exist?
	if not objExists(melGlobals['gCamera']):
		PlayblastToolQuitError("Camera " + melGlobals['gCamera'] + " does not exist.")
		
	if len(ls(melGlobals['gCamera']))>1:
		PlayblastToolQuitError("Found more than one camera named " + melGlobals['gCamera'] + ".")
		# are there multiples?
		#	if(size (`ls ("*" + $gCamera)`) > 1)
		# The aboce will throw faulty error in the case of the stereo cam, where the L_cam and R_cam
		# will be picked up by *cam.  I believe this is just looking for muliple cameras with the same
		# name (different proper paths, e.g. foo|cam and bob|cam).
		
	children=listRelatives(c=1,pa=melGlobals['gCamera'])
	# is it a camera?
	children=ls(children,
		type='camera')
	if not len(children):
		PlayblastToolQuitError("Node " + melGlobals['gCamera'] + " is not a camera.")
		
	melGlobals['gCameraShape']=children[0]
	# hide things we don't want shown
	attrs=["displayFilmGate",
		"displaySafeAction",
		"displayResolution",
		"displayFieldChart",
		"displaySafeTitle",
		"displayFilmPivot",
		"displayFilmOrigin"]
	for i in range(0,len(attrs)):
		catch( lambda: setAttr((melGlobals['gCameraShape'] + "." + attrs[i]),
			l=False) )
		catch( lambda: setAttr((melGlobals['gCameraShape'] + "." + attrs[i]),False) )
		
	for cam in ls(type="camera"):
		catch( lambda: setAttr((str(cam) + ".visibility"),
			0) )
		
	catch( lambda: setAttr((melGlobals['gCameraShape'] + ".renderable"),
		l=0) )
	# Set the camera to overscan @ 1.0
	catch( lambda: setAttr((melGlobals['gCameraShape'] + ".renderable"),
		1) )
	catch( lambda: setAttr((melGlobals['gCameraShape'] + ".filmFit"),
		l=0) )
	catch( lambda: setAttr((melGlobals['gCameraShape'] + ".filmFit"),
		3) )
	catch( lambda: setAttr((melGlobals['gCameraShape'] + ".overscan"),
		l=0) )
	catch( lambda: setAttr((melGlobals['gCameraShape'] + ".overscan"),
		1.0) )
	

# ---------------------------------------------------------------------------------------------------
# PlayblastToolRemapPaths - take care of any paths that dirmapping doesn't
# ---------------------------------------------------------------------------------------------------
def PlayblastToolRemapPaths():
	nodes=ls(type='imagePlane')
	# imageplanes
	for i in range(0,len(nodes)):
		path=str(getAttr(nodes[i] + ".imageName"))
		path=str(mel.getPath("ConformPath", [path]))
		setAttr((nodes[i] + ".imageName"),
			path,
			type="string")
		
	

# ---------------------------------------------------------------------------------------------------
# PlayblastToolSetupModelEditor - set up the model editor
# ---------------------------------------------------------------------------------------------------
def PlayblastToolSetupModelEditor():
	melGlobals.initVar( 'string', 'gCamera' )
	melGlobals.initVar( 'string', 'gCameraShape' )
	melGlobals.initVar( 'string', 'gShadingMode' )
	# wireframe, shaded, or textured.
	#	global int $gWireframeOnShaded;
	melGlobals.initVar( 'int', 'gLighting' )
	# Open GL lighting
	melGlobals.initVar( 'int', 'gHighQualityRendering' )
	# Hi Quality GL renderer
	melGlobals.initVar( 'string', 'gMainPane' )
	# Alias
	melGlobals.initVar( 'int', 'gDoOverlay' )
	# Determines whether we will show locators
	melGlobals.initVar( 'int', 'gIsStereo' )
	# If 1 then playblast through the stereo camera
	melGlobals.initVar( 'string', 'gPlayblastStereoCameraLeft' )
	melGlobals.initVar( 'string', 'gPlayblastStereoCameraRight' )
	melGlobals.initVar( 'string', 'gInputScene' )
	# The scene to playblast
	melGlobals.initVar( 'string', 'gRFXPlayblastModelPanel' )
	melGlobals.initVar( 'int', 'gConsiderDisplayLayers' )
	if about():
		return 
		
	headsUpDisplay(lv=False)
	# turn off the hud
	dispAppear="smoothShaded"
	dispTex=int(False)
	if melGlobals['gShadingMode'] == "wireframe":
		dispAppear="wireframe"
		
	if melGlobals['gShadingMode'] == "textured":
		dispTex=int(True)
		# switch to a single pane
		
	mel.switchPanes('single', 0)
	panel1=str(paneLayout(melGlobals['gMainPane'],
		q=1,p1=1))
	melGlobals['gRFXPlayblastModelPanel']=panel1
	if melGlobals['gIsStereo']:
		print "PlayblastTool: lookThroughModelPanel \"" + melGlobals['gPlayblastStereoCameraLeft'] + "\" \"" + panel1 + "\"\n"
		#		PlayblastToolMessage(" Setting up stereo view port...");
		#		/*
		#		PlayblastToolMessage("	Setting up stereo view port via python...");
		#		print("  Setting up stereo view port via python...\n");
		#		PlayblastToolMessage("	import...");
		#		python("import maya.mel as mel");
		#		PlayblastToolMessage("	stereoCameraSwitchToCamera...");
		#		python("mel.eval('stereoCameraSwitchToCamera " + $gCamera + " " + $panel1 + "')");
		#		PlayblastToolMessage("	from maya.app...");
		#		python("from maya.app.stereo import stereoCameraCustomPanel");
		#		PlayblastToolMessage("	stereoCameraCustromPanel.switch.");
		#		python("stereoCameraCustomPanel.switchToCamera(\"" + $gCamera + "\", \"StereoPanelEditor\")");
		#		PlayblastToolMessage("Done setting up stereo view port via python.");
		#		print("Done setting up stereo view port via python.\n");
		#		*/
		#		string $cmd = "source buildStereoLookthruMenu.mel;";
		#		eval $cmd;
		#		print("sourcing buildStereoLookthruMenu\n");
		#
		#		PlayblastToolMessage("	 stereoCameraSwitchToCamera " + $gCamera + " " + $panel1);
		#		catch(`stereoCameraSwitchToCamera $gCamera $panel1`);
		#		PlayblastToolMessage("Done setting up stereo view port.");
		#
		#		$panel1 = "StereoPanelEditor"; // the way alias gets the name of this panle is with `getPanel -withFocus` + "Editor"...
		#		$gRFXPlayblastModelPanel = $panel1;
		mel.lookThroughModelPanel(melGlobals['gPlayblastStereoCameraLeft'], panel1)
		
	
	else:
		mel.lookThroughModelPanel(melGlobals['gCameraShape'], panel1)
		
	displayLights="default"
	# lighting
	if melGlobals['gLighting']:
		buf=melGlobals['gConsiderDisplayLayers']
		# look for visible lights in the scene before turning on lighting
		melGlobals['gConsiderDisplayLayers']=int(True)
		okforLighting=int(False)
		allLights=ls(type="light")
		for i in range(0,len(allLights)):
			if mel.isVisible(allLights[i]):
				okforLighting=int(True)
				break
				
			
		if okforLighting:
			displayLights="all"
			
		
		else:
			PlayblastToolMessage("Lighting requested but there are no visible lights in the scene. Ignoring...")
			
		melGlobals['gConsiderDisplayLayers']=buf
		
	modelEditor(panel1,
		jointXray=0,
		manipulators=0,
		controlVertices=1,
		fogMode="linear",
		textureDisplay="modulate",
		viewSelected=0,
		transparencyAlgorithm="perPolygonSort",
		activeComponentsXray=0,
		textureHilight=1,
		activeOnly=0,
		deformers=0,
		dynamics=1,
		subdivSurfaces=1,
		displayAppearance=dispAppear,
		ikHandles=0,
		textureMaxSize=4096,
		textureSampling=1,
		cameras=1,
		fogStart=0,
		displayTextures=dispTex,
		fogSource="fragment",
		xray=0,
		lights=0,
		handles=0,
		nurbsCurves=0,
		joints=0,
		locators=melGlobals['gDoOverlay'],
		fogDensity=0.1,
		displayLights=displayLights,
		smoothWireframe=0,
		textures=0,
		sortTransparent=1,
		pivots=0,
		strokes=0,
		selectionHiliteDisplay=1,
		polymeshes=1,
		grid=0,
		fogEnd=100,
		useInteractiveMode=0,
		fogColor=(0.5, 0.5, 0.5, 1),
		nurbsSurfaces=1,
		backfaceCulling=0,
		shadows=0,
		headsUpDisplay=1,
		e=1,
		hulls=1,
		dimensions=0,
		hairSystems=0,
		textureAnisotropic=0,
		twoSidedLighting=1,
		planes=0,
		wireframeOnShaded=0,
		lineWidth=1,
		useDefaultMaterial=0,
		fogging=0)
	# turn off everything that we don't want to see, turn on everything we do.
	#		-camera "front"
	#		-bufferMode "double"
	#		-maxConstantTransparency 1
	#		-colorResolution 4 4
	#		-bumpResolution 4 4
	#		-textureCompression 0
	#		-transpInShadows 0
	#		-cullingOverride "none"
	#		-lowQualityLighting 0
	#		-maximumNumHardwareLights 0
	#		-occlusionCulling 0
	#		-shadingModel 0
	#		-useBaseRenderer 0
	#		-useReducedRenderer 0
	#		-smallObjectCulling 0
	#		-smallObjectThreshold -1
	#		-interactiveDisableShadows 0
	#		-interactiveBackFaceCull 0
	#		-fluids 0
	#		-hairSystems 0
	#		-follicles 0
	#		-nCloths 0
	#		-nParticles 0
	#		-nRigids 0
	#		-dynamicConstraints 0
	# Shading
	#$gWireframeOnShaded
	# Hardware Texturing
	# Hardware Fog
	# Lighting
	# Isolate Select
	# Show
	#	PlayblastToolMessage("Setting up modelEditor.");
	# High Quality Rendering
	if melGlobals['gHighQualityRendering'] == 0:
		modelEditor(panel1,
			rendererName="base_OpenGL_Renderer",e=1)
		setAttr("hardwareRenderingGlobals.multiSampleEnable",0)
		
	if melGlobals['gHighQualityRendering'] == 1:
		PlayblastToolMessage("Rendering with High Quality")
		modelEditor(panel1,
			rendererName="hwRender_OpenGL_Renderer",e=1)
		setAttr("hardwareRenderingGlobals.multiSampleEnable",0)
		
	if melGlobals['gHighQualityRendering'] == 2:
		PlayblastToolMessage("Rendering with Viewport 2.0")
		ActivateViewport20()
		setAttr("hardwareRenderingGlobals.multiSampleEnable",1)
		# Use all lights and display shadows otherwise why use viewport 2.0
		DisplayLight()
		modelEditor(panel1,
			shadows=True,e=1)
		
	

# apply shading mode
#	modelEditor -e -displayAppearance $dispAppear -displayTextures $dispTex -useDefaultMaterial off $panel1;
#	PlayblastToolMessage("modelEditor -e -displayAppearance " + $dispAppear + " -displayTextures " + $dispTex + " -useDefaultMaterial off " + $panel1);
# set up the anaplyph mode if we are doing stereo cameras
#
#	if($gIsStereo)
#	{
#		PlayblastToolMessage("Setting up anaplyph...");
#		print("Setting up anaplyph...\n");
#		stereoCameraView -e -displayMode anaglyph $panel1;
#		//python("stereoCameraCustomPanel.stereoCameraViewCallback( \"StereoPanelEditor\", \"{'displayMode': 'anaglyph'}\" )");
#		PlayblastToolMessage("Setting stereo panel mode to anaplyph for panel " + $panel1);
#	}
# ---------------------------------------------------------------------------------------------------
# PlayblastToolSourceScript - source the script. This has to be it's own proc, because you can't directly catch a source statement
# ---------------------------------------------------------------------------------------------------
def PlayblastToolSourceScript(file):
	mel.eval("source \"" + file + "\"")
	

# ---------------------------------------------------------------------------------------------------
# PlayblastToolExecutePerAssetCallbacks - execute per asset callbacks if desired and if they exist
# ---------------------------------------------------------------------------------------------------
def PlayblastToolExecutePerAssetCallbacks():
	melGlobals.initVar( 'int', 'gExecutePerAssetCallbacks' )
	# Execute per asset callbacks if any exist
	if not melGlobals['gExecutePerAssetCallbacks']:
		PlayblastToolMessage("Per-Asset Callbacks disabled.")
		return 
		
	refs=cmds.file(q=1,r=1)
	for i in range(0,len(refs)):
		ns=str(cmds.file(refs[i],
			q=1,ns=1))
		assetName=str(mel.getPath("AssetNameFromFilename", [refs[i]]))
		assetType=str(mel.getPath("AssetTypeFromFilename", [refs[i]]))
		assetInfoDir=str(mel.getPath("AssetInfoDir", [assetType,assetName]))
		callback=assetInfoDir + "/" + assetName + "PlayblastCallback.mel"
		if not os.path.exists( callback ) and os.path.getsize( callback ):
			PlayblastToolMessage("No callback found for " + assetName + ".")
			continue
			
		success=not (catch( lambda: PlayblastToolSourceScript(callback) ))
		if success:
			procName=assetName + "PlayblastCallback"
			if not mel.exists(procName):
				PlayblastToolMessage("Callback " + callback + " found. But no global proc " + procName + ". Callback will not be executed.")
				continue
				
			PlayblastToolMessage("Executing per-asset callback " + callback + ". ")
			success=not (catch( lambda: mel.eval(procName + " \"" + ns + "\"") ))
			if not success:
				PlayblastToolMessage("Error executing " + callback + ". Continuing..")
				continue
				
			
		
		else:
			PlayblastToolMessage("Warning: Error sourcing callback " + callback + ". Callback will not be executed.")
			
		
	

# ---------------------------------------------------------------------------------------------------
# PlayblastToolCheckMakeDir - See if the directory exists, if not make it, then check that we were able to
# ---------------------------------------------------------------------------------------------------
def PlayblastToolCheckMakeDir(dir):
	melGlobals.initVar( 'string', 'gInputScene' )
	# 02/02/07 - make the output dir subfolders
	# Output format for frames.
	melGlobals.initVar( 'string', 'gOutputFmt' )
	# Output format for frames.
	melGlobals.initVar( 'int', 'gFrameRangeStart' )
	# Start frame to playblast
	melGlobals.initVar( 'int', 'gFrameRangeEnd' )
	# End frame (inclusive) to playblast
	melGlobals.initVar( 'string', 'gTargetMoviePath' )
	# input will be something like /data/development/17199_pipeline_dir_test_new/cg/sequences/sq9000/sh0010/movies/lay
	# in old dir structure, input will be something like:
	# /data/entertainment/16252_webosaurs/animation/showWork/seqBATL/sg1010/playblasts
	# this is also called to make the output directory for frames, in this case the input will be something like:
	# new structure: /data/development/17199_pipeline_dir_test_new/cg/sequences/sq9000/sh0010/movies/lay/frames
	# old structure: /renders/entertainment/16252_webosaurs/show/seqBATL/sg1010/animation/standard/
	# also gTargetMoviePath will be:
	#
	# /data/development/17199_pipeline_dir_test_new/cg/sequences/sq9000/sh0010/movies/lay/9000_0010_lay.0001.mov
	# or /data/entertainment/16252_webosaurs/animation/showWork/seqBATL/sg1010/playblasts/BATL_1010_ani.0011.mov
	sequence=str(mel.getPath("SequenceFromFilename", [melGlobals['gInputScene']]))
	shot=str(mel.getPath("ShotFromFilename", [melGlobals['gInputScene']]))
	archiveDir=dir + "/archive"
	playblastDir=str(mel.getPath("ShotMovieDir", [sequence,shot]))
	tmp=str(mel.dirname(melGlobals['gTargetMoviePath']))
	isMovieDir=int((mel.getPath("ConformPath", [dir]) == mel.getPath("ConformPath", [tmp])))
	#	PlayblastToolMessage("DEBUG: PlayblastToolCheckMakeDir: dir = " + $dir);
	#	PlayblastToolMessage("DEBUG: PlayblastToolCheckMakeDir: isMovieDir = " + $isMovieDir);
	if os.path.isdir( dir ):
		if not isMovieDir:
			PlayblastToolMessage("Pre-playblast frame creation disabled.")
			#Since we now create our archives up front, we should delete prexisting frames from this folder
			#to guarantee we don't have old frames left hanging around after a change in editorial
			#This does not yet handle a second file type (like tga)
			#if(!`gmatch $dir "*playblasts*"`)
			# Need to delete 'extra' frames in the post process.
			# string $path = $dir + "/";
			# string $file;
			# string $fileSpec = "*." + $gOutputFmt;
			# string $fileList[] = `getFileList -fld $path -fs $fileSpec`;
			# for($file in $fileList)
			# {
			# 	$file = $path + $file;
			# 	sysFile -delete $file;
			# }
			# PlayblastToolMessage("Deleted frames in " + $path + " from previous playblast");
			#			if(($gFrameRangeEnd - $gFrameRangeStart) < 1000)
			#			{
			#				//Touch empty placeholders of the correct frame range.	These will be written over in a minute.
			#				string $temp_file;
			#				for($i = $gFrameRangeStart; $i <= $gFrameRangeEnd; $i += 1)
			#				{
			#					//Use getPath?
			#					$temp_file = $dir + "/" + $sequence + "_" + $shot + "." + padNumber($i, 4) + "." + $gOutputFmt + "\n";
			#					system("touch " + $temp_file);
			#				}
			#			}
			#			else
			#			{
			#			}
			
		return 1
		
	
	else:
		os.mkdir( dir ) 
		
	if not os.path.isdir( dir ):
		PlayblastToolQuitError("Couldn't create output directory " + dir + ". Check the permissions.")
		#Skip creating /archive and /playblast subfolders if $dir is a /playblasts folder
		
	if not isMovieDir:
		os.mkdir( archiveDir ) 
		if not os.path.isdir( archiveDir ):
			PlayblastToolQuitError("Couldn't create output directory " + archiveDir + ". Check the permissions.")
			
		os.mkdir( playblastDir ) 
		if not os.path.isdir( playblastDir ):
			PlayblastToolQuitError("Couldn't create output directory " + playblastDir + ". Check the permissions.")
			
		
	return 0
	

# ---------------------------------------------------------------------------------------------------
# PlayblastToolArchiveDir - See if the archive directory exists, if not make it and move the old frames
# ---------------------------------------------------------------------------------------------------
def PlayblastToolArchiveDir(dir,timestamp):
	archiveDir=dir + "/archive/" + str(timestamp)
	os.mkdir( archiveDir ) 
	if not os.path.isdir( archiveDir ):
		PlayblastToolQuitError("Couldn't create archive directory " + archiveDir + ". Check the permissions.")
		
	catch( lambda: internal.shellOutput("/bin/mv " + dir + "/*.png " + archiveDir, convertNewlines=False, stripTrailingNewline=False) )
	#catch(`system("/bin/mv " + $dir + "/*.tga " + $archiveDir)`);
	

# -----------------------------------------------------------------------------------------------------------
# PlayblastToolVersionDir - See if the versioned directory exists, if not make it and copy the current frames
# -----------------------------------------------------------------------------------------------------------
def PlayblastToolVersionDir():
	print "No tool version dir process\n"
	return 
	'''
	
		global string $gTargetMoviePath;
	
		global string $gTargetImagePath;
	
	
	
		print("PlayblastToolVersionDir started.\n");
	
	
	
		//From $gTargetMoviePath get the playblast version
	
		string $buffer[];
	
		$numTokens = tokenize((basename($gTargetMoviePath, "")), ".", $buffer);
	
		string $version_only = $buffer[1];
	
		string $version = $buffer[0] + "_" + $buffer[1];
	
	
	
		//From $gTargetImagePath get the path to the playblast render folder
	
		string $dir = dirname($gTargetImagePath);
	
		print("$dir = " + $dir + "\n");
	
	
	
		//Put it together for the the full $versionDir path
	
		string $versionDir = $dir + "/archive/" + $version; //we may move this up a level and discard the archive folder
	
	
	
		// If the version dir exists, empty it out.
	
		if(`filetest -d $versionDir`)
	
		{
	
			// use xargs when deleting large numbers of files
	
			catch(`system("ls " + $versionDir + "/*.png | xargs rm")`);
	
			string $file;
	
			string $fileList[] = `getFileList -fld $dir -filespec "*.png"`;
	
			for($file in $fileList)
	
			{
	
				$numTokens = tokenize($file, ".", $buffer);
	
				catch(`system("/bin/cp " + $dir + $file + " " + $versionDir + "/" + $version + "." + $buffer[1] + "." + $buffer[2])`);
	
			}
	
		}
	
		// If not, create it.
	
		else
	
		{
	
			sysFile -md $versionDir;
	
			if(!`filetest -d $versionDir`)
	
			{
	
				PlayblastToolQuitError("Couldn't create versioned directory " + $versionDir + ". Check the permissions.");
	
			}
	
			else
	
			{
	
				string $file;
	
				string $fileList[] = `getFileList -fld $dir -filespec "*.png"`;
	
				for($file in $fileList)
	
				{
	
					$numTokens = tokenize($file, ".", $buffer);
	
					catch(`system("/bin/cp " + $dir + $file + " " + $versionDir + "/" + $version + "." + $buffer[1] + "." + $buffer[2])`);
	
				}
	
			}
	
		}
	
	
	
		string $fileList[] = `getFileList -fld ($dir + "/") -fs "*.png"`;
	
		for($file in $fileList)
	
		{
	
			$numTokens = tokenize($file, ".", $buffer);
	
			//catch(`system("/bin/cp " + $dir + "/" + $file + " " + $versionDir + "/" + $version + "." + $buffer[1] + "." + $buffer[2])`);
	
			string $src_file = $dir + "/" + $file;
	
			string $dst_file = $versionDir + "/" + $buffer[0] + "_" + $version_only + "." + $buffer[1] + "." + $buffer[2];
	
			evalEcho("sysFile -mov \"" + $dst_file + "\" \"" + $src_file + "\";");
	
	
	
			string $link_file = "archive/" + $version + "/" + $buffer[0] + "_" + $version_only + "." + $buffer[1] + "." + $buffer[2];
	
			evalEcho("system(\"ln -s " + $link_file + " " + $src_file + "\");");
	
		}
	
		'''
	

# ---------------------------------------------------------------------------------------------------
# PlayblastToolDeepPlayblastSetup - setup namespace render layer and make deep playblast xml file
# ---------------------------------------------------------------------------------------------------
def PlayblastToolDeepPlayblastSetup():
	melGlobals.initVar( 'string', 'gInputScene' )
	# the scene to playblast
	melGlobals.initVar( 'int', 'gDoDeepPlayblast' )
	# deep playblast
	melGlobals.initVar( 'string', 'gNamespaceRenderLayer' )
	# name of the render layer that has namespace info coded
	melGlobals.initVar( 'string[]', 'gMeshesWithColorsOn' )
	melGlobals.initVar( 'string[]', 'gGpuMeshes' )
	melGlobals.initVar( 'string', 'gTargetMoviePath' )
	melGlobals.initVar( 'string', 'gDeepPlayblastMoviePath' )
	if melGlobals['gDoDeepPlayblast']:
		strucfile=""
		temp_strucfile=0
		seq=str(mel.getPath("SequenceFromFilename", [melGlobals['gInputScene']]))
		shot=str(mel.getPath("ShotFromFilename", [melGlobals['gInputScene']]))
		comp=str(mel.getPath("ComponentFromFilename", [melGlobals['gInputScene']]))
		if comp == "lay":
			temp_strucfile=1
			# create a temporary structure file from the current maya file
			strucfile=str(mel.getPath("TempFileUnique", ["strucfile.xml"]))
			mel.exportStructure(seq, shot, strucfile)
			
		
		else:
			strucfile=str(mel.getPath("ShotInfoDir", [seq,shot])) + "/" + seq + "_" + shot + "_structure.xml"
			# use the regular structure file
			
		mel.eval("source \"DeepPlayblastUtilities.mel\"")
		melGlobals['gNamespaceRenderLayer']=str(mel.DeepPlayblastMakeNamespaceRenderLayer(strucfile, melGlobals['gGpuMeshes']))
		if melGlobals['gNamespaceRenderLayer'] == "":
			PlayblastToolWarning("Failed to create render layer for Deep Playblast.")
			melGlobals['gGpuMeshes']=[]
			melGlobals['gDoDeepPlayblast']=0
			
		
		else:
			melGlobals['gMeshesWithColorsOn']=[]
			allmeshes=ls(type="mesh")
			for obj in allmeshes:
				displayColors=int(getAttr(str(obj) + ".displayColors"))
				if displayColors:
					melGlobals['gMeshesWithColorsOn'] += [str(obj)]
					
				
			melGlobals['gDeepPlayblastMoviePath']=melGlobals['gTargetMoviePath'].replace("mov$","deep.mov")
			playblastXml=str(mel.DeepPlayblastMakeXML(strucfile, melGlobals['gDeepPlayblastMoviePath'], "2"))
			xmlFilename=melGlobals['gTargetMoviePath'].replace("mov$","xml")
			if comp == "lay" and os.path.exists( xmlFilename ) and os.path.getsize( xmlFilename ):
				xml=str(mel.readXML(xmlFilename, 0))
				# the xml file already exists and we are in layout,
				# check if the file has slices, and if it does, back it up
				slices=mel.xml_getTag(xml, "Slice")
				if len(slices)>0:
					vers=1 + int(mel.getVersion("FromFilenameGeneric", [xmlFilename]))
					versStr=str(mel.padNumber(vers, 4))
					backupFilename=xmlFilename.replace("xml$",(versStr + ".xml"))
					shutil.copy( xmlFilename, backupFilename )
					
				
			mel.writeFile(xmlFilename, playblastXml)
			
		if temp_strucfile:
			os.remove( strucfile )
			
		
	

def _pushRenderLayer(renderLayer):
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
		
	mel.DeepPlayblastHandleGpuMeshRenderLayer(melGlobals['gGpuMeshes'], 1)
	mel.DeepPlayblastPushNamespaceMaterials()
	

def _popRenderLayer():
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
		
	mel.DeepPlayblastHandleGpuMeshRenderLayer(melGlobals['gGpuMeshes'], 0)
	mel.DeepPlayblastPopNamespaceMaterials()
	

# ------------------------------------------------------------------------- //
# Software Rendering.
# ------------------------------------------------------------------------- //
def _PlayblastTool.executeRender(camera,frame_num,output_path):
	result=""
	"""
	
			Render a single frame using the current renderer.
	
	
	
			@param camera: The camera to render through.
	
			@type camera: string
	
			@param frame_num: The frame to render.
	
			@type frame_num: float
	
			@param output_path: The path to the image file including the basename.
	
			@type output_path: string
	
	
	
			@returns: The path to the rendered image.
	
			@rtype: string
	
	
	
		"""
	# Set the frame range.
	setAttr("defaultRenderGlobals.startFrame",frame_num)
	setAttr("defaultRenderGlobals.endFrame",frame_num)
	# Make sure the camera is renderable.
	setAttr((camera + ".renderable"),True)
	# Render the image.
	filename=str(render(camera))
	# Rebuild the image path using the desired output_path.
	basename=str(mel.basename(filename, ""))
	comps=basename.split(".")
	comps[0]=output_path
	final_path=".".join(comps)
	# Move the image.
	success=os.rename( filename, final_path )
	if not success:
		mel.warning("Could not move:\n\t" + filename + "\n\t" + final_path)
		
	
	else:
		PlayblastToolMessage("Rendered " + final_path + "\n")
		
	result=final_path
	return result
	

def _PlayblastTool.executeRenderRangeBy(camera,start_frame,end_frame,by_frame,output_path):
	result=[]
	"""
	
			Render a frame range by the given increment using the current renderer.
	
	
	
			@param camera: The camera to render through.
	
			@type camera: string
	
			@param start_frame: The first frame to render.
	
			@type start_frame: float
	
			@param end_frame: The last frame to render.
	
			@type end_frame: float
	
			@param by_frame: The increment between frames to render.
	
			@type by_frame: float
	
			@param output_path: The path to the image file including the basename.
	
			@type output_path: string
	
	
	
			@returns: The paths to the rendered images.
	
			@rtype: string[]
	
	
	
		"""
	frame=0.0
	for frame in range(start_frame,end_frame+1,by_frame):
		result.append(str(_PlayblastTool.executeRender(camera, frame, output_path)))
		
	return result
	

def _PlayblastTool.executeRenderRange(camera,start_frame,end_frame,output_path):
	result=_PlayblastTool.executeRenderRangeBy(camera, start_frame, end_frame, 1.0, output_path)
	"""
	
			Render a frame range using the current renderer.
	
	
	
			@param camera: The camera to render through.
	
			@type camera: string
	
			@param start_frame: The first frame to render.
	
			@type start_frame: float
	
			@param end_frame: The last frame to render.
	
			@type end_frame: float
	
			@param output_path: The path to the image file including the basename.
	
			@type output_path: string
	
	
	
			@returns: The paths to the rendered images.
	
			@rtype: string[]
	
	
	
		"""
	return result
	

# ---------------------------------------------------------------------------------------------------
# PlayblastToolPlayblastAFrame - ?
# ---------------------------------------------------------------------------------------------------
def PlayblastToolPlayblastAFrame(frameNum):
	melGlobals.initVar( 'int', 'gFrameRangeStart' )
	# Start frame to playblast
	melGlobals.initVar( 'int', 'gFrameRangeEnd' )
	# End frame (inclusive) to playblast
	melGlobals.initVar( 'string', 'gTargetImagePath' )
	# Where to write images. Path, plus base name
	melGlobals.initVar( 'int', 'gResWidth' )
	# x resolution to playblast at
	melGlobals.initVar( 'int', 'gResHeight' )
	# y resolution to playblast at
	melGlobals.initVar( 'string', 'gLocal' )
	melGlobals.initVar( 'string', 'gOutputFmt' )
	melGlobals.initVar( 'string', 'gRFXPlayblastModelPanel' )
	#global int $gIsStereo;			// If 1 then playblast through the stereo camera
	melGlobals.initVar( 'int', 'gDoStereoPlayblast' )
	melGlobals.initVar( 'int', 'gDoDeepPlayblast' )
	melGlobals.initVar( 'string', 'gNamespaceRenderLayer' )
	melGlobals.initVar( 'int', 'gDoReload' )
	melGlobals.initVar( 'int', 'gDoHires' )
	melGlobals.initVar( 'int', 'gSoftwareRender' )
	melGlobals.initVar( 'string', 'gCameraShape' )
	melGlobals.initVar( 'string', 'gPlayblastStereoCameraLeft' )
	melGlobals.initVar( 'string', 'gPlayblastStereoCameraRight' )
	playblastCmd="playblast"
	playblastCmd+=" -cc true"
	playblastCmd+=" -v false"
	playblastCmd+=" -orn false"
	playblastCmd+=" -wh " + str(melGlobals['gResWidth']) + " " + str(melGlobals['gResHeight'])
	playblastCmd+=" -p 100"
	playblastCmd+=" -fmt \"image\""
	playblastCmd+=" -c " + melGlobals['gOutputFmt']
	playblastCmd+=" -st " + str(frameNum)
	playblastCmd+=" -et " + str(frameNum)
	# For local playblasts only, add the "offscreen" flag
	''' if ($gLocal != "") '''
	playblastCmd+=" -os "
	print str(str(frameNum)) + "\n"
	if melGlobals['gDoStereoPlayblast']:
		if melGlobals['gSoftwareRender']:
			_PlayblastTool.executeRender(melGlobals['gPlayblastStereoCameraLeft'], frameNum, melGlobals['gTargetImagePath'] + "_l")
			_PlayblastTool.executeRender(melGlobals['gPlayblastStereoCameraRight'], frameNum, melGlobals['gTargetImagePath'] + "_r")
			if melGlobals['gDoDeepPlayblast']:
				_pushRenderLayer(melGlobals['gNamespaceRenderLayer'])
				_PlayblastTool.executeRender(melGlobals['gPlayblastStereoCameraLeft'], frameNum, melGlobals['gTargetImagePath'] + "_ns")
				_popRenderLayer()
				
			
		
		else:
			mel.lookThroughModelPanel(melGlobals['gPlayblastStereoCameraLeft'], melGlobals['gRFXPlayblastModelPanel'])
			left_cmd=playblastCmd + " -filename \"" + melGlobals['gTargetImagePath'] + "_l\""
			PlayblastToolMessage(left_cmd)
			mel.eval(left_cmd)
			if melGlobals['gDoDeepPlayblast']:
				_pushRenderLayer(melGlobals['gNamespaceRenderLayer'])
				ns_cmd=playblastCmd + " -filename \"" + melGlobals['gTargetImagePath'] + "_ns\""
				PlayblastToolMessage(ns_cmd)
				mel.eval(ns_cmd)
				_popRenderLayer()
				
			mel.lookThroughModelPanel(melGlobals['gPlayblastStereoCameraRight'], melGlobals['gRFXPlayblastModelPanel'])
			right_cmd=playblastCmd + " -filename \"" + melGlobals['gTargetImagePath'] + "_r\""
			PlayblastToolMessage(right_cmd)
			mel.eval(right_cmd)
			
		
	
	elif melGlobals['gSoftwareRender']:
		_PlayblastTool.executeRender(melGlobals['gCameraShape'], frameNum, melGlobals['gTargetImagePath'])
		if melGlobals['gDoDeepPlayblast']:
			_pushRenderLayer(melGlobals['gNamespaceRenderLayer'])
			_PlayblastTool.executeRender(melGlobals['gCameraShape'], frameNum, melGlobals['gTargetImagePath'] + "_ns")
			_popRenderLayer()
			
		
	
	elif melGlobals['gDoDeepPlayblast']:
		_pushRenderLayer(melGlobals['gNamespaceRenderLayer'])
		ns_cmd=playblastCmd + " -filename \"" + melGlobals['gTargetImagePath'] + "_ns\""
		PlayblastToolMessage(ns_cmd)
		mel.eval(ns_cmd)
		_popRenderLayer()
		
	playblastCmd+=" -filename \"" + melGlobals['gTargetImagePath'] + "\""
	PlayblastToolMessage(playblastCmd)
	mel.eval(playblastCmd)
	nextFrame=frameNum + 1
	# go to the next frame and call again
	if nextFrame>melGlobals['gFrameRangeEnd']:
		mel.PlayblastToolPostPlayblast()
		# done with playblast - call the rest of the process
		
	
	else:
		currentTime(nextFrame)
		evalDeferred(lp=("PlayblastToolPlayblastAFrame(" + str(str(nextFrame)) + ");"))
		
	

# ---------------------------------------------------------------------------------------------------
# PlayblastToolPlayblastAll - ?
# ---------------------------------------------------------------------------------------------------
def PlayblastToolPlayblastAll():
	melGlobals.initVar( 'int', 'gFrameRangeStart' )
	# Start frame to playblast
	melGlobals.initVar( 'int', 'gFrameRangeEnd' )
	# End frame (inclusive) to playblast
	melGlobals.initVar( 'string', 'gTargetImagePath' )
	# Where to write images. Path, plus base name
	melGlobals.initVar( 'int', 'gResWidth' )
	# x resolution to playblast at
	melGlobals.initVar( 'int', 'gResHeight' )
	# y resolution to playblast at
	melGlobals.initVar( 'string', 'gRFXPlayblastModelPanel' )
	#global int $gIsStereo;			// If 1 then playblast through the stereo camera
	melGlobals.initVar( 'int', 'gDoStereoPlayblast' )
	melGlobals.initVar( 'int', 'gDoDeepPlayblast' )
	melGlobals.initVar( 'string', 'gNamespaceRenderLayer' )
	melGlobals.initVar( 'int', 'gSoftwareRender' )
	melGlobals.initVar( 'string', 'gCameraShape' )
	melGlobals.initVar( 'string', 'gPlayblastStereoCameraLeft' )
	melGlobals.initVar( 'string', 'gPlayblastStereoCameraRight' )
	melGlobals.initVar( 'string', 'gLocal' )
	melGlobals.initVar( 'string', 'gOutputFmt' )
	playblastCmd="playblast"
	playblastCmd+=" -cc true"
	playblastCmd+=" -v false"
	playblastCmd+=" -orn false"
	playblastCmd+=" -wh " + str(melGlobals['gResWidth']) + " " + str(melGlobals['gResHeight'])
	playblastCmd+=" -p 100"
	playblastCmd+=" -fmt \"image\""
	playblastCmd+=" -c " + melGlobals['gOutputFmt']
	playblastCmd+=" -st " + str(melGlobals['gFrameRangeStart'])
	playblastCmd+=" -et " + str(melGlobals['gFrameRangeEnd'])
	# For local playblasts only, add the "offscreen" flag
	if melGlobals['gLocal'] != "":
		playblastCmd+=" -os "
		
	if melGlobals['gDoStereoPlayblast']:
		if melGlobals['gSoftwareRender']:
			mel.PlayblastTool.doPreroll()
			_PlayblastTool.executeRenderRange(melGlobals['gPlayblastStereoCameraLeft'], melGlobals['gFrameRangeStart'], melGlobals['gFrameRangeEnd'], melGlobals['gTargetImagePath'] + "_l")
			mel.PlayblastTool.doPreroll()
			_PlayblastTool.executeRenderRange(melGlobals['gPlayblastStereoCameraRight'], melGlobals['gFrameRangeStart'], melGlobals['gFrameRangeEnd'], melGlobals['gTargetImagePath'] + "_r")
			if melGlobals['gDoDeepPlayblast']:
				_pushRenderLayer(melGlobals['gNamespaceRenderLayer'])
				mel.PlayblastTool.doPreroll()
				_PlayblastTool.executeRenderRange(melGlobals['gPlayblastStereoCameraLeft'], melGlobals['gFrameRangeStart'], melGlobals['gFrameRangeEnd'], melGlobals['gTargetImagePath'] + "_ns")
				_popRenderLayer()
				
			
		
		else:
			mel.PlayblastTool.doPreroll()
			mel.lookThroughModelPanel(melGlobals['gPlayblastStereoCameraLeft'], melGlobals['gRFXPlayblastModelPanel'])
			left_cmd=playblastCmd + " -filename \"" + melGlobals['gTargetImagePath'] + "_l\""
			PlayblastToolMessage(left_cmd)
			mel.eval(left_cmd)
			if melGlobals['gDoDeepPlayblast']:
				_pushRenderLayer(melGlobals['gNamespaceRenderLayer'])
				mel.PlayblastTool.doPreroll()
				ns_cmd=playblastCmd + " -filename \"" + melGlobals['gTargetImagePath'] + "_ns\""
				PlayblastToolMessage(ns_cmd)
				mel.eval(ns_cmd)
				_popRenderLayer()
				
			mel.PlayblastTool.doPreroll()
			mel.lookThroughModelPanel(melGlobals['gPlayblastStereoCameraRight'], melGlobals['gRFXPlayblastModelPanel'])
			right_cmd=playblastCmd + " -filename \"" + melGlobals['gTargetImagePath'] + "_r\""
			PlayblastToolMessage(right_cmd)
			mel.eval(right_cmd)
			
		
	
	elif melGlobals['gSoftwareRender']:
		mel.PlayblastTool.doPreroll()
		_PlayblastTool.executeRenderRange(melGlobals['gCameraShape'], melGlobals['gFrameRangeStart'], melGlobals['gFrameRangeEnd'], melGlobals['gTargetImagePath'])
		if melGlobals['gDoDeepPlayblast']:
			_pushRenderLayer(melGlobals['gNamespaceRenderLayer'])
			mel.PlayblastTool.doPreroll()
			_PlayblastTool.executeRenderRange(melGlobals['gCameraShape'], melGlobals['gFrameRangeStart'], melGlobals['gFrameRangeEnd'], melGlobals['gTargetImagePath'] + "_ns")
			_popRenderLayer()
			
		
	
	elif melGlobals['gDoDeepPlayblast']:
		_pushRenderLayer(melGlobals['gNamespaceRenderLayer'])
		mel.PlayblastTool.doPreroll()
		ns_cmd=playblastCmd + " -filename \"" + melGlobals['gTargetImagePath'] + "_ns\""
		PlayblastToolMessage(ns_cmd)
		mel.eval(ns_cmd)
		_popRenderLayer()
		
	mel.PlayblastTool.doPreroll()
	playblastCmd+=" -filename \"" + melGlobals['gTargetImagePath'] + "\""
	PlayblastToolMessage(playblastCmd)
	mel.eval(playblastCmd)
	mel.PlayblastToolPostPlayblast()
	# done with playblast - call the rest of the process
	

# ---------------------------------------------------------------------------------------------------
# PlayblastToolPrePlayblast - create output directory if none exists, then call the single frame playblast proc for the first time
# ---------------------------------------------------------------------------------------------------
def PlayblastTool.doPreroll():
	melGlobals.initVar( 'int', 'gFramePreRollStart' )
	"""
	
			Execute the preroll to wake everything up and get any simulations in order.
	
	
	
		"""
	# The frame on which the preroll should start.
	melGlobals.initVar( 'int', 'gFrameRangeStart' )
	# Start frame to playblast
	# If we have a preroll, step through the frames.
	if melGlobals['gFramePreRollStart']<=melGlobals['gFrameRangeStart']:
		# Step through the frames.
		for i in range(melGlobals['gFramePreRollStart'],melGlobals['gFrameRangeStart']+1):
			PlayblastToolMessage("Preroll: Setting current time: " + str(str(i)) + ".")
			# Set the time.
			# currentTime($i);
			currentTime(i,
				update=False)
			
		
	return 
	

def PlayblastToolPrePlayblast():
	melGlobals.initVar( 'int', 'gFrameRangeStart' )
	# Start frame to playblast
	melGlobals.initVar( 'int', 'gFrameRangeEnd' )
	# End frame (inclusive) to playblast
	melGlobals.initVar( 'string', 'gTargetImagePath' )
	# Where to write images. Path, plus base name
	melGlobals.initVar( 'string', 'gTargetImageArchivePath' )
	# Where to archive images. Path, plus base name plus archive plus timestamp
	melGlobals.initVar( 'int', 'gResWidth' )
	# x resolution to playblast at
	melGlobals.initVar( 'int', 'gResHeight' )
	# y resolution to playblast at
	melGlobals.initVar( 'int', 'gPlayblastStartTime' )
	# store the playblast start timestamp
	melGlobals.initVar( 'int', 'gDoReload' )
	# store the playblast start timestamp
	melGlobals.initVar( 'int', 'gFramePreRollStart' )
	# The frame on which the preroll should start.
	# make sure we have a directory
	checkMakeDir=0
	outputDir=str(mel.dirname(melGlobals['gTargetImagePath']))
	checkMakeDir=int(PlayblastToolCheckMakeDir(outputDir))
	PlayblastToolMessage("Finished PlayblastToolCheckMakeDir")
	# make sure the background is solid gray and not gradient (2011/2012 fix)
	if mel.getApplicationVersionAsFloat() == 2011 or mel.getApplicationVersionAsFloat() == 2012:
		PlayblastToolMessage("Before bg cycle")
		# need to swap from gradient to black, dark gray, then light gray
		CycleBackgroundColor()
		CycleBackgroundColor()
		CycleBackgroundColor()
		PlayblastToolMessage("After bg cycle")
		
	PlayblastToolMessage("Before time check")
	# // do a one frame pre-roll to help get everything woken up
	# if ($gExtraFramesAtHead == 0)
	# {
	# 	currentTime ($gFrameRangeStart-1);
	# 	currentTime ($gFrameRangeStart);
	# }
	# else
	# {
	# 	for ($i = $gExtraFramesAtHead; $i >= 0; $i--)
	# 	{
	# 	currentTime ($gFrameRangeStart - $i);
	# 	}
	# }
	# 11/08/07 - grab the start time from the filesystem instead
	temp_file=outputDir + "/" + str(mel.getpid())
	PlayblastToolMessage("temp_file is " + temp_file)
	# Test: implement "touch" operation via Python
	# Code pulled from rfxFileUtils module
	python("filename = '" + temp_file + "'")
	python("import os;fd = os.open(filename, os.O_WRONLY | os.O_CREAT, 0666);os.close(fd);os.utime(filename, None)")
	# 	system("touch " + $temp_file);
	'''    python("f = open('/proc/meminfo')");
	
		python("for line in f: print line.strip()");
	
		python("f.close()");'''
	PlayblastToolMessage("Touched temp_file")
	melGlobals['gPlayblastStartTime']=int(mel.getFileMTime(temp_file))
	PlayblastToolMessage("gPlayblastStartTime is " + str(melGlobals['gPlayblastStartTime']))
	python("os.remove(filename)")
	# 	system("rm " + $temp_file);
	PlayblastToolMessage("After time check")
	# Replaced timestamped archive with versioned archive.  This means we create the versioned archive immediately after rendering the frames.
	# Since we are no longer moving all the pre-existing frames to the archive, we now need to delete them all.  We do not allow multiple copies
	# of the same version to coexist, e.g. if version v05 is re-rendered, we delete the last version archive and replace it.
	# call the per-frame playblast proc for the first time
	PlayblastToolMessage("Doing Playblast...")
	if melGlobals['gDoReload']:
		PlayblastTool.doPreroll()
		# Execute the preroll.
		# Note: In this mode, the timeline will only advance once.
		if catch( lambda: evalDeferred(lp=("PlayblastToolPlayblastAFrame " + str(melGlobals['gFrameRangeStart']))) ):
			PlayblastToolQuitError("Errors occured while playblasting (PlayblastToolPlayblastAFrame).")
			
		
	
	elif catch( lambda: evalDeferred(lp=("PlayblastToolPlayblastAll")) ):
		PlayblastToolQuitError("Errors occured while playblasting (PlayblastToolPlayblastAll).")
		# Note: In this mode, we will run through the timeline for each eye.
		#       Preroll should be execute before each run.
		
	

# ---------------------------------------------------------------------------------------------------
# PlayblastToolSetAssetRenderRes - if rigs have a res attribute, set it to render
# ---------------------------------------------------------------------------------------------------
def PlayblastToolSetAssetRenderRes():
	melGlobals.initVar( 'int', 'gSwitchAssetsToRender' )
	if not melGlobals['gSwitchAssetsToRender']:
		return 
		
	masterNodes=mel.findAssetsByType("cpsvdCPD", 0)
	for i in range(0,len(masterNodes)):
		plug=masterNodes[i] + ".res"
		if not objExists(plug):
			continue
			
		if getAttr(type=plug) != "enum":
			continue
			
		if not len(listAttr(ud=plug)):
			continue
			# can't make assumptions about what kind of rig it is without it being a reference
			
		if not referenceQuery(inr=masterNodes[i]):
			continue
			# only switch to render res for ani rigs
			# this is no longer needed - there is control by task in Outsight in the project setup
			#string $file = `referenceQuery -f $masterNodes[$i]`;
			#if(!gmatch ($file, "*_" + getPath ("AniRigSuffix", {}) + ".m?"))
			#	continue;
			
		enumNames=str(addAttr(plug,
			q=1,en=1))
		enums=enumNames.split(":")
		renderVal=-1
		highVal=-1
		for j in range(0,len(enums)):
			if enums[j].lower() == "high":
				highVal=int(j)
				
			
			elif enums[j].lower() == "render":
				renderVal=int(j)
				
			
		val=(renderVal != -1) and renderVal or highVal
		if val != -1:
			in_=listConnections(plug,
				p=1,s=1,d=0)
			if len(in_):
				catch( lambda: disconnectAttr(in_[0],plug) )
				
			catch( lambda: setAttr(plug,val) )
			
		
	

# ---------------------------------------------------------------------------------------------------
#
# ---------------------------------------------------------------------------------------------------
def PlayblastToolSetUniversalEyeOn():
	melGlobals.initVar( 'int', 'gSwitchAssetsToRender' )
	if not melGlobals['gSwitchAssetsToRender']:
		return 
		
	masterNodes=mel.findAssetsByType("cpsvdCPD", 0)
	for i in range(0,len(masterNodes)):
		eyePlug=masterNodes[i] + ".enableUniversalEye"
		# switch universal eye attribtue on
		if not objExists(eyePlug):
			continue
			
		if not len(listAttr(ud=eyePlug)):
			continue
			
		if not referenceQuery(inr=masterNodes[i]):
			continue
			
		con=listConnections(eyePlug,
			p=1,s=1,d=0)
		if len(con):
			catch( lambda: disconnectAttr(con[0],eyePlug) )
			
		if objExists(eyePlug):
			catch( lambda: setAttr(eyePlug,1) )
			
		
	

# ---------------------------------------------------------------------------------------------------
# getOverrideSmooth - get the override smooth from a smooth node. If the smooth node is connected to multiple meshes
# get the greater smooth setting. If no override, return -1
# ---------------------------------------------------------------------------------------------------
def _getOverrideSmooth(smoothNode):
	future=listHistory(smoothNode,
		f=1)
	meshes=ls(ni=future,type='mesh')
	xforms=listRelatives(p=1,pa=meshes)
	level=-1
	for i in range(0,len(xforms)):
		if not objExists(xforms[i] + ".useOverride"):
			continue
			
		if not getAttr(xforms[i] + ".useOverride"):
			continue
			
		if not objExists(xforms[i] + ".overrideSmooth"):
			continue
			
		val=int(getAttr(xforms[i] + ".overrideSmooth"))
		if val>level:
			level=val
			
		
	return level
	

# ---------------------------------------------------------------------------------------------------
# PlayblastToolSetSmoothing - set all polySmoothFace's in the scene
# ---------------------------------------------------------------------------------------------------
def PlayblastToolSetSmoothing():
	melGlobals.initVar( 'int', 'gSetSmoothing' )
	# Smooth all the assets - if they have built in smoothing?
	melGlobals.initVar( 'int', 'gSmoothDivisions' )
	# How many divisions to smooth to.
	if not melGlobals['gSetSmoothing']:
		PlayblastToolMessage("Smoothing disabled.")
		return 
		
	nodes=ls(type='polySmoothFace')
	for i in range(0,len(nodes)):
		overrideSmooth=int(_getOverrideSmooth(nodes[i]))
		smooth=(overrideSmooth != -1) and overrideSmooth or melGlobals['gSmoothDivisions']
		plug=(nodes[i] + ".divisions")
		catch( lambda: setAttr(plug,
			l=False) )
		inputPlug=listConnections(plug,
			p=1,s=1,d=0)
		if len(inputPlug):
			catch( lambda: disconnectAttr(inputPlug[0],plug) )
			
		catch( lambda: setAttr(plug,smooth) )
		
	masterNodes=mel.findAssetsByType("cpsvCPD", 0)
	# also set at the master node level - this will take care of the new approach which uses maya's subdiv display rather than smooth nodes.
	for node in masterNodes:
		if objExists(str(node) + ".globalSmooth"):
			setAttr((str(node) + ".globalSmooth"),
				melGlobals['gSmoothDivisions'])
			
		
	nurbs=ls(type="nurbsSurface")
	# and also nurbs objects
	for node in nurbs:
		displaySmoothness(node,
			pointsWire=16,polygonObject=3,pointsShaded=4,divisionsV=3,divisionsU=3)
		
	

# ---------------------------------------------------------------------------------------------------
# PlayblastToolSetUniversalEyeTextures - Hide all locators in the scene
# ---------------------------------------------------------------------------------------------------
def PlayblastToolSetUniversalEyeTextures():
	melGlobals.initVar( 'string', 'gShadingMode' )
	if melGlobals['gShadingMode'] != "textured":
		return 
		
	masterNodes=mel.findAssetsByType("cpsvCPD", 0)
	for node in masterNodes:
		if objExists(str(node) + ".eyeResolution"):
			evalEcho("setAttr " + str(node) + ".eyeResolution 512")
			
		if objExists(str(node) + ".forceTextureBake"):
			evalEcho("setAttr " + str(node) + ".forceTextureBake 1")
			
		
	

# ---------------------------------------------------------------------------------------------------
# PlayblastToolHideLocators - Hide all locators in the scene
# ---------------------------------------------------------------------------------------------------
def PlayblastToolHideLocators():
	locators=ls(dag=1,type=['locator', 'snapshotShape', 'camera', 'lookAt'])
	# hide any pixel_separation_info locators manually, only if plugin is loaded.
	if objectType(tagFromType="pixel_separation_info") != 0:
		pixelSeps=ls(type="pixel_separation_info")
		pS=""
		for pS in pixelSeps:
			setAttr((str(pS) + ".visibility"),
				0)
			
		
	for node in locators:
		if not mel.isVisible(node):
			continue
			#print($node + "\n");
			# first find out if it's hidden
			# already hidden
			
		vis=str(node) + ".v"
		ove=str(node) + ".ove"
		disp=str(node) + ".overrideVisibility"
		lod_vis=str(node) + ".lodVisibility"
		if getAttr(vis) == 0:
			continue
			# already hidden
			
		if objExists(ove) and getAttr(ove) == 1 and getAttr(disp) == 0:
			continue
			# already hidden
			
		if objExists(lod_vis) == 0:
			continue
			# already hidden
			# if it's a camera, check to see if it has an imageplane. If so, don't hide it
			
		if len(ls(node,
			type='camera')):
			if len(listConnections((str(node) + ".imagePlane"),
				s=1,d=0)):
				catch( lambda: setAttr((str(node) + ".locatorScale"),
					0.0001) )
				# set the locator scale to 0. This "hides" the camera while leaving the imagePlane
				# Continue, otherwise the camera will get hidden.
				continue
				
			
		if objectType(node) == "rfxAlembicMeshGpuCache":
			continue
			# if it's an alembic mesh gpu cache, don't hide it
			
		if not referenceQuery(inr=node):
			if getAttr(l=vis):
				catch( lambda: setAttr(vis,
					l=0) )
				# find the first unlocked visibility plug. If the node is not referenced we can do what we like
				
			inputPlug=listConnections(vis,
				p=1,s=1,d=0)
			if len(inputPlug):
				catch( lambda: disconnectAttr(inputPlug[0],vis) )
				
			catch( lambda: setAttr(vis,0) )
			
		
		elif not getAttr(l=vis):
			inputPlug=listConnections(vis,
				p=1,s=1,d=0)
			# find the first unlocked attribute available
			if len(inputPlug):
				catch( lambda: disconnectAttr(inputPlug[0],vis) )
				
			catch( lambda: setAttr(vis,0) )
			continue
			
		if objExists(ove) and not getAttr(l=ove) and objExists(disp) and not getAttr(l=disp):
			inputPlug=listConnections(ove,
				p=1,s=1,d=0)
			if len(inputPlug):
				catch( lambda: disconnectAttr(inputPlug[0],ove) )
				
			catch( lambda: setAttr(ove,0) )
			inputPlug=listConnections(disp,
				p=1,s=1,d=0)
			if len(inputPlug):
				catch( lambda: disconnectAttr(inputPlug[0],disp) )
				
			catch( lambda: setAttr(disp,0) )
			continue
			
		if objExists(lod_vis) and not getAttr(l=lod_vis):
			inputPlug=listConnections(lod_vis,
				p=1,s=1,d=0)
			if len(inputPlug):
				catch( lambda: disconnectAttr(inputPlug[0],lod_vis) )
				
			catch( lambda: setAttr(lod_vis,0) )
			
		
	

# ---------------------------------------------------------------------------------------------------
# PlayblastToolSetCameraNearClip - ?
# ---------------------------------------------------------------------------------------------------
def PlayblastToolSetCameraNearClip():
	melGlobals.initVar( 'string', 'gCameraShape' )
	plug=(melGlobals['gCameraShape'] + ".nearClipPlane")
	nearClip=float(getAttr(plug))
	if nearClip<0.01:
		catch( lambda: lockNode(melGlobals['gCameraShape'],
			l=0) )
		catch( lambda: setAttr(plug,
			lock=False) )
		inputs=listConnections(plug,
			p=1,s=1,d=0)
		if len(inputs):
			catch( lambda: disconnectAttr(inputs[0],plug) )
			
		catch( lambda: setAttr(plug,0.01) )
		
	

# ---------------------------------------------------------------------------------------------------
# PlayblastToolSetupOverlay - set up the overlay
# ---------------------------------------------------------------------------------------------------
def PlayblastToolSetupOverlay():
	melGlobals.initVar( 'int', 'gDoOverlay' )
	melGlobals.initVar( 'string', 'gOverlayTemplate' )
	melGlobals.initVar( 'string', 'gCamera' )
	melGlobals.initVar( 'string', 'gTargetImagePath' )
	# Where to write images. Path, plus base name
	imageDir=str(mel.dirname(melGlobals['gTargetImagePath']))
	overlayExp=imageDir + "/overlay.xml"
	if not melGlobals['gDoOverlay']:
		PlayblastToolMessage("Overlay disabled.")
		if os.path.exists( overlayExp ) and os.path.getsize( overlayExp ):
			os.remove( overlayExp )
			
		return 
		
	PlayblastToolHideLocators()
	# hide all other locators - since the overlay is a locator, we must have show locators on in the model editor
	#	PlayblastToolMessage("Setting up to hide locators...");
	#	print("Done setting up hide locators.\n");
	# Make sure the near clip plane is not below 0.01 - this is a temporary measure until we have the rfxOverlay node locked down - currently clipping planes below 0.01
	# cause the text to jitter
	# 10/02/06 - no longer needed.
	#PlayblastToolSetCameraNearClip();
	#	PlayblastToolMessage("Creating overlay from template.....");
	mel.createRfxOverlayFromTemplate(melGlobals['gOverlayTemplate'], melGlobals['gCamera'], "")
	#	print("Done creating overlay from template.\n");
	# dump overlay to image directory - the presense of this indicates to movie robot that no overlay is required
	#	print("last bit...\n");
	if not os.path.isdir( imageDir ):
		os.mkdir( imageDir ) 
		
	mel.writeFile(overlayExp, melGlobals['gOverlayTemplate'])
	#	print("DONE last bit.\n");
	

# ---------------------------------------------------------------------------------------------------
# PlayblastToolCreateLockFile - Create lock file. This shows the wrapper process that we are in progress. If it is still there when maya quits, it means we failed.
# ---------------------------------------------------------------------------------------------------
def PlayblastToolCreateLockFile():
	melGlobals.initVar( 'string', 'gLockFile' )
	if melGlobals['gLockFile'] == "":
		PlayblastToolMessage("Warning: No lock file specified. Not creating one.")
		return 
		
	f=open(melGlobals['gLockFile'],"w")
	f.write("\n")
	f.close()
	

# ---------------------------------------------------------------------------------------------------
# PlayblastToolMaximizeMainWindow
# ---------------------------------------------------------------------------------------------------
def PlayblastToolMaximizeMainWindow():
	melGlobals.initVar( 'string', 'gMainWindow' )
	melGlobals.initVar( 'int[]', 'gOriginalSize' )
	melGlobals.initVar( 'int[]', 'gOriginalPosition' )
	melGlobals.initVar( 'int', 'gStatusLineBool' )
	melGlobals.initVar( 'int', 'gShelfBool' )
	melGlobals.initVar( 'int', 'gRangeSliderBool' )
	melGlobals.initVar( 'int', 'gCommandLineBool' )
	melGlobals.initVar( 'int', 'gHelpLineBool' )
	melGlobals.initVar( 'string', 'gLocal' )
	if about():
		return 
		
	xWidth=0
	xHeight=0
	modWidth=0
	modHeight=0
	thick=27
	#width of thick KDE 3.5 window decorations
	thin=4
	#width of thin KDE 3.5 window decorations
	# Maximize Main
	melGlobals['gOriginalSize']=window(melGlobals['gMainWindow'],
		q=1,wh=1)
	melGlobals['gOriginalPosition']=window(melGlobals['gMainWindow'],
		q=1,tlc=1)
	xWidth=int(int(internal.shellOutput("/usr/bin/xdpyinfo | grep -i dimension | awk '{print $2}' | awk -Fx '{print $1}'", convertNewlines=False, stripTrailingNewline=False)))
	xHeight=int(int(internal.shellOutput("/usr/bin/xdpyinfo | grep -i dimension | awk '{print $2}' | awk -Fx '{print $2}'", convertNewlines=False, stripTrailingNewline=False)))
	modWidth=xWidth - (thin + thin)
	modHeight=xHeight - (thick + thin)
	PlayblastToolMessage("modWidth is " + str(modWidth))
	PlayblastToolMessage("modHeight is " + str(modHeight))
	if melGlobals['gLocal'] != "":
		window(melGlobals['gMainWindow'],
			e=1,w=(melGlobals['gOriginalSize'][0] - 20))
		# KDE 4 forces windows to scale within a single monitor space,
		# so we have to cheat a bit to get the dimensions that we want.
		# First reduce the width in case the window is maximized from the last run
		# Next move the window so that it crosses both monitors
		window(melGlobals['gMainWindow'],
			leftEdge=(xWidth / 2 - (window(melGlobals['gMainWindow'],
				q=1,w=1) / 2)),e=1)
		# Now force a really large width before setting the values we want
		window(melGlobals['gMainWindow'],
			width=3000,e=1)
		
	window(melGlobals['gMainWindow'],
		tlc=(thick, thin),e=1)
	window(melGlobals['gMainWindow'],
		e=1,wh=(modWidth, modHeight))
	# Gather the state of UI components
	melGlobals['gStatusLineBool']=int(mel.isUIComponentVisible("Status Line"))
	melGlobals['gShelfBool']=int(mel.isUIComponentVisible("Shelf"))
	melGlobals['gRangeSliderBool']=int(mel.isUIComponentVisible("Range Slider"))
	melGlobals['gCommandLineBool']=int(mel.isUIComponentVisible("Command Line"))
	melGlobals['gHelpLineBool']=int(mel.isUIComponentVisible("Help Line"))
	# Close open UI components
	if melGlobals['gStatusLineBool']:
		mel.toggleUIComponentVisibility("Status Line")
		
	if melGlobals['gShelfBool']:
		mel.toggleUIComponentVisibility("Shelf")
		
	if melGlobals['gRangeSliderBool']:
		mel.toggleUIComponentVisibility("Range Slider")
		
	if melGlobals['gHelpLineBool']:
		mel.toggleUIComponentVisibility("Help Line")
		# Do a bit more for local playblasts to maximize screen real-estate
		
	if melGlobals['gLocal'] != "":
		if mel.isUIComponentVisible("Time Slider"):
			mel.toggleUIComponentVisibility("Time Slider")
			
		if melGlobals['gCommandLineBool']:
			mel.toggleUIComponentVisibility("Command Line")
			
		mel.toggleMenuBarsInPanels(False)
		ToggleModelEditorBars()
		#		   toggleModelEditorBarsInAllPanels 0;
		window(melGlobals['gMainWindow'],
			mbv=False,e=1)
		
	
	else:
		mel.setAllMainWindowComponentsVisible(0)
		
	

# ---------------------------------------------------------------------------------------------------
# PlayblastToolRestoreMainWindow
# ---------------------------------------------------------------------------------------------------
def PlayblastToolRestoreMainWindow():
	melGlobals.initVar( 'string', 'gMainWindow' )
	melGlobals.initVar( 'int[]', 'gOriginalSize' )
	melGlobals.initVar( 'int[]', 'gOriginalPosition' )
	melGlobals.initVar( 'int', 'gStatusLineBool' )
	melGlobals.initVar( 'int', 'gShelfBool' )
	melGlobals.initVar( 'int', 'gRangeSliderBool' )
	melGlobals.initVar( 'int', 'gCommandLineBool' )
	melGlobals.initVar( 'int', 'gHelpLineBool' )
	# Restore Main
	window(melGlobals['gMainWindow'],
		e=1,wh=(melGlobals['gOriginalSize'][0], melGlobals['gOriginalSize'][1]))
	window(melGlobals['gMainWindow'],
		tlc=(melGlobals['gOriginalPosition'][0], melGlobals['gOriginalPosition'][1]),e=1)
	# Open UI components closed by the script
	if melGlobals['gStatusLineBool']:
		mel.toggleUIComponentVisibility("Status Line")
		
	if melGlobals['gShelfBool']:
		mel.toggleUIComponentVisibility("Shelf")
		
	if melGlobals['gRangeSliderBool']:
		mel.toggleUIComponentVisibility("Range Slider")
		#if ($gCommandLineBool)
		#	toggleUIComponentVisibility "Command Line";
		
	if melGlobals['gHelpLineBool']:
		mel.toggleUIComponentVisibility("Help Line")
		
	

# ---------------------------------------------------------------------------------------------------
# PlayblastToolCreateMovieWithMencoder - Create a movie using mencoder
# ---------------------------------------------------------------------------------------------------
def PlayblastToolCreateMovieWithMencoder():
	melGlobals.initVar( 'int', 'gFrameRangeStart' )
	# Start frame to playblast
	melGlobals.initVar( 'int', 'gFrameRangeEnd' )
	# End frame (inclusive) to playblast
	melGlobals.initVar( 'int', 'gResWidth' )
	# x resolution to playblast at
	melGlobals.initVar( 'int', 'gResHeight' )
	# y resolution to playblast at
	melGlobals.initVar( 'string', 'gOutputFmt' )
	# Output format for frames.
	melGlobals.initVar( 'string', 'gTargetImagePath' )
	# Where to write images. Path, plus base name
	melGlobals.initVar( 'string', 'gTargetMoviePath' )
	# Where to write movies, if desired
	melGlobals.initVar( 'string', 'gEncoderVideoOptions' )
	# option string to send to mencoder for creating movies
	melGlobals.initVar( 'string', 'gEncoderAudioOptions' )
	# option string to send to mencoder for audio options
	melGlobals.initVar( 'string', 'gMovieFPS' )
	# fps for movie as a string , e.g. "film"
	melGlobals.initVar( 'string', 'gAudioPath' )
	# Path to audio for the shot
	melGlobals.initVar( 'int', 'gDoAudio' )
	# If we are making a movie, include audio?
	melGlobals.initVar( 'string', 'gInputScene' )
	# The scene to playblast
	project=str(mel.getPath("ProjectFromFilename", [melGlobals['gInputScene']]))
	imageDir=str(mel.dirname(melGlobals['gTargetImagePath']))
	imageName=str(mel.basename(melGlobals['gTargetImagePath'], ""))
	movieDir=str(mel.dirname(melGlobals['gTargetMoviePath']))
	PlayblastToolMessage("Building movie with mencoder, the FLV version will not be made.")
	# convert fps from a string (e.g. "film") to a number
	lookup=["film","24",
		"ntsc","30",
		"pal","25",
		"game","15",
		"ntscf",
		"60"]
	index=int(mel.stringArrayFindIndex(melGlobals['gMovieFPS'], lookup))
	fps=lookup[index + 1]
	if project == "16063_robosapien_rebooted":
		fps="23.976"
		# create a list file for mencoder
		
	listData=''
	listFile=imageDir + "/mencoder_list.txt"
	for i in range(melGlobals['gFrameRangeStart'],melGlobals['gFrameRangeEnd']+1):
		listData+=imageDir + "/" + imageName + "." + str(mel.padNumber(i, 4)) + "." + melGlobals['gOutputFmt'] + "\n"
		
	mel.writeFile(listFile, listData)
	# build the mencoder command
	cmd="mencoder "
	cmd+="mf://\"@" + listFile + "\" "
	cmd+="-mf w=" + str(melGlobals['gResWidth']) + ":h=" + str(melGlobals['gResHeight']) + ":fps=" + fps + ":type=" + melGlobals['gOutputFmt'] + " "
	cmd+="-o " + melGlobals['gTargetMoviePath'] + " "
	cmd+=melGlobals['gEncoderVideoOptions'] + " "
	if melGlobals['gDoAudio']:
		cmd+=melGlobals['gEncoderAudioOptions'] + " -audiofile " + melGlobals['gAudioPath']
		#$cmd += "-oac lavc -audiofile " + $gAudioPath;
		
	PlayblastToolMessage("mencoder call:")
	PlayblastToolMessage(cmd)
	internal.shellOutput(cmd, convertNewlines=False, stripTrailingNewline=False)
	'''
	
	// example mencoder call
	
	mencoder mf://"@/renders/entertainment/15374_socom/show/seq004/sg0012/animation/standard/list.txt" -mf fps=30 -o test3.avi -ovc lavc -lavcopts vcodec=mpeg4:mbd=2:trell:v4mv:last_pred=2:dia=-1:vmax_b_frames=2:vb_strategy=1:cmp=3:subcmp=3:precmp=0:vqcomp=0.6:turbo -oac lavc -audiofile /renders/entertainment/15374_socom/show/seq004/sg0012/animation/standard/5030_0030.wav
	
	
	
	'''
	

# ---------------------------------------------------------------------------------------------------
# PlayblastToolCreateMovieWithFfmpeg - Create a movie using ffmpeg
# ---------------------------------------------------------------------------------------------------
def PlayblastToolCreateMovieWithFfmpeg():
	melGlobals.initVar( 'int', 'gDoAudio' )
	# If we are making a movie, include audio?
	melGlobals.initVar( 'int', 'gResWidth' )
	# x resolution to playblast at
	melGlobals.initVar( 'int', 'gResHeight' )
	# y resolution to playblast at
	melGlobals.initVar( 'int', 'gMovieResWidth' )
	# x resolution of movie, may be different than frame size
	melGlobals.initVar( 'int', 'gMovieResHeight' )
	# y resolution of movie, may be different than frame size
	melGlobals.initVar( 'float', 'gMovieResAspect' )
	# aspect ratio of movie, may be different than for frames
	melGlobals.initVar( 'int', 'gFrameRangeStart' )
	# Start frame to playblast
	melGlobals.initVar( 'int', 'gFrameRangeEnd' )
	# End frame (inclusive) to playblast
	melGlobals.initVar( 'string', 'gTargetImagePath' )
	# Where to write images. Path, plus base name
	melGlobals.initVar( 'string', 'gTargetMoviePath' )
	# Where to write movies, if desired
	melGlobals.initVar( 'string', 'gTargetFLVMoviePath' )
	# Where to write movies, if desired
	melGlobals.initVar( 'string', 'gTargetFLVMoviePathTemp' )
	# Where to write movies, if desired
	melGlobals.initVar( 'string', 'gOutputFmt' )
	# Output format for frames.
	melGlobals.initVar( 'string', 'gAudioPath' )
	# Path to audio for the shot
	melGlobals.initVar( 'string', 'gMovieFPS' )
	# fps for movie
	melGlobals.initVar( 'string', 'gEncoderVideoOptions' )
	# option string to send to mencoder for creating movies
	melGlobals.initVar( 'string', 'gEncoderAudioOptions' )
	# option string to send to mencoder for audio options
	melGlobals.initVar( 'string', 'gInputScene' )
	# The scene to playblast
	melGlobals.initVar( 'int', 'gDoDeepPlayblast' )
	# deep playblast
	melGlobals.initVar( 'string', 'gDeepPlayblastMoviePath' )
	# Where to write deep playblast movie
	master_start_frame=0.0
	start_sec=0.0
	runtime=0.0
	# convert fps from a string (e.g. "film") to a number
	lookup=["film","24",
		"ntsc","30",
		"pal","25",
		"game","15",
		"ntscf",
		"60"]
	# HACK
	# Basic gist of subshot audio hack. We want to find out if the shot we are in is indeed a subshot.
	# We do this by using Insight's ipydata to query if there is a parent_shot_id associated with the shot.
	# If there is a parent_shot_id, we are in a subshot.  Now we query information from the parent shot
	# and the subshot to find out where the shot's master audio is and how far to offset the images when
	# making the movie.
	is_subshot=0
	python("from path_lib import path_extractor")
	python("from path_lib import path_finder")
	python("import ipydata")
	python("ipydata.set_global_stage('production')")
	# Using path extractor and the current file path to figure out what shot we're in.
	python("context = path_extractor.extract('" + melGlobals['gInputScene'] + "')")
	keys=python("context.keys()")
	# Check to see that we have enough information to complete the operation.
	if mel.stringArrayFindIndex("project", keys) != -1 and mel.stringArrayFindIndex("sq", keys) != -1 and mel.stringArrayFindIndex("sh", keys) != -1:
		python("project = ipydata.prod.Project.where(number=context['project'].split('_')[0]).first()")
		project=str(python("project.name"))
		python("sequence = project.sequences.where(number=context['sq']).first()")
		python("shot = sequence.shots.where(name=context['sh']).first()")
		is_subshot=int(python("shot.parent_shot_id"))
		if is_subshot != 0:
			python("parent_shot = project.shots.find(" + str(is_subshot) + ")")
			python("parent_seq = project.sequences.find(parent_shot.sequence_id)")
			sequence=str(python("parent_seq.number"))
			shot=str(python("parent_shot.name"))
			sound_path=str(python("path_finder.get_path(\"sh_audio_dir\", department=context['department'], project=context['project']" + ", sq='" + sequence + "', sh='" + shot + "')"))
			sound_file=(sound_path + "/" + sequence + "_" + shot + ".wav")
			file_exists=len(internal.shellOutput("ls " + sound_file, convertNewlines=False, stripTrailingNewline=False))
			if file_exists == 0:
				mel.error(sound_file + " Does not exist! Contact the Technical Director assigned to your show.")
				return 
				
			
			else:
				melGlobals['gAudioPath']=sound_file
				index=int(mel.stringArrayFindIndex(melGlobals['gMovieFPS'], lookup))
				tmp_fps=lookup[index + 1]
				master_start_frame=float(python("parent_shot.frame_range_start"))
				# Calculate what time the current shot starts in the master audio in seconds.
				start_sec=float((float(melGlobals['gFrameRangeStart']) - float(master_start_frame)) / float(tmp_fps))
				# Calculate how long the current shot runs in seconds.
				runtime=float((float(melGlobals['gFrameRangeEnd']) - float(melGlobals['gFrameRangeStart'])) / float(tmp_fps))
				
			
		
	project=str(mel.getPath("ProjectFromFilename", [melGlobals['gInputScene']]))
	imageDir=str(mel.dirname(melGlobals['gTargetImagePath']))
	imageName=str(mel.basename(melGlobals['gTargetImagePath'], ""))
	movieDir=str(mel.dirname(melGlobals['gTargetMoviePath']))
	#string $tempDir = $imageDir + "/" + getpid();
	tempDir=imageDir
	cmdFile=imageDir + "/ffmpeg_doIt.cmd"
	melGlobals['gTargetFLVMoviePath']=melGlobals['gTargetMoviePath'].replace("mov$","flv")
	melGlobals['gTargetFLVMoviePathTemp']=melGlobals['gTargetMoviePath'].replace("mov$","temp.flv")
	if os.path.exists( melGlobals['gTargetMoviePath'] ) and os.path.getsize( melGlobals['gTargetMoviePath'] ):
		internal.shellOutput("rm -r " + melGlobals['gTargetMoviePath'], convertNewlines=False, stripTrailingNewline=False)
		
	if os.path.exists( melGlobals['gTargetFLVMoviePath'] ) and os.path.getsize( melGlobals['gTargetFLVMoviePath'] ):
		internal.shellOutput("rm -r " + melGlobals['gTargetFLVMoviePath'], convertNewlines=False, stripTrailingNewline=False)
		
	if os.path.exists( melGlobals['gTargetFLVMoviePathTemp'] ) and os.path.getsize( melGlobals['gTargetFLVMoviePathTemp'] ):
		internal.shellOutput("rm -r " + melGlobals['gTargetFLVMoviePathTemp'], convertNewlines=False, stripTrailingNewline=False)
		
	if melGlobals['gDoDeepPlayblast'] and os.path.exists( melGlobals['gDeepPlayblastMoviePath'] ) and os.path.getsize( melGlobals['gDeepPlayblastMoviePath'] ):
		internal.shellOutput("rm -r " + melGlobals['gDeepPlayblastMoviePath'], convertNewlines=False, stripTrailingNewline=False)
		# Preparation:
		"""
		
				Create a temp dir, and create symbolic links to the original image files beginning at frame 0001
		
			"""
		#	PlayblastToolMessage("Preparing frames for ffmpeg...");
		#
		#	if(!`filetest -d $tempDir`)
		#		system("mkdir -m 777 " + $tempDir);
		#
		#	for($i = $gFrameRangeStart; $i <= $gFrameRangeEnd; $i += 1)
		#	{
		#		int $tgtFrame = $i - $gFrameRangeStart + 1;
		#
		#		string $src = $imageDir + "/" + $imageName + "." + padNumber ($i, 4) + "." + $gOutputFmt;
		#		string $tgt = $tempDir +"/" + $imageName + "." + padNumber ($tgtFrame, 4) + "." + $gOutputFmt;
		#
		#		//PlayblastToolMessage("Link source: " + $src);
		#		//PlayblastToolMessage("Link target: " + $tgt);
		#
		#		system("ln -s " + $src + " " + $tgt);
		#	}
		# convert fps from a string (e.g. "film") to a number
		
	lookup=["film","24",
		"ntsc","30",
		"pal","25",
		"game","15",
		"ntscf",
		"60"]
	index=int(mel.stringArrayFindIndex(melGlobals['gMovieFPS'], lookup))
	fps=lookup[index + 1]
	if project == "16063_robosapien_rebooted":
		fps="23.976"
		
	PlayblastToolMessage("Building encoder commands...")
	#
	# build the ffmpeg command for mov
	#
	cmd="ffmpeg "
	cmd+="-y "
	cmd+="-start_frame " + str(melGlobals['gFrameRangeStart']) + " "
	cmd+="-end_frame " + str(melGlobals['gFrameRangeEnd']) + " "
	cmd+="-r " + fps + " "
	if is_subshot != 0:
		cmd+="-itsoffset " + str(start_sec) + " "
		# We are a subshot so we need to offset the images in time to align with the audio properly.
		# We have to offset the images instead of the audio because of a bug in ffmpeg.
		# Six of one half a dozen of the other.
		
	cmd+="-i " + tempDir + "/" + imageName + ".%04d." + melGlobals['gOutputFmt'] + " "
	# add video options from instruction file
	cmd+=melGlobals['gEncoderVideoOptions'] + " "
	cmd+="-metadata album=\"" + melGlobals['gTargetMoviePath'] + "\" "
	if melGlobals['gDoAudio']:
		cmd+="-i " + melGlobals['gAudioPath'] + " "
		cmd+=melGlobals['gEncoderAudioOptions'] + " "
		
	if melGlobals['gMovieResWidth'] != melGlobals['gResWidth'] and melGlobals['gMovieResHeight'] != melGlobals['gResHeight']:
		cmd+="-s " + str(melGlobals['gMovieResWidth']) + "x" + str(melGlobals['gMovieResHeight']) + " "
		#$cmd += "-vframes " + ($gFrameRangeEnd-$gFrameRangeStart+1) + " ";
		
	if is_subshot != 0:
		tmp=melGlobals['gTargetMoviePath'].replace(".mov$",".tmp.mov")
		# Get a temporary path to write the image to since we need to run the movie process twice.
		# Once to create the movie with extra audio and again to cut the extra audio off.
		# We'll do the same thing later for the flv.
		if os.path.exists( tmp ) and os.path.getsize( tmp ):
			internal.shellOutput("rm -r " + tmp, convertNewlines=False, stripTrailingNewline=False)
			
		cmd+=tmp
		cmd+="; "
		cmd+="ffmpeg -ss " + str(start_sec) + " -t " + str(runtime) + " -sameq -i " + tmp + " "
		cmd+=(melGlobals['gTargetMoviePath'] + ";\n")
		
	
	else:
		cmd+=melGlobals['gTargetMoviePath']
		cmd+=";\n"
		
	if melGlobals['gDoDeepPlayblast']:
		cmd+="ffmpeg "
		#
		# build the ffmpeg command for deep playblast mov
		#
		cmd+="-y "
		cmd+="-start_frame " + str(melGlobals['gFrameRangeStart']) + " "
		cmd+="-end_frame " + str(melGlobals['gFrameRangeEnd']) + " "
		cmd+="-r " + fps + " "
		if is_subshot != 0:
			cmd+="-itsoffset " + str(start_sec) + " "
			# We are a subshot so we need to offset the images in time to align with the audio properly.
			# We have to offset the images instead of the audio because of a bug in ffmpeg.
			# Six of one half a dozen of the other.
			
		cmd+="-i " + tempDir + "/" + imageName + ".%04d." + melGlobals['gOutputFmt'] + " "
		# add video options from instruction file
		cmd+=melGlobals['gEncoderVideoOptions'] + " "
		cmd+="-metadata album=\"" + melGlobals['gTargetMoviePath'] + "\" "
		cmd+="-i " + tempDir + "/" + imageName + "_ns" + ".%04d." + melGlobals['gOutputFmt'] + " "
		cmd+=melGlobals['gEncoderVideoOptions'] + " "
		if melGlobals['gDoAudio']:
			cmd+="-i " + melGlobals['gAudioPath'] + " "
			cmd+=melGlobals['gEncoderAudioOptions'] + " "
			
		if melGlobals['gMovieResWidth'] != melGlobals['gResWidth'] and melGlobals['gMovieResHeight'] != melGlobals['gResHeight']:
			cmd+="-s " + str(melGlobals['gMovieResWidth']) + "x" + str(melGlobals['gMovieResHeight']) + " "
			#$cmd += "-vframes " + ($gFrameRangeEnd-$gFrameRangeStart+1) + " ";
			
		if is_subshot != 0:
			tmp=melGlobals['gDeepPlayblastMoviePath'].replace(".mov$",".tmp.mov")
			# Get a temporary path to write the image to since we need to run the movie process twice.
			# Once to create the movie with extra audio and again to cut the extra audio off.
			# We'll do the same thing later for the flv.
			if os.path.exists( tmp ) and os.path.getsize( tmp ):
				internal.shellOutput("rm -r " + tmp, convertNewlines=False, stripTrailingNewline=False)
				
			cmd+=tmp
			cmd+=" -vcodec png -newvideo"
			cmd+="; "
			cmd+="ffmpeg -ss " + str(start_sec) + " -t " + str(runtime) + " -sameq -i " + tmp + " "
			cmd+=(melGlobals['gDeepPlayblastMoviePath'] + ";\n")
			
		
		else:
			cmd+=melGlobals['gDeepPlayblastMoviePath']
			cmd+=" -vcodec png -newvideo"
			cmd+=";\n"
			
		cmd+="movutils "
		# set track 0 to layer 0, and track 1 to layer 1 so that the quicktime player
		# doesn't display the deep playblast track on top of the regular track
		cmd+=melGlobals['gDeepPlayblastMoviePath']
		cmd+=" -edit moov.trak0.tkhd layer 0"
		cmd+=" -edit moov.trak1.tkhd layer 1;\n"
		
	cmd+="ffmpeg "
	#
	# build the ffmpeg command for flv
	#
	cmd+="-start_frame " + str(melGlobals['gFrameRangeStart']) + " "
	cmd+="-end_frame " + str(melGlobals['gFrameRangeEnd']) + " "
	cmd+="-y "
	cmd+="-r " + fps + " "
	if is_subshot != 0:
		cmd+="-itsoffset " + str(start_sec) + " "
		
	cmd+="-i " + tempDir + "/" + imageName + ".%04d." + melGlobals['gOutputFmt'] + " "
	if melGlobals['gDoAudio']:
		cmd+="-i " + melGlobals['gAudioPath'] + " "
		#$cmd += $gEncoderAudioOptions + " ";
		cmd+="-acodec libfaac "
		
	cmd+="-g 1 -f flv -s " + str(PlayblastToolMultipleOfTwo(melGlobals['gMovieResWidth'])) + "x" + str(PlayblastToolMultipleOfTwo(melGlobals['gMovieResHeight'])) + " -ar 22050 -b 10000000 -r " + fps + " "
	cmd+="-vframes " + str((melGlobals['gFrameRangeEnd'] - melGlobals['gFrameRangeStart'] + 1)) + " "
	if is_subshot != 0:
		tmp=melGlobals['gTargetFLVMoviePathTemp'].replace(".flv$",".tmp.flv")
		if os.path.exists( tmp ) and os.path.getsize( tmp ):
			internal.shellOutput("rm -r " + tmp, convertNewlines=False, stripTrailingNewline=False)
			
		cmd+=tmp + "; "
		cmd+="ffmpeg -ss " + str(start_sec) + " -t " + str(runtime) + " -sameq -i " + tmp + " "
		
	cmd+=(melGlobals['gTargetFLVMoviePathTemp'] + ";\n")
	PlayblastToolMessage("ffmpeg commands to create mov files:")
	PlayblastToolMessage(cmd)
	mel.writeFile(cmdFile, (cmd))
	# write the file to disk and make executable
	# This is due to some peculiarities with ffmpeg - if maya is running in the background, ffmpeg will suspend the execution of maya!
	# This doesn't happen when you run ffmpeg from within a shell script
	internal.shellOutput("chmod 777 " + cmdFile, convertNewlines=False, stripTrailingNewline=False)
	PlayblastToolMessage("Invoking encoder...")
	PlayblastToolMessage(cmdFile)
	internal.shellOutput(cmdFile, convertNewlines=False, stripTrailingNewline=False)
	#	// remove the temp dir with the sym links
	#	system("rm -r " + $tempDir);
	"""
	
	example ffmpeg call
	
	ffmpeg -y -r 24 -i /path/to/frames.jpg -b 1000k -i /path/to/sound.wav -acodec pcm_s16le -vframes 463 output.mov
	
	"""
	

# ---------------------------------------------------------------------------------------------------
# PlayblastToolCreateMovie - Create a movie
# ---------------------------------------------------------------------------------------------------
def PlayblastToolCreateMovie():
	melGlobals.initVar( 'int', 'gDoMovie' )
	# Make a movie?
	melGlobals.initVar( 'int', 'gDoAudio' )
	# If we are making a movie, include audio?
	melGlobals.initVar( 'string', 'gMovieFPS' )
	# fps for movie
	melGlobals.initVar( 'string', 'gEncoderVideoOptions' )
	# option string to send to mencoder for creating movies
	melGlobals.initVar( 'string', 'gEncoderAudioOptions' )
	# option string to send to mencoder for audio options
	melGlobals.initVar( 'string', 'gAudioPath' )
	# Path to audio for the shot
	melGlobals.initVar( 'string', 'gTargetImagePath' )
	# Where to write images. Path, plus base name
	melGlobals.initVar( 'string', 'gTargetMoviePath' )
	# Where to write movies, if desired
	melGlobals.initVar( 'int', 'gFrameRangeStart' )
	# Start frame to playblast
	melGlobals.initVar( 'int', 'gFrameRangeEnd' )
	# End frame (inclusive) to playblast
	melGlobals.initVar( 'int', 'gResWidth' )
	# x resolution to playblast at
	melGlobals.initVar( 'int', 'gResHeight' )
	# y resolution to playblast at
	melGlobals.initVar( 'float', 'gResAspect' )
	# aspect ratio
	melGlobals.initVar( 'string', 'gOutputFmt' )
	# Output format for frames.
	melGlobals.initVar( 'string', 'gMovieType' )
	# mov or avi
	melGlobals.initVar( 'string', 'gEncoder' )
	# encoder to use "ffmpeg" or "mencoder"
	if not melGlobals['gDoMovie']:
		PlayblastToolMessage("Movie generation disabled.")
		return 
		
	imageDir=str(mel.dirname(melGlobals['gTargetImagePath']))
	imageName=str(mel.basename(melGlobals['gTargetImagePath'], ""))
	movieDir=str(mel.dirname(melGlobals['gTargetMoviePath']))
	"""
	
			$gTargetMoviePath will be something like:
	
			/data/development/17199_pipeline_dir_test_new/cg/sequences/sq9000/sh0010/movies/lay/9000_0010_lay.0001.mov
	
	
	
			so movieDir = /data/development/17199_pipeline_dir_test_new/cg/sequences/sq9000/sh0010/movies/lay
	
		"""
	# make sure we the target directory exists.
	PlayblastToolCheckMakeDir(movieDir)
	if melGlobals['gEncoder'] == "mencoder":
		PlayblastToolCreateMovieWithMencoder()
		
	
	else:
		PlayblastToolCreateMovieWithFfmpeg()
		
	

# ---------------------------------------------------------------------------------------------------
# PlayblastToolCheckFrames - Check that all the frames were created
# ---------------------------------------------------------------------------------------------------
def PlayblastToolCheckFrames():
	melGlobals.initVar( 'int', 'gPlayblastStartTime' )
	# store the playblast start timestamp
	melGlobals.initVar( 'string', 'gTargetImagePath' )
	# Where to write images. Path, plus base name
	melGlobals.initVar( 'int', 'gFrameRangeStart' )
	# Start frame to playblast
	melGlobals.initVar( 'int', 'gFrameRangeEnd' )
	# End frame (inclusive) to playblast
	melGlobals.initVar( 'string', 'gOutputFmt' )
	# Output format for frames.
	melGlobals.initVar( 'int', 'gDoStereoPlayblast' )
	melGlobals.initVar( 'int', 'gIsStereo' )
	melGlobals.initVar( 'int', 'gDoStereo' )
	imageDir=str(mel.dirname(melGlobals['gTargetImagePath']))
	imageName=str(mel.basename(melGlobals['gTargetImagePath'], ""))
	src=''
	temp=[]
	stamp=0
	numMissing=0
	#	if($gDoStereoPlayblast)
	if melGlobals['gIsStereo'] and melGlobals['gDoStereo']:
		for i in range(melGlobals['gFrameRangeStart'],melGlobals['gFrameRangeEnd']+1):
			file=imageName + "_l." + str(mel.padNumber(i, 4)) + "." + melGlobals['gOutputFmt']
			link=imageDir + "/" + imageName + "." + str(mel.padNumber(i, 4)) + "." + melGlobals['gOutputFmt']
			cmd="rm " + link
			if os.path.exists( link ) and os.path.getsize( link ):
				evalEcho("system(\"" + cmd + "\");")
				# if(!`endsWith($file, ".png"))
				# {
				# 	string $new_file = substitute(".iff", $file, ".png");
				# 	system("/usr/local/bin/imf_copy " + $file + $new_file);
				# 	$file = $new_file;
				# }
				
			cmd="ln -s " + file + " " + link
			evalEcho("system(\"" + cmd + "\");")
			
		
	for i in range(melGlobals['gFrameRangeStart'],melGlobals['gFrameRangeEnd']+1):
		suffixes=[""]
		if melGlobals['gDoStereoPlayblast']:
			suffixes=["","_l","_r"]
			
		for suffix in suffixes:
			src=imageDir + "/" + imageName + str(suffix) + "." + str(mel.padNumber(i, 4)) + "." + melGlobals['gOutputFmt']
			if not os.path.exists( src ) and os.path.getsize( src ):
				numMissing+=1
				continue
				
			
		
	# $stamp = getFileMTime($src);
	# if($stamp < $gPlayblastStartTime)
	# {
	# 	$numMissing += 1;
	# 	continue;
	# }
	# Create the main frame links to the latest (current) version.
	for i in range(melGlobals['gFrameRangeStart'],melGlobals['gFrameRangeEnd']+1):
		link_dir=str(mel.dirname(mel.dirname(mel.dirname(melGlobals['gTargetImagePath']))))
		link_name=str(mel.basename(melGlobals['gTargetImagePath'], ""))
		link_name=link_name.replace("_[0-9][0-9][0-9][0-9]$","")
		# Remove the _ani or _lay until we update the movie maker.
		link_name=link_name.replace("_[al][na][iy]$","")
		link=link_dir + "/" + link_name + "." + str(mel.padNumber(i, 4)) + "." + melGlobals['gOutputFmt']
		location=melGlobals['gTargetImagePath'].replace((link_dir + "/"),"") + "." + str(mel.padNumber(i, 4)) + "." + melGlobals['gOutputFmt']
		cmd="rm " + link
		if os.path.exists( link ) and os.path.getsize( link ):
			evalEcho("system(\"" + cmd + "\");")
			
		cmd="ln -s " + location + " " + link
		PlayblastToolMessage(cmd)
		evalEcho("system(\"" + cmd + "\");")
		#		string $image_base_name = $imageName + "." + padNumber($i, 4) + "." + $gOutputFmt;
		#		string $link_dir = dirname(dirname($imageDir));
		#		string $rel_dir = substitute(($link_dir + "/"), $imageDir, "");
		#
		#		string $rel_file = $rel_dir + "/" + $image_base_name;
		#		string $link = $link_dir + "/" + $image_base_name;
		#		string $cmd = "rm " + $link;
		#		system($cmd);
		#		$cmd = "ln -s " + $rel_file + " " + $link;
		#		system($cmd);
		
	if numMissing>0:
		PlayblastToolQuitError("Playblasted frames failed validation (" + str(numMissing) + " missing, or belonging to previous playblast).\nThe last source file was " + src + ".\nThe start time for the playblast was " + str(melGlobals['gPlayblastStartTime']) + ".\nThe stamp was " + str(stamp))
		
	

# ---------------------------------------------------------------------------------------------------
# PlayblastToolCheckMovie - Check that the movie was created
# ---------------------------------------------------------------------------------------------------
def PlayblastToolCheckMovie():
	melGlobals.initVar( 'int', 'gDoMovie' )
	# Make a movie?
	melGlobals.initVar( 'int', 'gPlayblastStartTime' )
	# store the playblast start timestamp
	melGlobals.initVar( 'string', 'gTargetMoviePath' )
	# Where to write movies, if desired
	if not melGlobals['gDoMovie']:
		PlayblastToolMessage("Movie generation disabled.")
		return 
		
	if not os.path.exists( melGlobals['gTargetMoviePath'] ) and os.path.getsize( melGlobals['gTargetMoviePath'] ):
		PlayblastToolQuitError("Movie file failed validation (none created).")
		
	stamp=int(mel.getFileMTime(melGlobals['gTargetMoviePath']))
	if stamp<melGlobals['gPlayblastStartTime']:
		PlayblastToolQuitError("Movie file failed validation (none created - movie exists from previous playblast).")
		
	

# ---------------------------------------------------------------------------------------------------
# PlayblastToolCheckFLVMovie - Check that the movie was created
# ---------------------------------------------------------------------------------------------------
def PlayblastToolCheckFLVMovie():
	melGlobals.initVar( 'int', 'gDoMovie' )
	# Make a movie?
	melGlobals.initVar( 'int', 'gPlayblastStartTime' )
	# store the playblast start timestamp
	melGlobals.initVar( 'string', 'gTargetFLVMoviePath' )
	# Where to write FLV movies, if desired
	if not melGlobals['gDoMovie']:
		PlayblastToolMessage("Movie generation disabled.")
		return 
		
	if not os.path.exists( melGlobals['gTargetFLVMoviePath'] ) and os.path.getsize( melGlobals['gTargetFLVMoviePath'] ):
		PlayblastToolQuitError("FLV Movie file failed validation (none created).")
		
	stamp=int(mel.getFileMTime(melGlobals['gTargetFLVMoviePath']))
	if stamp<melGlobals['gPlayblastStartTime']:
		PlayblastToolQuitError("FLV Movie file failed validation (none created - movie exists from previous playblast).")
		
	

# ----------------------------------------------------------------------------------------------------------------
# PlayblastToolPropogateFrames - Make copies of the frames in the edit_supervisor folder needed for the movie robot
# ----------------------------------------------------------------------------------------------------------------
def PlayblastToolPropogateFrames():
	melGlobals.initVar( 'string', 'gTargetImagePath' )
	#	global int $gPlayblastStartTime;	// store the playblast start timestamp
	# Where to write images. Path, plus base name
	melGlobals.initVar( 'string', 'gOutputFmt' )
	# Output format for frames.
	seq=str(mel.getPath("SequenceFromPlayblastDir", [melGlobals['gTargetImagePath']]))
	#
	shot=str(mel.getPath("ShotFromPlayblastDir", [melGlobals['gTargetImagePath']]))
	#
	type=str(mel.getPath("TypeFromPlayblastDir", [melGlobals['gTargetImagePath']]))
	# yields animation or layout in old structure, ani or lay in new
	res=str(mel.getPath("ResFromPlayblastDir", [melGlobals['gTargetImagePath']]))
	# yields standard or high in old structure, "" in new (discontinued)
	imageDir=str(mel.dirname(melGlobals['gTargetImagePath']))
	editSupervisorDir=str(mel.getPath("EditorialPlayblastLatestFramesDir", [seq,shot,res]))
	if editSupervisorDir == "":
		editSupervisorDir=imageDir
		# make sure the edit_supervisor directory exists
		
	if not os.path.isdir( editSupervisorDir ):
		os.mkdir( editSupervisorDir ) 
		internal.shellOutput("chmod +w " + editSupervisorDir, convertNewlines=False, stripTrailingNewline=False)
		
	PlayblastToolMessage("Deleting pre-existing frames from the edit_supervisor folder")
	# use xargs when deleting large numbers of files
	if len(mel.glob(editSupervisorDir + "/*.png")):
		catch( lambda: internal.shellOutput("ls " + editSupervisorDir + "/*.png | xargs rm", convertNewlines=False, stripTrailingNewline=False) )
		
	if len(mel.glob(editSupervisorDir + "/*.tga")):
		catch( lambda: internal.shellOutput("ls " + editSupervisorDir + "/*.tga | xargs rm", convertNewlines=False, stripTrailingNewline=False) )
		
	cmd=''
	fileList=getFileList(fs=("*." + melGlobals['gOutputFmt']),fld=(imageDir + "/"))
	for file in fileList:
		sourceFile=imageDir + "/" + str(file)
		destFile=editSupervisorDir + "/" + str(file)
		PlayblastToolMessage("Propogating " + sourceFile + " to edit_supervisor")
		cmd="/bin/cp " + sourceFile + " " + destFile
		internal.shellOutput(cmd, convertNewlines=False, stripTrailingNewline=False)
		#		//Editors are not using the Smoke system for any current projects, tgas not required
		#		//This should be added as an option to, then read from, project.xml
		#		if($project != "15923_open_season_2")
		#		{
		#			string $destFile = substitute ($gOutputFmt, $destFile, "tga");
		#			$cmd = "/usr/bin/convert " + $sourceFile + " -depth 8 " + $destFile;
		#			system($cmd);
		#		}
		
	

# END NEW CODE
# ---------------------------------------------------------------------------------------------------
# PlayblastToolPropogateMovie - Make copies of the movie in the location needed for the movie robot to pick it up
# ---------------------------------------------------------------------------------------------------
def PlayblastToolPropogateMovie():
	melGlobals.initVar( 'int', 'gDoMovie' )
	# Make a movie?
	melGlobals.initVar( 'int', 'gPlayblastStartTime' )
	# store the playblast start timestamp
	melGlobals.initVar( 'string', 'gTargetMoviePath' )
	# Where to write movies, if desired
	melGlobals.initVar( 'string', 'gTargetImagePath' )
	# Where to write images. Path, plus base name
	if not melGlobals['gDoMovie']:
		return 
		
	seq=str(mel.getPath("SequenceFromPlayblastDir", [melGlobals['gTargetImagePath']]))
	"""
	
		targets for propogated movie, for example:
	
			/renders/entertainment/15015_boz_hv107_production/show/seq7010/sg0230/layout/standard/playblast/7010_0230.mov
	
			/renders/entertainment/15015_boz_hv107_production/show/seq7010/sg0230/layout/standard/playblast/7010_0230_lay.0001.mov
	
			/renders/entertainment/15015_boz_hv107_production/show/seq7010/sg0230/edit_supervisor/standard/playblast/7010_0230.mov
	
	
	
			New targets for propogated movie:
	
			shot/movies/dept/seq_shot.mov - for editorial. Sym-link? Not for now.
	
			shot/movies/latest/seq_shot.mov - for editorial
	
	
	
	
	
			outMovieName
	
			outMovieNameVer
	
			outMovieNameES
	
	
	
			// incoming $gTargetImagePath
	
			// old:/renders/entertainment/16252_webosaurs/show/seqBATL/sg1010/animation/standard/BATL_1010
	
			// new:/data/development/17199_pipeline_dir_test_new/cg/sequences/sq9000/sh0010/movies/lay/frames//9000_0010
	
		"""
	#
	shot=str(mel.getPath("ShotFromPlayblastDir", [melGlobals['gTargetImagePath']]))
	#
	type=str(mel.getPath("TypeFromPlayblastDir", [melGlobals['gTargetImagePath']]))
	# yields animation or layout in old structure, ani or lay in new
	res=str(mel.getPath("ResFromPlayblastDir", [melGlobals['gTargetImagePath']]))
	# yields standard or high in old structure, "" in new (discontinued)
	imageDir=str(mel.getPath("EditorialPlayblastDir", [seq,shot,type,res]))
	movieBaseName=str(mel.basename(melGlobals['gTargetMoviePath'], ""))
	buf=[]
	buf=movieBaseName.split(".")
	movieExt=buf[- 1]
	movieName=''
	movieName=buf[0].replace("_lay$","")
	movieName=movieName.replace("_previs$","")
	movieName=movieName.replace("_ani$","")
	movieName=movieName.replace("_cloth$","")
	# construct mov target paths
	outMovieName=imageDir + "/" + movieName + "." + movieExt
	outMovieNameVer=imageDir + "/" + movieBaseName
	outMovieNameES=str(mel.getPath("EditorialPlayblastLatestDir", [seq,shot,res])) + "/" + movieName + "." + movieExt
	# construct flv target paths
	outFLVMovieName=outMovieName.replace("mov$","flv")
	outFLVMovieNameVer=outMovieNameVer.replace("mov$","flv")
	PlayblastToolMessage("The outMovieName is " + outMovieName)
	PlayblastToolMessage("The outMovieNameVer is " + outMovieNameVer)
	PlayblastToolMessage("The outMovieNameES is " + outMovieNameES)
	PlayblastToolMessage("The outFLVMovieName is " + outFLVMovieName)
	PlayblastToolMessage("The outFLVMovieNameVer is " + outFLVMovieNameVer)
	# make sure directories exist, and copy movies
	for file in [outMovieName,outMovieNameVer,outMovieNameES]:
		dir=str(mel.dirname(file))
		if not os.path.isdir( dir ):
			os.mkdir( dir ) 
			
		internal.shellOutput("chmod +w " + dir, convertNewlines=False, stripTrailingNewline=False)
		if file != melGlobals['gTargetMoviePath']:
			shutil.copy( melGlobals['gTargetMoviePath'], file )
			internal.shellOutput("chmod +w " + str(file), convertNewlines=False, stripTrailingNewline=False)
			
		
		else:
			PlayblastToolMessage(str(file) + " is the same as " + melGlobals['gTargetMoviePath'] + ". Skipping copy.")
			
		
	movies_to_check=[outMovieName,outMovieNameES]
	error=int(False)
	for i in range(0,len(movies_to_check)):
		if not os.path.exists( movies_to_check[i] ) and os.path.getsize( movies_to_check[i] ):
			error=int(True)
			break
			
		stamp=int(mel.getFileMTime(movies_to_check[i]))
		if stamp<melGlobals['gPlayblastStartTime']:
			error=int(True)
			break
			
		
	if error:
		movies_to_delete=[outMovieName,outMovieNameES,melGlobals['gTargetMoviePath']]
		# if there is an error, blast everything, even the source movie. This reduces the possibility of there being a mismatch between what shows up in Insight and in the contextual movie
		# due to the main playblast succeeding but the copy failing.
		for i in range(0,len(movies_to_delete)):
			if os.path.exists( movies_to_delete[i] ) and os.path.getsize( movies_to_delete[i] ):
				os.remove( movies_to_delete[i] )
				
			
		PlayblastToolCheckMovie()
		# check the movie to throw an error
		
	

# ---------------------------------------------------------------------------------------------------
# PlayblastToolBuildSequenceMovies - Submit process to the farm to build sequence movies which use the shot
# ---------------------------------------------------------------------------------------------------
def PlayblastToolBuildSequenceMovies():
	melGlobals.initVar( 'string', 'gInputScene' )
	# The scene to playblast
	department=str(mel.getPath("DepartmentFromFilename", [melGlobals['gInputScene']]))
	project=str(mel.getPath("ProjectFromFilename", [melGlobals['gInputScene']]))
	projectShort=mel.getPath("QubeJobPrefix", ["",""]).upper()
	sequence=str(mel.getPath("SequenceFromFilename", [melGlobals['gInputScene']]))
	playblastType=str(mel.getPath("PlayblastFromFilename", [melGlobals['gInputScene']]))
	PlayblastToolMessage("PlayblastToolBuildSequenceMovies gInputScene is: " + melGlobals['gInputScene'])
	PlayblastToolMessage("PlayblastToolBuildSequenceMovies department is: " + department)
	PlayblastToolMessage("PlayblastToolBuildSequenceMovies project is: " + project)
	PlayblastToolMessage("PlayblastToolBuildSequenceMovies short project name is: " + projectShort)
	PlayblastToolMessage("PlayblastToolBuildSequenceMovies sequence is: " + sequence)
	PlayblastToolMessage("PlayblastToolBuildSequenceMovies playblastType is: " + playblastType)
	#	// Test PATH
	#	string $each;
	#	string $test_path[];
	#	python ("import sys");
	#	$test_path = python("sys.path");
	#	PlayblastToolMessage("PYTHONPATH");
	#	for($each in $test_path)
	#		PlayblastToolMessage("	" + $each);
	#
	#	// Test of the Qube ENV variables
	#	string $qbjobid = "";
	#	$qbjobid = `getenv "QBJOBID"`;
	#	if($qbjobid != "")
	#		PlayblastToolMessage("The qube jobid is " + $qbjobid);
	#
	#	// Test user
	#	string $user_test;
	#	python("import qb");
	#	$user_test = python("qb.jobinfo(id=" + $qbjobid + ")[0]['user']");
	#	PlayblastToolMessage("The user who executed this script is " + $user_test);
	qbjobid=""
	qbuser="render"
	qbjobid=os.environ[ "QBJOBID" ]
	if qbjobid != "":
		python("import qb")
		
	qbuser=str(python("qb.jobinfo(id=" + qbjobid + ")[0]['user']"))
	PlayblastToolMessage("The user who executed this script is " + qbuser)
	# build the qbsub command
	qbsubCmd=''
	jobName=projectShort + "__" + sequence + "__MOVIES"
	cluster="scripts"
	rfxBuildMoviesPath=str(mel.getPath("ProjectPythonDir", [])) + "/rfxBuildMovies.py"
	qbsubCmd=str((about()))
	qbsubCmd and os.environ[ "QBDIR" ] + "/bin/qbsub " or "qbsub "
	#	$qbsubCmd += "--user render ";
	qbsubCmd+="--user " + qbuser + " "
	qbsubCmd+="--priority 4000 "
	qbsubCmd+="--name " + jobName + " "
	qbsubCmd+="--cluster /" + cluster + " "
	qbsubCmd+="--requirements host." + cluster + "=1 "
	if os.path.exists( rfxBuildMoviesPath ) and os.path.getsize( rfxBuildMoviesPath ):
		qbsubCmd+="/usr/bin/python " + rfxBuildMoviesPath + " "
		
	
	else:
		qbsubCmd+="/usr/bin/python /data/film/apps/reelfx/python/rfxBuildMovies.py "
		
	qbsubCmd+="-v " + department + " "
	qbsubCmd+="-p " + project + " "
	qbsubCmd+="-q " + sequence + " "
	qbsubCmd+="-t " + playblastType
	PlayblastToolMessage("qbsubCmd: " + qbsubCmd)
	internal.shellOutput(qbsubCmd, convertNewlines=False, stripTrailingNewline=False)
	

# ---------------------------------------------------------------------------------------------------
# PlayblastToolFastStartMovie - Run qt fast start on the movie
# ---------------------------------------------------------------------------------------------------
def PlayblastToolFastStartMovie():
	melGlobals.initVar( 'int', 'gDoMovie' )
	# Make a movie?
	melGlobals.initVar( 'int', 'gFastStart' )
	# do fast start?
	melGlobals.initVar( 'string', 'gTargetMoviePath' )
	# Where to write movies, if desired
	melGlobals.initVar( 'string', 'gMovieType' )
	# mov or avi
	if not melGlobals['gDoMovie']:
		PlayblastToolMessage("Movie generation disabled.")
		return 
		
	if not melGlobals['gFastStart']:
		PlayblastToolMessage("Fast Start disabled.")
		return 
		
	movieDir=str(mel.dirname(melGlobals['gTargetMoviePath']))
	# move the non fast start movie
	basename=str(mel.basename(melGlobals['gTargetMoviePath'], ""))
	buf=[]
	buf=basename.split(".")
	non_fs_movie=buf[0] + "_NoFS"
	for i in range(1,len(buf)):
		non_fs_movie+="." + buf[i]
		
	non_fs_movie=movieDir + "/" + str(non_fs_movie)
	PlayblastToolMessage("Archiving non fast start movie to " + non_fs_movie + ".")
	os.rename( melGlobals['gTargetMoviePath'], non_fs_movie )
	# build the fast start command
	cmd="/usr/bin/qt-faststart"
	cmd_long=cmd + " " + non_fs_movie + " " + melGlobals['gTargetMoviePath']
	#Execute the system command in Python so we can wrap it in a 30 second timeout
	PlayblastToolMessage("Executing Fast Start Command... " + cmd_long)
	python("import sys")
	python("sys.path.append('/data/film/apps/reelfx/python')")
	python("import timeout")
	fastStartMovieResult=python("timeout.timeout_command(['" + cmd + "', '" + non_fs_movie + "', '" + melGlobals['gTargetMoviePath'] + "'], 30)")
	if fastStartMovieResult[0] == "killed":
		PlayblastToolMessage("The qt-faststart process failed")
		
	
	else:
		PlayblastToolMessage("The qt-faststart process succeeded")
		# remove the non fast start version
		
	os.remove( non_fs_movie )
	

# ---------------------------------------------------------------------------------------------------
# PlayblastToolFlvtool - Run flvtool++ on the flv file
# ---------------------------------------------------------------------------------------------------
def PlayblastToolFlvtool():
	melGlobals.initVar( 'string', 'gTargetFLVMoviePath' )
	# Where to write movies, if desired
	melGlobals.initVar( 'string', 'gTargetFLVMoviePathTemp' )
	# Where to write movies, if desired
	cmd="/usr/local/bin/flvtool++ " + melGlobals['gTargetFLVMoviePathTemp'] + " " + melGlobals['gTargetFLVMoviePath'] + "\n"
	PlayblastToolMessage("flvtool++ command: " + cmd)
	internal.shellOutput(cmd, convertNewlines=False, stripTrailingNewline=False)
	# remove the temp flv file
	if len(mel.glob(melGlobals['gTargetFLVMoviePathTemp'])):
		internal.shellOutput("rm -r " + melGlobals['gTargetFLVMoviePathTemp'], convertNewlines=False, stripTrailingNewline=False)
		
	

# ---------------------------------------------------------------------------------------------------
def PlayblastToolStartMessage():
	melGlobals.initVar( 'int', 'gSessionStartTime' )
	melGlobals['gSessionStartTime']=int(mel.eval("systemTime -asTimeStamp"))
	PlayblastToolMessage("Process initiated at " + str(mel.eval("systemTime")))
	

# ---------------------------------------------------------------------------------------------------
def PlayblastToolEndMessage():
	melGlobals.initVar( 'int', 'gSessionStartTime' )
	elapsed=int(mel.eval("systemTime -asTimeStamp") - melGlobals['gSessionStartTime'])
	mins=int(mel.eval("timeStampToDate -fmt \"%M\" \"" + str(elapsed) + "\""))
	secs=int(mel.eval("timeStampToDate -fmt \"%S\" \"" + str(elapsed) + "\""))
	PlayblastToolMessage("Process successfully completed at " + str(mel.eval("systemTime")))
	PlayblastToolMessage("Elapsed time: " + str(mins) + " minute" + str(((mins != 1) and "s" or "")) + ", " + str(secs) + " second" + str(((secs != 1) and "s" or "")) + ".")
	

# ---------------------------------------------------------------------------------------------------
def PlayblastToolCheckPreCallback():
	melGlobals.initVar( 'string', 'gPlayblastPreCallback' )
	# if it exists, this will be the path to the pre playblast callback
	if mel.exists("PlayblastToolPreCallback"):
		melGlobals['gPlayblastPreCallback']="PlayblastToolPreCallback"
		#string $buffer[];
		#string $results = `whatIs PlayblastToolPreCallback`;
		#tokenize($results, ":", $buffer);
		#if(size($buffer) == 2)
		#{
		#$gPlayblastPreCallback = $buffer[2];
		#}
		
	

# ---------------------------------------------------------------------------------------------------
def _PlayblastTool.hideAllLights():
	lights=ls()
	for light in lights:
		PlayblastToolMessage("Hiding light '" + str(light) + "'.")
		if referenceQuery(inr=light):
			if getAttr(str(light) + ".v") == 0:
				continue
				
			if not getAttr(l=(str(light) + ".v")):
				if not len(listConnections((str(light) + ".v"),
					s=1,d=0)):
					catch( lambda: setAttr((str(light) + ".v"),
						0) )
					continue
					
				
			if getAttr(str(light) + ".lodv") == 0:
				continue
				
			if not getAttr(l=(str(light) + ".lodv")):
				if not len(listConnections((str(light) + ".lodv"),
					s=1,d=0)):
					catch( lambda: setAttr((str(light) + ".lodv"),
						0) )
					continue
					
				
			if getAttr(str(light) + ".ove") == 1 and getAttr(str(light) + ".ovv") == 0:
				continue
				
			if not getAttr(l=(str(light) + ".ove")) and not getAttr(l=(str(light) + ".ovv")):
				if not len(listConnections((str(light) + ".ove"),(str(light) + ".ovv"),
					s=1,d=0)):
					catch( lambda: setAttr((str(light) + ".ove"),
						1) )
					catch( lambda: setAttr((str(light) + ".ovv"),
						0) )
					continue
					
				
			mel.warning("Could not hide light '" + str(light) + "'.")
			continue
			
		
		elif getAttr(str(light) + ".v") != 0:
			if getAttr(l=(str(light) + ".v")):
				catch( lambda: setAttr((str(light) + ".v"),
					l=0) )
				
			cons=listConnections((str(light) + ".v"),
				p=1,s=1,c=0,d=0)
			if len(cons):
				catch( lambda: disconnectAttr(cons[0],
					(str(light) + ".v")) )
				
			catch( lambda: setAttr((str(light) + ".v"),
				0) )
			
		
	

# ------------------------------------------------------------------------- //
# Load Light Rig
# ------------------------------------------------------------------------- //
def PlayblastTool.loadLightRig():
	melGlobals.initVar( 'int', 'gFramePreRollStart' )
	melGlobals.initVar( 'string', 'gLightRigName' )
	melGlobals.initVar( 'string', 'gCamera' )
	melGlobals.initVar( 'string', 'gInputScene' )
	# See if we have a light rig to import.
	if len(melGlobals['gLightRigName']):
		filename=str(mel.getPath("ProjectPresetDir", [])) + "/lightRigs/" + melGlobals['gLightRigName'] + ".ma"
		# See if the light rig file exists.
		if os.path.exists( filename ) and os.path.getsize( filename ):
			_PlayblastTool.hideAllLights()
			PlayblastToolMessage("Importing " + filename + ".")
			# Import the light rig.
			nodes=cmds.file(i=filename,ns="lightRig",rnn=1)
			groups=ls(assemblies=nodes)
			# Change the current time to orient the lights to the camera.
			mel.insight()
			sq=str(mel.getPath("SequenceFromFilename", [melGlobals['gInputScene']]))
			sh=str(mel.getPath("ShotFromFilename", [melGlobals['gInputScene']]))
			hero_frame=int(mel.insight.shot.getHeroFrame("", sq, sh))
			if hero_frame:
				currentTime(hero_frame)
				# If we have a hero frame, use it.
				
			
			else:
				currentTime(melGlobals['gFramePreRollStart'])
				# Otherwise, use the start of the frame range.
				
			# Orient the light rig to the starting angle of the camera.
			for group in groups:
				xform=melGlobals['gCamera']
				if not objectType(xform,
					isa="transform"):
					pars=listRelatives(p=1,pa=melGlobals['gCamera'])
					xform=pars[0]
					
				delete(orientConstraint(xform,group,
					sk=["x", "z"]))
				
			
		
		else:
			PlayblastToolQuitError("Could not find light rig '" + melGlobals['gLightRigName'] + "' -> " + filename + ".")
			
		
	

# ---------------------------------------------------------------------------------------------------
# PlayblastToolLockLocal
# ---------------------------------------------------------------------------------------------------
def PlayblastToolLockLocal():
	melGlobals.initVar( 'string', 'gLocal' )
	PlayblastToolMessage("Checking desktop lock for " + melGlobals['gLocal'])
	python("import qb")
	python("if not bool(qb.jobinfo(filters={'hosts':'" + melGlobals['gLocal'] + "'}, status='pending')):    qb.workerlock({'name':'" + melGlobals['gLocal'] + "'}, lockingString='host.processor_all=1')")
	

# ---------------------------------------------------------------------------------------------------
# PlayblastToolInsightCallback
#
#	Media statuses
#	--------------
#	1 - pending
#	2 - failed
#	3 - complete
#	4 - running
#
# ---------------------------------------------------------------------------------------------------
def PlayblastToolInsightCallback(status,message):
	melGlobals.initVar( 'int', 'gInsightMediaFileId' )
	# Media file id for insight playblast.
	PlayblastToolMessage("gInsightMediaFileId: " + str(str(melGlobals['gInsightMediaFileId'])))
	PlayblastToolMessage("status: " + str(str(status)))
	PlayblastToolMessage("message: " + message)
	id=melGlobals['gInsightMediaFileId']
	if id == 0:
		PlayblastToolMessage("The gInsightMediaFileId was 0, skip callback to Insight")
		return 
		
	result=str(mel.insightUpdateMediaFileStatus(melGlobals['gInsightMediaFileId'], status, message))
	PlayblastToolMessage("The result of the NEW callback to Insight was: " + result)
	

# ---------------------------------------------------------------------------------------------------
# PlayblastToolUpdateInsightJobId -
# ---------------------------------------------------------------------------------------------------
def PlayblastToolUpdateInsightJobId():
	melGlobals.initVar( 'int', 'gInsightMediaFileId' )
	# Media file id for insight playblast.
	media_file_id=melGlobals['gInsightMediaFileId']
	if media_file_id == 0:
		return 
		
	qube_job_id=0
	env=os.environ[ "QBJOBID" ]
	if len(env):
		qube_job_id=int(int(env))
		mel.insightUpdateMediaFileQubeJobId(media_file_id, qube_job_id)
		
	
	else:
		PlayblastToolMessage("Warning: Qube job id 'QBJOBID' could not be retrieved.\n")
		
	PlayblastToolInsightCallback(4, "Playblasting.")
	

# ---------------------------------------------------------------------------------------------------
# PlayblastTooCheckPostCallback - Sets the global string for the path to the post callback
# ---------------------------------------------------------------------------------------------------
def PlayblastToolCheckPostCallback():
	melGlobals.initVar( 'string', 'gPlayblastPostCallback' )
	# if it exists, this will be the path to the post playblast callback
	if mel.exists("PlayblastToolPostCallback"):
		buffer=[]
		results=str(mel.whatIs("PlayblastToolPostCallback"))
		buffer=results.split(":")
		if len(buffer) == 2:
			melGlobals['gPlayblastPostCallback']=buffer[1]
			
		
	

# ---------------------------------------------------------------------------------------------------
# PlayblastToolPostPlayblast - Everything that is needed after the playblast is done
# ---------------------------------------------------------------------------------------------------
def PlayblastToolPostPlayblast():
	melGlobals.initVar( 'int', 'gBypassPostPlayblast' )
	melGlobals.initVar( 'int', 'gFastStart' )
	melGlobals.initVar( 'int', 'gDoMovie' )
	melGlobals.initVar( 'string', 'gPlayblastPostCallback' )
	melGlobals.initVar( 'string', 'gLocal' )
	# ---------------------
	# Stop now if post process will be handled elsewhere.
	# ---------------------
	if melGlobals['gBypassPostPlayblast']:
		PlayblastToolQuitSuccess()
		return 
		
	PlayblastToolMessage("Checking Playblast Frames.")
	# ---------------------
	# Check that the playblasted frames made it
	# ---------------------
	PlayblastToolInsightCallback(4, "Checking Playblast Frames.")
	if catch( lambda: mel.eval("PlayblastToolCheckFrames") ):
		PlayblastToolQuitError("Errors occured while checking playblast frames (PlayblastToolCheckFrames).")
		# ---------------------
		# Run the post call back if we have one
		# ---------------------
		
	PlayblastToolMessage("Running PostCallback.")
	if melGlobals['gPlayblastPostCallback'] != "":
		mel.PlayblastToolPostCallback()
		# ---------------------
		# Make the movie
		# ---------------------
		
	PlayblastToolMessage("Creating the mov and flv files.")
	PlayblastToolInsightCallback(4, "Creating the mov and flv files.")
	if catch( lambda: mel.eval("PlayblastToolCreateMovie") ):
		PlayblastToolQuitError("Errors occured while creating movie (PlayblastToolCreateMovie).")
		# ---------------------
		# flvtool++ the flv movie
		# ---------------------
		
	PlayblastToolMessage("Running flvtool++.")
	if catch( lambda: mel.eval("PlayblastToolFlvtool") ):
		PlayblastToolQuitError("Errors occured while creating flv (PlayblastToolFlvtool).")
		# ---------------------
		# Check the mov file
		# ---------------------
		
	PlayblastToolMessage("Checking the mov.")
	if catch( lambda: mel.eval("PlayblastToolCheckMovie") ):
		PlayblastToolQuitError("Errors occured while checking movie (PlayblastToolCheckMovie).")
		# ---------------------
		# Check the flv file
		# ---------------------
		
	PlayblastToolMessage("Checking the flv.")
	if catch( lambda: mel.eval("PlayblastToolCheckFLVMovie") ):
		PlayblastToolQuitError("Errors occured while checking FLV movie (PlayblastToolCheckFLVMovie).")
		# ---------------------
		# fast start the mov file
		# ---------------------
		
	if melGlobals['gFastStart']:
		PlayblastToolMessage("Fast Starting Movie.")
		if catch( lambda: mel.eval("PlayblastToolFastStartMovie") ):
			PlayblastToolQuitError("Errors occured while fast starting movie (PlayblastToolFastStartMovie).")
			# check the movie again (fast-started version)
			
		PlayblastToolMessage("Checking Movie...")
		if catch( lambda: mel.eval("PlayblastToolCheckMovie") ):
			PlayblastToolQuitError("Errors occured while checking movie (PlayblastToolCheckMovie).")
			
		
	if melGlobals['gDoMovie']:
		PlayblastToolMessage("Propogating mov and flv files.")
		# ---------------------
		# propogate the movie to the location needed for the movie robot
		# ---------------------
		if catch( lambda: mel.eval("PlayblastToolPropogateMovie") ):
			PlayblastToolQuitError("Errors occured propogating movie.")
			
		PlayblastToolInsightCallback(4, "Movies Complete.")
		
	PlayblastToolMessage("Propogating Frames.")
	# ---------------------
	# propogate frames to the location needed for the movie robot
	# ---------------------
	if catch( lambda: mel.eval("PlayblastToolPropogateFrames") ):
		PlayblastToolQuitError("Errors occured propogating Frames.")
		# ---------------------
		# create versioned archive
		# ---------------------
		
	PlayblastToolMessage("Creating versioned archive.")
	if catch( lambda: mel.eval("PlayblastToolVersionDir") ):
		PlayblastToolQuitError("Errors occured creating the versioned archive.")
		#PlayblastToolMessage("DEBUG: Stopping after PlayblastToolVersionDir.");
		#PlayblastToolQuitSuccess();
		# ---------------------
		# Kick off sequence movies
		# ---------------------
		
	if melGlobals['gDoMovie']:
		PlayblastToolMessage("Submitting rfxBuildMovies to the farm.")
		if catch( lambda: mel.eval("PlayblastToolBuildSequenceMovies") ):
			PlayblastToolQuitError("Errors submitting sequence movies to the farm.")
			
		
	if catch( lambda: PlayblastToolInsightCallback(3, "") ):
		PlayblastToolQuitError("Errors occured submitting callback to Insight (PlayblastToolInsightCallback).")
		# --------------------------------------------------------
		# Perform Insight callback
		# --------------------------------------------------------
		#if(catch(eval("PlayblastToolInsightCallback")))
		#	PlayblastToolQuitError("Errors occured submitting callback to Insight (PlayblastToolInsightCallback).");
		# --------------------------------------------------------
		# Lock workstation if this was a local playblast
		# --------------------------------------------------------
		
	if melGlobals['gLocal'] != "":
		if catch( lambda: mel.eval("PlayblastToolLockLocal") ):
			PlayblastToolQuitError("Errors occured locking the local host (PlayblastToolLockLocal).")
			
		
	if melGlobals['gLocal'] != "":
		if catch( lambda: mel.eval("PlayblastToolRestoreMainWindow") ):
			PlayblastToolQuitError("Errors occured restoring the main window (PlayblastToolRestoreMainWindow).")
			# --------------------------------------------------------
			# Restore the main window if this was a local playblast
			# --------------------------------------------------------
			
		
	if catch( lambda: mel.eval("PlayblastToolSetLogState 0") ):
		PlayblastToolQuitError("Errors occured stopping the log (PlayblastToolSetLogState).")
		# ---------------------
		# Stop the script editor log
		# ---------------------
		# ---------------------
		# Output the end message
		# ---------------------
		
	if catch( lambda: mel.eval("PlayblastToolEndMessage") ):
		PlayblastToolQuitError("Errors occured outputting end message (PlayblastToolEndMessage).")
		# ---------------------
		# Get out of here
		# ---------------------
		
	PlayblastToolQuitSuccess()
	

# ---------------------------------------------------------------------------------------------------
# PlayblastTool - Get everything ready to playblast - then evalDeferred the playblast routines.
#				   This is so that control will return to Maya so it can finish initializing the graphics
# ---------------------------------------------------------------------------------------------------
def PlayblastTool(args):
	mel.eval("source \"argList.mel\"")
	# load plugins and source scripts
	mel.eval("source \"parseXML.mel\"")
	mel.eval("source \"fileIO.mel\"")
	mel.eval("source \"UIComponents.mel\"")
	_loadPlugins()
	# global vars
	melGlobals.initVar( 'string', 'gInstructionFile' )
	# name of the instruction file
	melGlobals.initVar( 'string', 'gLockFile' )
	# name of the lock file
	melGlobals.initVar( 'string', 'gLocal' )
	# HOSTNAME if playblast is local
	melGlobals.initVar( 'string', 'gMainWindow' )
	# handle for the Maya Main window
	melGlobals.initVar( 'int[]', 'gOriginalSize' )
	# main window size, [L,W]
	melGlobals.initVar( 'int[]', 'gOriginalPosition' )
	# tlc of Main window, [X,Y]
	melGlobals.initVar( 'string', 'gPlayblastPreCallback' )
	# if it exists, this will be the path to the pre playblast callback
	melGlobals.initVar( 'string', 'gPlayblastPostCallback' )
	# if it exists, this will be the path to the post playblast callback
	melGlobals.initVar( 'int', 'gInsightMediaFileId' )
	# media file id for insight playblast
	melGlobals.initVar( 'string', 'gInputScene' )
	# the scene to playblast
	melGlobals.initVar( 'int', 'gIsStereo' )
	# stereo show
	melGlobals.initVar( 'int', 'gDoDeepPlayblast' )
	# deep playblast
	melGlobals.initVar( 'string', 'gNamespaceRenderLayer' )
	# name of the render layer that has namespace info coded
	melGlobals.initVar( 'string[]', 'gMeshesWithColorsOn' )
	melGlobals.initVar( 'string[]', 'gGpuMeshes' )
	melGlobals.initVar( 'string', 'gTargetMoviePath' )
	melGlobals.initVar( 'string', 'gDeepPlayblastMoviePath' )
	melGlobals.initVar( 'int', 'gBypassPostPlayblast' )
	# Skip the post playblast process (will be handled elsewhere).
	melGlobals.initVar( 'int', 'gPostPlayblastOnly' )
	# Just run the post playblast process.
	melGlobals.initVar( 'int', 'gPlayblasting' )
	melGlobals['gPlayblasting']=int(True)
	# Used by other processes to determine if we are in the playblast tool
	melGlobals['gNamespaceRenderLayer']=""
	melGlobals['gDoDeepPlayblast']=0
	#$gInsightMediaFileId = int(getArgValueDefault($args, "media_file_id", "0"));
	# find the pre and post callback scripts if they exist
	#
	PlayblastToolCheckPreCallback()
	PlayblastToolCheckPostCallback()
	# ---------------------
	# Setup
	# ---------------------
	# ---------------------
	# Output the start message
	# ---------------------
	if catch( lambda: mel.eval("PlayblastToolStartMessage") ):
		PlayblastToolQuitError("Errors occured outputting start message (PlayblastToolStartMessage).")
		# parse arg list
		
	melGlobals['gInstructionFile']=str(mel.getArgValue(args, "instructions"))
	melGlobals['gLockFile']=str(mel.getArgValue(args, "lockFile"))
	melGlobals['gLocal']=str(mel.getArgValue(args, "local"))
	PlayblastToolMessage("gLocal is " + melGlobals['gLocal'])
	# ---------------------
	# Create lock file
	# ---------------------
	PlayblastToolMessage("Creating lock file...")
	if catch( lambda: mel.eval("PlayblastToolCreateLockFile") ):
		PlayblastToolQuitError("Errors occured creating lock file (PlayblastToolCreateLockFile).")
		# ---------------------
		# parse instructions
		# ---------------------
		
	PlayblastToolSeparator()
	PlayblastToolMessage("Parsing Instructions...")
	if catch( lambda: mel.eval("PlayblastToolParseInstructions") ):
		PlayblastToolQuitError("Errors occured parsing instructions. (PlayblastToolParseInstructions)")
		# ---------------------
		# Update insight with the qube job id.
		# ---------------------
		
	PlayblastToolSeparator()
	PlayblastToolMessage("Sending the Qube job id to Insight...")
	if catch( lambda: mel.eval("PlayblastToolUpdateInsightJobId") ):
		PlayblastToolQuitError("Errors occured updaing Insight with the Qube job id. (PlayblastToolUpdateInsightJobId)")
		# ---------------------
		# print instructions
		# ---------------------
		
	if catch( lambda: mel.eval("PlayblastToolPrintOptions") ):
		PlayblastToolQuitError("Errors occured printing options (PlayblastToolPrintOptions).")
		# ---------------------
		# Start the script editor log
		# ---------------------
		
	if catch( lambda: mel.eval("PlayblastToolSetLogState 1") ):
		PlayblastToolQuitError("Errors occured starting the log (PlayblastToolSetLogState).")
		# --------------------------------------------------------------------- //
		# Post Playblast Process Override.
		# --------------------------------------------------------------------- //
		
	if melGlobals['gPostPlayblastOnly']:
		PlayblastToolMessage("Post Process Only")
		# If this is a post playblast process job, just jump to the post
		# process.
		PlayblastToolPostPlayblast()
		return 
		
	PlayblastToolSeparator()
	# ---------------------
	# Set this up with playblast info.
	# ---------------------
	PlayblastToolMessage("Setting this file as a playblast file...")
	if catch( lambda: mel.eval("fileInfo \"isPlayblast\" 1") ):
		PlayblastToolQuitError("Errors occured setting render globals (fileInfo \"isPlayblast\" 1).")
		# ---------------------
		# Open the scene
		# ---------------------
		
	PlayblastToolSeparator()
	PlayblastToolMessage("Opening scene...")
	if catch( lambda: mel.eval("PlayblastToolOpenScene") ):
		PlayblastToolQuitError("Errors occured opening scene (PlayblastToolOpenScene).")
		# ---------------------
		# Setup render globals
		# ---------------------
		
	PlayblastToolSeparator()
	PlayblastToolMessage("Setting up Render Globals...")
	if catch( lambda: mel.eval("PlayblastToolSetupRenderGlobals") ):
		PlayblastToolQuitError("Errors occured setting render globals (PlayblastToolSetupRenderGlobals).")
		# ---------------------
		# Set Smoothing
		# ---------------------
		
	PlayblastToolSeparator()
	PlayblastToolMessage("Setting Smoothing...")
	if catch( lambda: mel.eval("PlayblastToolSetSmoothing") ):
		PlayblastToolQuitError("Errors occured setting smoothing (PlayblastToolSetSmoothing).")
		# ---------------------
		# Set Universal Eye Textures
		# ---------------------
		
	PlayblastToolSeparator()
	PlayblastToolMessage("Setting Universal Eye Textures...")
	if catch( lambda: mel.eval("PlayblastToolSetUniversalEyeTextures") ):
		PlayblastToolQuitError("Errors occured setting smoothing (PlayblastToolSetUniversalEyeTextures).")
		#
		# ---------------------
		# Set Asset Render Res
		# ---------------------
		
	PlayblastToolSeparator()
	PlayblastToolMessage("Setting Render Res...")
	if catch( lambda: mel.eval("PlayblastToolSetAssetRenderRes") ):
		PlayblastToolQuitError("Errors occured setting render res (PlayblastToolSetAssetRenderRes).")
		# ---------------------
		# Set Asset Universal Eye
		# ---------------------
		
	PlayblastToolSeparator()
	PlayblastToolMessage("Setting Universal Eye...")
	if catch( lambda: mel.eval("PlayblastToolSetUniversalEyeOn") ):
		PlayblastToolQuitError("Errors occured setting render res (PlayblastToolSetUniversalEyeOn).")
		# ---------------------
		# Perform per-asset callbacks
		# ---------------------
		
	PlayblastToolSeparator()
	PlayblastToolMessage("Executing per-asset callbacks...")
	if catch( lambda: mel.eval("PlayblastToolExecutePerAssetCallbacks") ):
		PlayblastToolQuitError("Errors occured performing per-asset callbacks (PlayblastToolExecutePerAssetCallbacks).")
		# ---------------------
		# Do deep playblast setup
		# ---------------------
		
	if melGlobals['gDoDeepPlayblast']:
		PlayblastToolSeparator()
		PlayblastToolMessage("Executing Deep Playblast setup...")
		if catch( lambda: mel.eval("PlayblastToolDeepPlayblastSetup") ):
			PlayblastToolQuitError("Errors occured performing Deep Playblast setup (PlayblastToolDeepPlayblastSetup).")
			
		
	PlayblastToolSeparator()
	# ---------------------
	# Check Camera
	# ---------------------
	PlayblastToolMessage("Checking Camera...")
	if catch( lambda: mel.eval("PlayblastToolCheckCamera") ):
		PlayblastToolQuitError("Errors occured checking camera (PlayblastToolCheckCamera).")
		# ---------------------
		# Import light rig.
		# ---------------------
		
	PlayblastToolSeparator()
	PlayblastToolMessage("Loading Light Rig...")
	if catch( lambda: mel.eval("PlayblastTool.loadLightRig") ):
		PlayblastToolQuitError("Errors occurred while loading the light rig (PlayblastTool.loadLightRig).")
		
	PlayblastToolSeparator()
	# ---------------------
	# Set Paths
	# ---------------------
	PlayblastToolMessage("Setting Paths...")
	if catch( lambda: mel.eval("PlayblastToolRemapPaths") ):
		PlayblastToolQuitError("Errors occured setting paths (PlayblastToolRemapPaths).")
		# ---------------------
		# Setup Model Editor
		# ---------------------
		
	PlayblastToolSeparator()
	PlayblastToolMessage("Setting up Model Editor...")
	if catch( lambda: mel.eval("PlayblastToolSetupModelEditor") ):
		PlayblastToolQuitError("Errors occured setting up model editor (PlayblastToolSetupModelEditor).")
		# ---------------------
		# Setup Overlay
		# ---------------------
		
	PlayblastToolSeparator()
	PlayblastToolMessage("Setting up Overlay...")
	if catch( lambda: mel.eval("PlayblastToolSetupOverlay") ):
		PlayblastToolQuitError("Errors occured setting up overlay (PlayblastToolSetupOverlay).")
		# ---------------------
		# Apply stereo overrides
		# ---------------------
		
	if melGlobals['gIsStereo']:
		PlayblastToolSeparator()
		PlayblastToolMessage("Applying Stereo Overrides...")
		if catch( lambda: mel.eval("source \"stereoCameras\"") ):
			PlayblastToolQuitError("Errors occured sourcing stereoCameras.mel.")
			
		if catch( lambda: mel.eval("stereoCameras.readShotSettingsFromPipeline") ):
			PlayblastToolQuitError("Errors occured applying stereo overrides (stereoCameras.readShotSettingsFromPipeline).")
			
		
	PlayblastToolSeparator()
	# ---------------------
	# Maximize Main Window
	# ---------------------
	#	if ($gLocal != "")
	PlayblastToolMessage("Resizing Main Window...")
	if catch( lambda: mel.eval("PlayblastToolMaximizeMainWindow") ):
		PlayblastToolQuitError("Errors setting the Main Window size (PlayblastToolMaximizeMainWindow).")
		
	PlayblastToolSeparator()
	# ---------------------
	# Accessories
	# ---------------------
	PlayblastToolMessage("Setting up Accessories...")
	sequence=str(mel.getPath("SequenceFromFilename", [melGlobals['gInputScene']]))
	shot=str(mel.getPath("ShotFromFilename", [melGlobals['gInputScene']]))
	acc_cmd="accessories(\"" + sequence + "\", \"" + shot + "\");"
	PlayblastToolMessage(acc_cmd)
	if catch( lambda: mel.eval(acc_cmd) ):
		PlayblastToolQuitError("Errors occured setting up accessories (accesories.mel).")
		
	select()
	# small bug fix. Sometimes objects are still selected when maya playblasts. This just makes sure that's not the case.
	#
	# ---------------------
	# Run the pre call back if we have one
	# ---------------------
	PlayblastToolSeparator()
	PlayblastToolMessage("Running PreCallback...")
	if melGlobals['gPlayblastPreCallback'] != "":
		mel.PlayblastToolPreCallback()
		# ------------- End of setup
		
	evalDeferred(lp="PlayblastToolPrePlayblast")
	

