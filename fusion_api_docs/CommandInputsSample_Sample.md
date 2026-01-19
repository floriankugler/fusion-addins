# Command Inputs API Sample

## Description

Creates a command dialog that demonstrates all of the available command inputs.

To use the sample, create a new Python or C++ script and copy and paste this code, replacing the default code. You also need to unpack this zip file which contains a [resource folder](../ExtraFiles/CommandInputsResources.zip) into the same folder where the source code file (.py or .cpp) is.

## Code Samples

";
                tab1ChildInputs->addTextBoxCommandInput("fullWidth_textBox", "", message, 1, true);

                // Create a selection input.
                Ptr selectionInput =
                    tab1ChildInputs->addSelectionInput("selection", "Select", "Basic select command input");
                if (!selectionInput)
                    return;
                selectionInput->setSelectionLimits(0);

                // Create string value input.
                Ptr strInput =
                    tab1ChildInputs->addStringValueInput("string", "Text", "Basic string command input");

                // Create value input.
                tab1ChildInputs->addValueInput("value", "Value", "cm", ValueInput::createByReal(0.0));

                // Create bool value input with checkbox style.
                tab1ChildInputs->addBoolValueInput("checkbox", "Checkbox", true, "", false);

                // Create bool value input with button style that can be clicked.
                tab1ChildInputs->addBoolValueInput("buttonClick", "Click Button", false, "resources/button", true);

                // Create bool value input with button style that has a state.
                tab1ChildInputs->addBoolValueInput("buttonState", "State Button", true, "resources/button", true);

                // Create float slider input with two sliders.
                tab1ChildInputs->addFloatSliderCommandInput("floatSlider", "Float Slider", "cm", 0, 10.0, true);

                // Create float slider input with two sliders and a value list
                std::vector floatValueList;
                floatValueList.push_back(1.0);
                floatValueList.push_back(3.0);
                floatValueList.push_back(4.0);
                floatValueList.push_back(7.0);
                tab1ChildInputs->addFloatSliderListCommandInput("floatSlider2", "Float Slider 2", "cm", floatValueList);

                // Create float slider input with two sliders and visible texts
                Ptr floatSlider3 =
                    tab1ChildInputs->addFloatSliderCommandInput("floatSlider3", "Float Slider 3", "", 0, 50.0, false);
                if (!floatSlider3)
                    return;
                floatSlider3->setText("Min", "Max");

                // Create integer slider input with one slider
                tab1ChildInputs->addIntegerSliderCommandInput("intSlider", "Integer Slider", 0, 10);

                // Create integer slider input with two sliders and a value list
                std::vector valueList;
                valueList.push_back(1);
                valueList.push_back(3);
                valueList.push_back(4);
                valueList.push_back(7);
                valueList.push_back(11);
                tab1ChildInputs->addIntegerSliderListCommandInput("intSlider2", "Integer Slider 2", valueList);

                // Create float spinner input.
                tab1ChildInputs->addFloatSpinnerCommandInput("spinnerFloat", "Float Spinner", "cm", 0.2, 9.0, 2.2, 1);

                // Create integer spinner input.
                tab1ChildInputs->addIntegerSpinnerCommandInput("spinnerInt", "Integer Spinner", 2, 9, 2, 3);

                // Create dropdown input with checkbox style.
                Ptr dropdownInput = tab1ChildInputs->addDropDownCommandInput(
                    "dropdown", "Dropdown 1", DropDownStyles::CheckBoxDropDownStyle);
                if (!dropdownInput)
                    return;
                Ptr dropdownItems = dropdownInput->listItems();
                if (!dropdownItems)
                    return;
                dropdownItems->add("Item 1", false, "resources/One");
                dropdownItems->add("Item 2", false, "resources/Two");

                // Create dropdown input with icon style.
                Ptr dropdownInput2 = tab1ChildInputs->addDropDownCommandInput(
                    "dropdown2", "Dropdown 2", DropDownStyles::LabeledIconDropDownStyle);
                if (!dropdownInput2)
                    return;
                Ptr dropdown2Items = dropdownInput2->listItems();
                if (!dropdown2Items)
                    return;
                dropdown2Items->add("Item 1", true, "resources/One");
                dropdown2Items->add("Item 2", false, "resources/Two");

                // Create dropdown input with radio style.
                Ptr dropdownInput3 = tab1ChildInputs->addDropDownCommandInput(
                    "dropdown3", "Dropdown 3", DropDownStyles::LabeledIconDropDownStyle);
                if (!dropdownInput3)
                    return;
                Ptr dropdown3Items = dropdownInput3->listItems();
                if (!dropdown3Items)
                    return;
                dropdown3Items->add("Item 1", true, "");
                dropdown3Items->add("Item 2", false, "");

                // Create dropdown input with test list style.
                Ptr dropdownInput4 = tab1ChildInputs->addDropDownCommandInput(
                    "dropdown4", "Dropdown 4", DropDownStyles::TextListDropDownStyle);
                if (!dropdownInput4)
                    return;
                Ptr dropdown4Items = dropdownInput4->listItems();
                if (!dropdown4Items)
                    return;
                dropdown4Items->add("Item 1", true, "");
                dropdown4Items->add("Item 2", false, "");

                // Create single selectable button row input.
                Ptr buttonRowInput =
                    tab1ChildInputs->addButtonRowCommandInput("buttonRow", "Button Row 1", false);
                if (!buttonRowInput)
                    return;
                Ptr buttonRowItems = buttonRowInput->listItems();
                if (!buttonRowItems)
                    return;
                buttonRowItems->add("Item 1", false, "resources/One");
                buttonRowItems->add("Item 2", false, "resources/Two");

                // Create multi selectable button row input.
                Ptr buttonRowInput2 =
                    tab1ChildInputs->addButtonRowCommandInput("buttonRow2", "Button Row 2", true);
                if (!buttonRowInput2)
                    return;
                Ptr buttonRow2Items = buttonRowInput2->listItems();
                if (!buttonRow2Items)
                    return;
                buttonRow2Items->add("Item 1", false, "resources/One");
                buttonRow2Items->add("Item 2", false, "resources/Two");

                // Create tab input 2.
                Ptr tabCmdInput2 = inputs->addTabCommandInput("tab_2", "Tab 2");
                if (!tabCmdInput2)
                    return;
                Ptr tab2ChildInputs = tabCmdInput2->children();
                if (!tab2ChildInputs)
                    return;

                // Create group input.
                Ptr groupCmdInput = tab2ChildInputs->addGroupCommandInput("group", "Group");
                if (!groupCmdInput)
                    return;
                groupCmdInput->isExpanded(true);
                groupCmdInput->isEnabledCheckBoxDisplayed(true);
                Ptr groupChildInputs = groupCmdInput->children();
                if (!groupChildInputs)
                    return;

                // Create radio button group input.
                Ptr radioButtonGroup =
                    groupChildInputs->addRadioButtonGroupCommandInput("radioButtonGroup", "Radio button group");
                if (!radioButtonGroup)
                    return;
                Ptr radioButtonItems = radioButtonGroup->listItems();
                if (!radioButtonItems)
                    return;
                radioButtonItems->add("Item 1", false);
                radioButtonItems->add("Item 2", false);
                radioButtonItems->add("Item 3", false);

                // Create image input
                Ptr imageCmdInput =
                    groupChildInputs->addImageCommandInput("image", "Image", "resources/image.png");
                if (!imageCmdInput)
                    return;

                // Create direction input 1.
                Ptr directionCmdInput =
                    tab2ChildInputs->addDirectionCommandInput("direction", "Direction");
                if (!directionCmdInput)
                    return;
                directionCmdInput->setManipulator(Point3D::create(0, 0, 0), Vector3D::create(1, 0, 0));

                // Create direction input 2.
                Ptr directionCmdInput2 =
                    tab2ChildInputs->addDirectionCommandInput("direction2", "Direction 2", "resources/One");
                if (!directionCmdInput2)
                    return;
                directionCmdInput2->setManipulator(Point3D::create(0, 0, 0), Vector3D::create(0, 1, 0));
                directionCmdInput2->isDirectionFlipped(true);

                // Create distance value input 1.
                Ptr distanceValueInput = tab2ChildInputs->addDistanceValueCommandInput(
                    "distanceValue", "Distance Value", ValueInput::createByReal(2));
                if (!distanceValueInput)
                    return;
                distanceValueInput->setManipulator(Point3D::create(0, 0, 0), Vector3D::create(1, 0, 0));
                distanceValueInput->minimumValue(0);
                distanceValueInput->isMinimumValueInclusive(true);
                distanceValueInput->maximumValue(10);
                distanceValueInput->isMaximumValueInclusive(true);

                // Create distance value input 2.
                Ptr distanceValueInput2 = tab2ChildInputs->addDistanceValueCommandInput(
                    "distanceValue2", "DistanceValue 2", ValueInput::createByReal(1));
                if (!distanceValueInput2)
                    return;
                distanceValueInput2->setManipulator(Point3D::create(0, 0, 0), Vector3D::create(0, 1, 0));
                distanceValueInput2->expression("1 in");
                distanceValueInput2->hasMinimumValue(false);
                distanceValueInput2->hasMaximumValue(false);

                // Create table input.
                Ptr tableInput = tab2ChildInputs->addTableCommandInput("table", "Table", 3, "1:1:1");
                addRowToTable(tableInput);

                // Add inputs into the table.
                Ptr addButtonInput =
                    tab2ChildInputs->addBoolValueInput("tableAdd", "Add", false, "", true);
                tableInput->addToolbarCommandInput(addButtonInput);
                Ptr deleteButtonInput =
                    tab2ChildInputs->addBoolValueInput("tableDelete", "Delete", false, "", true);
                tableInput->addToolbarCommandInput(deleteButtonInput);

                // Create angle value input.
                Ptr angleValueInput = tab2ChildInputs->addAngleValueCommandInput(
                    "angleValue", "AngleValue", ValueInput::createByString("30 degree"));
                angleValueInput->setManipulator(
                    Point3D::create(0, 0, 0), Vector3D::create(1, 0, 0), Vector3D::create(0, 0, 1));
                angleValueInput->hasMinimumValue(false);
                angleValueInput->hasMaximumValue(false);

                // Create tab inputs 3
                Ptr tabCmdInput3 = inputs->addTabCommandInput("tab_3", "Tab 3");
                if (!tabCmdInput3)
                    return;
                Ptr tab3ChildInputs = tabCmdInput3->children();
                if (!tab3ChildInputs)
                    return;
                // Create group
                Ptr sliderGroup =
                    tab3ChildInputs->addGroupCommandInput("slider_configuration", "Configuration");
                if (!sliderGroup)
                {
                    return;
                }
                Ptr sliderInputs = sliderGroup->children();
                // Create integer spinner input
                sliderInputs->addIntegerSpinnerCommandInput("slider_controller", "Num sliders", 1, 5, 1, 1);
                if (!sliderInputs)
                {
                    return;
                }
                updateSliders(sliderInputs);
            }
        }
    }

  private:
    OnExecuteEventHander onExecuteHandler;
    OnDestroyEventHandler onDestroyHandler;
    OnInputChangedEventHander onInputChangedHandler;
} _cmdCreatedHandler;

