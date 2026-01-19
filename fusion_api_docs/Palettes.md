# Palettes Object

Derived from: [Base](Base.md) Object  

## Description

Provides access to a set of palettes, which are docked or floating windows that display HTML.

## Methods

| Name | Description |
|----|----|
| [add](Palettes_add.md) | Creates a new Palette. |
| [add2](Palettes_add2.md) | Creates a new Palette. |
| [addTransparent](Palettes_addTransparent.md) | Creates a new transparent Palette. |
| [classType](Palettes_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [item](Palettes_item.md) | Returns the specified palette using an index into the collection. |
| [itemById](Palettes_itemById.md) | Returns the palette at the specified ID. |

## Properties

| Name | Description |
| --- | --- |
| [count](Palettes_count.md) | Gets the number of Palettes. |
| [isValid](Palettes_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](Palettes_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[UserInterface.palettes](UserInterface_palettes.md)

## Samples

| Name | Description |
| --- | --- |
| [Palette Sample](PaletteSample_Sample.md) | Demonstrates how to create a palette, how to dock and snap palettes and how Fusion communicates with the palette HTML. The sample is an add-in. To use it, create a new Python add-in and replace the code with the code below. You also need to create an html file using the name and code below. The html file needs to be in the same folder as the py file. When you load the add-in, you'll see two new commands under the ADD-INS panel of the TOOLS tab. The "Show Custom Palette" command will cause the custom palette to be displayed. It will remain displayed until you click its Close button. Clicking the "Click to send info to Fusion" button on the palette, will send information to your add-in, which uses the API to display that information in a message box. Running the "Send Info to HTML" command to send data to the javascript running in the palette, which uses it to update the content of a paragraph. palette.html      Click the button below to send data to Fusion. Click to send info to Fusion Run the "Send Info to HTML" command in the ADD-INS panel to update this text.      function sendInfoToFusion(){ var today = new Date(); var dd = String(today.getDate()).padStart(2, '0'); var mm = String(today.getMonth() + 1).padStart(2, '0'); var yyyy = today.getFullYear(); var hours = String(today.getHours()).padStart(2, '0'); var minutes = String(today.getMinutes()).padStart(2, '0'); var seconds = String(today.getSeconds()).padStart(2, '0'); var date = dd + '/' + mm + '/' + yyyy; var time = hours + ':' + minutes + ':' + seconds; var args = { arg1 : "Sample argument 1", arg2 : "Sample argument 2" }; adsk.fusionSendData('send', JSON.stringify(args)); } window.fusionJavaScriptHandler = {handle: function(action, data){ try { if (action == 'send') { // Update a paragraph with the data passed in. document.getElementById('p1').innerHTML = data; } else if (action == 'debugger') { debugger; } else { return 'Unexpected command type: ' + action; } } catch (e) { console.log(e); console.log('exception caught with command: ' + action + ', data: ' + data); } return 'OK'; }};   |

## Version

Introduced in version March 2017  

