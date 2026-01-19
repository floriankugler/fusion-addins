# ArrangeComponent.occurrence Property

Parent Object: [ArrangeComponent](ArrangeComponent.md)  

## Description

Returns the Occurrence associated with this ArrangeComponent. If an Occurrence was used to define this ArrangeComponent, this will return the same thing as the occurrenceOrFace. If a BRepFace was used to define this ArrangeComponent, this will return the Occurrence the face is in. This is a convenience property to make accessing the occurrence simpler.

## Syntax

"arrangeComponent_var" is a variable referencing an ArrangeComponent object.  

```python
# Get the value of the property.
propertyValue = arrangeComponent_var.occurrence
```

## Property Value

This is a read only property whose value is an [Occurrence](Occurrence.md).

## Version

Introduced in version January 2025  

