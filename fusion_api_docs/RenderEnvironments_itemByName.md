# RenderEnvironments.itemByName Method

Parent Object: [RenderEnvironments](RenderEnvironments.md)  

## Description

Returns the specified render environment using the name as seen in the user interface.

## Syntax

"renderEnvironments_var" is a variable referencing a [RenderEnvironments](RenderEnvironments.md) object.

```python
returnValue = renderEnvironments_var.itemByName(name)
```

## Return Value

| Type | Description |
|----|----|
| [RenderEnvironment](RenderEnvironment.md) | Returns the specified render environment or null if there's no match on the name. |

## Parameters

| Name | Type   | Description                                   |
|------|--------|-----------------------------------------------|
| name | string | The name of the render environment to return. |

## Version

Introduced in version May 2023  

