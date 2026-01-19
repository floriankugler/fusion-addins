# CustomGraphicsBillBoard.billBoardStyle Property

Parent Object: [CustomGraphicsBillBoard](CustomGraphicsBillBoard.md)  

## Description

Specifies the type of billboarding to use. When a new CustomGraphicsBillBoard object is created this defaults to ScreenBillBoardStyle so the graphics will all be facing the view plane. It can also be set to an arbitrary plane by setting this to AxialBillBoardStyle and can be defined so that it never appear backwards by setting it to RightReadingBillBoardStyle.

## Syntax

"customGraphicsBillBoard_var" is a variable referencing a CustomGraphicsBillBoard object.  

```python
# Get the value of the property.
propertyValue = customGraphicsBillBoard_var.billBoardStyle

# Set the value of the property.
customGraphicsBillBoard_var.billBoardStyle = propertyValue
```

## Property Value

This is a read/write property whose value is a [CustomGraphicsBillBoardStyles](CustomGraphicsBillBoardStyles.md).

## Version

Introduced in version September 2017  