extern "C" XI_EXPORT bool run(const char* context)
{
    app = Application::get();
    if (!app)
        return false;

    ui = app->userInterface();
    if (!ui)
        return false;

    // Create the command definition.
    Ptr commandDefinitions = ui->commandDefinitions();
    if (!commandDefinitions)
        return nullptr;

    // Get the existing command definition or create it if it doesn't already exist.
    Ptr cmdDef = commandDefinitions->itemById("cmdInputsSample");
    if (!cmdDef)
    {
        cmdDef = commandDefinitions->addButtonDefinition(
            "cmdInputsSample", "Command Inputs Sample", "Sample to demonstrate various command inputs.");
    }

    // Connect to the command created event.
    Ptr commandCreatedEvent = cmdDef->commandCreated();
    if (!commandCreatedEvent)
        return false;
    commandCreatedEvent->add(&_cmdCreatedHandler);

    // Execute the command definition.
    cmdDef->execute();

    // Prevent this module from being terminated when the script returns, because we are waiting for event handlers to
    // fire.
    adsk::autoTerminate(false);

    return true;
}
#Author-Autodesk Inc.
#Description-Demo command input examples
import adsk.core, adsk.fusion, traceback

_app = None
_ui  = None
_rowNumber = 0

# Global set of event handlers to keep them referenced for the duration of the command
_handlers = []

