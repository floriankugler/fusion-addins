# ToolingCapabilitiesMachineElement.staticTypeId Method

Parent Object: [ToolingCapabilitiesMachineElement](ToolingCapabilitiesMachineElement.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Identifying name for all elements of this type. Pass this to the itemByType or itemById methods of MachineElements to filter to elements of this type.

## Syntax

This is a static method.  

```python

returnValue = adsk.cam.ToolingCapabilitiesMachineElement.staticTypeId()
```

## Return Value

| Type   | Description                      |
|--------|----------------------------------|
| string | Returns identifier of this type. |

## Version

Introduced in version September 2025  

