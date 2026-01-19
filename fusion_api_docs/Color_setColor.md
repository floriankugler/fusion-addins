# Color.setColor Method

Parent Object: [Color](Color.md)  

## Description

Sets all of the color information.

## Syntax

"color_var" is a variable referencing a [Color](Color.md) object.

```python
returnValue = color_var.setColor(red, green, blue, opacity)
```

## Return Value

| Type    | Description                                                   |
|---------|---------------------------------------------------------------|
| boolean | Returns true if setting the color information was successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| red | short | The red component of the color. The value can be 0 to 255. |
| green | short | The green component of the color. The value can be 0 to 255. |
| blue | short | The blue component of the color. The value can be 0 to 255. |
| opacity | short | The opacity of the color. The value can be 0 to 255. A value of 255 indicates it is completely opaque. Depending on where the color is used, the opacity value may be ignored. |

## Version

Introduced in version August 2014  

