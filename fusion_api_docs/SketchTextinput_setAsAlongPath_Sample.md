# SketchTextInput.setAsAlongPath

## Description

Demonstrates the SketchTextInput.setAsAlongPath method.

## Code Samples

| Copy Code |
|----------:|

```python
def demo_SketchTextInput_setAsAlongPath(sketch: adsk.fusion.Sketch):
    texts = sketch.sketchTexts
    input = texts.createInput2('Autodesk', 0.5)
    
    path = sketch.sketchCurves.sketchArcs.addByThreePoints(adsk.core.Point3D.create(-10, 0, 0),
                                                          adsk.core.Point3D.create(-5, 3, 0),
                                                          adsk.core.Point3D.create(0, 0, 0))

    horizontalAlignment = adsk.core.HorizontalAlignments.CenterHorizontalAlignment
    characterSpacing = 0
    isAbovePath = False

    input.setAsAlongPath(path, isAbovePath, horizontalAlignment, characterSpacing)
    texts.add(input)
```

