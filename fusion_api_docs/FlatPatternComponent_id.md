# FlatPatternComponent.id Property

Parent Object: [FlatPatternComponent](FlatPatternComponent.md)  

## Description

Returns the persistent ID of the component. This ID is created with the component and does not change. Because this ID does not change, different revisions of the same design or copies of the design asset/file will retain this ID. If components from different designs have the same ID, it indicates they are either different revisions or a copy of the design was made. Therefore, this ID will always be unique within a single design, but may not be unique in an assembly where externally referenced designs include different revisions or copies of a design.  

The ID is also the same ID used by PIM (Product Information Model).

## Syntax

"flatPatternComponent_var" is a variable referencing a FlatPatternComponent object.  

```python
# Get the value of the property.
propertyValue = flatPatternComponent_var.id
```

## Property Value

This is a read only property whose value is a string.

## Version

Introduced in version October 2022  

