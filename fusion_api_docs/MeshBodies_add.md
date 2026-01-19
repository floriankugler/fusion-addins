# MeshBodies.add Method

Parent Object: [MeshBodies](MeshBodies.md)  

## Description

Creates a new mesh body by importing an STL, OBJ or 3MF file.  

Because of a current limitation, if you want to create a mesh body in a parametric model, you must first call the edit method of the base or form feature, use this method to create the mesh body, and then call the finishEdit method of the base or form feature. The base or form feature must be in an "edit" state to be able to add any additional items to it.

## Syntax

"meshBodies_var" is a variable referencing a [MeshBodies](MeshBodies.md) object.

```python
# Uses no optional arguments.
returnValue = meshBodies_var.add(fullFilename, units)

# Uses optional arguments.
returnValue = meshBodies_var.add(fullFilename, units, baseOrFormFeature)
```

## Return Value

| Type | Description |
|----|----|
| [MeshBodyList](MeshBodyList.md) | Returns a list of the newly created mesh bodies or null if the creation failed. Multiple bodies can be created in the case where a .obj file that contains multiple bodies was imported. STL files always contain a single body. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| fullFilename | string | The full filename (path and file) of a STL, OBJ or 3MF file. |
| units | [MeshUnits](MeshUnits.md) | The units to use when importing the file. |
| baseOrFormFeature | [Base](Base.md) | The BaseFeature or FormFeature object that this mesh body will be associated with. This is an optional requirement. It is required in a parametric modeling design but is ignored in a direct modeling design. This is an optional argument whose default value is null. |

## Version

Introduced in version August 2014  

