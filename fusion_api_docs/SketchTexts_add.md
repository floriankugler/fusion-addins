# SketchTexts.add Method

Parent Object: [SketchTexts](SketchTexts.md)  

## Description

Creates a sketch text.

## Syntax

"sketchTexts_var" is a variable referencing a [SketchTexts](SketchTexts.md) object.

```python
returnValue = sketchTexts_var.add(input)
```

## Return Value

| Type | Description |
|----|----|
| [SketchText](SketchText.md) | Returns the newly created SketchText object or null in the case of failure. |

## Parameters

| Name | Type | Description |
|----|----|----|
| input | [SketchTextInput](SketchTextInput.md) | A SketchTextInput object created using the SketchTexts.createInput method. |

## Samples

| Name | Description |
|----|----|
| [SketchTextInput.setAsAlongPath](SketchTextinput_setAsAlongPath_Sample.md) | Demonstrates the SketchTextInput.setAsAlongPath method. |
| [SketchTextInput.setAsFitOnPath](SketchTextInput_setAsFitOnPath_Sample.md) | Demoonstrates the SketchTextInput.setAsFitOnPath method. |
| [SketchTextInput.setAsMultiLine](SketchTextInput_setAsMultiLine_Sample.md) | Demonstrates the SketchTextInput.setAsMultiLine method. |
| [Sketch Text API Sample](SketchTextSample_Sample.md) | Demonstrates creating sketch text by creating both mult-line text and text along a curve. |

## Version

Introduced in version March 2015  

