# Occurrence.visibleOpacity Property

Parent Object: [Occurrence](Occurrence.md)  

## Description

The user can set an override opacity for components and these opacity overrides combine if children and parent components have overrides. This property returns the actual opacity that is being used to render the occurrence. To set the opacity use the opacity property of the Component object.

## Syntax

"occurrence_var" is a variable referencing an Occurrence object.  

```python
# Get the value of the property.
propertyValue = occurrence_var.visibleOpacity
```

## Property Value

This is a read only property whose value is a double.

## Version

Introduced in version January 2017  

