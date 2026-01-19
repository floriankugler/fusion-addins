# Vector2D.create Method

Parent Object: [Vector2D](Vector2D.md)  

## Description

Creates a 2D vector object.

## Syntax

This is a static method.  

```python

# Uses no optional arguments.
returnValue = adsk.core.Vector2D.create()

# Uses optional arguments.
returnValue = adsk.core.Vector2D.create(x, y)
```

## Return Value

| Type | Description |
|----|----|
| [Vector2D](Vector2D.md) | Returns the new Vector2D object or null if the creation failed. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| x | double | The x coordinate of the vector. This is an optional argument whose default value is 0.0. |
| y | double | The y coordinate of the vector. This is an optional argument whose default value is 0.0. |

## Version

Introduced in version August 2014  

