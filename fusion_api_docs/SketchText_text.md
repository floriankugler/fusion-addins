# SketchText.text Property

Parent Object: [SketchText](SketchText.md)  

## Description

This function is retired. See more information in the 'Remarks' section below.  

This property has been retired and you should now use the textValue and expression properties of the Parameter object associated with this SketchText, which you can obtain by using the SketchText.textParameter property.

## Remarks

Gets and sets the text. This is a simple string and ignores any formatting defined within the text.

## Syntax

"sketchText_var" is a variable referencing a SketchText object.  

```python
# Get the value of the property.
propertyValue = sketchText_var.text

# Set the value of the property.
sketchText_var.text = propertyValue
```

## Property Value

This is a read/write property whose value is a string.

## Version

Introduced in version March 2015  
Retired in version November 2025  

