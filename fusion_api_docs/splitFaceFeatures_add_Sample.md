# splitFaceFeatures.add

## Description

Demonstrates the splitFaceFeatures.add method by spliting a face with another intersecting face.

## Code Samples

| Copy Code |
|----------:|

```python
def demo_splitFaceFeatures_add(rootComp: adsk.fusion.Component):
    selection = _ui.selectEntity('Select a face', 'Faces').entity
    faces = adsk.core.ObjectCollection.create()
    faces.add(selection)
    splittingTool = _ui.selectEntity('Select a face', 'Faces').entity
    isExtended = True

    splitFaceFeatures = rootComp.features.splitFaceFeatures
    input = splitFaceFeatures.createInput(faces, splittingTool, isExtended)
    splitFaceFeature = splitFaceFeatures.add(input)
```

