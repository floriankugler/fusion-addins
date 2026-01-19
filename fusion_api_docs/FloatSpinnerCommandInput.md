# FloatSpinnerCommandInput Object

Derived from: [CommandInput](CommandInput.md) Object  

## Description

Provides a command input to get the value of a spinner from the user, the value type is float.

## Methods

| Name | Description |
|----|----|
| [classType](FloatSpinnerCommandInput_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [deleteMe](FloatSpinnerCommandInput_deleteMe.md) | Deletes this Command input. |

## Properties

| Name | Description |
| --- | --- |
| [commandInputs](FloatSpinnerCommandInput_commandInputs.md) | Gets the CommandInputs class of the parent, which can be a Command, GroupCommandInput or TabCommandInput. |
| [expression](FloatSpinnerCommandInput_expression.md) | Gets or sets the expression displayed in the input field. This can contain equations and references to parameters. It is evaluated using the specified unit type. |
| [id](FloatSpinnerCommandInput_id.md) | Gets the unique identifier for this input in the command's CommandInputs. |
| [isEnabled](FloatSpinnerCommandInput_isEnabled.md) | Gets or sets if this input is currently enabled or disabled for user interaction. Currently, the isEnabled property does not disable SelectionCommandInput objects but instead has the same effect as the SelectionCommandInput.hasFocus property. |
| [isFullWidth](FloatSpinnerCommandInput_isFullWidth.md) | Gets or sets if this input fills the entire width of the dialog. If true, the name is ignored and the input control will fill the entire width of the command dialog. The default value for this property in a new command input if false, or not to fill the width. This property does not apply to GroupCommandInputs or TabCommandInputs. |
| [isValid](FloatSpinnerCommandInput_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [isValidExpression](FloatSpinnerCommandInput_isValidExpression.md) | Returns true if the current expression is valid and can be evaluated. If this is false, the value returned should be ignored because there currently is not a valid value. |
| [isVisible](FloatSpinnerCommandInput_isVisible.md) | Gets or sets if this input will be visible to the user. Setting a SelectionCommandInput to be invisible will clear any selections it currently has. |
| [maximumValue](FloatSpinnerCommandInput_maximumValue.md) | Gets the maximum allowed value of the spinner in database units. |
| [minimumValue](FloatSpinnerCommandInput_minimumValue.md) | Gets the minimum allowed value of the spinner in database units. |
| [name](FloatSpinnerCommandInput_name.md) | Gets the user visible name of this input. |
| [objectType](FloatSpinnerCommandInput_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [parentCommand](FloatSpinnerCommandInput_parentCommand.md) | Gets the parent Command. |
| [parentCommandInput](FloatSpinnerCommandInput_parentCommandInput.md) | Gets the parent CommandInput if this commandInput is the child of a TabCommandInput or GroupCommandInput. Returns null if there is no parent. |
| [spinStep](FloatSpinnerCommandInput_spinStep.md) | Gets the spin step value in the unit type set by the unitType argument. The value should be more than zero. This is the amount the spinner will advance when the user clicks the spin button beside the value. |
| [toolClipFilename](FloatSpinnerCommandInput_toolClipFilename.md) | Gets or sets the full filename of the image file (PNG) used for the tool clip. The tooltip is always shown but as the user hovers over the control it will progressively display the tool clip and description text. |
| [tooltip](FloatSpinnerCommandInput_tooltip.md) | Gets or sets the base tooltip string. This is always shown for commands. If the tooltip description and/or tool clip are also specified then the tooltip will progressively display more information as the user hovers the mouse over the control. |
| [tooltipDescription](FloatSpinnerCommandInput_tooltipDescription.md) | Gets or sets additional text to display progressively along with the tooltip. The text for the description can contain some basic HTML formatting tags to format the tags. For example the br tag can be used to create multiple paragraphs. The tooltip is always shown but as the user hovers over the control it will progressively display the tool clip and description text. |
| [unitType](FloatSpinnerCommandInput_unitType.md) | Gets the unit type that is used when evaluating the user's input. |
| [value](FloatSpinnerCommandInput_value.md) | Gets and sets the value associated with this input. The value is always in the database units of the unit type specified. For example, if the unit type is "inch" this value is in centimeters since centimeters are the database length unit. When setting the value it is converted into a string using the unit type and displayed in the input box. The isValidExpression property should be checked before using this value within the command because if the expression can't be evaluated there isn't a valid value. Fusion won't allow the execution of a command that contains ValueCommandInput object with invalid expressions so you can dependably use the value in the execute event of the command. |

## Accessed From

[CommandInputs.addFloatSpinnerCommandInput](CommandInputs_addFloatSpinnerCommandInput.md)

## Version

Introduced in version July 2015  

