# Appearance.usedBy Property

Parent Object: [Appearance](Appearance.md)  

## Description

Returns a collection of the entities currently using this appearance. This property is only valid for an appearance in a Design and where the IsUsed property returns true. The collection returned can contain

## Syntax

"appearance_var" is a variable referencing an Appearance object.  

```python
# Get the value of the property.
propertyValue = appearance_var.usedBy
```

## Property Value

This is a read only property whose value is an [ObjectCollection](ObjectCollection.md).

## Version

Introduced in version August 2014  

