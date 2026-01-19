# TabCommandInput Object

Derived from: [CommandInput](CommandInput.md) Object  

## Description

Tab command inputs contain a set of command inputs and/or group command inputs/

## Methods

| Name | Description |
|----|----|
| [activate](TabCommandInput_activate.md) | Sets this to be the currently activated (selected) tab. |
| [classType](TabCommandInput_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [deleteMe](TabCommandInput_deleteMe.md) | Deletes this Command input. |

## Properties

| Name | Description |
| --- | --- |
| [children](TabCommandInput_children.md) | Gets the CommandInputs collection for this TabCommandInput. Use the add methods on this collection to add child CommandInputs to this Tab in the desired order. |
| [commandInputs](TabCommandInput_commandInputs.md) | Gets the CommandInputs class of the parent, which can be a Command, GroupCommandInput or TabCommandInput. |
| [id](TabCommandInput_id.md) | Gets the unique identifier for this input in the command's CommandInputs. |
| [isActive](TabCommandInput_isActive.md) | Gets if this is the currently activated (selected) tab. |
| [isEnabled](TabCommandInput_isEnabled.md) | Gets or sets if this input is currently enabled or disabled for user interaction. Currently, the isEnabled property does not disable SelectionCommandInput objects but instead has the same effect as the SelectionCommandInput.hasFocus property. |
| [isFullWidth](TabCommandInput_isFullWidth.md) | Gets or sets if this input fills the entire width of the dialog. If true, the name is ignored and the input control will fill the entire width of the command dialog. The default value for this property in a new command input if false, or not to fill the width. This property does not apply to GroupCommandInputs or TabCommandInputs. |
| [isValid](TabCommandInput_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [isVisible](TabCommandInput_isVisible.md) | Gets or sets if this input will be visible to the user. Setting a SelectionCommandInput to be invisible will clear any selections it currently has. |
| [name](TabCommandInput_name.md) | Gets the user visible name of this input. |
| [objectType](TabCommandInput_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [parentCommand](TabCommandInput_parentCommand.md) | Gets the parent Command. |
| [parentCommandInput](TabCommandInput_parentCommandInput.md) | Gets the parent CommandInput if this commandInput is the child of a TabCommandInput or GroupCommandInput. Returns null if there is no parent. |
| [resourceFolder](TabCommandInput_resourceFolder.md) | Gets the folder that contains the icon for the tab. If no name is specified (no text on tab), a resourceFolder containing the icon needs to be provided. Icons can be defined using either PNG or SVG files. More information about icons can be found in the user manual topic [User Interface Customization](UserInterface_UM.htm#IconsForCommands). |
| [toolClipFilename](TabCommandInput_toolClipFilename.md) | Gets or sets the full filename of the image file (PNG) used for the tool clip. The tooltip is always shown but as the user hovers over the control it will progressively display the tool clip and description text. |
| [tooltip](TabCommandInput_tooltip.md) | Gets or sets the base tooltip string. This is always shown for commands. If the tooltip description and/or tool clip are also specified then the tooltip will progressively display more information as the user hovers the mouse over the control. |
| [tooltipDescription](TabCommandInput_tooltipDescription.md) | Gets or sets additional text to display progressively along with the tooltip. The text for the description can contain some basic HTML formatting tags to format the tags. For example the br tag can be used to create multiple paragraphs. The tooltip is always shown but as the user hovers over the control it will progressively display the tool clip and description text. |

## Accessed From

[CommandInputs.addTabCommandInput](CommandInputs_addTabCommandInput.md)

## Samples

| Name | Description |
| --- | --- |
| [Command Inputs API Sample](CommandInputsSample_Sample.md) | Creates a command dialog that demonstrates all of the available command inputs. To use the sample, create a new Python or C++ script and copy and paste this code, replacing the default code. You also need to unpack this zip file which contains a [resource folder](../ExtraFiles/CommandInputsResources.zip) into the same folder where the source code file (.py or .cpp) is. |

## Version

Introduced in version July 2015  

