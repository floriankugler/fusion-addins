# RenderEnvironments.itemById Method

Parent Object: [RenderEnvironments](RenderEnvironments.md)  

## Description

Returns the render environment with the specified ID.

## Syntax

"renderEnvironments_var" is a variable referencing a [RenderEnvironments](RenderEnvironments.md) object.

```python
returnValue = renderEnvironments_var.itemById(id)
```

## Return Value

| Type | Description |
|----|----|
| [RenderEnvironment](RenderEnvironment.md) | Returns the specified render environment or null if the ID does not match a render environment. |

## Parameters

| Name | Type   | Description                                 |
|------|--------|---------------------------------------------|
| id   | string | The ID of the render environment to return. |

## Version

Introduced in version May 2023  

