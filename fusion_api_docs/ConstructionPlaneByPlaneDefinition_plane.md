# ConstructionPlaneByPlaneDefinition.plane Property

Parent Object: [ConstructionPlaneByPlaneDefinition](ConstructionPlaneByPlaneDefinition.md)  

## Description

Gets and sets the position of the construction plane. Setting this property is only valid for a construction plane in a direct edit design or in a base feature. Construction planes in a parametric model are parametrically controlled and cannot be directly edited.

## Syntax

"constructionPlaneByPlaneDefinition_var" is a variable referencing a ConstructionPlaneByPlaneDefinition object.  

```python
# Get the value of the property.
propertyValue = constructionPlaneByPlaneDefinition_var.plane

# Set the value of the property.
constructionPlaneByPlaneDefinition_var.plane = propertyValue
```

## Property Value

This is a read/write property whose value is a [Plane](Plane.md).

## Version

Introduced in version August 2014  

