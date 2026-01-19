# surfaceDeleteFeatures.add

## Description

Demonstrates the surfaceDeleteFeatures.add method.

## Code Samples

| Copy Code |
|----------:|

```python
def demo_surfaceDeleteFaceFeatures_add(rootComp: adsk.fusion.Component):
    face = _ui.selectEntity('Select a face to delete.', 'Faces').entity
    faces = adsk.core.ObjectCollection.create()
    faces.add(face)

    surfaceDeleteFaceFeatures = rootComp.features.surfaceDeleteFaceFeatures
    deleteSurface = surfaceDeleteFaceFeatures.add(faces)
```

