# NamedView.camera Property

Parent Object: [NamedView](NamedView.md)  

## Description

Gets and sets the camera associated with this named view. This property acts as read-only for the four standard named views. This can be determined by checking to see if the isBuiltIn property is true.

## Syntax

"namedView_var" is a variable referencing a NamedView object.  

```python
# Get the value of the property.
propertyValue = namedView_var.camera

# Set the value of the property.
namedView_var.camera = propertyValue
```

## Property Value

This is a read/write property whose value is a [Camera](Camera.md).

## Version

Introduced in version September 2023  

