# ThreadFeatures Object

Derived from: [Base](Base.md) Object  

## Description

Collection that provides access to all of the existing thread features in a component and supports the ability to create new thread features.  

The creation of a tapped hole also results in the creation of a thread feature. These thread features are also returned by this collection, even though they aren't present in the timeline and are represented by the hole feature.

## Methods

| Name | Description |
|----|----|
| [add](ThreadFeatures_add.md) | Creates a new thread feature. |
| [classType](ThreadFeatures_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [createInput](ThreadFeatures_createInput.md) | Creates a ThreadFeatureInput object. This object is the API equivalent of the Thread feature dialog. It collects the required input and once fully defined you can pass this object to the ThreadFeatures.add method to create the thread feature. |
| [createThreadInfo](ThreadFeatures_createThreadInfo.md) | \*\*RETIRED\*\* Method that creates a new ThreadInfo object that can be used in creating thread features. The ThreadInfo object that defines the type and size of the thread to create. When creating a thread, the type and size of the thread is specified by referencing thread information defined in one of the XML files in the ThreadData folder within the Fusion install folder. You can use the ThreadDataQuery object to query these XML files to find the specific thread you want to create. The ThreadDataQuery object can be obtained by using the ThreadFeatures.threadDataQuery property. |
| [item](ThreadFeatures_item.md) | Function that returns the specified thread feature using an index into the collection. |
| [itemByName](ThreadFeatures_itemByName.md) | Function that returns the specified thread feature using the name of the feature. |

## Properties

| Name | Description |
| --- | --- |
| [count](ThreadFeatures_count.md) | The number of thread features in the collection. |
| [isValid](ThreadFeatures_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](ThreadFeatures_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [threadDataQuery](ThreadFeatures_threadDataQuery.md) | **RETIRED** Property that returns the ThreadDataQuery object. When creating a thread, the type and size of the thread is specified by referencing thread information defined in one of the XML files in the ThreadData folder. The ThreadDataQuery is an object that supports methods to query the existing threads defined in these files. |

## Accessed From

[Features.threadFeatures](Features_threadFeatures.md)

## Samples

| Name | Description |
|----|----|
| [Thread Feature API Sample](ThreadFeatureSample_Sample.md) | Demonstrates creating a new thread feature. |

## Version

Introduced in version January 2015  

