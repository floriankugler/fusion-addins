# Curve3DPath.item Method

Parent Object: [Curve3DPath](Curve3DPath.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Returns the Curve3D at the specified index from this collection of Curve3D objects.

## Syntax

"curve3DPath_var" is a variable referencing a [Curve3DPath](Curve3DPath.md) object.

```python
returnValue = curve3DPath_var.item(index)
```

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the Curve3D within this Curve3D collection to return. The first Curve3D in this collection has an index of 0. |

## Version

Introduced in version September 2023  

