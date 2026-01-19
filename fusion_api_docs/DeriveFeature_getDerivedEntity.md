# DeriveFeature.getDerivedEntity Method

Parent Object: [DeriveFeature](DeriveFeature.md)  

## Description

Method that returns the derived entity for a source entity.

## Syntax

"deriveFeature_var" is a variable referencing a [DeriveFeature](DeriveFeature.md) object.

```python
returnValue = deriveFeature_var.getDerivedEntity(sourceEntity)
```

## Return Value

| Type | Description |
|----|----|
| [Base](Base.md) | Returns the derived entity for the source entity or null if it failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| sourceEntity | [Base](Base.md) | Input an entity (e.g. a BRepBody, MeshBody, Sketch, SketchEntity, ConstructionPlane, Occurrence, Canvas etc.) from the sourceDesign that is derived by this DeriveFeature. |

## Version

Introduced in version January 2026  

