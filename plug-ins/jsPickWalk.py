import maya.cmds as cmds
import maya.mel as mel
import pymel.core as pm
import collections
import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx

main_buttons = {}
CREATE_MODE_NAME = "create"
NAV_MODE_NAME = "navigate"
SHELF_NAME = "JSPickWalk"
UI_WINDOW_NAME = "JSPickWalkWindow"

LEFT_BUTTON = "js_leftButton"
RIGHT_BUTTON = "js_rightButton"
UP_BUTTON = "js_upButton"
DOWN_BUTTON = "js_downButton"
CENTRE_BUTTON = "js_centreButton"
BUTTON_NAMES = [LEFT_BUTTON, RIGHT_BUTTON, UP_BUTTON, DOWN_BUTTON, CENTRE_BUTTON]

INIT_CMD = ""
UP_CMD = "jsPickWalkUp"
DOWN_CMD = "jsPickWalkDown"
LEFT_CMD = "jsPickWalkLeft"
RIGHT_CMD = "jsPickWalkRight"
UP_ADD_CMD = "jsPickWalkAddUp"
DOWN_ADD_CMD = "jsPickWalkAddDown"
LEFT_ADD_CMD = "jsPickWalkAddLeft"
RIGHT_ADD_CMD = "jsPickWalkAddRight"

NULL_KEY_BINDING = "None"

command_info = collections.namedtuple('command_info', ['key_binding', 'name', 'cmd_creator', 'ctrl', 'alt'])
# CMDS = [command_info("Up", UP_CMD, lambda *args: OpenMayaMPx.asMPxPtr( PickWalkUpCommand() ), False, False),
#         command_info("Down", DOWN_CMD, lambda *args: OpenMayaMPx.asMPxPtr( PickWalkDownCommand() ), False, False),
#         command_info("Up", UP_ADD_CMD, lambda *args: OpenMayaMPx.asMPxPtr( PickWalkAddUpCommand() ), True, False),
#         command_info("Down", DOWN_ADD_CMD, lambda *args: OpenMayaMPx.asMPxPtr( PickWalkAddDownCommand() ), True, False),
#         command_info("Left", LEFT_CMD, lambda *args: OpenMayaMPx.asMPxPtr( PickWalkLeftCommand() ), True, False),
#         command_info("Right", RIGHT_CMD, lambda *args: OpenMayaMPx.asMPxPtr( PickWalkRightCommand() ), True, False),
#         command_info("Left", LEFT_ADD_CMD, lambda *args: OpenMayaMPx.asMPxPtr( PickWalkAddLeftCommand() ), True, True),
#         command_info("Right", RIGHT_ADD_CMD, lambda *args: OpenMayaMPx.asMPxPtr( PickWalkAddRightCommand() ), True, True)]

CMDS = [command_info("Up", UP_CMD, lambda *args: OpenMayaMPx.asMPxPtr( PickWalkUpCommand() ), False, False),
        command_info("Down", DOWN_CMD, lambda *args: OpenMayaMPx.asMPxPtr( PickWalkDownCommand() ), False, False),
        command_info("Up", UP_ADD_CMD, lambda *args: OpenMayaMPx.asMPxPtr( PickWalkAddUpCommand() ), True, False),
        command_info("Down", DOWN_ADD_CMD, lambda *args: OpenMayaMPx.asMPxPtr( PickWalkAddDownCommand() ), True, False),
        command_info(NULL_KEY_BINDING, LEFT_CMD, lambda *args: OpenMayaMPx.asMPxPtr( PickWalkLeftCommand() ), True, False),
        command_info(NULL_KEY_BINDING, RIGHT_CMD, lambda *args: OpenMayaMPx.asMPxPtr( PickWalkRightCommand() ), True, False),
        command_info(NULL_KEY_BINDING, LEFT_ADD_CMD, lambda *args: OpenMayaMPx.asMPxPtr( PickWalkAddLeftCommand() ), True, True),
        command_info(NULL_KEY_BINDING, RIGHT_ADD_CMD, lambda *args: OpenMayaMPx.asMPxPtr( PickWalkAddRightCommand() ), True, True)]


OnExitCallback = None

js_pick_walk_mode = CREATE_MODE_NAME

