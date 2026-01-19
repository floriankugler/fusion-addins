# CommandInputs Object

Derived from: [Base](Base.md) Object  

## Description

Provides access to the set of inputs for a command. Command inputs are used to gather inputs from the user when a command is executed. The set of inputs used by a command are created and added to the command with the methods in this class.

## Methods

| Name | Description |
| --- | --- |
| [addAngleValueCommandInput](CommandInputs_addAngleValueCommandInput.md) | Adds a new angle value input to the command. This displays a field in the command dialog where an angle value can be entered. It displays the angle in the dialog using degrees. There is also a graphical manipulator associated with the input to allow the user to graphically set the value. You use the setManipulator method of the returned AngleValueCommandInput object to define the position and orientation of the manipulator. |
| [addBoolValueInput](CommandInputs_addBoolValueInput.md) | Adds a new boolean input to the command. The input can be shown as a check box or a button. If it's a button you need to specify the resource folder to define the icon to use. Buttons don't have an up or down state but can just be clicked. |
| [addBrowserCommandInput](CommandInputs_addBrowserCommandInput.md) | Adds a new command input to the command that behaves as a browser. |
| [addButtonRowCommandInput](CommandInputs_addButtonRowCommandInput.md) | Adds a new row of buttons as a command input. Depending on the isMultiSelectEnabled argument it can act like an option list where only a single button on the row can be selected at a time or multiple buttons can be selected. The buttons are defined by using the returned ButtonRowCommandInput object. |
| [addDirectionCommandInput](CommandInputs_addDirectionCommandInput.md) | Adds a new direction command input to the command. The input can be shown as a check box or a button. If it's a button you need to specify the resource folder to define the icon to use for the Button. |
| [addDistanceValueCommandInput](CommandInputs_addDistanceValueCommandInput.md) | Adds a new distance value input to the command. This displays a field in the command dialog where a distance value can be entered. It displays the distance in the dialog using current document default unit. There is also a graphical manipulator associated with the input. You use the setManipulator method of the returned DistanceValueCommandInput object to define the position and orientation of the manipulator. |
| [addDropDownCommandInput](CommandInputs_addDropDownCommandInput.md) | Adds a new empty drop-down input to the command. drop-downs of various types are supported. To add items to the drop down use the returned DropDownCommandInput object. |
| [addFloatSliderCommandInput](CommandInputs_addFloatSliderCommandInput.md) | Adds a new slider input to the command. The value type is double. |
| [addFloatSliderListCommandInput](CommandInputs_addFloatSliderListCommandInput.md) | Adds a new slider input to the command. The value type is float. |
| [addFloatSpinnerCommandInput](CommandInputs_addFloatSpinnerCommandInput.md) | Adds a new spinner input to the command. The value type is float. |
| [addGroupCommandInput](CommandInputs_addGroupCommandInput.md) | Adds a new Group input to the command. Group Command inputs organize a set of command inputs into a collapsible list within a command dialog. |
| [addImageCommandInput](CommandInputs_addImageCommandInput.md) | Adds a new Image input to the command. |
| [addIntegerSliderCommandInput](CommandInputs_addIntegerSliderCommandInput.md) | Adds a new slider input to the command. The value type is integer. |
| [addIntegerSliderListCommandInput](CommandInputs_addIntegerSliderListCommandInput.md) | Adds a new slider input to the command. The value type is integer. |
| [addIntegerSpinnerCommandInput](CommandInputs_addIntegerSpinnerCommandInput.md) | Adds a new spinner input to the command. The value type is integer. |
| [addRadioButtonGroupCommandInput](CommandInputs_addRadioButtonGroupCommandInput.md) | Adds a new Radio Button Group input to the command. |
| [addSelectionInput](CommandInputs_addSelectionInput.md) | Adds a new selection input to the command. This allows you to get entity selections from the user. The default behavior is that only one entity can be selected and it can be of any type. To change the selection behavior to select specific types and control the number of items selected use the methods and properties on the returned SelectionCommandInput object. You can also use the selectionEvent event that's associated with the command to have additional control over the selection process. |
| [addSeparatorCommandInput](CommandInputs_addSeparatorCommandInput.md) | Adds a new Separator input to the command. A separator input is for visual purposes only and creates a line in the dialog providing a visual separation between the command inputs above and below where the separator is inserted. |
| [addStringValueInput](CommandInputs_addStringValueInput.md) | Adds a new string input to the command. |
| [addTabCommandInput](CommandInputs_addTabCommandInput.md) | Adds a new Tab input to the command. Tab command inputs contain a set of command inputs and/or group command inputs |
| [addTableCommandInput](CommandInputs_addTableCommandInput.md) | Adds a new table command input to the command. |
| [addTextBoxCommandInput](CommandInputs_addTextBoxCommandInput.md) | Adds a text box input to the command. |
| [addTriadCommandInput](CommandInputs_addTriadCommandInput.md) | Adds a new triad command input to the command. The input is initially invisible to allow you to define the desired behavior and then set the isVisible property to true when you're ready to display the triad. The creation of a triad command input results in displaying many input fields in the command dialog. For example, there can be individual fields for the X, Y, and Z offset distances, the X, Y, and Z scales, the X, Y, and Z angles, etc. You control which fields are visible by setting properties on the returned TriadCommandInput. Even though each of these appears as an individual input in the command dialog, and they are all associated with the single TriadCommandInput object. It also results in graphics widgets being displayed to allow the user to define the values graphically. When a new triad is created, it displays all inputs except those that control scaling. You can use the properties on the returned triad to define the inputs you want to display further. To simplify your command dialog it can be useful put the TriadCommandInput within a GroupCommandInput so it's apparent to the user these items are related and they can be collapsed to reduce clutter in the dialog. This also allows you to label the set of displayed inputs by using the name of the GroupCommandInput. |
| [addValueInput](CommandInputs_addValueInput.md) | Adds a new value input to the command. |
| [classType](CommandInputs_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [item](CommandInputs_item.md) | Returns the specified command input using an index into the collection. |
| [itemById](CommandInputs_itemById.md) | Returns the command input that has the specified ID. |

## Properties

| Name | Description |
| --- | --- |
| [command](CommandInputs_command.md) | Gets the parent Command object. |
| [count](CommandInputs_count.md) | Gets the number of inputs. |
| [isValid](CommandInputs_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](CommandInputs_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[AngleValueCommandInput.commandInputs](AngleValueCommandInput_commandInputs.md), [BoolValueCommandInput.commandInputs](BoolValueCommandInput_commandInputs.md), [BrowserCommandInput.commandInputs](BrowserCommandInput_commandInputs.md), [ButtonRowCommandInput.commandInputs](ButtonRowCommandInput_commandInputs.md), [Command.commandInputs](Command_commandInputs.md), [CommandInput.commandInputs](CommandInput_commandInputs.md), [DirectionCommandInput.commandInputs](DirectionCommandInput_commandInputs.md), [DistanceValueCommandInput.commandInputs](DistanceValueCommandInput_commandInputs.md), [DropDownCommandInput.commandInputs](DropDownCommandInput_commandInputs.md), [FloatSliderCommandInput.commandInputs](FloatSliderCommandInput_commandInputs.md), [FloatSpinnerCommandInput.commandInputs](FloatSpinnerCommandInput_commandInputs.md), [GroupCommandInput.children](GroupCommandInput_children.md), [GroupCommandInput.commandInputs](GroupCommandInput_commandInputs.md), [ImageCommandInput.commandInputs](ImageCommandInput_commandInputs.md), [InputChangedEventArgs.inputs](InputChangedEventArgs_inputs.md), [IntegerSliderCommandInput.commandInputs](IntegerSliderCommandInput_commandInputs.md), [IntegerSpinnerCommandInput.commandInputs](IntegerSpinnerCommandInput_commandInputs.md), [RadioButtonGroupCommandInput.commandInputs](RadioButtonGroupCommandInput_commandInputs.md), [SelectionCommandInput.commandInputs](SelectionCommandInput_commandInputs.md), [SeparatorCommandInput.commandInputs](SeparatorCommandInput_commandInputs.md), [SliderCommandInput.commandInputs](SliderCommandInput_commandInputs.md), [StringValueCommandInput.commandInputs](StringValueCommandInput_commandInputs.md), [TabCommandInput.children](TabCommandInput_children.md), [TabCommandInput.commandInputs](TabCommandInput_commandInputs.md), [TableCommandInput.commandInputs](TableCommandInput_commandInputs.md), [TextBoxCommandInput.commandInputs](TextBoxCommandInput_commandInputs.md), [TriadCommandInput.commandInputs](TriadCommandInput_commandInputs.md), [ValidateInputsEventArgs.inputs](ValidateInputsEventArgs_inputs.md), [ValueCommandInput.commandInputs](ValueCommandInput_commandInputs.md)

## Samples

| Name | Description |
| --- | --- |
| [Command Inputs API Sample](CommandInputsSample_Sample.md) | Creates a command dialog that demonstrates all of the available command inputs. To use the sample, create a new Python or C++ script and copy and paste this code, replacing the default code. You also need to unpack this zip file which contains a [resource folder](../ExtraFiles/CommandInputsResources.zip) into the same folder where the source code file (.py or .cpp) is. |

## Version

Introduced in version August 2014  

