# BrowserCommandInput.maximumHeight Property

Parent Object: [BrowserCommandInput](BrowserCommandInput.md)  

## Description

Gets and sets the maximum height of the browser within the command dialog, in pixels. As the user resizes the dialog, the area taken up by the browser will shrink and grow to fit within the defined space. It will never shrink to be less than the minimum height or expand to be larger than the maximum height. If the content displayed within the browser does not fit within the current area, a scroll bar will appear to allow the user to scroll to see the entire browser content. The default value of zero sets no maximum height, so the browser will expand to the maximum extent available.

## Syntax

"browserCommandInput_var" is a variable referencing a BrowserCommandInput object.  

```python
# Get the value of the property.
propertyValue = browserCommandInput_var.maximumHeight

# Set the value of the property.
browserCommandInput_var.maximumHeight = propertyValue
```

## Property Value

This is a read/write property whose value is an integer.

## Version

Introduced in version July 2021  

