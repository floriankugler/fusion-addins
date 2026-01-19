# DeriveFeature.setSourceEntities Method

Parent Object: [DeriveFeature](DeriveFeature.md)  

## Description

Sets the array of entities that are derived. The array of entities that will be derived. You can use the sourceDesign to access various elements within the source Design to add them to the list of elements to derive These can be any entity that is supported by derive. For example, BRepBody, MeshBody, Sketch, ConstructionPlane, Occurrence, Component, FlatPattern, Canvas etc. The array of entities that will be excluded from the sourceEntities. Returns true if successful.

## Syntax

"deriveFeature_var" is a variable referencing a [DeriveFeature](DeriveFeature.md) object.

```python
returnValue = deriveFeature_var.setSourceEntities(entities, excludedEntities)
```

## Parameters

| Name | Type | Description |
|----|----|----|
| entities | Base\[\] | The array of entities that will be derived. You can use the sourceDesign to access various elements within the source Design to add them to the list of elements to derive These can be any entity that is supported by derive. For example, BRepBody, MeshBody, Sketch, ConstructionPlane, Occurrence, Component, FlatPattern, Canvas etc. |
| excludedEntities | Base\[\] | The array of entities that will be excluded from the sourceEntities. |

## Version

Introduced in version January 2026  

