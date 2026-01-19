# Component.opacity Property

Parent Object: [Component](Component.md)  

## Description

Gets and sets the opacity override assigned to this component. A value of 1.0 specifies that is it completely opaque and a value of 0.0 specifies that is it completely transparent.  

This is only applicable for a non-root local component.  

This value is not necessarily related to what the user sees because the opacity is inherited. For example, if you have TopComponent and it has a component in it called SubComponent and you set the opacity of TopComponent to be 0.5, SubComponent will also be shown as slightly transparent even though the opacity property for it will return 1.0. Because a component can be referenced as an occurrence in other components and they can have different opacity settings, it's possible that different instances of the same component can display using different opacity levels. To get the opacity that it is being displayed with use the Occurrence.visibleOpacity property.

## Syntax

"component_var" is a variable referencing a Component object.  

```python
# Get the value of the property.
propertyValue = component_var.opacity

# Set the value of the property.
component_var.opacity = propertyValue
```

## Property Value

This is a read/write property whose value is a double.

## Version

Introduced in version January 2017  

