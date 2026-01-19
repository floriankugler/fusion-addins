# AssemblyConstraint.nativeObject Property

Parent Object: [AssemblyConstraint](AssemblyConstraint.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

The NativeObject is the object outside the context of an assembly and in the context of it's parent component. Returns null in the case where this object is not in the context of an assembly but is already the native object.

## Syntax

"assemblyConstraint_var" is a variable referencing an AssemblyConstraint object.  

```python
# Get the value of the property.
propertyValue = assemblyConstraint_var.nativeObject
```

## Property Value

This is a read only property whose value is an [AssemblyConstraint](AssemblyConstraint.md).

## Version

Introduced in version July 2025  

