# PhysicalProperties Object

Derived from: [Base](Base.md) Object  

## Description

The physical properties of a Component, Occurrence or BRepBody

## Methods

| Name | Description |
|----|----|
| [classType](PhysicalProperties_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [getPrincipalAxes](PhysicalProperties_getPrincipalAxes.md) | Method that returns the principal axes. |
| [getPrincipalMomentsOfInertia](PhysicalProperties_getPrincipalMomentsOfInertia.md) | Method that returns the moments of inertia about the principal axes. Unit for returned values is kg\*cm^2. |
| [getRadiusOfGyration](PhysicalProperties_getRadiusOfGyration.md) | Method that returns the radius of gyration about the principal axes. Unit for returned values is cm. |
| [getRotationToPrincipal](PhysicalProperties_getRotationToPrincipal.md) | Gets the rotation from the world coordinate system of the target to the principal coordinate system. |
| [getXYZMomentsOfInertia](PhysicalProperties_getXYZMomentsOfInertia.md) | Method that gets the moment of inertia about the world coordinate system. Unit for returned values is kg\*cm^2. |

## Properties

| Name | Description |
| --- | --- |
| [accuracy](PhysicalProperties_accuracy.md) | Returns the accuracy that was used for the calculation. |
| [area](PhysicalProperties_area.md) | Gets the area in square centimeters. |
| [centerOfMass](PhysicalProperties_centerOfMass.md) | Returns the center of mass position |
| [density](PhysicalProperties_density.md) | Gets the density in kilograms per cubic centimeter. |
| [isValid](PhysicalProperties_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [mass](PhysicalProperties_mass.md) | Gets the mass in kilograms. |
| [objectType](PhysicalProperties_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [volume](PhysicalProperties_volume.md) | Gets the volume in the cubic centimeters. |

## Accessed From

[BRepBody.getPhysicalProperties](BRepBody_getPhysicalProperties.md), [BRepBody.physicalProperties](BRepBody_physicalProperties.md), [Component.getPhysicalProperties](Component_getPhysicalProperties.md), [Component.physicalProperties](Component_physicalProperties.md), [Design.physicalProperties](Design_physicalProperties.md), [FlatPatternComponent.getPhysicalProperties](FlatPatternComponent_getPhysicalProperties.md), [FlatPatternComponent.physicalProperties](FlatPatternComponent_physicalProperties.md), [FlatPatternProduct.physicalProperties](FlatPatternProduct_physicalProperties.md), [Occurrence.getPhysicalProperties](Occurrence_getPhysicalProperties.md), [Occurrence.physicalProperties](Occurrence_physicalProperties.md), [WorkingModel.physicalProperties](WorkingModel_physicalProperties.md)

## Samples

| Name | Description |
|----|----|
| [Get Physical Properties API Sample](GetPhysicalProperties_Sample.md) | Script that demonstrates getting physical properties using the API. When this script is run it will create a new document, build a simple model, and get the various physical properties from the model. |

## Version

Introduced in version September 2015  

