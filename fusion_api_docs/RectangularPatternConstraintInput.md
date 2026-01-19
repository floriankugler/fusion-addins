# RectangularPatternConstraintInput Object

Derived from: [Base](Base.md) Object  

## Description

Used to define the inputs need to create a rectangular pattern in a sketch.

## Methods

| Name | Description |
|----|----|
| [classType](RectangularPatternConstraintInput_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [setDirectionOne](RectangularPatternConstraintInput_setDirectionOne.md) | Sets all of the input required to define the pattern in the first direction. |
| [setDirectionTwo](RectangularPatternConstraintInput_setDirectionTwo.md) | Sets all of the input required to define the pattern in the second direction. |

## Properties

| Name | Description |
| --- | --- |
| [directionOneEntity](RectangularPatternConstraintInput_directionOneEntity.md) | Defines the first direction of the pattern. This can be null which indicates to use the default which is the X-axis of the sketch. Setting this property to null will automatically clear directionTwoEntity, if it has been set. |
| [directionTwoEntity](RectangularPatternConstraintInput_directionTwoEntity.md) | Defines the second direction of the pattern. This can be null which indicates to use the default which is perpendicular to direction one. The directionOneEntity property must be set before setting this property. |
| [distanceOne](RectangularPatternConstraintInput_distanceOne.md) | Gets and sets the distance in the first direction. |
| [distanceTwo](RectangularPatternConstraintInput_distanceTwo.md) | Gets and sets the distance in the second direction. |
| [distanceType](RectangularPatternConstraintInput_distanceType.md) | Gets and sets how the distance between elements is computed. |
| [entities](RectangularPatternConstraintInput_entities.md) | Gets and sets the entities to pattern. Sketch points and curves are valid entities to pattern. |
| [isSuppressed](RectangularPatternConstraintInput_isSuppressed.md) | Specifies which, if any, instances of the pattern are suppressed. This defaults to all instances being visible. This returns an array of Booleans that indicates if a particular instance in the pattern is suppressed or not. A value of true will result in the associated instance being suppressed. Both the quantityOne and quantityTwo properties must be set with valid values before using the isSuppressed property is valid. A quantity of one is a valid value. The indices represent the pattern instances in a row-column order, with the initial geometry not counting. For example, if you have a 4x4 pattern, the array will have 15 elements rather than 16 because the original geometry cannot be suppressed as part of the pattern. The first element in the array is the one next to the original in the first direction. The second element is the next one on the first row, and the third is the next one. The fourth element will be the first element in the row next to the first row that contains the original geometry. |
| [isSymmetricInDirectionOne](RectangularPatternConstraintInput_isSymmetricInDirectionOne.md) | Gets and sets if the pattern in direction one is in one direction or is symmetric. |
| [isSymmetricInDirectionTwo](RectangularPatternConstraintInput_isSymmetricInDirectionTwo.md) | Gets and sets if the pattern in direction two is in one direction or is symmetric. |
| [isValid](RectangularPatternConstraintInput_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](RectangularPatternConstraintInput_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [quantityOne](RectangularPatternConstraintInput_quantityOne.md) | Gets and sets the number of instances in the first direction. |
| [quantityTwo](RectangularPatternConstraintInput_quantityTwo.md) | Gets and sets the number of instances in the second direction. |

## Accessed From

[GeometricConstraints.createRectangularPatternInput](GeometricConstraints_createRectangularPatternInput.md)

## Version

Introduced in version September 2022  

