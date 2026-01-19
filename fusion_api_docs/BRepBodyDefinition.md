# BRepBodyDefinition Object

Derived from: [Base](Base.md) Object  

## Description

This object is used to define a temporary B-Rep body. This includes solid, surface, and wire bodies. The class supports the ability to define the geometry and topology of the B-Rep and once the definition is complete, it supports the creation of a temporary BRepBody object.

## Methods

| Name | Description |
|----|----|
| [classType](BRepBodyDefinition_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [create](BRepBodyDefinition_create.md) | Static function that creates a new BRepBodyDefinition object. It's initially empty but you can use the functionality it provides to define the geometry and topology of the B-Rep object you want to create. |
| [createBody](BRepBodyDefinition_createBody.md) | Attempts to create a temporary BRepBody object using the definition provided by this BRepBodyDefinition object. Properties on this BRepBodyDefinition are used to define some of the criteria that control how the body is created. |
| [createEdgeDefinitionByCurve](BRepBodyDefinition_createEdgeDefinitionByCurve.md) | Using a curve in model space it creates a new BRepEdgeDefinition object that's associated with the body. |
| [createVertexDefinition](BRepBodyDefinition_createVertexDefinition.md) | Creates a new BRepVertexDefinition object that's associated with the body. |

## Properties

| Name | Description |
| --- | --- |
| [doFullHealing](BRepBodyDefinition_doFullHealing.md) | Specifies if full healing is done when creating the body. This defaults to true and it's highly recommended that you do full healing because it can find and correct problems with the input. If you're sure that the B-Rep definition that you've constructed is correct then you can set this to false to skip the full healing process. |
| [isValid](BRepBodyDefinition_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [lumpDefinitions](BRepBodyDefinition_lumpDefinitions.md) | Provides access to the BRepLumpDefinitions object associated with this BRepBodyDefinition. It's through the returned collection that you can create new BRepLumpDefinition objects. |
| [objectType](BRepBodyDefinition_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [outcomeInfo](BRepBodyDefinition_outcomeInfo.md) | Returns an array of strings that contain information about the outcome of the previous call of the createBody method. This is especially useful when the createBody method fails, (returns null), because it provides information about why the failure occurred. It can also sometimes provide some information even when createBody succeeds. Each string that's returned represents a single set of information and is packaged as JSON such as '{"description":"vertex data is null or inconsistent with edge geometry","associativeID":"unknown","code":37}' The description is an English description of the error or warning. The associativeID maps back to the entity provided that is the cause of the problem. The ID is the associative ID you can optionally assign to the entity definition. The code is an internal code for the error or warning. An empty array is returned if createBody succeeded and there's no additional information. |

## Accessed From

[BRepBodyDefinition.create](BRepBodyDefinition_create.md)

## Samples

| Name | Description |
|----|----|
| [BRep Body definition Sample](BRepBodyDefinition_Sample.md) | Demonstrates creating BRep bodies by BRepBodyDefinition. |

## Version

Introduced in version September 2020  

