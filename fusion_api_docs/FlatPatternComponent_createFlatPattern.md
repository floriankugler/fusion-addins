# FlatPatternComponent.createFlatPattern Method

Parent Object: [FlatPatternComponent](FlatPatternComponent.md)  

## Description

Creates a flat pattern of the sheet metal folded body. The isSheetMetal property of the BRepBody object can be used to determine if a particular body can be flattened. Creating a flat pattern will fail if a flat pattern already exists in the component. You can determine if a flat pattern already exists by checking if the flatPattern property returns a FlatPattern object or null.

## Syntax

"flatPatternComponent_var" is a variable referencing a [FlatPatternComponent](FlatPatternComponent.md) object.

```python
returnValue = flatPatternComponent_var.createFlatPattern(stationaryFace)
```

## Return Value

| Type                           | Description                             |
|--------------------------------|-----------------------------------------|
| [FlatPattern](FlatPattern.md) | Returns the newly created flat pattern. |

## Parameters

| Name | Type | Description |
|----|----|----|
| stationaryFace | [BRepFace](BRepFace.md) | A planar face in the sheet metal body that is on the top or bottom of the part and not an edge face. This face will be positioned on the X-Y plane of the flat pattern and the rest of the model will be flattened relative to this face. The face must exist on a body that is owned by this component. |

## Version

Introduced in version October 2022  

