# SketchTextInput.setAsMultiLine Method

Parent Object: [SketchTextInput](SketchTextInput.md)  

## Description

Defines the first corner point of the rectangle that will contain the text.

## Syntax

"sketchTextInput_var" is a variable referencing a [SketchTextInput](SketchTextInput.md) object.

```python
returnValue = sketchTextInput_var.setAsMultiLine(cornerPoint, diagonalPoint, horizontalAlignment, verticalAlignment, characterSpacing)
```

## Return Value

| Type    | Description                                                |
|---------|------------------------------------------------------------|
| boolean | Returns true if the setting the definition was successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| cornerPoint | [Base](Base.md) | Specifies the location of one of the corner points of the rectangle that will contain the text. This can be a Point3D object, with a Z component of zero, to define any arbitrary location on the X-Y plane of the sketch or it can be an existing SketchPoint that lies on the sketch X-Y plane. |
| diagonalPoint | [Base](Base.md) | Specifies the location of the diagonal point of the rectangle that will contain the text. This point cannot be aligned vertically or horizontally to the corner point but be a diagonal point to define a rectangle. This can be a Point3D object, with a Z component of zero, to define any arbitrary location on the X-Y plane of the sketch or it can be an existing SketchPoint that lies on the sketch X-Y plane and the sketch point will become the opposing corner point. |
| horizontalAlignment | [HorizontalAlignments](HorizontalAlignments.md) | Specifies the horizontal alignment of the text with respect to the text rectangle. |
| verticalAlignment | [VerticalAlignments](VerticalAlignments.md) | Specifies the vertical alignment of the text with respect to the text rectangle. |
| characterSpacing | double | The spacing between the characters. This is an additional spacing to apply that is defined as a percentage of the default spacing. A spacing of 0 indicates no additional spacing. A spacing of 50 indicates to use the default plus 50% of the default. |

## Samples

| Name | Description |
|----|----|
| [SketchTextInput.setAsMultiLine](SketchTextInput_setAsMultiLine_Sample.md) | Demonstrates the SketchTextInput.setAsMultiLine method. |
| [Sketch Text API Sample](SketchTextSample_Sample.md) | Demonstrates creating sketch text by creating both mult-line text and text along a curve. |

## Version

Introduced in version December 2020  

