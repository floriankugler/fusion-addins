# TemporaryBRepManager.createSilhouetteCurves Method

Parent Object: [TemporaryBRepManager](TemporaryBRepManager.md)  

## Description

Calculates the silhouette curve geometry for a given face as viewed from a given direction.

## Syntax

"temporaryBRepManager_var" is a variable referencing a [TemporaryBRepManager](TemporaryBRepManager.md) object.

```python
returnValue = temporaryBRepManager_var.createSilhouetteCurves(face, viewDirection, returnCoincidentSilhouettes)
```

## Return Value

| Type | Description |
|----|----|
| [BRepBody](BRepBody.md) | Returns a SurfaceBody object that will contain one or more BRepWire objects that represent the silhouette curve(s). This method can return null in the case where there is not a silhouette curve for the specified face. |

## Parameters

| Name | Type | Description |
|----|----|----|
| face | [BRepFace](BRepFace.md) | Input BRepFace object to calculate the silhouette curve for. |
| viewDirection | [Vector3D](Vector3D.md) | Input Vector3D object that defines the view direction to calculate the silhouette curve relative to. The silhouette curve(s) will lie along the path where the face normal is perpendicular to the view direction. |
| returnCoincidentSilhouettes | boolean | Input Boolean that specifies if silhouette curves that are coincident to the edges of the face should be returned or not. If true, these curves will be returned. |

## Samples

| Name | Description |
|----|----|
| [TemporaryBRepManager API Sample](TemporaryBRepManager_Sample.md) | TemporaryBRepManager related functions |

## Version

Introduced in version December 2017  

