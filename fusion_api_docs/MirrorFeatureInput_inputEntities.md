# MirrorFeatureInput.inputEntities Property

Parent Object: [MirrorFeatureInput](MirrorFeatureInput.md)  

## Description

Gets and sets the entities that are mirrored. It can contain faces, features, bodies, or components. The input must all be of a single type. For example, you can't provide a body and a component but the collection must be either all bodies or all components.

## Syntax

"mirrorFeatureInput_var" is a variable referencing a MirrorFeatureInput object.  

```python
# Get the value of the property.
propertyValue = mirrorFeatureInput_var.inputEntities

# Set the value of the property.
mirrorFeatureInput_var.inputEntities = propertyValue
```

## Property Value

This is a read/write property whose value is an [ObjectCollection](ObjectCollection.md).

## Version

Introduced in version November 2014  

