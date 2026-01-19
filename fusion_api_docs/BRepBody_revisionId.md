# BRepBody.revisionId Property

Parent Object: [BRepBody](BRepBody.md)  

## Description

Returns the current revision ID of the body. This ID changes any time the body is modified in any way. By getting and saving the ID when you create any data that is dependent on the body, you can then compare the saved ID with the current ID to determine if the body has changed to know if you should update your data.

## Syntax

"bRepBody_var" is a variable referencing a BRepBody object.  

```python
# Get the value of the property.
propertyValue = bRepBody_var.revisionId
```

## Property Value

This is a read only property whose value is a string.

## Samples

| Name | Description |
|----|----|
| [BRep Body Sample](BRepBodySample_Sample.md) | B-Rep (Boundary Representation) body related functions |

## Version

Introduced in version September 2017  

