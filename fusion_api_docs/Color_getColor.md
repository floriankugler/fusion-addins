# Color.getColor Method

Parent Object: [Color](Color.md)  

## Description

Gets all of the information defining this color.

## Syntax

"color_var" is a variable referencing a [Color](Color.md) object.  

```python
(returnValue, red, green, blue, opacity) = color_var.getColor()
```

## Return Value

| Type    | Description                                                   |
|---------|---------------------------------------------------------------|
| boolean | Returns true if getting the color information was successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| red | short | The red component of the color. The value can be 0 to 255. |
| green | short | The green component of the color. The value can be 0 to 255. |
| blue | short | The blue component of the color. The value can be 0 to 255. |
| opacity | short | The opacity of the color. The value can be 0 to 255. A value of 255 indicates it is completely opaque. |

## Version

Introduced in version August 2014  

