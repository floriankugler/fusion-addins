# Setup.models Property

Parent Object: [Setup](Setup.md)  

## Description

Gets and sets the input models associated with the setup. Passing in an empty ObjectCollection will remove all current inputs. Valid collection items are Occurrence, BRepBody, or MeshBody.

## Syntax

"setup_var" is a variable referencing a Setup object.  

```python
# Get the value of the property.
propertyValue = setup_var.models

# Set the value of the property.
setup_var.models = propertyValue
```

## Property Value

This is a read/write property whose value is an [ObjectCollection](ObjectCollection.md).

## Version

Introduced in version December 2017  

