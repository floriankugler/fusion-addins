# CommandInput Object

Derived from: [Base](Base.md) Object  

## Description

The base class for all command inputs. A CommandInput is used to gather an input value from the user when a command is executed.

## Methods

| Name | Description |
|----|----|
| [classType](CommandInput_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [deleteMe](CommandInput_deleteMe.md) | Deletes this Command input. |

## Properties

| Name | Description |
| --- | --- |
| [commandInputs](CommandInput_commandInputs.md) | Gets the CommandInputs class of the parent, which can be a Command, GroupCommandInput or TabCommandInput. |
| [id](CommandInput_id.md) | Gets the unique identifier for this input in the command's CommandInputs. |
| [isEnabled](CommandInput_isEnabled.md) | Gets or sets if this input is currently enabled or disabled for user interaction. Currently, the isEnabled property does not disable SelectionCommandInput objects but instead has the same effect as the SelectionCommandInput.hasFocus property. |
| [isFullWidth](CommandInput_isFullWidth.md) | Gets or sets if this input fills the entire width of the dialog. If true, the name is ignored and the input control will fill the entire width of the command dialog. The default value for this property in a new command input if false, or not to fill the width. This property does not apply to GroupCommandInputs or TabCommandInputs. |
| [isValid](CommandInput_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [isVisible](CommandInput_isVisible.md) | Gets or sets if this input will be visible to the user. Setting a SelectionCommandInput to be invisible will clear any selections it currently has. |
| [name](CommandInput_name.md) | Gets the user visible name of this input. |
| [objectType](CommandInput_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [parentCommand](CommandInput_parentCommand.md) | Gets the parent Command. |
| [parentCommandInput](CommandInput_parentCommandInput.md) | Gets the parent CommandInput if this commandInput is the child of a TabCommandInput or GroupCommandInput. Returns null if there is no parent. |
| [toolClipFilename](CommandInput_toolClipFilename.md) | Gets or sets the full filename of the image file (PNG) used for the tool clip. The tooltip is always shown but as the user hovers over the control it will progressively display the tool clip and description text. |
| [tooltip](CommandInput_tooltip.md) | Gets or sets the base tooltip string. This is always shown for commands. If the tooltip description and/or tool clip are also specified then the tooltip will progressively display more information as the user hovers the mouse over the control. |
| [tooltipDescription](CommandInput_tooltipDescription.md) | Gets or sets additional text to display progressively along with the tooltip. The text for the description can contain some basic HTML formatting tags to format the tags. For example the br tag can be used to create multiple paragraphs. The tooltip is always shown but as the user hovers over the control it will progressively display the tool clip and description text. |

## Accessed From

[AngleValueCommandInput.parentCommandInput](AngleValueCommandInput_parentCommandInput.md), [BoolValueCommandInput.parentCommandInput](BoolValueCommandInput_parentCommandInput.md), [BrowserCommandInput.parentCommandInput](BrowserCommandInput_parentCommandInput.md), [ButtonRowCommandInput.parentCommandInput](ButtonRowCommandInput_parentCommandInput.md), [CommandInput.parentCommandInput](CommandInput_parentCommandInput.md), [CommandInputs.item](CommandInputs_item.md), [CommandInputs.itemById](CommandInputs_itemById.md), [DirectionCommandInput.parentCommandInput](DirectionCommandInput_parentCommandInput.md), [DistanceValueCommandInput.parentCommandInput](DistanceValueCommandInput_parentCommandInput.md), [DropDownCommandInput.parentCommandInput](DropDownCommandInput_parentCommandInput.md), [FloatSliderCommandInput.parentCommandInput](FloatSliderCommandInput_parentCommandInput.md), [FloatSpinnerCommandInput.parentCommandInput](FloatSpinnerCommandInput_parentCommandInput.md), [GroupCommandInput.parentCommandInput](GroupCommandInput_parentCommandInput.md), [ImageCommandInput.parentCommandInput](ImageCommandInput_parentCommandInput.md), [InputChangedEventArgs.input](InputChangedEventArgs_input.md), [IntegerSliderCommandInput.parentCommandInput](IntegerSliderCommandInput_parentCommandInput.md), [IntegerSpinnerCommandInput.parentCommandInput](IntegerSpinnerCommandInput_parentCommandInput.md), [RadioButtonGroupCommandInput.parentCommandInput](RadioButtonGroupCommandInput_parentCommandInput.md), [SelectionCommandInput.parentCommandInput](SelectionCommandInput_parentCommandInput.md), [SeparatorCommandInput.parentCommandInput](SeparatorCommandInput_parentCommandInput.md), [SliderCommandInput.parentCommandInput](SliderCommandInput_parentCommandInput.md), [StringValueCommandInput.parentCommandInput](StringValueCommandInput_parentCommandInput.md), [TabCommandInput.parentCommandInput](TabCommandInput_parentCommandInput.md), [TableCommandInput.getInputAtPosition](TableCommandInput_getInputAtPosition.md), [TableCommandInput.parentCommandInput](TableCommandInput_parentCommandInput.md), [TextBoxCommandInput.parentCommandInput](TextBoxCommandInput_parentCommandInput.md), [TriadCommandInput.parentCommandInput](TriadCommandInput_parentCommandInput.md), [ValueCommandInput.parentCommandInput](ValueCommandInput_parentCommandInput.md)

## Derived Classes

[AngleValueCommandInput](AngleValueCommandInput.md), [BoolValueCommandInput](BoolValueCommandInput.md), [BrowserCommandInput](BrowserCommandInput.md), [ButtonRowCommandInput](ButtonRowCommandInput.md), [DirectionCommandInput](DirectionCommandInput.md), [DistanceValueCommandInput](DistanceValueCommandInput.md), [DropDownCommandInput](DropDownCommandInput.md), [FloatSpinnerCommandInput](FloatSpinnerCommandInput.md), [GroupCommandInput](GroupCommandInput.md), [ImageCommandInput](ImageCommandInput.md), [IntegerSpinnerCommandInput](IntegerSpinnerCommandInput.md), [RadioButtonGroupCommandInput](RadioButtonGroupCommandInput.md), [SelectionCommandInput](SelectionCommandInput.md), [SeparatorCommandInput](SeparatorCommandInput.md), [SliderCommandInput](SliderCommandInput.md), [StringValueCommandInput](StringValueCommandInput.md), [TabCommandInput](TabCommandInput.md), [TableCommandInput](TableCommandInput.md), [TextBoxCommandInput](TextBoxCommandInput.md), [TriadCommandInput](TriadCommandInput.md), [ValueCommandInput](ValueCommandInput.md)

## Samples

| Name | Description |
| --- | --- |
| [Command Inputs API Sample](CommandInputsSample_Sample.md) | Creates a command dialog that demonstrates all of the available command inputs. To use the sample, create a new Python or C++ script and copy and paste this code, replacing the default code. You also need to unpack this zip file which contains a [resource folder](../ExtraFiles/CommandInputsResources.zip) into the same folder where the source code file (.py or .cpp) is. |

## Version

Introduced in version August 2014  

