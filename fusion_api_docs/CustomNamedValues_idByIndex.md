# CustomNamedValues.idByIndex Method

Parent Object: [CustomNamedValues](CustomNamedValues.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Function that returns the name of a value specified by its index.

## Syntax

"customNamedValues_var" is a variable referencing a [CustomNamedValues](CustomNamedValues.md) object.

```python
returnValue = customNamedValues_var.idByIndex(index)
```

## Return Value

| Type | Description |
|----|----|
| string | Returns the ID of the specified item or asserts if an out of bounds index is used. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the item within the collection to return the name of. The first item in the collection has an index of 0 and the last item is the count of this collection minus 1. |

## Version

Introduced in version July 2021  

