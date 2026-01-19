# BRepBody.opacity Property

Parent Object: [BRepBody](BRepBody.md)  

## Description

Gets and sets the opacity override assigned to this body. A value of 1.0 specifies that is it completely opaque and a value of 0.0 specifies that is it completely transparent.  

This value is not necessarily related to what the user sees because the opacity is inherited. For example, if you this body is in a component and that component's opacity is set to something other than 1.0, the body will also be shown as slightly transparent even though the opacity property for the body will return 1.0. Because the component that contains the body can be referenced as an occurrence in other components and they can have different opacity settings, it's possible that different instances of the same body can display using different opacity levels. To get the opacity that it is being displayed with use the BrepBody.visibleOpacity property.  

This is the API equivalent of the "Opacity Control" command available for the body in the browser.

## Syntax

"bRepBody_var" is a variable referencing a BRepBody object.  

```python
# Get the value of the property.
propertyValue = bRepBody_var.opacity

# Set the value of the property.
bRepBody_var.opacity = propertyValue
```

## Property Value

This is a read/write property whose value is a double.

## Version

Introduced in version August 2017  

