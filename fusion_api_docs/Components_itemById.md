# Components.itemById Method

Parent Object: [Components](Components.md)  

## Description

Returns the Component that has the specified ID.

## Syntax

"components_var" is a variable referencing a [Components](Components.md) object.

```python
returnValue = components_var.itemById(id)
```

## Return Value

| Type | Description |
|----|----|
| [Component](Component.md) | Returns the specified Component or null in the case where there isn't a Component with the specified ID in this Design. |

## Parameters

| Name | Type | Description |
|----|----|----|
| id | string | The ID of the Component to get. This is the same id used by PIM (Product Information Model). |

## Version

Introduced in version December 2020  