# Adds a new row to the table.
def addRowToTable(tableInput):
    global _rowNumber
    # Get the CommandInputs object associated with the parent command.
    cmdInputs = adsk.core.CommandInputs.cast(tableInput.commandInputs)

    # Create three new command inputs.
    valueInput = cmdInputs.addValueInput('TableInput_value{}'.format(_rowNumber), 'Value', 'cm', adsk.core.ValueInput.createByReal(_rowNumber))
    stringInput =  cmdInputs.addStringValueInput('TableInput_string{}'.format(_rowNumber), 'String', str(_rowNumber))
    spinnerInput = cmdInputs.addIntegerSpinnerCommandInput('spinnerInt{}'.format(_rowNumber), 'Integer Spinner', 0 , 100 , 2, int(_rowNumber))

    # Add the inputs to the table.
    row = tableInput.rowCount
    tableInput.addCommandInput(valueInput, row, 0)
    tableInput.addCommandInput(stringInput, row, 1)
    tableInput.addCommandInput(spinnerInput, row, 2)

    # Increment a counter used to make each row unique.
    _rowNumber = _rowNumber + 1

def updateSliders(sliderInputs):
    """
    Populate 'slider_configuration' group with as many sliders as set in 'slider_controller'.
    Delete previous ones and create new sliders.
    """
    spinner = sliderInputs.itemById("slider_controller")
    value = spinner.value
    # check ranges
    if value > spinner.maximumValue or value A "full width" message using html.
