# CommandInputs.addTriadCommandInput Method

Parent Object: [CommandInputs](CommandInputs.md)  

## Description

Adds a new triad command input to the command. The input is initially invisible to allow you to define the desired behavior and then set the isVisible property to true when you're ready to display the triad.  

The creation of a triad command input results in displaying many input fields in the command dialog. For example, there can be individual fields for the X, Y, and Z offset distances, the X, Y, and Z scales, the X, Y, and Z angles, etc. You control which fields are visible by setting properties on the returned TriadCommandInput. Even though each of these appears as an individual input in the command dialog, and they are all associated with the single TriadCommandInput object. It also results in graphics widgets being displayed to allow the user to define the values graphically.  

When a new triad is created, it displays all inputs except those that control scaling. You can use the properties on the returned triad to define the inputs you want to display further.  

To simplify your command dialog it can be useful put the TriadCommandInput within a GroupCommandInput so it's apparent to the user these items are related and they can be collapsed to reduce clutter in the dialog. This also allows you to label the set of displayed inputs by using the name of the GroupCommandInput.

## Syntax

"commandInputs_var" is a variable referencing a [CommandInputs](CommandInputs.md) object.

```python
returnValue = commandInputs_var.addTriadCommandInput(id, transform)
```

## Return Value

| Type | Description |
|----|----|
| [TriadCommandInput](TriadCommandInput.md) | Returns the created TriadCommandInput object or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| id | string | The unique ID of this command input. It must be unique with respect to the other inputs associated with this command. |
| transform | [Matrix3D](Matrix3D.md) | Defines the initial position and orientation of the manipulator. |

## Version

Introduced in version May 2022  

