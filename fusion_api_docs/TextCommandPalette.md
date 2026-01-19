# TextCommandPalette Object

Derived from: [Palette](Palette.md) Object  

## Description

Represents the palette that is the Text Command window in Fusion.

## Remarks

You can obtain the Text Command palette by using the itemById method of the Palettes object and using "TextCommands" as the ID. Below is some sample code that illustrates making sure the palette is visible and writing some text to it.

```python
# Get the palette that represents the TEXT COMMANDS window.
textPalette = ui.palettes.itemById('TextCommands')

# Make sure the palette is visible.
if not textPalette.isVisible:
   textPalette.isVisible = True

# Write some text.
textPalette.writeText('This is a text message.') 
```

## Methods

| Name | Description |
| --- | --- |
| [classType](TextCommandPalette_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [deleteMe](TextCommandPalette_deleteMe.md) | Deletes this palette. Fusion native palettes cannot be deleted. Use the isNative property to determine if this is a native or API created palette. |
| [sendInfoToHTML](TextCommandPalette_sendInfoToHTML.md) | Sends the string to the JavaScript associated with the loaded HTML. |
| [setMaximumSize](TextCommandPalette_setMaximumSize.md) | Sets the maximum size of the palette. The user cannot resize it to be larger than this size. This does not change the current size of the palette unless the palette is already larger than this size. Calling this method and setting the width and height to zero, removes the maximum size restriction. |
| [setMinimumSize](TextCommandPalette_setMinimumSize.md) | Sets the minimum size of the palette. The user cannot resize it to be smaller than this size. This does not change the current size of the palette unless the palette is already smaller than this size. Calling this method and setting the width and height to zero, removes the minimum size restriction. |
| [setPosition](TextCommandPalette_setPosition.md) | Sets the position of the palette. If the palette is docked or snapped, this will result in changing it to be floating. |
| [setSize](TextCommandPalette_setSize.md) | Sets the size of the palette. This is best used for a floating palette because either the width or height can be locked when a palette is docked. |
| [snapTo](TextCommandPalette_snapTo.md) | Snaps this palette to another palette. |
| [writeText](TextCommandPalette_writeText.md) | Write the specified text to the TEXT COMMAND window. |

## Properties

| Name | Description |
| --- | --- |
| [dockingOption](TextCommandPalette_dockingOption.md) | Defines the docking behavior for this palette. This controls how the user is allowed to dock the palette. |
| [dockingState](TextCommandPalette_dockingState.md) | Gets and sets how the palette is currently docked. |
| [height](TextCommandPalette_height.md) | Gets and sets the height of the palette. Setting this property may not always set the height. Depending on how the palette is docked or snapped, the height may not be editable. |
| [htmlFileURL](TextCommandPalette_htmlFileURL.md) | Gets and sets the URL to the HTML file that will be displayed in the palette. This can be a local file or a URL on the web where the HTML will be read. To avoid reading a file, this can also be the full HTML definition as a string. If you are providing the HTML content as a string, it should begin with the element. Any references made in the HTML should be to URL's and not local files since the local path is ambiguous. |
| [id](TextCommandPalette_id.md) | Gets The unique, language independent, ID of this palette. |
| [isNative](TextCommandPalette_isNative.md) | Indicates if this is one of the standard Fusion palettes or a custom palette created through the API. If true, it is a standard Fusion palette and will have some restrictions on changing its properties and cannot be deleted. |
| [isTransparent](TextCommandPalette_isTransparent.md) | Returns if this palette was created as a transparent palette. |
| [isValid](TextCommandPalette_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [isVisible](TextCommandPalette_isVisible.md) | Gets and sets whether this palette is currently being displayed in the user interface. |
| [left](TextCommandPalette_left.md) | Gets and sets the left side of the palette relative to screen space and in pixels. Because palettes can be positioned outside of the Fusion window, a value of zero indicates the left side of the screen and not the Fusion window. |
| [name](TextCommandPalette_name.md) | Gets and set the name of the palette as seen in the user interface. The name of native palettes cannot be set. |
| [objectType](TextCommandPalette_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [top](TextCommandPalette_top.md) | Gets and sets the top of the palette relative to screen space and in pixels. Because palettes can be positioned outside of the Fusion window, a value of zero indicates the top of the screen and not the Fusion window. |
| [width](TextCommandPalette_width.md) | Gets and sets the width of the palette. Setting this property may not always set the width. Depending on how the palette is docked or snapped, the width may not be editable. |

## Events

| Name | Description |
|----|----|
| [closed](TextCommandPalette_closed.md) | This event is fired when the user clicks the "Close" button on the palette. You can choose if the "Close" button is available or not when you initially create the palette. When a palette is closed, it still exists but is change to invisible so you can still interact with it and retrieve any needed information and can make it visible again. Use the deleteMe method to delete the palette. |
| [incomingFromHTML](TextCommandPalette_incomingFromHTML.md) | This event is fired when the JavaScript associated with the HTML calls the adsk.fusionSendData function. This allows the HTML to communicate with the add-in by passing information to the add-in. |
| [navigatingURL](TextCommandPalette_navigatingURL.md) | This event is fired when a navigation event occurs on the page. This allows the add-in to determine how this navigation should be handled by the browser. |

## Samples

| Name | Description |
|----|----|
| [Customizing the UI using the API Sample](UICustomizationSample_Sample.md) | Demonstrates how to work with tabs, panels, and command in the user interface. The full source for [C++](../ExtraFiles/UICustomizationSampleCPP.zip) and [Python](../ExtraFiles/UICustomizationSamplePython.zip) samples can be downloaded. This is especially useful for getting the resource files. |

## Version

Introduced in version August 2017  

