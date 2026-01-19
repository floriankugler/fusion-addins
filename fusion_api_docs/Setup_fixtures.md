# Setup.fixtures Property

Parent Object: [Setup](Setup.md)  

## Description

Gets and sets the fixtures associated with the setup, which are represented by an ObjectCollection of models, where a model can be an Occurrence, BRepBody, or MeshBody. To be able to set models as fixtures, the fixturesEnabled property has to be set first.

## Syntax

"setup_var" is a variable referencing a Setup object.  

```python
# Get the value of the property.
propertyValue = setup_var.fixtures

# Set the value of the property.
setup_var.fixtures = propertyValue
```

## Property Value

This is a read/write property whose value is an [ObjectCollection](ObjectCollection.md).

## Version

Introduced in version May 2020  

