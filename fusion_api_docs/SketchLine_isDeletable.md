# SketchLine.isDeletable Property

Parent Object: [SketchLine](SketchLine.md)  

## Description

Indicates if this sketch entity can be deleted. There are cases, especially with sketch points where another entity is dependent on an entity so deleting it is not allowed. For example, you can't delete the center point of circle by itself but deleting the circle will delete the point. The same is true for the end points of a line.

## Syntax

"sketchLine_var" is a variable referencing a SketchLine object.  

```python
# Get the value of the property.
propertyValue = sketchLine_var.isDeletable
```

## Property Value

This is a read only property whose value is a boolean.

## Version

Introduced in version June 2015  

