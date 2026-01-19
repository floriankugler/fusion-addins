# BRepEdgeDefinition Object

Derived from: [Base](Base.md) Object  

## Description

Represents the definition of a B-Rep edge that can be used as input to create a BRepBody.

## Methods

| Name | Description |
|----|----|
| [classType](BRepEdgeDefinition_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [associativeID](BRepEdgeDefinition_associativeID.md) | Gets and sets the associate ID of this edge definition. This ID will be copied to the corresponding edge when the BRepBodyDefinition is used to create a BrepBody. It is used internally by Fusion as the identifier for the edge and is used for tracking this geometry for parametric recomputes. |
| [endVertex](BRepEdgeDefinition_endVertex.md) | Gets and sets the end vertex of the edge definition. |
| [isMergeable](BRepEdgeDefinition_isMergeable.md) | Gets and sets if the two faces that share this edge can be merged along this edge. This property defaults to true so that merging is always done but this can be set to false in cases where you want to preserve the edge. An example where merging is typically done is when you have multiple planar faces that all lie on the same plane and are connected. When merging is allowed these faces can be replaced by a single face and the edges connecting the faces (the merged edges) are no longer part of the body. |
| [isValid](BRepEdgeDefinition_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [modelSpaceCurve](BRepEdgeDefinition_modelSpaceCurve.md) | Gets and sets the curve that defines the shape of the edge. |
| [objectType](BRepEdgeDefinition_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [startVertex](BRepEdgeDefinition_startVertex.md) | Gets and sets the start vertex of the edge definition. |

## Accessed From

[BRepBodyDefinition.createEdgeDefinitionByCurve](BRepBodyDefinition_createEdgeDefinitionByCurve.md), [BRepCoEdgeDefinition.edgeDefinition](BRepCoEdgeDefinition_edgeDefinition.md)

## Samples

| Name | Description |
|----|----|
| [BRep Body definition Sample](BRepBodyDefinition_Sample.md) | Demonstrates creating BRep bodies by BRepBodyDefinition. |

## Version

Introduced in version September 2020  

