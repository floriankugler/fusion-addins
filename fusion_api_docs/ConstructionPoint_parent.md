# ConstructionPoint.parent Property

Parent Object: [ConstructionPoint](ConstructionPoint.md)  

## Description

Returns the parent component or base feature. If both the design and the construction point are parametric, the parent will be a component. If the design is parametric and the construction point is not, the parent will be a base feature. If the design is not parametric the parent will be a component.

## Syntax

"constructionPoint_var" is a variable referencing a ConstructionPoint object.  

```python
# Get the value of the property.
propertyValue = constructionPoint_var.parent
```

## Property Value

This is a read only property whose value is a [Base](Base.md).

## Version

Introduced in version August 2014  

