# Joint.nativeObject Property

Parent Object: [Joint](Joint.md)  

## Description

The NativeObject is the object outside the context of an assembly and in the context of it's parent component. Returns null in the case where this object is not in the context of an assembly but is already the native object.

## Syntax

"joint_var" is a variable referencing a Joint object.  

```python
# Get the value of the property.
propertyValue = joint_var.nativeObject
```

## Property Value

This is a read only property whose value is a [Joint](Joint.md).

## Version

Introduced in version July 2015  

