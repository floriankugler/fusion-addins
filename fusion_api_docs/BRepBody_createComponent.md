# BRepBody.createComponent Method

Parent Object: [BRepBody](BRepBody.md)  

## Description

Creates a new component and occurrence within the component that currently owns this body. This body is moved into the new component and returned. The newly created component can be obtained by using the parentComponent property of the BRepBody object.  

This method is only valid if the IsTransient property is false.

## Syntax

"bRepBody_var" is a variable referencing a [BRepBody](BRepBody.md) object.

```python
returnValue = bRepBody_var.createComponent()
```

## Return Value

| Type | Description |
|----|----|
| [BRepBody](BRepBody.md) | Returns the BRrepBody in the new component or null in the case the creation failed. |

## Version

Introduced in version June 2015  

