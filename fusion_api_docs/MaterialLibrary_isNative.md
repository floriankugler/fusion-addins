# MaterialLibrary.isNative Property

Parent Object: [MaterialLibrary](MaterialLibrary.md)  

## Description

Gets if this is a native material library. Native libraries are those that are delivered with Fusion and are always available. And non-native libraries are user created. If This returns True then there are some limitations to what can be done with the library. For example, if this is a native material library it cannot be unloaded.

## Syntax

"materialLibrary_var" is a variable referencing a MaterialLibrary object.  

```python
# Get the value of the property.
propertyValue = materialLibrary_var.isNative
```

## Property Value

This is a read only property whose value is a boolean.

## Version

Introduced in version March 2017  

