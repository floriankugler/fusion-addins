# UserInterface Object

Derived from: [Base](Base.md) Object  

## Description

Provides access to the user-interface related objects and functionality.

## Methods

| Name | Description |
| --- | --- |
| [classType](UserInterface_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [createCloudFileDialog](UserInterface_createCloudFileDialog.md) | Creates a new CloudFileDialog object which provides the ability to show a file selection dialog to the user that allows them to choose a file from Fusion web client. |
| [createFileDialog](UserInterface_createFileDialog.md) | Creates a new FileDialog object which provides the ability to show a standard file selection dialog to the user. |
| [createFolderDialog](UserInterface_createFolderDialog.md) | Creates a new FolderDialog object which provides the ability to show a standard folder selection dialog to the user. |
| [createProgressDialog](UserInterface_createProgressDialog.md) | Creates a new ProgressDialog object that you can use to display and control a progress dialog. |
| [getText](UserInterface_getText.md) | Get the localized text for a specific application text string. The strings used by Fusion are stored in localized XML files that are installed with Fusion. On Windows, you can find them here: %LocalAppData%\Autodesk\webdeploy\production\VERSION_CODE\StringTable And on Mac, you can find them here: ~/Library/Application Support/Autodesk/webdeploy/production/VERSION_CODE/Autodesk Fusion.app/Contents/Libraries/Neutron/StringTable There is a folder for each language that Fusion supports, and the strings for that language are defined in files within that folder. Fusion will use the language specified by the user in their preferences. |
| [inputBox](UserInterface_inputBox.md) | Displays a modal dialog to get string input from the user. |
| [messageBox](UserInterface_messageBox.md) | Display a modal message box with the provided text. |
| [selectEntity](UserInterface_selectEntity.md) | Supports the selection of a single entity. This provides a simple way to prompt the user for for a selection in a script. If you need more control over the selection a command should be created and a SelectionCommandInput used. |
| [terminateActiveCommand](UserInterface_terminateActiveCommand.md) | Method that causes the currently active (running) command to be terminated |
| [toolbarPanelsByProductType](UserInterface_toolbarPanelsByProductType.md) | Gets all of the toolbar panels associated with the specified product. |
| [toolbarTabsByProductType](UserInterface_toolbarTabsByProductType.md) | Gets all of the toolbar tabs associated with the specified product. |
| [workspacesByProductType](UserInterface_workspacesByProductType.md) | Returns all of the workspaces associated with the specified product. |

## Properties

| Name | Description |
| --- | --- |
| [activeCommand](UserInterface_activeCommand.md) | Gets the id of the command definition from the active command (the one that is currently running) |
| [activeSelections](UserInterface_activeSelections.md) | Gets the current set of selected objects. |
| [activeToolbar](UserInterface_activeToolbar.md) | Retrieve the active Toolbar being displayed in the user interface. |
| [activeToolbarTab](UserInterface_activeToolbarTab.md) | Retrieve the active ToolbarTab being displayed in the user interface. This may be null. |
| [activeWorkspace](UserInterface_activeWorkspace.md) | Gets the active workspace. The active workspace is the one currently active in the user interface. This can be null if there is no active product. |
| [allToolbarPanels](UserInterface_allToolbarPanels.md) | Gets all of the toolbar panels. This returns all of the panels available, regardless of which workspace or product they're associated with. |
| [allToolbarTabs](UserInterface_allToolbarTabs.md) | Gets all of the toolbar tabs. This returns all of the tabs available, regardless of which workspace or product they're associated with. |
| [commandDefinitions](UserInterface_commandDefinitions.md) | Gets all of the command definitions currently defined. This is all command definitions both internal and those defined through the API. |
| [isTabbedToolbarUI](UserInterface_isTabbedToolbarUI.md) | Returns true if Tabbed Toolbars are being used. |
| [isUIEnabled](UserInterface_isUIEnabled.md) | Gets and sets if the Fusion user interface is enabled or not. By default it is enabled allowing the user to interact with Fusion. When set to false, the UI is disabled which blocks all interaction, including running commands, manipulating the view and interacting with the browser. |
| [isValid](UserInterface_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](UserInterface_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [palettes](UserInterface_palettes.md) | Returns the collection object that provides access to all of the existing palettes and provides the functionality to create new custom palettes. |
| [progressBar](UserInterface_progressBar.md) | Gets the ProgressBar object that can be used to display a progress bar in the lower-right corner of the Fusion window. |
| [statusMessage](UserInterface_statusMessage.md) | Gets and sets the current message displayed in the lower-right corner of the Fusion window. This is useful when displaying progress information to the user for the current process. Set the value to an empty string to remove the message. The lifetime of your message is indeterminant because Fusion uses the same field to display messages. If your process is running in the main thread of Fusion, you will need to call adsk.doEvents to give control back to Fusion, so it can update the UI. The ProgressBar can also be used as a way to communicate to the user the current progress of a running process. |
| [toolbars](UserInterface_toolbars.md) | Gets a collection that provides access to the toolbars. This includes the left and right QAT, and the Navbar. |
| [workspaces](UserInterface_workspaces.md) | Gets all of the workspaces currently available. |

## Events

| Name | Description |
| --- | --- |
| [activeSelectionChanged](UserInterface_activeSelectionChanged.md) | This event fires whenever the contents of the active selection changes. This occurs as the user selects or unselects entities while using the Fusion Select command. The Select command is the default command that is always running if no other command is active. Pressing Escape terminates the currently active command and starts the Select command. If the Select command is running and you press Escape, it terminates the current Select command and starts a new one. This event is only associated with the selection associated with the Select command and does not fire when any other command is running. The event fires when there is any change to the active selection, including when the selection is cleared when the Select command is terminated. It is also fired when the user clicks in an open area of the canvas to clear the current selection. |
| [commandCreated](UserInterface_commandCreated.md) | The commandCreated event fires immediately after the command is created. |
| [commandStarting](UserInterface_commandStarting.md) | The commandStarting event fires when a request for a command to be executed has been received but before the command is executed. Through this event, it's possible to cancel the command from being executed. |
| [commandTerminated](UserInterface_commandTerminated.md) | Gets an event that is fired when a command is terminated. |
| [markingMenuDisplaying](UserInterface_markingMenuDisplaying.md) | The markingMenuDisplaying event fires just before the marking menu and context menus are displayed. The marking menu is the round menu displayed when the user right-clicks the mouse within Fusion. The context menu is the vertical menu displayed. The event provides both the marking menu and the context menu so you can examine and edit the contents of either one or both of them before they are displayed. Fusion will then display the marking and context menu that you've customized. If either one is empty it will not be displayed. |
| [workspaceActivated](UserInterface_workspaceActivated.md) | The workspaceActivated event fires at the VERY end of a workspace being activated. The client can add or remove WorkspaceEventHandlers from the WorkspaceEvent. |
| [workspaceDeactivated](UserInterface_workspaceDeactivated.md) | The workspaceDeactivated event fires at the VERY end of a workspace being deactivated. The client can add or remove WorkspaceEventHandlers from the WorkspaceEvent. |
| [workspacePreActivate](UserInterface_workspacePreActivate.md) | The workspacePreActivate event fires at the VERY start of a workspace being activated. The client can add or remove WorkspaceEventHandlers from the WorkspaceEvent. |
| [workspacePreDeactivate](UserInterface_workspacePreDeactivate.md) | The workspacePreDeactivate event fires at the VERY start of a workspace being deactivated. The client can add or remove WorkspaceEventHandlers from the WorkspaceEvent. |

## Accessed From

[Application.userInterface](Application_userInterface.md), [Toolbar.parentUserInterface](Toolbar_parentUserInterface.md), [ToolbarPanel.parentUserInterface](ToolbarPanel_parentUserInterface.md), [ToolbarTab.parentUserInterface](ToolbarTab_parentUserInterface.md)

## Samples

| Name | Description |
| --- | --- |
| [Palette Sample](PaletteSample_Sample.md) | Demonstrates how to create a palette, how to dock and snap palettes and how Fusion communicates with the palette HTML. The sample is an add-in. To use it, create a new Python add-in and replace the code with the code below. You also need to create an html file using the name and code below. The html file needs to be in the same folder as the py file. When you load the add-in, you'll see two new commands under the ADD-INS panel of the TOOLS tab. The "Show Custom Palette" command will cause the custom palette to be displayed. It will remain displayed until you click its Close button. Clicking the "Click to send info to Fusion" button on the palette, will send information to your add-in, which uses the API to display that information in a message box. Running the "Send Info to HTML" command to send data to the javascript running in the palette, which uses it to update the content of a paragraph. palette.html      Click the button below to send data to Fusion. Click to send info to Fusion Run the "Send Info to HTML" command in the ADD-INS panel to update this text.      function sendInfoToFusion(){ var today = new Date(); var dd = String(today.getDate()).padStart(2, '0'); var mm = String(today.getMonth() + 1).padStart(2, '0'); var yyyy = today.getFullYear(); var hours = String(today.getHours()).padStart(2, '0'); var minutes = String(today.getMinutes()).padStart(2, '0'); var seconds = String(today.getSeconds()).padStart(2, '0'); var date = dd + '/' + mm + '/' + yyyy; var time = hours + ':' + minutes + ':' + seconds; var args = { arg1 : "Sample argument 1", arg2 : "Sample argument 2" }; adsk.fusionSendData('send', JSON.stringify(args)); } window.fusionJavaScriptHandler = {handle: function(action, data){ try { if (action == 'send') { // Update a paragraph with the data passed in. document.getElementById('p1').innerHTML = data; } else if (action == 'debugger') { debugger; } else { return 'Unexpected command type: ' + action; } } catch (e) { console.log(e); console.log('exception caught with command: ' + action + ', data: ' + data); } return 'OK'; }};   |
| [Customizing the UI using the API Sample](UICustomizationSample_Sample.md) | Demonstrates how to work with tabs, panels, and command in the user interface. The full source for [C++](../ExtraFiles/UICustomizationSampleCPP.zip) and [Python](../ExtraFiles/UICustomizationSamplePython.zip) samples can be downloaded. This is especially useful for getting the resource files. |
| [Write user interface to a file API Sample](WriteUserInterfaceToFile_Sample.md) | Writes out the full structure of the Fusion user interface. This information is useful when editing the user-interface, as discussed in the usre manual topic [User-Interface Customization with Fusion's API](UserInterface_UM.md) |

## Version

Introduced in version August 2014  

