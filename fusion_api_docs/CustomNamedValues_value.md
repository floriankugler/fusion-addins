# CustomNamedValues.value Method

Parent Object: [CustomNamedValues](CustomNamedValues.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Function that returns the specified value given its ID.

## Syntax

"customNamedValues_var" is a variable referencing a [CustomNamedValues](CustomNamedValues.md) object.

```python
returnValue = customNamedValues_var.value(id)
```

## Return Value

| Type | Description |
|----|----|
| string | Returns the value or an empty string if the specified ID was not found. |

## Parameters

| Name | Type | Description |
|----|----|----|
| id | string | The ID of the value, which was assigned when the value was created. |

## Version

Introduced in version July 2021  

