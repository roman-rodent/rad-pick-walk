#Radiant Pickwalk Module

##Setup
1. Clone the repository somewhere on your computer, e.g. C:/SomeStuff/Repo
2. Edit the folder in the radPickWalkModule.mod file to match the folder from step 1
3. Copy the radPickWalkModule.mod file to Maya's modules folder (likely Documents/maya/<version>/modules)
    * If you don't know where the folder is run getenv(MAYA_MODULE_PATH) in the Script Editor
4. Run Maya, and go to Window -> Settings/Preferences -> Plug-in Manager
5. You should see radPickWalk.py. Click on "Loaded" and "Auto-Load"


##Usage
Before you can pickwalk you need to mark up your scene with attributes that encode the
spatial relationships between the nodes.

###Navigation
To navigate use UP and DOWN. CTRL + UP/DOWN will add the node to the selected set.

There are no out-of-the-box keybindings for LEFT and RIGHT, but you can bind whatever keys you want
to the "radPickWalkLeft", "radPickWalkRight", "radPickWalkAddLeft", "radPickWalkAddRight" commands.

###Creating Relationships
Go to the RadPickWalk shelf and click the button to open the UI.

The general workflow is:
* Select a node and click the centre button to set it as the source node
* Select another node and click on the up/down/left/right button to create the relationship

For example, if you select _node1_, click the centre button, select _node2_, and click the top button then
whenever you have _node1_ selected CTRL-UP will select _node2_.

To clear a relationship, select nothing and then click on the direction you want to clear.

Note: Creating a relationship like _node1_ -> UP -> _node2_ does NOT create a _node2_ -> DOWN -> _node1_ relationship. You've gotta do the work yourself.
