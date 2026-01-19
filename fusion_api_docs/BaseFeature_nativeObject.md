# BaseFeature.nativeObject Property

Parent Object: [BaseFeature](BaseFeature.md)  

## Description

The NativeObject is the object outside the context of an assembly and in the context of its parent component. Returns null in the case where this object is not in the context of an assembly but is already the native object.

## Syntax

"baseFeature_var" is a variable referencing a BaseFeature object.  

```python
# Get the value of the property.
propertyValue = baseFeature_var.nativeObject
```

## Property Value

This is a read only property whose value is a [BaseFeature](BaseFeature.md).

## Version

Introduced in version January 2021  

