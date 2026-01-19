# SketchTextInput.setAsMultiLine

## Description

Demonstrates the SketchTextInput.setAsMultiLine method.

## Code Samples

| Copy Code |
|----------:|

```python
def demo_SketchTextInput_setAsMultiline(sketch: adsk.fusion.Sketch):
    texts = sketch.sketchTexts
    input = texts.createInput2('This is a long line of text that is broken automatically.\n\nAnd this is a defined line break.', 0.5)

    cornerPoint = adsk.core.Point3D.create(0, 0, 0)
    diagonalPoint = adsk.core.Point3D.create(10, 5, 0)
    horizontalAlignment = adsk.core.HorizontalAlignments.LeftHorizontalAlignment
    verticalAlignment = adsk.core.VerticalAlignments.TopVerticalAlignment
    characterSpacing = 0
    
    input.setAsMultiLine(cornerPoint,
                         diagonalPoint,
                         horizontalAlignment,
                         verticalAlignment,
                         characterSpacing)
    texts.add(input)
```

