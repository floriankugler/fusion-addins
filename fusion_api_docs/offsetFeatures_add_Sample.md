# offsetFeatures.add

## Description

Demonstrates the offsetFeatures.add method. This is the equivalent of the Offset command in the SURFACE tab.

## Code Samples

| Copy Code |
|----------:|

```python
def demo_offsetFeatures_add(rootComp: adsk.fusion.Design.rootComponent):
    offsetFace = _ui.selectEntity('Select the face to offset.', 'Faces').entity
    offsetFaces = adsk.core.ObjectCollection.create()
    offsetFaces.add(offsetFace)
    distance = adsk.core.ValueInput.createByReal(2)
    operation = adsk.fusion.FeatureOperations.NewBodyFeatureOperation

    offsetFeatures = rootComp.features.offsetFeatures
    input = offsetFeatures.createInput(offsetFaces, distance, operation)
    offsetFeature = offsetFeatures.add(input)
```

