# FlatPatternComponent.assemblyConstraints Property

Parent Object: [FlatPatternComponent](FlatPatternComponent.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Returns the collection of assembly constraints associated with this component.

## Syntax

"flatPatternComponent_var" is a variable referencing a FlatPatternComponent object.  

```python
# Get the value of the property.
propertyValue = flatPatternComponent_var.assemblyConstraints
```

## Property Value

This is a read only property whose value is an [AssemblyConstraints](AssemblyConstraints.md).

## Version

Introduced in version July 2025  

