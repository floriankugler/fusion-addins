# Design.activeEditObject Property

Parent Object: [Design](Design.md)  

## Description

Returns the current edit target as seen in the user interface. This edit target is defined as the container object that will be added to if something is created. For example, a component can be an edit target so that when new bodies are created they are added to that component. A sketch can also be an edit target.

## Syntax

"design_var" is a variable referencing a Design object.  

```python
# Get the value of the property.
propertyValue = design_var.activeEditObject
```

## Property Value

This is a read only property whose value is a [Base](Base.md).

## Version

Introduced in version August 2014  

