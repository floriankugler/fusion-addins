# ToEntityExtentDefinition Object

Derived from: [ExtentDefinition](ExtentDefinition.md) Object  

## Description

A definition object that is used to define the extents of a feature to be up to a specified construction plane or face.

## Methods

| Name | Description |
|----|----|
| [classType](ToEntityExtentDefinition_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [create](ToEntityExtentDefinition_create.md) | Statically creates a new ToEntityExtentDefinition object. This is used as input when defining the extents of a feature to be up to a construction plane or face. |

## Properties

| Name | Description |
| --- | --- |
| [directionHint](ToEntityExtentDefinition_directionHint.md) | Gets and sets a direction that is used when the result is ambiguous. For example, if you have a profile in the center of a torus and are extruding to the torus, the extrusion can go in either direction. When needed, this provides the information to tell Fusion which direction to go. In most cases this is not needed and the property will be null. |
| [entity](ToEntityExtentDefinition_entity.md) | Gets and sets the entity that the feature extent is defined up to. This can be a ConstructionPlane, Profile, BrepFace, BrepBody, or BRepVertex. |
| [isChained](ToEntityExtentDefinition_isChained.md) | Gets and sets whether connected faces to the input entity should also be used when calculating the extent or if the input entity should be extended. A value of true indicates that connected entities should be used. |
| [isMinimumSolution](ToEntityExtentDefinition_isMinimumSolution.md) | Gets and sets if the minimum or maximum solution is calculated. This is only used when the input entity is a body and defines if the extrusion to go to the near side (minimum solution) of the body or the far side. When a new ToEntityExtentDefinition object is created, this property defaults to True. |
| [isValid](ToEntityExtentDefinition_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](ToEntityExtentDefinition_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [offset](ToEntityExtentDefinition_offset.md) | Returns the current offset. If the EntityExtentDefinition object has been created statically and isn't associated with a feature this will return a ValueInput object. If the EntityExtentDefinition object is obtained from a feature this will return a ModelParameter object. You can use properties of the parameter to edit its value which will result in the feature updating. |
| [parentFeature](ToEntityExtentDefinition_parentFeature.md) | Returns the parent feature that this definition is associated with. If this definition has been created statically and is not associated with a feature this property will return null. |

## Accessed From

[ToEntityExtentDefinition.create](ToEntityExtentDefinition_create.md)

## Samples

| Name | Description |
|----|----|
| [extrudeFeatures.add using setTwoSidesExtent](extrudeFeaturesTwoSidesExtent_add_Sample.md) | Demonstrates the extrudeFeatures.add method using the setTwoSidesExtent method. To use this sample have a design open that contains a profile and a body that is positioned away from the profile but is a size where when the profile is extruded it will intersect the body. When you run the script you will be prompted to select the profile that will be used to create the extrusion and the body to extrude to. The extrusion will be created up to the body with an offset and will also be offset from the sketch plane. |

## Version

Introduced in version November 2016  

