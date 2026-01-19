# BoolValueCommandInput Object

Derived from: [CommandInput](CommandInput.md) Object  

## Description

Provides a command input to get a boolean value from the user. This is represented in the user interface as either a button or a check box.

## Methods

| Name | Description |
|----|----|
| [classType](BoolValueCommandInput_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [deleteMe](BoolValueCommandInput_deleteMe.md) | Deletes this Command input. |

## Properties

| Name | Description |
| --- | --- |
| [commandInputs](BoolValueCommandInput_commandInputs.md) | Gets the CommandInputs class of the parent, which can be a Command, GroupCommandInput or TabCommandInput. |
| [id](BoolValueCommandInput_id.md) | Gets the unique identifier for this input in the command's CommandInputs. |
| [isCheckBox](BoolValueCommandInput_isCheckBox.md) | Indicates if this is being shown as a button or check box. |
| [isEnabled](BoolValueCommandInput_isEnabled.md) | Gets or sets if this input is currently enabled or disabled for user interaction. Currently, the isEnabled property does not disable SelectionCommandInput objects but instead has the same effect as the SelectionCommandInput.hasFocus property. |
| [isFullWidth](BoolValueCommandInput_isFullWidth.md) | Gets or sets if this input fills the entire width of the dialog. If true, the name is ignored and the input control will fill the entire width of the command dialog. The default value for this property in a new command input if false, or not to fill the width. This property does not apply to GroupCommandInputs or TabCommandInputs. |
| [isValid](BoolValueCommandInput_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [isVisible](BoolValueCommandInput_isVisible.md) | Gets or sets if this input will be visible to the user. Setting a SelectionCommandInput to be invisible will clear any selections it currently has. |
| [name](BoolValueCommandInput_name.md) | Gets the user visible name of this input. |
| [objectType](BoolValueCommandInput_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [parentCommand](BoolValueCommandInput_parentCommand.md) | Gets the parent Command. |
| [parentCommandInput](BoolValueCommandInput_parentCommandInput.md) | Gets the parent CommandInput if this commandInput is the child of a TabCommandInput or GroupCommandInput. Returns null if there is no parent. |
| [resourceFolder](BoolValueCommandInput_resourceFolder.md) | Gets and sets the folder that contains the icon to display on the button. Text can also be displayed, which is specified using the text property. More information about icons can be found in the user manual topic [User Interface Customization](UserInterface_UM.htm#IconsForCommands). |
| [text](BoolValueCommandInput_text.md) | Gets and sets text to be displayed on the button. If the resourceFolder is not specified then the button will be displayed with only text. If text and the resource folder are specified then both the icon and text will be displayed. |
| [toolClipFilename](BoolValueCommandInput_toolClipFilename.md) | Gets or sets the full filename of the image file (PNG) used for the tool clip. The tooltip is always shown but as the user hovers over the control it will progressively display the tool clip and description text. |
| [tooltip](BoolValueCommandInput_tooltip.md) | Gets or sets the base tooltip string. This is always shown for commands. If the tooltip description and/or tool clip are also specified then the tooltip will progressively display more information as the user hovers the mouse over the control. |
| [tooltipDescription](BoolValueCommandInput_tooltipDescription.md) | Gets or sets additional text to display progressively along with the tooltip. The text for the description can contain some basic HTML formatting tags to format the tags. For example the br tag can be used to create multiple paragraphs. The tooltip is always shown but as the user hovers over the control it will progressively display the tool clip and description text. |
| [value](BoolValueCommandInput_value.md) | Gets or sets the state of this input. If it's being displayed as a check box a value of true indicates the input is checked. If it's being displayed as a button, a value of true indicates the button is currently depressed. |

## Accessed From

[CommandInputs.addBoolValueInput](CommandInputs_addBoolValueInput.md)

## Samples

| Name | Description |
| --- | --- |
| [Command Inputs API Sample](CommandInputsSample_Sample.md) | Creates a command dialog that demonstrates all of the available command inputs. To use the sample, create a new Python or C++ script and copy and paste this code, replacing the default code. You also need to unpack this zip file which contains a [resource folder](../ExtraFiles/CommandInputsResources.zip) into the same folder where the source code file (.py or .cpp) is. |

## Version

Introduced in version August 2014  

