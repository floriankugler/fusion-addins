# MirrorFeatures.createInput Method

Parent Object: [MirrorFeatures](MirrorFeatures.md)  

## Description

Creates a MirrorFeatureInput object. Use properties and methods on this object to define the mirror you want to create and then use the Add method, passing in the MirrorFeatureInput object.

## Syntax

"mirrorFeatures_var" is a variable referencing a [MirrorFeatures](MirrorFeatures.md) object.

```python
returnValue = mirrorFeatures_var.createInput(inputEntities, mirrorPlane)
```

## Return Value

| Type | Description |
|----|----|
| [MirrorFeatureInput](MirrorFeatureInput.md) | Returns the newly created MirrorFeatureInput object or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| inputEntities | [ObjectCollection](ObjectCollection.md) | A collection of the entities to mirror. It can contain faces, features, bodies, or components. The input must all be of a single type. For example, you can't provide a body and a component but the collection must be either all bodies or all components. |
| mirrorPlane | [Base](Base.md) | Input planar entity that defines the mirror plane. This can be either a planar face or a construction plane. |

## Samples

| Name | Description |
|----|----|
| [mirrorFeatures.add](mirrorFeatures_add_Sample.md) | Demonstrates the mirrorFeatures.add method by mirroring the selected body around the base X-Y construction plane. |

## Version

Introduced in version November 2014  

