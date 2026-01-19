# DeriveFeatureInput.sourceEntities Property

Parent Object: [DeriveFeatureInput](DeriveFeatureInput.md)  

## Description

The array of entities that will be derived. These can be any entity that is supported by derive. For example, BRepBody, MeshBody, Sketch, ConstructionPlane, Occurrence, Component(rootComponent), FlatPattern, Canvas etc.

## Syntax

"deriveFeatureInput_var" is a variable referencing a DeriveFeatureInput object.  

```python
# Get the value of the property.
propertyValue = deriveFeatureInput_var.sourceEntities

# Set the value of the property.
deriveFeatureInput_var.sourceEntities = propertyValue
```

## Property Value

This is a read/write property whose value is an array of type [Base](Base.md).

## Version

Introduced in version January 2026  

