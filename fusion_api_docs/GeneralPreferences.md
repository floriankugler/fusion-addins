# GeneralPreferences Object

Derived from: [Base](Base.md) Object  

## Description

Provides access to the general preferences.

## Methods

| Name | Description |
|----|----|
| [classType](GeneralPreferences_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [activeUserInterfaceTheme](GeneralPreferences_activeUserInterfaceTheme.md) | Gets the active user interface theme. This property is only different from userInterfaceTheme in the case the theme is DeviceUserInterfaceTheme. In that case the theme used will be returned. |
| [areAutodesk360NotificationsShown](GeneralPreferences_areAutodesk360NotificationsShown.md) | Gets and sets if Autodesk 360 notifications are shown. |
| [areInCommandErrorsAndWarningsShown](GeneralPreferences_areInCommandErrorsAndWarningsShown.md) | Gets and sets if in command errors and warnings are shown. |
| [areTipsAndTricksShown](GeneralPreferences_areTipsAndTricksShown.md) | Gets and sets if in command tips and tricks are shown. |
| [areTooltipsShown](GeneralPreferences_areTooltipsShown.md) | Gets and sets if tooltips are shown. |
| [automateVersioningTimeInterval](GeneralPreferences_automateVersioningTimeInterval.md) | Gets and sets the interval, in minutes, for automatic versioning. |
| [defaultModelingOrientation](GeneralPreferences_defaultModelingOrientation.md) | Gets and sets the default for which direction is considered "up". |
| [defaultOrbit](GeneralPreferences_defaultOrbit.md) | Get and sets the type of orbit. |
| [graphicsDriver](GeneralPreferences_graphicsDriver.md) | Gets and sets the graphics driver used to display the graphics. |
| [isAutomaticSaveOnCloseEnabled](GeneralPreferences_isAutomaticSaveOnCloseEnabled.md) | Gets and sets if the file is automatically saved on close. |
| [isAutomaticVersioningEnabled](GeneralPreferences_isAutomaticVersioningEnabled.md) | Gets and sets if a version of the file is automatically saved using a background thread. |
| [isCameraPivotEnabled](GeneralPreferences_isCameraPivotEnabled.md) | Gets and sets if zoom and orbit commands use camera pivot point for transition. |
| [isCommandPromptShown](GeneralPreferences_isCommandPromptShown.md) | Gets and sets if the command prompt is shown. |
| [isDefaultMeasureShown](GeneralPreferences_isDefaultMeasureShown.md) | Gets and sets if the default measure is shown. |
| [isGestureBasedViewNavigationUsed](GeneralPreferences_isGestureBasedViewNavigationUsed.md) | Gets and sets if gesture based view navigation is used. |
| [isHangDetectionEnabled](GeneralPreferences_isHangDetectionEnabled.md) | Gets and sets whether hang detection is enabled. This is a Windows only setting. If True, Fusion will detect when a task processes for longer than a specific time. A dialog is displayed if a hang is detected, allowing the user to continue processing or stop Fusion and send an error report. |
| [isSkipCreationWhenLiveUpdate](GeneralPreferences_isSkipCreationWhenLiveUpdate.md) | Gets and sets if the creation of launch items should be skipped for live update. |
| [isValid](GeneralPreferences_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [isZoomDirectionReversed](GeneralPreferences_isZoomDirectionReversed.md) | Gets and sets if the direction of the zoom is reversed. |
| [objectType](GeneralPreferences_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [offlineCachePeriod](GeneralPreferences_offlineCachePeriod.md) | Gets and sets the length of time, in days, that the offline cache of a document will remain. |
| [panZoomOrbitShortcuts](GeneralPreferences_panZoomOrbitShortcuts.md) | Gets and sets how pan, zoom, and orbit should behave. |
| [userInterfaceTheme](GeneralPreferences_userInterfaceTheme.md) | Gets and sets which color theme is used by the user interface. |
| [userLanguage](GeneralPreferences_userLanguage.md) | Gets and sets the current language. Setting the language does not take effect until the next time Fusion is started. |

## Accessed From

[Preferences.generalPreferences](Preferences_generalPreferences.md)

## Version

Introduced in version August 2014  