class PickWalkUpCommand(OpenMayaMPx.MPxCommand):
	def __init__(self):
		OpenMayaMPx.MPxCommand.__init__(self)

	def doIt(self, argList):
		js_pick_walk("up", False)

class PickWalkDownCommand(OpenMayaMPx.MPxCommand):
	def __init__(self):
		OpenMayaMPx.MPxCommand.__init__(self)

	def doIt(self, argList):
		js_pick_walk("down", False)

class PickWalkLeftCommand(OpenMayaMPx.MPxCommand):
	def __init__(self):
		OpenMayaMPx.MPxCommand.__init__(self)

	def doIt(self, argList):
		js_pick_walk("left", False)

class PickWalkRightCommand(OpenMayaMPx.MPxCommand):
	def __init__(self):
		OpenMayaMPx.MPxCommand.__init__(self)

	def doIt(self, argList):
		js_pick_walk("right", False)

class PickWalkAddUpCommand(OpenMayaMPx.MPxCommand):
	def __init__(self):
		OpenMayaMPx.MPxCommand.__init__(self)

	def doIt(self, argList):
		js_pick_walk("up", True)

class PickWalkAddDownCommand(OpenMayaMPx.MPxCommand):
	def __init__(self):
		OpenMayaMPx.MPxCommand.__init__(self)

	def doIt(self, argList):
		js_pick_walk("down", True)

class PickWalkAddLeftCommand(OpenMayaMPx.MPxCommand):
	def __init__(self):
		OpenMayaMPx.MPxCommand.__init__(self)

	def doIt(self, argList):
		js_pick_walk("left", True)

class PickWalkAddRightCommand(OpenMayaMPx.MPxCommand):
	def __init__(self):
		OpenMayaMPx.MPxCommand.__init__(self)

	def doIt(self, argList):
		js_pick_walk("right", True)

def check_valid_dir(direction):
	if direction not in ["up", "down", "left", "right"]:
		raise NameError("Invalid direction: " + direction)

def check_valid_obj(obj):
	if not pm.objExists(obj):
		raise NameError("Invalid object: " + obj)

def dir_to_attr(direction):
	return "js_" + direction

def mark_scene_dirty():
	mel.eval("file -modified 1")

def make_pick_walk(source, destination, direction):
	check_valid_dir(direction)
	check_valid_obj(source)
	check_valid_obj(destination)

	print "Adding pick walk from " + source + " to " + destination + " with direction " + direction

	attr_name = dir_to_attr(direction)
	if not pm.attributeQuery(attr_name, node=source, exists=True):
		pm.addAttr(source, attributeType="message", longName=attr_name)

	pm.connectAttr(destination + ".message", source + "." + attr_name, force=True)
	mark_scene_dirty()

def break_pick_walk(source, destination, direction):
	pm.disconnectAttr(destination + ".message", source + "." + dir_to_attr(direction))
	mark_scene_dirty()

def find_connected_object(source, direction):
	if pm.attributeQuery(dir_to_attr(direction), node=source, exists=True):
		connections = pm.listConnections(source + "." + dir_to_attr(direction))
		if connections:
			return connections[0]
	return ""

def js_pick_walk(direction, add):
	check_valid_dir(direction)

	selectedObjs = pm.ls(selection=True)
	if not selectedObjs:
		return

	newSelectedObjs = []
	for obj in selectedObjs:
		if add and obj not in newSelectedObjs:
			newSelectedObjs.append(obj)
	connection = find_connected_object(selectedObjs[len(selectedObjs) - 1], direction)
	if connection:
		# If going back to previous node, handle it as "unselect"
		if len(newSelectedObjs) > 1 and newSelectedObjs[len(newSelectedObjs) - 2] == connection:
			newSelectedObjs.pop(len(newSelectedObjs) - 1)
		else:
			# Connection should be at the end of the list, since that
			# will be the selected node
			try:
				newSelectedObjs.remove(connection)
			except:
				pass
			newSelectedObjs.append(connection)
	if newSelectedObjs:
		pm.select(newSelectedObjs, replace=True)

def set_pick_walk_create():
	global js_pick_walk_mode
	js_pick_walk_mode = CREATE_MODE_NAME

def set_pick_walk_navigate():
	global js_pick_walk_mode
	js_pick_walk_mode = NAV_MODE_NAME

