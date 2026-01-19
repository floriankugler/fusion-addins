# MeshBody.copyToComponent Method

Parent Object: [MeshBody](MeshBody.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Creates a copy of this mesh body into the specified target.

## Syntax

"meshBody_var" is a variable referencing a [MeshBody](MeshBody.md) object.

```python
returnValue = meshBody_var.copyToComponent(target)
```

## Return Value

| Type | Description |
|----|----|
| [MeshBody](MeshBody.md) | Returns the moved mesh body or null in the case the move failed. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| target | [Base](Base.md) | The target can be either the root component or an occurrence. In the case where an occurrence is specified, the mesh body will be copied into the parent component of the target occurrence and the target occurrence defines the transform of how the mesh body will be copied so that the body maintains it's same position with respect to the assembly. |

## Version

Introduced in version July 2025  

