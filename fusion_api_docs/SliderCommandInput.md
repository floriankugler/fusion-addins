# SliderCommandInput Object

Derived from: [CommandInput](CommandInput.md) Object  

## Description

Provides a command input to get the value of a slider from the user.

## Methods

| Name | Description |
|----|----|
| [classType](SliderCommandInput_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [deleteMe](SliderCommandInput_deleteMe.md) | Deletes this Command input. |
| [getText](SliderCommandInput_getText.md) | Gets the texts of the slider if text has been defined. |
| [setText](SliderCommandInput_setText.md) | Sets the text of the slider. Both the left and the right text should be set. |

## Properties

| Name | Description |
| --- | --- |
| [commandInputs](SliderCommandInput_commandInputs.md) | Gets the CommandInputs class of the parent, which can be a Command, GroupCommandInput or TabCommandInput. |
| [expressionOne](SliderCommandInput_expressionOne.md) | Uses an expression to set the value in the first input field. This can contain equations and is evaluated using the specified unit type. |
| [expressionTwo](SliderCommandInput_expressionTwo.md) | Uses an expression to set the value in the second input field. This can contain equations and is evaluated using the specified unit type. This property is only available when the hasTwoSliders property returns true. |
| [hasTwoSliders](SliderCommandInput_hasTwoSliders.md) | Gets if the command input has two sliders. |
| [id](SliderCommandInput_id.md) | Gets the unique identifier for this input in the command's CommandInputs. |
| [isEnabled](SliderCommandInput_isEnabled.md) | Gets or sets if this input is currently enabled or disabled for user interaction. Currently, the isEnabled property does not disable SelectionCommandInput objects but instead has the same effect as the SelectionCommandInput.hasFocus property. |
| [isFullWidth](SliderCommandInput_isFullWidth.md) | Gets or sets if this input fills the entire width of the dialog. If true, the name is ignored and the input control will fill the entire width of the command dialog. The default value for this property in a new command input if false, or not to fill the width. This property does not apply to GroupCommandInputs or TabCommandInputs. |
| [isValid](SliderCommandInput_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [isVisible](SliderCommandInput_isVisible.md) | Gets or sets if this input will be visible to the user. Setting a SelectionCommandInput to be invisible will clear any selections it currently has. |
| [name](SliderCommandInput_name.md) | Gets the user visible name of this input. |
| [objectType](SliderCommandInput_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [parentCommand](SliderCommandInput_parentCommand.md) | Gets the parent Command. |
| [parentCommandInput](SliderCommandInput_parentCommandInput.md) | Gets the parent CommandInput if this commandInput is the child of a TabCommandInput or GroupCommandInput. Returns null if there is no parent. |
| [toolClipFilename](SliderCommandInput_toolClipFilename.md) | Gets or sets the full filename of the image file (PNG) used for the tool clip. The tooltip is always shown but as the user hovers over the control it will progressively display the tool clip and description text. |
| [tooltip](SliderCommandInput_tooltip.md) | Gets or sets the base tooltip string. This is always shown for commands. If the tooltip description and/or tool clip are also specified then the tooltip will progressively display more information as the user hovers the mouse over the control. |
| [tooltipDescription](SliderCommandInput_tooltipDescription.md) | Gets or sets additional text to display progressively along with the tooltip. The text for the description can contain some basic HTML formatting tags to format the tags. For example the br tag can be used to create multiple paragraphs. The tooltip is always shown but as the user hovers over the control it will progressively display the tool clip and description text. |
| [unitType](SliderCommandInput_unitType.md) | Gets and sets the unit type that is used when evaluating the user's input. |

## Derived Classes

[FloatSliderCommandInput](FloatSliderCommandInput.md), [IntegerSliderCommandInput](IntegerSliderCommandInput.md)

## Version

Introduced in version June 2015  

