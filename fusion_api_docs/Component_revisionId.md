# Component.revisionId Property

Parent Object: [Component](Component.md)  

## Description

Returns the current revision ID of the component. This ID changes any time the component is modified in any way. By getting and saving the ID when you create any data that is dependent on the component, you can then compare the saved ID with the current ID to determine if the component has changed to know if you should update your data.

## Syntax

"component_var" is a variable referencing a Component object.  

```python
# Get the value of the property.
propertyValue = component_var.revisionId
```

## Property Value

This is a read only property whose value is a string.

## Samples

| Name | Description |
|----|----|
| [Component Sample](ComponentSample_Sample.md) | Component related functions |

## Version

Introduced in version September 2017  

