# Application Object

Derived from: [Base](Base.md) Object  

## Description

The top-level object that represents the Fusion application (all of Fusion). This provides access to the modeler and files.

## Methods

| Name | Description |
| --- | --- |
| [classType](Application_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [executeTextCommand](Application_executeTextCommand.md) | Executes the input text command. |
| [fireCustomEvent](Application_fireCustomEvent.md) | Fires a previously registered custom event. This method is used by a worker thread or another add-in to fire an event to the add-in that registered the event and is running in the primary thread. Firing a custom event does not immediately result in the event handler being called. When a custom event is fired the event is put on the queue and will be handled in the main thread when Fusion is idle. |
| [get](Application_get.md) | Access to the root Application object. |
| [getLastError](Application_getLastError.md) | Returns information about the last error that occurred. |
| [log](Application_log.md) | Logs messages to either the TEXT COMMAND window or the Fusion app log file. |
| [registerCustomEvent](Application_registerCustomEvent.md) | This registers a new CustomEvent which is intended to be primarily used to send an event from a worker thread you've created back to your add-in running in the primary thread. It's also possible that two add-ins could be cooperating and another add-in can fire the event to your add-in. |
| [unregisterCustomEvent](Application_unregisterCustomEvent.md) | Unregisters an existing CustomEvent. |

## Properties

| Name | Description |
| --- | --- |
| [activeDocument](Application_activeDocument.md) | Returns the current active document. |
| [activeEditObject](Application_activeEditObject.md) | Returns the current edit target as seen in the user interface. This edit target is defined as the container object that will be added to if something is created. For example, a component can be an edit target so that when new bodies are created they are added to that component. A sketch can also be an edit target. |
| [activeProduct](Application_activeProduct.md) | Returns the current active product. |
| [activeViewport](Application_activeViewport.md) | Returns the currently active graphics view. |
| [applicationFolders](Application_applicationFolders.md) | Returns the ApplicationFolders object which provides access to the paths of various folders associated with Fusion. |
| [currentUser](Application_currentUser.md) | Returns the User that is currently logged in. |
| [data](Application_data.md) | Returns the Data object which provides access the files. |
| [documents](Application_documents.md) | Returns the Documents collection object which supports accessing opened documents, opening existing documents, and creating new documents. |
| [favoriteAppearances](Application_favoriteAppearances.md) | Returns the set of favorite appearances. |
| [favoriteMaterials](Application_favoriteMaterials.md) | Returns the set of favorite materials. |
| [fontNames](Application_fontNames.md) | Returns the names of all of the fonts that are available in Fusion when creating text. |
| [hasActiveJobs](Application_hasActiveJobs.md) | Gets whether there are any active jobs. |
| [importManager](Application_importManager.md) | Returns the ImportManager. You use the ImportManager to import files (of various neutral formats.) into existing components or new document. |
| [isComponentColorsDisplayed](Application_isComponentColorsDisplayed.md) | Get and sets if component colors are used when displaying the components within a design. This is the API equivalent of the "Display Component Colors" command. |
| [isOffLine](Application_isOffLine.md) | Gets and sets if Fusion is offline or not. |
| [isStartupComplete](Application_isStartupComplete.md) | Boolean property indicating whether Fusion has completed its initialization. This includes initialization of all the Add-ins loaded at startup. |
| [isValid](Application_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [lightingEnvironment](Application_lightingEnvironment.md) | Gets and sets the current lighting environment to use when rendering the graphics. |
| [materialLibraries](Application_materialLibraries.md) | Returns the collection of material libraries currently available. |
| [measureManager](Application_measureManager.md) | Get the MeasureManager object which can be used to perform measurements of geometry. |
| [objectType](Application_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [pointTolerance](Application_pointTolerance.md) | The modeling tolerance used internally when comparing two points. The value is in centimeters. |
| [preferences](Application_preferences.md) | Provides access to all of the application preferences. |
| [scripts](Application_scripts.md) | Returns the Scripts object which provides the ability to manage scripts and add-ins. |
| [supportedProductTypes](Application_supportedProductTypes.md) | Returns an array containing the names of the products types currently supported by Fusion. For example, the name returned for Fusion is "DesignProductType". These product type names are used to identify specific products in some other API functions such as the productType property on the Workspace and ToolbarPanel objects. |
| [userId](Application_userId.md) | Returns the internal name of the Autodesk account currently logged in. This can be used by applications sold through the Autodesk Exchange Store to verify that the user has in fact purchased the product. |
| [userInterface](Application_userInterface.md) | Provides access to functionality specific to the user interface. |
| [userName](Application_userName.md) | Returns the user name of the Autodesk account currently logged in. |
| [vectorAngleTolerance](Application_vectorAngleTolerance.md) | The modeling tolerance used when comparing vector angles. The value is in radians. |
| [version](Application_version.md) | Returns the current version of the Fusion application. |

## Events

| Name | Description |
| --- | --- |
| [cameraChanged](Application_cameraChanged.md) | The cameraChanged event fires immediately after a change in the camera has been made. Camera changes happen when user changes the view by rotating, zooming in or out, panning, changing from parallel to perspective, or when the extents of the viewport changes. You can add or remove event handlers from the CameraEvent. |
| [dataFileComplete](Application_dataFileComplete.md) | The dataFileComplete event fires when a data file upload has completed including any cloud side translations. |
| [dataFileCopyComplete](Application_dataFileCopyComplete.md) | The dataFileCopyComplete event fires when a data file copy has completed including any PIM Data copy. |
| [documentActivated](Application_documentActivated.md) | The DocumentActivated event fires at the VERY end of a document being activated. |
| [documentActivating](Application_documentActivating.md) | The DocumentActivating event fires at the VERY start of a document being activated. |
| [documentClosed](Application_documentClosed.md) | The DocumentClosed event fires at the VERY end of a document being closed. The Document object is not longer available because it has been closed. |
| [documentClosing](Application_documentClosing.md) | The DocumentClosing event fires at the VERY start of a document being closed. User can set the isSaveCanceled property of DocumentEventArgs to true to cancel the document close. |
| [documentCreated](Application_documentCreated.md) | The DocumentCreated event fires when a new document is created. |
| [documentDeactivated](Application_documentDeactivated.md) | The DocumentDeactivated event fires at the VERY end of a document being deactivated. |
| [documentDeactivating](Application_documentDeactivating.md) | The DocumentDeactivating event fires at the VERY start of a document being deactivated. |
| [documentOpened](Application_documentOpened.md) | The DocumentOpened event fires at the VERY end of a document being opened so the Document object is available to be used. When a document is opened that references other documents, only the top-level document will cause the documentOpened event to be fired. You can access the referenced documents by using the documentReferences property of the Document object. |
| [documentOpening](Application_documentOpening.md) | The DocumentOpening event fires at the VERY start of a document being opened. There is no promise that the document will be opened, hence a documentOpened event may not follow. When a document is being opened that references other documents, only the top-level document will cause a documentOpening event to be fired. |
| [documentSaved](Application_documentSaved.md) | The DocumentSaved event fires after the save operation has been completed. |
| [documentSaving](Application_documentSaving.md) | The DocumentSaving event fires at the VERY start of a document being saved. You can set the isSaveCanceled property of DocumentEventArgs to true to cancel the document save. |
| [insertedFromURL](Application_insertedFromURL.md) | The insertedFromURL event fires after the user has clicked a link in a web page that uses the Fusion protocol handler to insert a file as new component and that operation has completed. |
| [insertingFromURL](Application_insertingFromURL.md) | The insertingFromURL event fires when the user has clicked a link in a web page that uses the Fusion protocol handler to insert a file as new component. This event is fired at the beginning of the request but before Fusion has take any action so that it's still possible to cancel the operation. |
| [mfgdmDataReady](Application_mfgdmDataReady.md) | The mfgdmDataReady event fires when the MFGDM data structure for a document has been updated and properties to IDs and structure from the data model is ready. |
| [onlineStatusChanged](Application_onlineStatusChanged.md) | The onlineStatusChanged event fires immediately after Fusion goes online or offline. This event fires whether or not the online status was changed deliberately by the user by using the Fusion 'Work Offline' command or because of inadvertent network/Internet connectivity issues. You can get the isOffline property of ApplicationEventArgs to determine whether Fusion has gone Offline or has come back online. The client can add or remove ApplicationEventHandlers from the ApplicationEvent. |
| [openedFromURL](Application_openedFromURL.md) | The openedFromURL event fires after the user has clicked a link in a web page that uses the Fusion protocol handler to create a new using an existing file as the initial contents and that operation has completed. |
| [openingFromURL](Application_openingFromURL.md) | The openingFromURL event fires when the user has clicked a link in a web page that uses the Fusion protocol handler to create a new file using an existing file as the initial contents. This event is fired at the beginning of the request but before Fusion has take any action so that it's still possible to cancel the operation. |
| [startupCompleted](Application_startupCompleted.md) | The startupCompleted event fires after Fusion has completed its initialization. This includes initialization of all the Add-ins loaded at startup. The client can add or remove ApplicationEventHandlers from the ApplicationEvent. |

## Accessed From

[Application.get](Application_get.md), [Document.parent](Document_parent.md), [DrawingDocument.parent](DrawingDocument_parent.md), [FusionDocument.parent](FusionDocument_parent.md)

## Version

Introduced in version August 2014  

