# Matrix2D Object

Derived from: [Base](Base.md) Object  

## Description

Transient 2D 3x3 matrix. This object is a wrapper over 2D matrix data and is used as way to pass matrix data in and out of the API and as a convenience when operating on matrix data. They are created statically using the create method of the Matrix2D class.

## Methods

| Name | Description |
|----|----|
| [asArray](Matrix2D_asArray.md) | Returns the contents of the matrix as a 9 element array. |
| [classType](Matrix2D_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [copy](Matrix2D_copy.md) | Creates an independent copy of this matrix. |
| [create](Matrix2D_create.md) | Creates a transient 2D matrix (3x3) object. It is initialized as an identity matrix. |
| [getAsCoordinateSystem](Matrix2D_getAsCoordinateSystem.md) | Gets the matrix data as the components that define a coordinate system. |
| [getCell](Matrix2D_getCell.md) | Gets the value of the specified cell in the 3x3 matrix. |
| [invert](Matrix2D_invert.md) | Invert this matrix. |
| [isEqualTo](Matrix2D_isEqualTo.md) | Compares this matrix with another matrix and returns True if they're identical. |
| [setCell](Matrix2D_setCell.md) | Sets the specified cell in the 3x3 matrix to the specified value. |
| [setToAlignCoordinateSystems](Matrix2D_setToAlignCoordinateSystems.md) | Sets this matrix to be the matrix that maps from the 'from' coordinate system to the 'to' coordinate system. |
| [setToIdentity](Matrix2D_setToIdentity.md) | Resets this matrix to be an identity matrix. |
| [setToRotateTo](Matrix2D_setToRotateTo.md) | Sets to the matrix of rotation that would align the 'from' vector with the 'to' vector. |
| [setToRotation](Matrix2D_setToRotation.md) | Sets this matrix to the matrix of rotation by the specified angle, through the specified origin. |
| [setWithArray](Matrix2D_setWithArray.md) | Sets the contents of the array using a 9 element array. |
| [setWithCoordinateSystem](Matrix2D_setWithCoordinateSystem.md) | Reset this matrix to align with a specific coordinate system. |
| [transformBy](Matrix2D_transformBy.md) | Transforms this matrix using the input matrix. |

## Properties

| Name | Description |
| --- | --- |
| [determinant](Matrix2D_determinant.md) | Returns the determinant of the matrix. |
| [isValid](Matrix2D_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](Matrix2D_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[Canvas.transform](Canvas_transform.md), [CanvasInput.transform](CanvasInput_transform.md), [Matrix2D.copy](Matrix2D_copy.md), [Matrix2D.create](Matrix2D_create.md)

## Version

Introduced in version August 2014  

