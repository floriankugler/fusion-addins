# CustomFeatureParameters.itemById Method

Parent Object: [CustomFeatureParameters](CustomFeatureParameters.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Function that returns the specified CustomParameter object given its ID.

## Syntax

"customFeatureParameters_var" is a variable referencing a [CustomFeatureParameters](CustomFeatureParameters.md) object.

```python
returnValue = customFeatureParameters_var.itemById(id)
```

## Return Value

| Type | Description |
|----|----|
| [CustomFeatureParameter](CustomFeatureParameter.md) | Returns the specified item or null if the specified ID was not found. |

## Parameters

| Name | Type | Description |
|----|----|----|
| id | string | The ID of the custom parameter, which was assigned when the parameter was defined and the custom feature was created. |

## Version

Introduced in version January 2021  

