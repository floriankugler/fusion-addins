# FloatSliderCommandInput Object

Derived from: [SliderCommandInput](SliderCommandInput.md) Object  

## Description

Provides a command input to get the value of a slider from the user, the value type is float.

## Methods

| Name | Description |
|----|----|
| [classType](FloatSliderCommandInput_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [deleteMe](FloatSliderCommandInput_deleteMe.md) | Deletes this Command input. |
| [getText](FloatSliderCommandInput_getText.md) | Gets the texts of the slider if text has been defined. |
| [setText](FloatSliderCommandInput_setText.md) | Sets the text of the slider. Both the left and the right text should be set. |

## Properties

| Name | Description |
| --- | --- |
| [commandInputs](FloatSliderCommandInput_commandInputs.md) | Gets the CommandInputs class of the parent, which can be a Command, GroupCommandInput or TabCommandInput. |
| [expressionOne](FloatSliderCommandInput_expressionOne.md) | Uses an expression to set the value in the first input field. This can contain equations and is evaluated using the specified unit type. |
| [expressionTwo](FloatSliderCommandInput_expressionTwo.md) | Uses an expression to set the value in the second input field. This can contain equations and is evaluated using the specified unit type. This property is only available when the hasTwoSliders property returns true. |
| [hasTwoSliders](FloatSliderCommandInput_hasTwoSliders.md) | Gets if the command input has two sliders. |
| [id](FloatSliderCommandInput_id.md) | Gets the unique identifier for this input in the command's CommandInputs. |
| [isEnabled](FloatSliderCommandInput_isEnabled.md) | Gets or sets if this input is currently enabled or disabled for user interaction. Currently, the isEnabled property does not disable SelectionCommandInput objects but instead has the same effect as the SelectionCommandInput.hasFocus property. |
| [isFullWidth](FloatSliderCommandInput_isFullWidth.md) | Gets or sets if this input fills the entire width of the dialog. If true, the name is ignored and the input control will fill the entire width of the command dialog. The default value for this property in a new command input if false, or not to fill the width. This property does not apply to GroupCommandInputs or TabCommandInputs. |
| [isValid](FloatSliderCommandInput_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [isVisible](FloatSliderCommandInput_isVisible.md) | Gets or sets if this input will be visible to the user. Setting a SelectionCommandInput to be invisible will clear any selections it currently has. |
| [maximumValue](FloatSliderCommandInput_maximumValue.md) | Gets and sets maximum value of the slider in database units. Gets a failure when set if the value of this command input was added by value list. |
| [minimumValue](FloatSliderCommandInput_minimumValue.md) | Gets and sets minimum value of the slider in database units. Gets a failure when set if the value of this command input was added by value list. |
| [name](FloatSliderCommandInput_name.md) | Gets the user visible name of this input. |
| [objectType](FloatSliderCommandInput_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [parentCommand](FloatSliderCommandInput_parentCommand.md) | Gets the parent Command. |
| [parentCommandInput](FloatSliderCommandInput_parentCommandInput.md) | Gets the parent CommandInput if this commandInput is the child of a TabCommandInput or GroupCommandInput. Returns null if there is no parent. |
| [spinStep](FloatSliderCommandInput_spinStep.md) | Gets and sets the spin step value in the unit type set by the unitType argument. The value should be more than zero. This is the amount the slider will advance when the user clicks the spin button beside the value. |
| [toolClipFilename](FloatSliderCommandInput_toolClipFilename.md) | Gets or sets the full filename of the image file (PNG) used for the tool clip. The tooltip is always shown but as the user hovers over the control it will progressively display the tool clip and description text. |
| [tooltip](FloatSliderCommandInput_tooltip.md) | Gets or sets the base tooltip string. This is always shown for commands. If the tooltip description and/or tool clip are also specified then the tooltip will progressively display more information as the user hovers the mouse over the control. |
| [tooltipDescription](FloatSliderCommandInput_tooltipDescription.md) | Gets or sets additional text to display progressively along with the tooltip. The text for the description can contain some basic HTML formatting tags to format the tags. For example the br tag can be used to create multiple paragraphs. The tooltip is always shown but as the user hovers over the control it will progressively display the tool clip and description text. |
| [unitType](FloatSliderCommandInput_unitType.md) | Gets and sets the unit type that is used when evaluating the user's input. |
| [valueList](FloatSliderCommandInput_valueList.md) | Gets the value list of the slider. This property is valid when this input represents a list type of slider command input. Otherwise an empty list will be returned. |
| [valueOne](FloatSliderCommandInput_valueOne.md) | Gets or sets the first value associated with this input. The value is always in the database units of the unit type specified. For example, if the unit type is "inch" this value is in centimeters since centimeters are the database length unit. When setting the value it is converted into a string using the unit type and displayed in the input box. |
| [valueTwo](FloatSliderCommandInput_valueTwo.md) | Gets or sets the second value associated with this input. The value is always in the database units of the unit type specified. For example, if the unit type is "inch" this value is in centimeters since centimeters are the database length unit. When setting the value it is converted into a string using the unit type and displayed in the input box. This property is only available when the hasTwoSliders property returns true. |

## Accessed From

[CommandInputs.addFloatSliderCommandInput](CommandInputs_addFloatSliderCommandInput.md), [CommandInputs.addFloatSliderListCommandInput](CommandInputs_addFloatSliderListCommandInput.md)

## Samples

| Name | Description |
| --- | --- |
| [Command Inputs API Sample](CommandInputsSample_Sample.md) | Creates a command dialog that demonstrates all of the available command inputs. To use the sample, create a new Python or C++ script and copy and paste this code, replacing the default code. You also need to unpack this zip file which contains a [resource folder](../ExtraFiles/CommandInputsResources.zip) into the same folder where the source code file (.py or .cpp) is. |

## Version

Introduced in version June 2015  

