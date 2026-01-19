# ProgressBar Object

Derived from: [Base](Base.md) Object  

## Description

Provides access to the progress bar.

## Methods

| Name | Description |
|----|----|
| [classType](ProgressBar_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [hide](ProgressBar_hide.md) | Hides the progress or busy bar. This should be used when the process has completed. |
| [show](ProgressBar_show.md) | This method displays a message in the progress bar in the lower-right corner of the Fusion window. The progress bar can be used to display a continually updated message indicating the progress of a process. The progress is determined by comparing the current progress value with the minimum and maximum values. |
| [showBusy](ProgressBar_showBusy.md) | This method displays a message in the busy bar in the lower-right corner of the Fusion window. The busy bar can be used to display a continually updated message indicating the progress of a process. The busy bar is different from the progress bar, because it does not show a meter indicating the current progress. Instead is shows a continually moving bar to indicate processing without showing the current progress. This is useful in cases where the length of the process is unknown. |

## Properties

| Name | Description |
| --- | --- |
| [isValid](ProgressBar_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [message](ProgressBar_message.md) | Gets and sets the message to display in the progress bar. The following symbols can be used to display values. "%p" is replaced by the percentage completed. "%v" is replaced by the current value. %m is replaced by the total number of steps. For example, the message "Processing section %v of %m." will result in the message "Processing section 1 of 10." to be displayed if the maximum value is 10 and the current value is 1. When a busy bar is displayed, only a simple message is supported and symbols are not supported. If your process is running in the main thread of Fusion, you will need to call adsk.doEvents to give control back to Fusion, so it can update the UI. |
| [objectType](ProgressBar_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [progressValue](ProgressBar_progressValue.md) | Gets and sets the current progress value. This value determines the progress based on this value relative to the minimum and maximum values specified when the progress bar was created. This will also update the values displayed in the message string. If your process is running in the main thread of Fusion, you will need to call adsk.doEvents to give control back to Fusion, so it can update the UI. This value is ignored when a busy bar is displayed. |

## Accessed From

[UserInterface.progressBar](UserInterface_progressBar.md)

## Version

Introduced in version May 2024  

