# ShellFeature.nativeObject Property

Parent Object: [ShellFeature](ShellFeature.md)  

## Description

The NativeObject is the object outside the context of an assembly and in the context of its parent component. Returns null in the case where this object is not in the context of an assembly but is already the native object.

## Syntax

"shellFeature_var" is a variable referencing a ShellFeature object.  

```python
# Get the value of the property.
propertyValue = shellFeature_var.nativeObject
```

## Property Value

This is a read only property whose value is a [ShellFeature](ShellFeature.md).

## Version

Introduced in version November 2014  

