# Sketch.isVisible Property

Parent Object: [Sketch](Sketch.md)  

## Description

Gets if this sketch is currently visible in the graphics window. Use the isLightBulbOn to change if the light bulb beside the sketch node in the browser is on or not. Parent nodes in the browser can have their light bulb off which affects all of their children. This property indicates the final result and whether this body is actually visible or not.

## Syntax

"sketch_var" is a variable referencing a Sketch object.  

```python
# Get the value of the property.
propertyValue = sketch_var.isVisible

# Set the value of the property.
sketch_var.isVisible = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version August 2014  

