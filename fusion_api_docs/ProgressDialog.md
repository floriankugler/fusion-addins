# ProgressDialog Object

Derived from: [Base](Base.md) Object  

## Description

Provides access to the progress dialog.

## Methods

| Name | Description |
|----|----|
| [classType](ProgressDialog_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [hide](ProgressDialog_hide.md) | Hides the progress dialog. This should be used when the process has completed. |
| [reset](ProgressDialog_reset.md) | Method that resets the progress bar. The progress bar "rewinds" and shows no progress. This is the same as setting the progress value to the minimum value. |
| [show](ProgressDialog_show.md) | Displays the progress dialog that includes a progress bar that can be used to display a continually updated message indicating the progress of a process that will take more than a few seconds. The progress is determined by comparing the current progress value with the minimum and maximum values. |

## Properties

| Name | Description |
| --- | --- |
| [cancelButtonText](ProgressDialog_cancelButtonText.md) | Sets the text label on the Cancel button. The default text label is "Cancel". |
| [isBackgroundTranslucent](ProgressDialog_isBackgroundTranslucent.md) | Gets and sets if the dialog background is translucent. This is false by default |
| [isCancelButtonShown](ProgressDialog_isCancelButtonShown.md) | Gets and sets if the cancel button is included in the dialog. This is false by default. |
| [isShowing](ProgressDialog_isShowing.md) | Gets if the Progress Dialog is currently being displayed |
| [isValid](ProgressDialog_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [maximumValue](ProgressDialog_maximumValue.md) | The maximum value of the progress bar. This is used along with the minimum value and the progress value to compute the current percentage complete. |
| [message](ProgressDialog_message.md) | Gets and sets the message to display along with the progress bar. The following symbols can be used to display values. "%p" is replaced by the percentage completed. "%v" is replaced by the current value. %m is replaced by the total number of steps. For example, the message "Processing section %v of %m." will result in the message "Processing section 1 of 10." to be displayed if the maximum value is 10 and the current value is 1. Specify an empty string ("") for no message to appear along with the progress panel. |
| [minimumValue](ProgressDialog_minimumValue.md) | The minimum value of the progress bar. This is used along with the maximum value and the progress value to compute the current percentage complete. This is also the initial progress value when the progress bar is first displayed. |
| [objectType](ProgressDialog_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [progressValue](ProgressDialog_progressValue.md) | Gets and sets the current progress bar value. Progress is determined based on this value relative to the minimum and maximum values. This will update the values displayed in the message string. |
| [title](ProgressDialog_title.md) | Gets and sets the title of the progress dialog |
| [wasCancelled](ProgressDialog_wasCancelled.md) | Indicates if the cancel button was selected the last time the Progress Dialog was shown. |

## Accessed From

[UserInterface.createProgressDialog](UserInterface_createProgressDialog.md)

## Samples

| Name | Description |
|----|----|
| [Generate Toolpaths API Sample](GenerateToolpaths_Sample_Sample.md) | Demonstrates generating the toolpaths in the active document. |
| [Progress Dialog API Sample](ProgressDialogSample_Sample.md) | Demonstrates how to use progress dialog |

## Version

Introduced in version January 2016  

