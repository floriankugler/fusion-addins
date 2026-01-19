# ProductUsageData Object

Derived from: [Base](Base.md) Object  

## Description

Provides access to the product usage data settings.

## Methods

| Name | Description |
|----|----|
| [classType](ProductUsageData_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [isGoogleAnalyticsTrackingEnabled](ProductUsageData_isGoogleAnalyticsTrackingEnabled.md) | Gets and sets if Google Analytics tracking is enabled. |
| [isLearningPanelContextEnabled](ProductUsageData_isLearningPanelContextEnabled.md) | Gets and sets if data can be collected to enable the Learning Panel to show information based on the current context. |
| [isTrackingToImproveCommunicationEnabled](ProductUsageData_isTrackingToImproveCommunicationEnabled.md) | Gets and sets if data can be collected to improve communications. This is the preferences setting titled "Customize our messaging". |
| [isTrackingToImproveSoftwareEnabled](ProductUsageData_isTrackingToImproveSoftwareEnabled.md) | Gets and sets if data can be collected to help improve the products and services that Autodesk provides. This is the preference setting titled "Help develop our products and services". |
| [isValid](ProductUsageData_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](ProductUsageData_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[Preferences.productUsageData](Preferences_productUsageData.md)

## Version

Introduced in version August 2014  