'
            tab1ChildInputs.addTextBoxCommandInput('fullWidth_textBox', '', message, 1, True)            

            # Create a selection input.
            selectionInput = tab1ChildInputs.addSelectionInput('selection', 'Select', 'Basic select command input')
            selectionInput.setSelectionLimits(0)

            # Create a string value input.
            strInput = tab1ChildInputs.addStringValueInput('string', 'Text', 'Basic string command input')

            # Create value input.
            tab1ChildInputs.addValueInput('value', 'Value', 'cm', adsk.core.ValueInput.createByReal(0.0))

            # Create bool value input with checkbox style.
            tab1ChildInputs.addBoolValueInput('checkbox', 'Checkbox', True, '', False)

            # Create bool value input with button style that can be clicked.
            tab1ChildInputs.addBoolValueInput('buttonClick', 'Click Button', False, 'resources/button', True)

            # Create bool value input with button style that has a state.
            tab1ChildInputs.addBoolValueInput('buttonState', 'State Button', True, 'resources/button', True)

            # Create float slider input with two sliders.
            tab1ChildInputs.addFloatSliderCommandInput('floatSlider', 'Float Slider', 'cm', 0, 10.0, True)

            # Create float slider input with two sliders and a value list.
            floatValueList = [1.0, 3.0, 4.0, 7.0]
            tab1ChildInputs.addFloatSliderListCommandInput('floatSlider2', 'Float Slider 2', 'cm', floatValueList)

            # Create float slider input with two sliders and visible texts.
            floatSlider3 = tab1ChildInputs.addFloatSliderCommandInput('floatSlider3', 'Float Slider 3', '', 0, 50.0, False)
            floatSlider3.setText('Min', 'Max')

            # Create integer slider input with one slider.
            tab1ChildInputs.addIntegerSliderCommandInput('intSlider', 'Integer Slider', 0, 10);
            valueList = [1, 3, 4, 7, 11]

            # Create integer slider input with two sliders and a value list.
            tab1ChildInputs.addIntegerSliderListCommandInput('intSlider2', 'Integer Slider 2', valueList)

            # Create float spinner input.
            tab1ChildInputs.addFloatSpinnerCommandInput('spinnerFloat', 'Float Spinner', 'cm', 0.2 , 9.0 , 2.2, 1)

            # Create integer spinner input.
            tab1ChildInputs.addIntegerSpinnerCommandInput('spinnerInt', 'Integer Spinner', 2 , 9 , 2, 3)

            # Create dropdown input with checkbox style.
            dropdownInput = tab1ChildInputs.addDropDownCommandInput('dropdown', 'Dropdown 1', adsk.core.DropDownStyles.CheckBoxDropDownStyle)
            dropdownItems = dropdownInput.listItems
            dropdownItems.add('Item 1', False, 'resources/One')
            dropdownItems.add('Item 2', False, 'resources/Two')

            # Create dropdown input with icon style.
            dropdownInput2 = tab1ChildInputs.addDropDownCommandInput('dropdown2', 'Dropdown 2', adsk.core.DropDownStyles.LabeledIconDropDownStyle);
            dropdown2Items = dropdownInput2.listItems
            dropdown2Items.add('Item 1', True, 'resources/One')
            dropdown2Items.add('Item 2', False, 'resources/Two')

            # Create dropdown input with radio style.
            dropdownInput3 = tab1ChildInputs.addDropDownCommandInput('dropdown3', 'Dropdown 3', adsk.core.DropDownStyles.LabeledIconDropDownStyle);
            dropdown3Items = dropdownInput3.listItems
            dropdown3Items.add('Item 1', True, '')
            dropdown3Items.add('Item 2', False, '')

            # Create dropdown input with test list style.
            dropdownInput4 = tab1ChildInputs.addDropDownCommandInput('dropdown4', 'Dropdown 4', adsk.core.DropDownStyles.TextListDropDownStyle);
            dropdown4Items = dropdownInput4.listItems
            dropdown4Items.add('Item 1', True, '')
            dropdown4Items.add('Item 2', False, '')

            # Create single selectable button row input.
            buttonRowInput = tab1ChildInputs.addButtonRowCommandInput('buttonRow', 'Single Select Buttons', False)
            buttonRowInput.listItems.add('Item 1', False, 'resources/One')
            buttonRowInput.listItems.add('Item 2', False, 'resources/Two')

            # Create multi selectable button row input.
            buttonRowInput2 = tab1ChildInputs.addButtonRowCommandInput('buttonRow2', 'Multi-select Buttons', True)
            buttonRowInput2.listItems.add('Item 1', False, 'resources/One')
            buttonRowInput2.listItems.add('Item 2', False, 'resources/Two')

            # Create tab input 2
            tabCmdInput2 = inputs.addTabCommandInput('tab_2', 'Tab 2')
            tab2ChildInputs = tabCmdInput2.children

            # Create group input.
            groupCmdInput = tab2ChildInputs.addGroupCommandInput('group', 'Group')
            groupCmdInput.isExpanded = True
            groupCmdInput.isEnabledCheckBoxDisplayed = True
            groupChildInputs = groupCmdInput.children

            # Create radio button group input.
            radioButtonGroup = groupChildInputs.addRadioButtonGroupCommandInput('radioButtonGroup', 'Radio button group')
            radioButtonItems = radioButtonGroup.listItems
            radioButtonItems.add("Item 1", False)
            radioButtonItems.add("Item 2", False)
            radioButtonItems.add("Item 3", False)

            # Create image input.
            groupChildInputs.addImageCommandInput('image', 'Image', "resources/image.png")

            # Create direction input 1.
            directionCmdInput = tab2ChildInputs.addDirectionCommandInput('direction', 'Direction1')
            directionCmdInput.setManipulator(adsk.core.Point3D.create(0, 0, 0), adsk.core.Vector3D.create(1, 0, 0))

            # Create direction input 2.
            directionCmdInput2 = tab2ChildInputs.addDirectionCommandInput('direction2', 'Direction 2', 'resources/One')
            directionCmdInput2.setManipulator(adsk.core.Point3D.create(0, 0, 0), adsk.core.Vector3D.create(0, 1, 0)) 
            directionCmdInput2.isDirectionFlipped = True

            # Create distance value input 1.
            distanceValueInput = tab2ChildInputs.addDistanceValueCommandInput('distanceValue', 'DistanceValue', adsk.core.ValueInput.createByReal(2))
            distanceValueInput.setManipulator(adsk.core.Point3D.create(0, 0, 0), adsk.core.Vector3D.create(1, 0, 0))
            distanceValueInput.minimumValue = 0
            distanceValueInput.isMinimumValueInclusive = True
            distanceValueInput.maximumValue = 10
            distanceValueInput.isMaximumValueInclusive = True

            # Create distance value input 2.
            distanceValueInput2 = tab2ChildInputs.addDistanceValueCommandInput('distanceValue2', 'DistanceValue 2', adsk.core.ValueInput.createByReal(1))
            distanceValueInput2.setManipulator(adsk.core.Point3D.create(0, 0, 0), adsk.core.Vector3D.create(0, 1, 0))
            distanceValueInput2.expression = '1 in'
            distanceValueInput2.hasMinimumValue = False
            distanceValueInput2.hasMaximumValue = False

            # Create table input
            tableInput = tab2ChildInputs.addTableCommandInput('table', 'Table', 3, '1:1:1')
            addRowToTable(tableInput)

            # Add inputs into the table.            
            addButtonInput = tab2ChildInputs.addBoolValueInput('tableAdd', 'Add', False, '', True)
            tableInput.addToolbarCommandInput(addButtonInput)
            deleteButtonInput = tab2ChildInputs.addBoolValueInput('tableDelete', 'Delete', False, '', True)
            tableInput.addToolbarCommandInput(deleteButtonInput)

            # Create angle value input.
            angleValueInput = tab2ChildInputs.addAngleValueCommandInput('angleValue', 'AngleValue', adsk.core.ValueInput.createByString('30 degree'))
            angleValueInput.setManipulator(adsk.core.Point3D.create(0, 0, 0), adsk.core.Vector3D.create(1, 0, 0), adsk.core.Vector3D.create(0, 0, 1))
            angleValueInput.hasMinimumValue = False
            angleValueInput.hasMaximumValue = False

            # Create tab input 3
            tabCmdInput3 = inputs.addTabCommandInput('tab_3', 'Tab 3')
            tab3ChildInputs = tabCmdInput3.children
            # Create group
            sliderGroup = tab3ChildInputs.addGroupCommandInput("slider_configuration", "Configuration")
            sliderInputs = sliderGroup.children
            # Create integer spinner input
            sliderInputs.addIntegerSpinnerCommandInput("slider_controller", "Num sliders", 1, 5, 1, 1)
            updateSliders(sliderInputs)
        except:
            _ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

def run(context):
    try:
        global _app, _ui
        _app = adsk.core.Application.get()
        _ui = _app.userInterface

        # Get the existing command definition or create it if it doesn't already exist.
        cmdDef = _ui.commandDefinitions.itemById('cmdInputsSample')
        if not cmdDef:
            cmdDef = _ui.commandDefinitions.addButtonDefinition('cmdInputsSample', 'Command Inputs Sample', 'Sample to demonstrate various command inputs.')

        # Connect to the command created event.
        onCommandCreated = MyCommandCreatedHandler()
        cmdDef.commandCreated.add(onCommandCreated)
        _handlers.append(onCommandCreated)

        # Execute the command definition.
        cmdDef.execute()

        # Prevent this module from being terminated when the script returns, because we are waiting for event handlers to fire.
        adsk.autoTerminate(False)
    except:
        if _ui:
            _ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
```

