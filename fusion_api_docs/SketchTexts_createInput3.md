# SketchTexts.createInput3 Method

Parent Object: [SketchTexts](SketchTexts.md)  

## Description

Creates a SketchTextInput object that is used to define the additional input to create text. The SketchTextInput object is equivalent to the Sketch Text dialog in that it collects all of the input required to create sketch text. You must call setAsFitOnPath, setAsAlongPath, or setAsMultiLine methods to define one of the three types of text. Once the properties of the SketchTextInput object have been defined, pass the SketchTextInput to the add method to create the sketch text.

## Syntax

"sketchTexts_var" is a variable referencing a [SketchTexts](SketchTexts.md) object.

```python
returnValue = sketchTexts_var.createInput3(expression, height)
```

## Return Value

| Type | Description |
|----|----|
| [SketchTextInput](SketchTextInput.md) | Returns a SketchTextInput object that can be used to set additional formatting and is used as input to the add method. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| expression | string | This defines the expression of the parameter that will be created when this SketchText is created. It can be a simple string or it can be an expression that combines text with parameter values. Simple text must be enclosed within single quotes, the same as it is required in the TEXT command dialog. An example of a valid expression is: "'Length: ' + lengthParam" and will result in "Length: 3.0 mm". The expression result can be obtained by using the text property on the created SketchTextInput object. |
| height | [ValueInput](ValueInput.md) | A ValueInput that defines the height of the text. This value is used to create a parameter that will control the height of the text. It can be a value where it defines the height of the text in centimeters, or it can be a string where it defines the equation of the parameter and must evaluate to a valid length. |

## Version

Introduced in version November 2025  

