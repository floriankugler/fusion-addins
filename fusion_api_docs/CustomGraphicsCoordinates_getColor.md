# CustomGraphicsCoordinates.getColor Method

Parent Object: [CustomGraphicsCoordinates](CustomGraphicsCoordinates.md)  

## Description

Gets the color assigned to the coordinate at the specified index.

## Syntax

"customGraphicsCoordinates_var" is a variable referencing a [CustomGraphicsCoordinates](CustomGraphicsCoordinates.md) object.

```python
returnValue = customGraphicsCoordinates_var.getColor(index)
```

## Return Value

| Type | Description |
|----|----|
| [Color](Color.md) | Returns the color associated with the index. Can also return null in the case where there is no color assigned. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | integer | The index of the color to return. The first color has an index of 0. |

## Version

Introduced in version September 2017  

