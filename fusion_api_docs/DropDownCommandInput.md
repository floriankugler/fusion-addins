# DropDownCommandInput Object

Derived from: [CommandInput](CommandInput.md) Object  

## Description

Provides a command input to get the choice in a drop-down list from the user.

## Methods

| Name | Description |
|----|----|
| [classType](DropDownCommandInput_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [deleteMe](DropDownCommandInput_deleteMe.md) | Deletes this Command input. |

## Properties

| Name | Description |
| --- | --- |
| [commandInputs](DropDownCommandInput_commandInputs.md) | Gets the CommandInputs class of the parent, which can be a Command, GroupCommandInput or TabCommandInput. |
| [dropDownStyle](DropDownCommandInput_dropDownStyle.md) | Returns the style of drop down this was created as. |
| [id](DropDownCommandInput_id.md) | Gets the unique identifier for this input in the command's CommandInputs. |
| [isEnabled](DropDownCommandInput_isEnabled.md) | Gets or sets if this input is currently enabled or disabled for user interaction. Currently, the isEnabled property does not disable SelectionCommandInput objects but instead has the same effect as the SelectionCommandInput.hasFocus property. |
| [isFullWidth](DropDownCommandInput_isFullWidth.md) | Gets or sets if this input fills the entire width of the dialog. If true, the name is ignored and the input control will fill the entire width of the command dialog. The default value for this property in a new command input if false, or not to fill the width. This property does not apply to GroupCommandInputs or TabCommandInputs. |
| [isValid](DropDownCommandInput_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [isVisible](DropDownCommandInput_isVisible.md) | Gets or sets if this input will be visible to the user. Setting a SelectionCommandInput to be invisible will clear any selections it currently has. |
| [listItems](DropDownCommandInput_listItems.md) | Returns the ListItems object associated with this drop-down. You use this object to populate and interact with the items in the drop-down. |
| [maxVisibleItems](DropDownCommandInput_maxVisibleItems.md) | Gets or sets the maximum allowed size on screen of the drop down list, measured in items. |
| [name](DropDownCommandInput_name.md) | Gets the user visible name of this input. |
| [objectType](DropDownCommandInput_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [parentCommand](DropDownCommandInput_parentCommand.md) | Gets the parent Command. |
| [parentCommandInput](DropDownCommandInput_parentCommandInput.md) | Gets the parent CommandInput if this commandInput is the child of a TabCommandInput or GroupCommandInput. Returns null if there is no parent. |
| [selectedItem](DropDownCommandInput_selectedItem.md) | Gets the item in the list that is currently selected. This can return null in the case where no item in the list has been selected. This should be ignored for CheckBoxDropDownStyle style drop-downs because multiple items can be selected and each LiteItem should be checked individually. |
| [toolClipFilename](DropDownCommandInput_toolClipFilename.md) | Gets or sets the full filename of the image file (PNG) used for the tool clip. The tooltip is always shown but as the user hovers over the control it will progressively display the tool clip and description text. |
| [tooltip](DropDownCommandInput_tooltip.md) | Gets or sets the base tooltip string. This is always shown for commands. If the tooltip description and/or tool clip are also specified then the tooltip will progressively display more information as the user hovers the mouse over the control. |
| [tooltipDescription](DropDownCommandInput_tooltipDescription.md) | Gets or sets additional text to display progressively along with the tooltip. The text for the description can contain some basic HTML formatting tags to format the tags. For example the br tag can be used to create multiple paragraphs. The tooltip is always shown but as the user hovers over the control it will progressively display the tool clip and description text. |

## Accessed From

[CommandInputs.addDropDownCommandInput](CommandInputs_addDropDownCommandInput.md)

## Samples

| Name | Description |
| --- | --- |
| [Command Inputs API Sample](CommandInputsSample_Sample.md) | Creates a command dialog that demonstrates all of the available command inputs. To use the sample, create a new Python or C++ script and copy and paste this code, replacing the default code. You also need to unpack this zip file which contains a [resource folder](../ExtraFiles/CommandInputsResources.zip) into the same folder where the source code file (.py or .cpp) is. |

## Version

Introduced in version January 2015  