def make_pick_walk_button_click(name):
	button = main_buttons[name]
	if not button:
		raise NameError("Invalid button: " + name)
	direction = ""
	if name == UP_BUTTON:
		direction = "up"
	elif name == DOWN_BUTTON:
		direction = "down"
	elif name == LEFT_BUTTON:
		direction = "left"
	elif name == RIGHT_BUTTON:
		direction = "right"
	else:
		raise NameError("Invalid button: " + name)

	attr_name = dir_to_attr(direction)

	centre_obj = main_buttons[CENTRE_BUTTON]
	centre_obj_name = centre_obj.getLabel()
	print centre_obj_name
	print js_pick_walk_mode
	if pm.objExists(centre_obj_name):
		if js_pick_walk_mode == CREATE_MODE_NAME:
			selection = pm.ls(selection=True)
			if selection:
				if not pm.attributeQuery(attr_name, node=centre_obj_name, exists=True):
					pm.addAttr(centre_obj_name, longName=attr_name, attributeType="message")

				if centre_obj_name == selection[0]:
					pm.confirmDialog(message="Can't pickwalk to itself, silly...")
					pm.error("Can't pickwalk to self, silly...")
				else:
					make_pick_walk(centre_obj_name, selection[0], direction)
			else:
				label = button.getLabel()
				if label != "blank":
					result = pm.confirmDialog(message="You have nothing selected. Do you want to clear the " + direction + " direction for " + centre_obj_name + "?", button=["Yes", "No"], cancelButton="No")
					if result == "Yes":
						connections = pm.listConnections(centre_obj_name + "." + attr_name)
						if connections:
							break_pick_walk(centre_obj_name, connections[0], direction)

		elif js_pick_walk_mode == NAV_MODE_NAME:
			js_pick_walk(direction, False)
			add_selected_obj_to_middle()

	update_pick_walk_window()


def build_make_pick_walk_window(window_name):
	pm.window(window_name, title="Make Pick Walk")
	pm.columnLayout(adjustableColumn=True)
	form_layout = pm.formLayout(numberOfDivisions=100)
	topLeftBlank = pm.text("js_topLeftBlank", label="")
	upButton = pm.button(UP_BUTTON, label="blank", command= lambda *args: make_pick_walk_button_click(UP_BUTTON))
	topRightBlank = pm.text("js_topRightBlank", label="")

	leftButton = pm.button(LEFT_BUTTON, label="blank", command= lambda *args: make_pick_walk_button_click(LEFT_BUTTON))
	centreButton = pm.button(CENTRE_BUTTON, label="nothing selected", command= lambda *args: add_selected_obj_to_middle())
	rightButton = pm.button(RIGHT_BUTTON, label="blank", command= lambda *args: make_pick_walk_button_click(RIGHT_BUTTON))

	botLeftBlank = pm.text("js_botLeftBlank", label="")
	downButton = pm.button(DOWN_BUTTON, label="blank", command= lambda *args: make_pick_walk_button_click(DOWN_BUTTON))
	botRightBlank = pm.text("js_botRightBlank", label="")

	main_buttons[UP_BUTTON] = upButton
	main_buttons[LEFT_BUTTON] = leftButton
	main_buttons[CENTRE_BUTTON] = centreButton
	main_buttons[RIGHT_BUTTON] = rightButton
	main_buttons[DOWN_BUTTON] = downButton


	mode = pm.radioButtonGrp(columnWidth=[[1,100]], columnAlign=[[1,"left"]], label="CURRENT MODE: ", label1="Creation", label2="Navigation", select=1, numberOfRadioButtons=2, onCommand1= lambda *args: set_pick_walk_create(), onCommand2= lambda *args: set_pick_walk_navigate())
	form_layout.attachForm(mode, "top", 5)
	form_layout.attachForm(mode, "left", 5)
	form_layout.attachForm(mode, "right", 5)

	form_layout.attachControl(topLeftBlank, "top", 10, mode)
	form_layout.attachForm(topLeftBlank, "left", 0)
	form_layout.attachPosition(topLeftBlank, "right", 0, 33)

	form_layout.attachControl(upButton, "top", 10, mode)
	form_layout.attachPosition(upButton, "left", 0, 33)
	form_layout.attachPosition(upButton, "right", 0, 66)

	form_layout.attachControl(topRightBlank, "top", 10, mode)
	form_layout.attachPosition(topRightBlank, "left", 0, 66)
	form_layout.attachForm(topRightBlank, "right", 0)

	form_layout.attachControl(leftButton, "top", 5, upButton)
	form_layout.attachForm(leftButton, "left", 0)
	form_layout.attachPosition(leftButton, "right", 0, 33)

	form_layout.attachControl(centreButton, "top", 5, upButton)
	form_layout.attachPosition(centreButton, "left", 0, 33)
	form_layout.attachPosition(centreButton, "right", 0, 66)

	form_layout.attachControl(rightButton, "top", 5, upButton)
	form_layout.attachPosition(rightButton, "left", 0, 66)
	form_layout.attachForm(rightButton, "right", 0)

	form_layout.attachControl(botLeftBlank, "top", 5, leftButton)
	form_layout.attachForm(botLeftBlank, "left", 0)
	form_layout.attachPosition(botLeftBlank, "right", 0, 33)

	form_layout.attachControl(downButton, "top", 5, leftButton)
	form_layout.attachPosition(downButton, "left", 0, 33)
	form_layout.attachPosition(downButton, "right", 0, 66)

	form_layout.attachControl(botRightBlank, "top", 5, leftButton)
	form_layout.attachPosition(botRightBlank, "left", 0, 66)
	form_layout.attachForm(botRightBlank, "right", 0)

