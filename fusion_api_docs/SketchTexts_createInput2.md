# SketchTexts.createInput2 Method

Parent Object: [SketchTexts](SketchTexts.md)  

## Description

This function is retired. See more information in the 'Remarks' section below.  

This method has been retired and replaced by createInput3. Use the new method to define text using an expression that can combine literal text with parameter values.

## Remarks

Creates a SketchTextInput object that is used to define the additional input to create text. The SketchTextInput object is equivalent to the Sketch Text dialog in that it collects all of the input required to create sketch text. You must call setAsFitOnPath, setAsAlongPath, or setAsMultiLine methods to define one of the three types of text. Once the properties of the SketchTextInput object have been defined, pass the SketchTextInput to the add method to create the sketch text.

## Syntax

"sketchTexts_var" is a variable referencing a [SketchTexts](SketchTexts.md) object.

```python
returnValue = sketchTexts_var.createInput2(formattedText, height)
```

## Return Value

| Type | Description |
|----|----|
| [SketchTextInput](SketchTextInput.md) | Returns a SketchTextInput object that can be used to set additional formatting and is used as input to the add method. |

## Parameters

| Name | Type | Description |
|----|----|----|
| formattedText | string | The text used for the sketch text. This is the equivalent of the text that would be entered into the "Text" command dialog. It can be a simple string or it can be an expression that combines text with parameter values. In the case of a simple string, no quotes are needed, but for an expression, text should be quoted using a single quote. |
| height | double | The height of the text in centimeters. |

## Samples

| Name | Description |
|----|----|
| [SketchTextInput.setAsAlongPath](SketchTextinput_setAsAlongPath_Sample.md) | Demonstrates the SketchTextInput.setAsAlongPath method. |
| [SketchTextInput.setAsFitOnPath](SketchTextInput_setAsFitOnPath_Sample.md) | Demoonstrates the SketchTextInput.setAsFitOnPath method. |
| [SketchTextInput.setAsMultiLine](SketchTextInput_setAsMultiLine_Sample.md) | Demonstrates the SketchTextInput.setAsMultiLine method. |
| [Sketch Text API Sample](SketchTextSample_Sample.md) | Demonstrates creating sketch text by creating both mult-line text and text along a curve. |

## Version

Introduced in version December 2020  
Retired in version November 2025  

