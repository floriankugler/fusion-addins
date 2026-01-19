# MeshBody.cut Method

Parent Object: [MeshBody](MeshBody.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Cuts the mesh body to the clipboard.

## Syntax

"meshBody_var" is a variable referencing a [MeshBody](MeshBody.md) object.

```python
returnValue = meshBody_var.cut()
```

## Return Value

| Type    | Description                             |
|---------|-----------------------------------------|
| boolean | Returns true if the cut was successful. |

## Version

Introduced in version July 2025  

