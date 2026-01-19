# MeshBody.createComponent Method

Parent Object: [MeshBody](MeshBody.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Creates a new component and occurrence within the component that currently owns this body. This body is moved into the new component and returned. The newly created component can be obtained by using the parentComponent property of the MeshBody object.

## Syntax

"meshBody_var" is a variable referencing a [MeshBody](MeshBody.md) object.

```python
returnValue = meshBody_var.createComponent()
```

## Return Value

| Type | Description |
|----|----|
| [MeshBody](MeshBody.md) | Returns the MeshBody in the new component or null in the case the creation failed. |

## Version

Introduced in version January 2024  

