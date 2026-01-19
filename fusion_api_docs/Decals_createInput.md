# Decals.createInput Method

Parent Object: [Decals](Decals.md)  

## Description

Creates a new DecalInput object. A DecalInput object is the logical equivalent to the Decal command dialog by providing access to all the decal options. Passing in the DecalInput object to the add method is the equivalent of clicking the OK button on the dialog to create the decal.

## Syntax

"decals_var" is a variable referencing a [Decals](Decals.md) object.

```python
returnValue = decals_var.createInput(imageFilename, faces, point)
```

## Return Value

| Type | Description |
|----|----|
| [DecalInput](DecalInput.md) | Returns a DecalInput object or null in the case of failure. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| imageFilename | string | The full filename to the image to use for the decal. PNG, JPEG, and TIFF files are supported. |
| faces | BRepFace[] | Specifies the faces the decal will be associated with. Typically, this will be an array containing a single face. If the isChainFaces property on the input is true, only a single face is needed, and the rest of the faces in the body will automatically be used. If the isChainFaces property is false, this defines a subset of faces in the body to which the decal will be applied. If multiple faces are provided, the first face in the array is used to position and orient the decal. The position and orientation are relative to the first face. Any additional faces should connect directly or indirectly through other connected faces to the first face. |
| point | [Point3D](Point3D.md) | Specifies a point on the first face that defines the center position of the decal. |

## Version

Introduced in version September 2024  

