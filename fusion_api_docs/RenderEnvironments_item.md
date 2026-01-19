# RenderEnvironments.item Method

Parent Object: [RenderEnvironments](RenderEnvironments.md)  

## Description

Method that returns the specified render environment using an index into the collection.

## Syntax

"renderEnvironments_var" is a variable referencing a [RenderEnvironments](RenderEnvironments.md) object.

```python
returnValue = renderEnvironments_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [RenderEnvironment](RenderEnvironment.md) | Returns the specified render environment or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | integer | The index of the item within the collection. The first item has an index of 0. |

## Version

Introduced in version May 2023  

