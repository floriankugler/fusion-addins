# Color.create Method

Parent Object: [Color](Color.md)  

## Description

Creates a new color.

## Syntax

This is a static method.  

```python

returnValue = adsk.core.Color.create(red, green, blue, opacity)
```

## Return Value

| Type | Description |
|----|----|
| [Color](Color.md) | Returns the newly created color or null if the creation failed. |

## Parameters

| Name    | Type  | Description                                                  |
|---------|-------|--------------------------------------------------------------|
| red     | short | The red component of the color. The value can be 0 to 255.   |
| green   | short | The green component of the color. The value can be 0 to 255. |
| blue    | short | The blue component of the color. The value can be 0 to 255.  |
| opacity | short | The opacity of the color. The value can be 0 to 255.         |

## Version

Introduced in version August 2014  

