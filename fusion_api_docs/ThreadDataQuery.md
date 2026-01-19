# ThreadDataQuery Object

Derived from: [Base](Base.md) Object  

## Description

This object provides methods to query the thread data contained in the XML files in ThreadData folder within the Fusion install folder. You can use the queried values to create a ThreadInfo object that is then used to create a thread feature.

## Methods

| Name | Description |
|----|----|
| [allClasses](ThreadDataQuery_allClasses.md) | Returns and array/list of all the available classes for a thread type of a given thread designation. |
| [allDesignations](ThreadDataQuery_allDesignations.md) | returns an array/list of all the available thread designations for a thread type of a given size. Valid thread types and sizes and be obtained by using the allThreadTypes and allSizes functions. |
| [allSizes](ThreadDataQuery_allSizes.md) | Returns an array/list of all the available thread sizes for a given thread type. You can use the allThreadTypes property to get the available thread types. |
| [classType](ThreadDataQuery_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [create](ThreadDataQuery_create.md) | Static method to create a new ThreadDataQuery object. The ThreadDataQuery object is a utility object that provides methods to query for the valid thread definitions defined in Fusion. This object provides similar functionality as the Thread and Hole command dialogs to find valid thread types, designations and classes which can be used to create thread and tapped hole features. |
| [recommendThreadData](ThreadDataQuery_recommendThreadData.md) | Method that gets the recommended thread data for a given cylinder diameter. This method is only valid for straight threads and will fail for tapered threads. |
| [threadTypeCustomName](ThreadDataQuery_threadTypeCustomName.md) | Method that returns the custom name for a given thread type. The custom name is the localized name of the thread type using the current language specified for Fusion. |
| [threadTypeUnit](ThreadDataQuery_threadTypeUnit.md) | Method that returns the unit for a given thread type. |

## Properties

| Name | Description |
| --- | --- |
| [allThreadTypes](ThreadDataQuery_allThreadTypes.md) | This method returns an array of all the available thread types (families). The type names are always English. This English name should be used in the other methods that take the type as an input argument. If you need to display the type name to the user, you can use the threadTypeCustomName method To get the localized name. |
| [defaultInchThreadType](ThreadDataQuery_defaultInchThreadType.md) | Gets the default thread type for inch threads. |
| [defaultMetricThreadType](ThreadDataQuery_defaultMetricThreadType.md) | Gets the default thread type for metric threads. |
| [isTapered](ThreadDataQuery_isTapered.md) | Returns if this ThreadDataQuery was created to query for standard or tapered threads. |
| [isValid](ThreadDataQuery_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](ThreadDataQuery_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[ThreadDataQuery.create](ThreadDataQuery_create.md), [ThreadFeatures.threadDataQuery](ThreadFeatures_threadDataQuery.md)

## Samples

| Name | Description |
|----|----|
| [Thread Feature API Sample](ThreadFeatureSample_Sample.md) | Demonstrates creating a new thread feature. |

## Version

Introduced in version January 2015  

