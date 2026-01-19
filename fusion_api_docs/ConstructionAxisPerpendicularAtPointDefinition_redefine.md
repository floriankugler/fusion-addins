# ConstructionAxisPerpendicularAtPointDefinition.redefine Method

Parent Object: [ConstructionAxisPerpendicularAtPointDefinition](ConstructionAxisPerpendicularAtPointDefinition.md)  

## Description

Redefines the input geometry of the construction axis.

## Syntax

"constructionAxisPerpendicularAtPointDefinition_var" is a variable referencing a [ConstructionAxisPerpendicularAtPointDefinition](ConstructionAxisPerpendicularAtPointDefinition.md) object.

```python
returnValue = constructionAxisPerpendicularAtPointDefinition_var.redefine(face, pointEntity)
```

## Return Value

| Type    | Description                                                 |
|---------|-------------------------------------------------------------|
| boolean | Returns true if the redefinition of the axis is successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| face | [BRepFace](BRepFace.md) | The face (BRepFace object) to create the axis perpendicular to. |
| pointEntity | [Base](Base.md) | The point (sketch point, vertex, construction point) used to position the axis. |

## Version

Introduced in version August 2014  

