# User Object

Derived from: [Base](Base.md) Object  

## Description

A class that represents a Fusion User

## Methods

| Name | Description |
|----|----|
| [classType](User_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [displayName](User_displayName.md) | Returns display name of the user. (i.e. the name that shows up in the Fusion UI) |
| [email](User_email.md) | Get the email associated with this users Fusion account |
| [isValid](User_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](User_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [userId](User_userId.md) | Returns the user's internal Autodesk account name. This can be used by applications sold through the Autodesk Exchange Store to verify that the user has in fact purchased the product. |
| [userName](User_userName.md) | Returns the user name associated with this user's Autodesk account |

## Accessed From

[Application.currentUser](Application_currentUser.md), [DataFile.createdBy](DataFile_createdBy.md), [DataFile.inUseBy](DataFile_inUseBy.md), [DataFile.lastUpdatedBy](DataFile_lastUpdatedBy.md), [DesignDataFile.createdBy](DesignDataFile_createdBy.htm), [DesignDataFile.inUseBy](DesignDataFile_inUseBy.htm), [DesignDataFile.lastUpdatedBy](DesignDataFile_lastUpdatedBy.htm)

## Version

Introduced in version January 2016  

