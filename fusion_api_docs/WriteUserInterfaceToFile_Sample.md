# Write user interface to a file API Sample

## Description

Writes out the full structure of the Fusion user interface. This information is useful when editing the user-interface, as discussed in the usre manual topic [User-Interface Customization with Fusion's API](UserInterface_UM.md)

## Code Samples

| Copy Code |
|----------:|

```python
import adsk.core, traceback
import codecs

def run(context):
    ui = None
    try:
        app: adsk.core.Application = adsk.core.Application.get()
        ui  = app.userInterface

        fileDialog = ui.createFileDialog()
        fileDialog.isMultiSelectEnabled = False
        fileDialog.title = "Specify result filename"
        fileDialog.filter = 'XML files (*.xml)'
        fileDialog.filterIndex = 0
        dialogResult = fileDialog.showSave()
        if dialogResult == adsk.core.DialogResults.DialogOK:
            filename = fileDialog.filename
        else:
            return

        result = '\n'
        result += f'{TabSpace(1)}\n'
        for wsIndex in range(ui.workspaces.count):
            try:
                ws: adsk.core.Workspace = ui.workspaces.item(wsIndex)
            except:
                ws = None

            if ws:
                result += f'{TabSpace(2)}\n'
                try:
                    tabs = ws.toolbarTabs
                except:
                    tabs = None

                if tabs:
                    result += f'{TabSpace(3)}\n'
                    for tab in tabs:
                        result += f'{TabSpace(4)}\n'

                        result += GetPanelsXML(tab.toolbarPanels, 5)

                        result += f'{TabSpace(4)}\n'

                    result += f'{TabSpace(3)}\n'
                else:
                    result += f'{TabSpace(3)}\n'
                    result += f'{TabSpace(3)}\n'

                result += f'{TabSpace(2)}\n'

        result += f'{TabSpace(1)}\n'

        result += f'{TabSpace(1)}\n'
        toolbar: adsk.core.Toolbar
        for toolbar in ui.toolbars:
            result += f'{TabSpace(2)}\n'
            result += f'{TabSpace(3)}\n'
            result += GetControls(toolbar.controls, 1, False)
            result += f'{TabSpace(3)}\n'
            result += f'{TabSpace(2)}\n'
        result += f'{TabSpace(1)}\n'
        result += ''

        f = open(filename, 'w', -1, 'utf-8-sig')
        f.write(result)
        f.close()
        ui.messageBox(f'Finished writing to:\n{filename}')
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


# Builds XML data for all of the panel information from the ToolbarPanels collection passed in.
def GetPanelsXML(panels: adsk.core.ToolbarPanels, tabs: int) -> str:
    result = f'{TabSpace(tabs)}\n'
    for panelIndex in range(panels.count):
        try:
            panel: adsk.core.ToolbarPanel = panels.item(panelIndex)
        except:
            panel = None

        if panel:
            result += f'{TabSpace(tabs + 1)}\n'
            result += f'{TabSpace(tabs + 2)}\n'
            result += GetControls(panel.controls, tabs, True)
            result += f'{TabSpace(tabs + 2)}\n'
            result += f'{TabSpace(tabs + 1)}\n'

    result += f'{TabSpace(tabs + 1)}\n'
    return result


# Builds XML data for all of the controls in the ToolbarControls collection passed in.
def GetControls(controls: adsk.core.ToolbarControls, tabs: int, isPanel: bool) -> str:
    result = ''
    for control in controls:
        if control.objectType == adsk.core.DropDownControl.classType():
            dropControl: adsk.core.DropDownControl = control

            if isPanel:
                try:
                    dropName = dropControl.name
                except:
                    dropName = "**** Error getting name."

                result += f'{TabSpace(tabs + 3)}\n'
            else:
                result += f'{TabSpace(tabs + 3)}\n'

            result += GetControls(dropControl.controls, tabs + 1, isPanel)
            result += f'{TabSpace(tabs + 3)}\n'
        elif control.objectType == adsk.core.SplitButtonControl.classType():
            splitControl: adsk.core.SplitButtonControl = control
            result += f'{TabSpace(tabs + 3)}\n'

            try:
                defaultCmdDef = splitControl.defaultCommandDefinition
            except:
                defaultCmdDef = None
            
            if defaultCmdDef:
                result += f'{TabSpace(tabs + 4)}\n'

                additionalDefs = splitControl.additionalDefinitions
                result += f'{TabSpace(tabs + 4)}\n'
                for additionalDef in additionalDefs:
                    result += f'{TabSpace(tabs + 5)}\n'
                result += f'{TabSpace(tabs + 4)}\n'
            else:
                result += f'{TabSpace(tabs + 4)}\n'

            result += f'{TabSpace(tabs + 3)}\n'

        else:
            if control.objectType == adsk.core.SeparatorControl.classType():
                result += f'{TabSpace(tabs + 3)}\n'
            else:
                cmdDef: adsk.core.CommandDefinition = None
                try:                 
                    cmdDef = control.commandDefinition
                except:
                    cmdDef = None

                if cmdDef:
                    try:
                        commandType = ObjectName(cmdDef.controlDefinition)
                    except:
                        commandType = '**** Failed to get associated control.'

                    isPromotedOK = True
                    try:
                        isPromoted = control.isPromoted
                    except:
                        isPromotedOK = False


                    if isPanel and isPromotedOK:
                        result += f'{TabSpace(tabs + 3)}\n'
                    else:
                        result += f'{TabSpace(tabs + 3)}\n'
                else:
                    result += f'{TabSpace(tabs + 3)}\n'

    return result


# Return a string of spaces that can be used to prepend to a string to
# represent the specified number of tabs. 
def TabSpace(tabs: int) -> str:
    spacesPerTab = 4
    return ' ' * (spacesPerTab * tabs)


# Splits out the object name from the full object name passed in.
def ObjectName(object: adsk.core.Base) -> str:
    parts = object.objectType.split('::')
    return parts[len(parts)-1]
```

