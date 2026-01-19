# SketchTexts.createInput Method

Parent Object: [SketchTexts](SketchTexts.md)  

## Description

This function is retired. See more information in the 'Remarks' section below.  

Creates a SketchTextInput object that can be used to define additional settings when creating sketch text. The SketchTextInput object is equivalent to the Sketch Text dialog in that it collects all of the input required to create sketch text. Once the properties of the SketchTextInput object have been defined, use the add method to create the sketch text.

## Remarks

This method has been retired and is replaced by the createInput2 method, which supports defining multi-line text and text along a curve.

## Syntax

"sketchTexts_var" is a variable referencing a [SketchTexts](SketchTexts.md) object.

```python
returnValue = sketchTexts_var.createInput(formattedText, height, position)
```

## Return Value

| Type | Description |
|----|----|
| [SketchTextInput](SketchTextInput.md) | Returns a SketchTextInput object that can be used to set additional formatting and is used as input to the add method. |

## Parameters

| Name | Type | Description |
|----|----|----|
| formattedText | string | The text used for the sketch text. This is a simple string as no additional formatting is currently supported. |
| height | double | The height of the text in centimeters. |
| position | [Point3D](Point3D.md) | The position of the text on the x-y plane of the sketch. The text must lie on the x-y plane so the Z component of the point is ignored and always treated as zero. |

## Version

Introduced in version March 2015  
Retired in version January 2021  

