# CommandControl Object

Derived from: [ToolbarControl](ToolbarControl.md) Object  

## Description

Represents a button, check box, or radio control list in a panel, toolbar, or drop-down.

## Methods

| Name | Description |
|----|----|
| [classType](CommandControl_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [deleteMe](CommandControl_deleteMe.md) | Deletes the ToolbarControl |
| [promote](CommandControl_promote.md) | Promote the command to the parent panel and optionally position it relative to an already- promoted control. |

## Properties

| Name | Description |
| --- | --- |
| [commandDefinition](CommandControl_commandDefinition.md) | Gets the command definition associated with this button. The command definition defines all of the resource information used to display this button and receives the event when the button is clicked. |
| [id](CommandControl_id.md) | Gets the unique ID of this control. The ID is unique with respect to the other controls within the same panel, toolbar, or drop-down control. |
| [index](CommandControl_index.md) | Gets the position of this control within the list of controls within the panel, toolbar, or drop-down control. |
| [isPromoted](CommandControl_isPromoted.md) | Gets or sets if this command has been promoted to the parent panel. This property is ignored in the case where this control isn't in a panel. The promote method provides more options over how the control is promoted. |
| [isPromotedByDefault](CommandControl_isPromotedByDefault.md) | Gets or sets if this command is a default command in the panel. This defines the default state of the panel if the UI is reset. This property is ignored in the case where this control isn't in a panel. The promote method provides more options over how the control is promoted. |
| [isValid](CommandControl_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [isVisible](CommandControl_isVisible.md) | Gets or sets if this control is currently visible. |
| [objectType](CommandControl_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [parent](CommandControl_parent.md) | Gets the Parent object. When associated with a toolbar (right or left QAT or the NavBar) this returns the parent Toolbar object. When associated with a panel it returns the parent ToolbarPanel object. When associated with a control (DropDownControl) it returns the parent control. |

## Accessed From

[ToolbarControls.addCommand](ToolbarControls_addCommand.md)

## Version

Introduced in version August 2014  

