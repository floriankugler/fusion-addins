# Component.allAssemblyConstraints Property

Parent Object: [Component](Component.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Returns all assembly constraints in this component and any sub components. The assembly constraints returned are all in the context of this component so any joints in sub components will be proxies. This is primarily useful when used from the root component because Fusion flattens the assembly structure, including joints, when manipulating an assembly.

## Syntax

"component_var" is a variable referencing a Component object.  

```python
# Get the value of the property.
propertyValue = component_var.allAssemblyConstraints
```

## Property Value

This is a read only property whose value is an array of type [AssemblyConstraint](AssemblyConstraint.md).

## Version

Introduced in version July 2025  