def reset_pick_walk_buttons():
	for button_name in BUTTON_NAMES:
		button = main_buttons[button_name]
		if button:
			if button_name == CENTRE_BUTTON:
				button.setLabel("nothing selected")
			else:
				button.setLabel("blank")


def update_pick_walk_window():
	centre_obj = main_buttons[CENTRE_BUTTON]
	centre_obj_name = centre_obj.getLabel()
	if not pm.objExists(centre_obj_name):
		reset_pick_walk_buttons()
	else:
		up = find_connected_object(centre_obj_name, "up")
		down = find_connected_object(centre_obj_name, "down")
		left = find_connected_object(centre_obj_name, "left")
		right = find_connected_object(centre_obj_name, "right")

		if not up:
			up = "blank"
		if not down:
			down = "blank"
		if not left:
			left = "blank"
		if not right:
			right = "blank"
		main_buttons[UP_BUTTON].setLabel(up)
		main_buttons[DOWN_BUTTON].setLabel(down)
		main_buttons[LEFT_BUTTON].setLabel(left)
		main_buttons[RIGHT_BUTTON].setLabel(right)


def make_pick_walk_from_sel(direction):
	check_valid_dir(direction)
	selection = pm.ls(selection=True)
	if len(selection) != 2:
		pm.error("You need to select 2 objects to make pick walk from selection")

	destination = selection[0]
	source = selection[1]

	make_pick_walk(source, destination, direction)

def add_selected_obj_to_middle():
	selectedObjs = pm.ls(selection=True)
	if selectedObjs:
		dabutton = main_buttons[CENTRE_BUTTON]
		dabutton.setLabel(selectedObjs[0])
	update_pick_walk_window()

def destroy_pick_walk_ui():
	if pm.window(UI_WINDOW_NAME, exists=True):
		pm.deleteUI(UI_WINDOW_NAME)

def make_pick_walk_ui():
	destroy_pick_walk_ui()
	build_make_pick_walk_window(UI_WINDOW_NAME)
	pm.showWindow(UI_WINDOW_NAME)
	print main_buttons
	add_selected_obj_to_middle()

def cmd_creator():
	return OpenMayaMPx.asMPxPtr( PickWalkCommand() )

def teardown_shelf(*args):
	try:
		mel.eval('if (`shelfLayout -exists {0} `) deleteShelfTabNoPrompt {0};'.format(SHELF_NAME))
	except:
		print "Error"

def setup_shelf():
	teardown_shelf()
	shelfTab = mel.eval('addNewShelfTab {}'.format(SHELF_NAME))
	cmds.shelfButton(command=make_pick_walk_ui, image="jsIcon.png", label="Activate UI", annotation="Activate UI", parent=shelfTab)


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
    destroy_pick_walk_ui()
    teardown_shelf()
    global OnExitCallback
    OpenMaya.MSceneMessage.removeCallback(OnExitCallback)
    OnExitCallback = None
    deregister_cmds(mobject)
