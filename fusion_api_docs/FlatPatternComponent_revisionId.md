# FlatPatternComponent.revisionId Property

Parent Object: [FlatPatternComponent](FlatPatternComponent.md)  

## Description

Returns the current revision ID of the component. This ID changes any time the component is modified in any way. By getting and saving the ID when you create any data that is dependent on the component, you can then compare the saved ID with the current ID to determine if the component has changed to know if you should update your data.

## Syntax

"flatPatternComponent_var" is a variable referencing a FlatPatternComponent object.  

```python
# Get the value of the property.
propertyValue = flatPatternComponent_var.revisionId
```

## Property Value

This is a read only property whose value is a string.

## Version

Introduced in version October 2022  

