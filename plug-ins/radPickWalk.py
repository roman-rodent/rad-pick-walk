import maya.cmds as cmds
import maya.mel as mel
import pymel.core as pm
import collections
import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx
import radPickWalkFunctions

SHELF_NAME = "RadPickWalk"

INIT_CMD = ""
UP_CMD = "radPickWalkUp"
DOWN_CMD = "radPickWalkDown"
LEFT_CMD = "radPickWalkLeft"
RIGHT_CMD = "radPickWalkRight"
UP_ADD_CMD = "radPickWalkAddUp"
DOWN_ADD_CMD = "radPickWalkAddDown"
LEFT_ADD_CMD = "radPickWalkAddLeft"
RIGHT_ADD_CMD = "radPickWalkAddRight"

NULL_KEY_BINDING = "None"

command_info = collections.namedtuple('command_info', ['key_binding', 'name', 'cmd_creator', 'ctrl', 'alt'])
# CMDS = [command_info("Up", UP_CMD, lambda *args: OpenMayaMPx.asMPxPtr( RadPickWalkUpCommand() ), False, False),
#         command_info("Down", DOWN_CMD, lambda *args: OpenMayaMPx.asMPxPtr( RadPickWalkDownCommand() ), False, False),
#         command_info("Up", UP_ADD_CMD, lambda *args: OpenMayaMPx.asMPxPtr( RadPickWalkAddUpCommand() ), True, False),
#         command_info("Down", DOWN_ADD_CMD, lambda *args: OpenMayaMPx.asMPxPtr( RadPickWalkAddDownCommand() ), True, False),
#         command_info("Left", LEFT_CMD, lambda *args: OpenMayaMPx.asMPxPtr( RadPickWalkLeftCommand() ), True, False),
#         command_info("Right", RIGHT_CMD, lambda *args: OpenMayaMPx.asMPxPtr( RadPickWalkRightCommand() ), True, False),
#         command_info("Left", LEFT_ADD_CMD, lambda *args: OpenMayaMPx.asMPxPtr( RadPickWalkAddLeftCommand() ), True, True),
#         command_info("Right", RIGHT_ADD_CMD, lambda *args: OpenMayaMPx.asMPxPtr( RadPickWalkAddRightCommand() ), True, True)]

CMDS = [command_info("Up", UP_CMD, lambda *args: OpenMayaMPx.asMPxPtr( radPickWalkFunctions.RadPickWalkUpCommand() ), False, False),
        command_info("Down", DOWN_CMD, lambda *args: OpenMayaMPx.asMPxPtr( radPickWalkFunctions.RadPickWalkDownCommand() ), False, False),
        command_info("Up", UP_ADD_CMD, lambda *args: OpenMayaMPx.asMPxPtr( radPickWalkFunctions.RadPickWalkAddUpCommand() ), True, False),
        command_info("Down", DOWN_ADD_CMD, lambda *args: OpenMayaMPx.asMPxPtr( radPickWalkFunctions.RadPickWalkAddDownCommand() ), True, False),
        command_info(NULL_KEY_BINDING, LEFT_CMD, lambda *args: OpenMayaMPx.asMPxPtr( radPickWalkFunctions.RadPickWalkLeftCommand() ), True, False),
        command_info(NULL_KEY_BINDING, RIGHT_CMD, lambda *args: OpenMayaMPx.asMPxPtr( radPickWalkFunctions.RadPickWalkRightCommand() ), True, False),
        command_info(NULL_KEY_BINDING, LEFT_ADD_CMD, lambda *args: OpenMayaMPx.asMPxPtr( radPickWalkFunctions.RadPickWalkAddLeftCommand() ), True, True),
        command_info(NULL_KEY_BINDING, RIGHT_ADD_CMD, lambda *args: OpenMayaMPx.asMPxPtr( radPickWalkFunctions.RadPickWalkAddRightCommand() ), True, True)]


OnExitCallback = None

def teardown_shelf(*args):
	try:
		mel.eval('if (`shelfLayout -exists {0} `) deleteShelfTabNoPrompt {0};'.format(SHELF_NAME))
	except:
		print "Error"

def setup_shelf():
	teardown_shelf()
	shelfTab = mel.eval('addNewShelfTab {}'.format(SHELF_NAME))
	cmds.shelfButton(command=radPickWalkFunctions.make_pick_walk_ui, image="radIcon.png", label="RadPickWalk UI", annotation="RadPickWalk UI", parent=shelfTab, style="iconOnly")


def deregister_cmds(mobject):
	plugin = OpenMayaMPx.MFnPlugin(mobject)
	for command_info in CMDS:
		try:
			# Unbind the hotkey completely
			plugin.deregisterCommand(command_info.name)
			if command_info.key_binding != NULL_KEY_BINDING:
				pm.hotkey(keyShortcut = command_info.key_binding, ctrlModifier=command_info.ctrl, altModifier=command_info.alt, name="")
			print "Deregistered command " + command_info.name
		except:
			print "Failed to deregister command " + command_info.name


def register_cmds(mobject):
	deregister_cmds(mobject)
	plugin = OpenMayaMPx.MFnPlugin(mobject)
	for command_info in CMDS:
		try:
			plugin.registerCommand(command_info.name, command_info.cmd_creator)
			pm.nameCommand(command_info.name, ann=command_info.name, command = command_info.name)
			if command_info.key_binding != NULL_KEY_BINDING:
				pm.hotkey(keyShortcut = command_info.key_binding, name=command_info.name, ctrlModifier=command_info.ctrl, altModifier=command_info.alt)
			print "Registered command " + command_info.name
		except:
			print "Failed to register command " + command_info.name

# Initialize the script plug-in
def initializePlugin(mobject):
	setup_shelf()
	global OnExitCallback
	OnExitCallback = OpenMaya.MSceneMessage.addCallback(OpenMaya.MSceneMessage.kMayaExiting, teardown_shelf)
	register_cmds(mobject)


# Uninitialize the script plug-in
def uninitializePlugin(mobject):
    radPickWalkFunctions.destroy_pick_walk_ui()
    teardown_shelf()
    global OnExitCallback
    OpenMaya.MSceneMessage.removeCallback(OnExitCallback)
    OnExitCallback = None
    deregister_cmds(mobject)
