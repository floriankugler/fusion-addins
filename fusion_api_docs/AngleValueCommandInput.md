# AngleValueCommandInput Object

Derived from: [CommandInput](CommandInput.md) Object  

## Description

Represents a command input that gets an angle from the user. This displays an entry in the command dialog where the user can enter a value and also displays a manipulator in the graphics window to allow them to graphically set the value. The input box is displayed in the dialog when the isVisible property of the command input is true. The manipulator is displayed in the graphics when both the isVisible and isEnabled properties are true.

## Methods

| Name | Description |
|----|----|
| [classType](AngleValueCommandInput_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [deleteMe](AngleValueCommandInput_deleteMe.md) | Deletes this Command input. |
| [setManipulator](AngleValueCommandInput_setManipulator.md) | Defines the position and orientation of the manipulator. The manipulator is only visible when both the isVisible and isEnabled properties are true. If those properties are true and the setManipulator has not been called, the manipulator will be displayed in a default location (0,0,0) using default directions; x direction (1,0,0) and y direction (0,1,0). Because of that the input is typically set to be invisible and/or disabled and then enabled once enough input has been specified that you can display the manipulator in the desired location. |

## Properties

| Name | Description |
| --- | --- |
| [commandInputs](AngleValueCommandInput_commandInputs.md) | Gets the CommandInputs class of the parent, which can be a Command, GroupCommandInput or TabCommandInput. |
| [expression](AngleValueCommandInput_expression.md) | Gets or sets the expression displayed in the input field. This can contain equations and references to parameters but must result in a valid angle expression. If units are not specified as part of the expression, the default user units of degrees are used. |
| [hasMaximumValue](AngleValueCommandInput_hasMaximumValue.md) | Gets and sets if there is a maximum value for this command input. When setting this property, it is only valid to set it to False to remove the maximum value. Setting the maximumValue property will result in this property being set to True. |
| [hasMinimumValue](AngleValueCommandInput_hasMinimumValue.md) | Gets and sets if there is a minimum value for this command input. When setting this property, it is only valid to set it to False to remove the minimum value. Setting the minimumValue property will result in this property being set to True. |
| [id](AngleValueCommandInput_id.md) | Gets the unique identifier for this input in the command's CommandInputs. |
| [isEnabled](AngleValueCommandInput_isEnabled.md) | Gets or sets if this input is currently enabled or disabled for user interaction. Currently, the isEnabled property does not disable SelectionCommandInput objects but instead has the same effect as the SelectionCommandInput.hasFocus property. |
| [isFullWidth](AngleValueCommandInput_isFullWidth.md) | Gets or sets if this input fills the entire width of the dialog. If true, the name is ignored and the input control will fill the entire width of the command dialog. The default value for this property in a new command input if false, or not to fill the width. This property does not apply to GroupCommandInputs or TabCommandInputs. |
| [isMaximumValueInclusive](AngleValueCommandInput_isMaximumValueInclusive.md) | Gets and sets if the value of the input includes the maximum value or is up to the maximum value. For example, if the maximum value is the value of pi (180 degrees) and this property is True, the maximum value can be pi. If this is False, the minimum value must be less than pi. When the maximum value is first defined using the maximumValue property, this property is set to True. The value returned by this property is only meaningful when the hasMaximumValue property returns True. |
| [isMinimumValueInclusive](AngleValueCommandInput_isMinimumValueInclusive.md) | Gets and sets if the value of the input includes the minimum value or is up to the minimum value. For example, if the minimum value is zero and this property is True, the minimum value can be zero. If this is False, the minimum value must be greater than zero. When the minimum value is first defined using the minimumValue property, this property is set to True. The value returned by this property is only meaningful when the hasMinimumValue property returns True. |
| [isValid](AngleValueCommandInput_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [isValidExpression](AngleValueCommandInput_isValidExpression.md) | Returns true if the current expression is valid and can be evaluated. If this is false, the value returned should be ignored because there currently is not a valid value. |
| [isVisible](AngleValueCommandInput_isVisible.md) | Gets or sets if this input will be visible to the user. Setting a SelectionCommandInput to be invisible will clear any selections it currently has. |
| [manipulatorOrigin](AngleValueCommandInput_manipulatorOrigin.md) | Gets the origin point of the manipulator in the model space of the root component. To set the origin use the setManipulator method. |
| [manipulatorXDirection](AngleValueCommandInput_manipulatorXDirection.md) | Gets the X direction of the manipulator in the model space of the root component. The X direction is the 0 angle direction. This direction, along with the Y direction vector define the plane that the manipulator is displayed on. To set the direction use the setManipulator method. |
| [manipulatorYDirection](AngleValueCommandInput_manipulatorYDirection.md) | Gets the Y direction of the manipulator in the model space of the root component. The X and Y direction vectors define the plane that the manipulator is displayed on. To set the direction use the setManipulator method. |
| [maximumValue](AngleValueCommandInput_maximumValue.md) | Gets and sets maximum value, if any, that the value can be. The value is in radians. When getting this property you should first check the hasMaximumValue property to see if this property applies. Also, the isMaximumValueInclusive indicates if the minimum includes this value or will be up to this value. Setting this value will change the isMaximumValueInclusive to True and the hasMaximumValue property to True if hasMaximumValue is currently False, otherwise it will just update the value. |
| [minimumValue](AngleValueCommandInput_minimumValue.md) | Gets and sets minimum value, if any, that the value can be. The value is in radians. When getting this property you should first check the hasMinimumValue property to see if this property applies. Also, the isMinimumValueInclusive indicates if the minimum includes this value or will be up to this value. Setting this value will change the isMinimumValueInclusive to True and the hasMinimumValue property to True if hasMinimumValue is currently False, otherwise it will just update the value. |
| [name](AngleValueCommandInput_name.md) | Gets the user visible name of this input. |
| [objectType](AngleValueCommandInput_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [parentCommand](AngleValueCommandInput_parentCommand.md) | Gets the parent Command. |
| [parentCommandInput](AngleValueCommandInput_parentCommandInput.md) | Gets the parent CommandInput if this commandInput is the child of a TabCommandInput or GroupCommandInput. Returns null if there is no parent. |
| [toolClipFilename](AngleValueCommandInput_toolClipFilename.md) | Gets or sets the full filename of the image file (PNG) used for the tool clip. The tooltip is always shown but as the user hovers over the control it will progressively display the tool clip and description text. |
| [tooltip](AngleValueCommandInput_tooltip.md) | Gets or sets the base tooltip string. This is always shown for commands. If the tooltip description and/or tool clip are also specified then the tooltip will progressively display more information as the user hovers the mouse over the control. |
| [tooltipDescription](AngleValueCommandInput_tooltipDescription.md) | Gets or sets additional text to display progressively along with the tooltip. The text for the description can contain some basic HTML formatting tags to format the tags. For example the br tag can be used to create multiple paragraphs. The tooltip is always shown but as the user hovers over the control it will progressively display the tool clip and description text. |
| [value](AngleValueCommandInput_value.md) | Gets and sets the current value of the command input. The value is in radians but will be displayed to the user in degrees. Setting this value can fail if the input value is not within the minimum and maximum value range. The isValidExpression property should be checked before using the value within the command because if the expression can't be evaluated there isn't a valid value. Fusion won't allow the execution of a command that contains ValueCommandInput object with invalid expressions so you can dependably use the value in the execute event of the command. |

## Accessed From

[CommandInputs.addAngleValueCommandInput](CommandInputs_addAngleValueCommandInput.md)

## Samples

| Name | Description |
| --- | --- |
| [Command Inputs API Sample](CommandInputsSample_Sample.md) | Creates a command dialog that demonstrates all of the available command inputs. To use the sample, create a new Python or C++ script and copy and paste this code, replacing the default code. You also need to unpack this zip file which contains a [resource folder](../ExtraFiles/CommandInputsResources.zip) into the same folder where the source code file (.py or .cpp) is. |

## Version

Introduced in version January 2017  

