# BRepBody.visibleOpacity Property

Parent Object: [BRepBody](BRepBody.md)  

## Description

The user can set an override opacity for components and bodies these opacity overrides combine if children and parent components have overrides. This property returns the actual opacity that is being used to render the body. To set the opacity use the opacity property of the BRepBody object.

## Syntax

"bRepBody_var" is a variable referencing a BRepBody object.  

```python
# Get the value of the property.
propertyValue = bRepBody_var.visibleOpacity
```

## Property Value

This is a read only property whose value is a double.

## Version

Introduced in version September 2017  

