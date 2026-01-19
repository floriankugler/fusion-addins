# Customizing the UI using the API Sample

## Description

Demonstrates how to work with tabs, panels, and command in the user interface. The full source for [C++](../ExtraFiles/UICustomizationSampleCPP.zip) and [Python](../ExtraFiles/UICustomizationSamplePython.zip) samples can be downloaded. This is especially useful for getting the resource files.

## Code Samples

| Copy Code |
|----------:|

```python
#Author-
#Description-

import adsk.core, adsk.fusion, traceback
from typing import List

_app = adsk.core.Application.get()
_ui = _app.userInterface

_handlers = []
_commandDefs: List[adsk.core.CommandDefinition] = []

def run(context):
    try:
        _app.log(' ')
        _app.log(' ')
        _app.log('===============================================================')

        createUserInterface()

        # Make sure the "TEXT COMMANDS" windows is visible.
        textPalette: adsk.core.TextCommandPalette = _ui.palettes.itemById('TextCommands')
        if not textPalette.isVisible:
            textPalette.isVisible = True

        _ui.messageBox('Information about this sample is displayed in the TEXT COMMAND window.')

        return True
    except:
        if _ui:
            _ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


def stop(context):
    try:
        _app.log('Stopping and cleaning up add-in.')

        # Get the Render workspace.
        renderWS = _ui.workspaces.itemById('FusionRenderEnvironment')

        if renderWS:
            _app.log('Cleaning up toolbar.')
            tab = renderWS.toolbarTabs.itemById('UITestTab');
            if tab:
                # Get the test panels and delete them.
                panel = tab.toolbarPanels.itemById('testPanelOne')
                if panel:
                    panel.deleteMe()

                panel = tab.toolbarPanels.itemById('testPanelTwo')
                if panel:
                    panel.deleteMe()

                # Delete the tab.
                tab.deleteMe()

        # Get the "Render" tab.
        renderTab = renderWS.toolbarTabs.itemById('RenderTab')
        if renderTab:
            # Get "Render" panel.
            renderPanel = renderTab.toolbarPanels.itemById('RenderPanel')
            if renderPanel:
                # Delete the "Scripts and Add-Ins" command.
                scriptMgrControl = renderPanel.controls.itemById('ScriptsManagerCommand')
                if scriptMgrControl:
                    scriptMgrControl.deleteMe()

        # Delete the command definitions.
        for cmdDef in _commandDefs:
            _app.log(f'Deleting command definition: {cmdDef.id}')
            cmdDef.deleteMe()
    except:
        _ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


def createUserInterface():
    try:
        # Create all the custom commands.
        cmdDefs = _ui.commandDefinitions
        sampleCmd = cmdDefs.addButtonDefinition('SampleCmd', 'Sample Command', 'This is the longer original tooltip.', 'Resources/SampleCmdBW')
        _commandDefs.append(sampleCmd)

        sampleCmd.toolClipFilename = 'Resources/SampleCmdToolClip.png'

        toggleNameCmd = cmdDefs.addButtonDefinition('toggleNameCmd', 'Toggle Name', 'Running this command will toggle the command name of the sample command.', 'Resources/toggleName');
        _commandDefs.append(toggleNameCmd)

        toggleTooltipCmd = cmdDefs.addButtonDefinition('toggleTooltipCmd', 'Toggle Tooltip', 'Running this command will toggle the tooltip of the sample command.', 'Resources/toggleTooltip');
        _commandDefs.append(toggleTooltipCmd)

        toggleIconCmd = cmdDefs.addButtonDefinition('toggleIconCmd', 'Toggle Icon', 'Running this command will toggle the icon of the sample command.', 'Resources/toggleIcon');
        _commandDefs.append(toggleIconCmd)

        toggleVisibleCmd = cmdDefs.addButtonDefinition('toggleVisibleCmd', 'Toggle Visibility', 'Running this command will toggle the visibility of the sample command.', 'Resources/toggleVisible');
        _commandDefs.append(toggleVisibleCmd)

        toggleEnabledCmd = cmdDefs.addButtonDefinition('toggleEnabledCmd', 'Toggle Enabled', 'Running this command will toggle the enabled state of the sample command.', 'Resources/toggleEnabled');
        _commandDefs.append(toggleEnabledCmd)

        # Get the Render workspace.
        renderWS = _ui.workspaces.itemById('FusionRenderEnvironment')
        if renderWS:
            # Add a custom tab to the workspace.
            testTab = renderWS.toolbarTabs.add('UITestTab', 'UI Test Tab')

            if testTab:        
                # Add a panel to the tab.
                panel1 = testTab.toolbarPanels.add('testPanelOne', 'Test Panel 1')

                if panel1:
                    # Add the test command to the new panel.
                    cmdCntrl = panel1.controls.addCommand(sampleCmd)                   
                    cmdCntrl.isPromoted = True

                    # Add a button to toggle the icon to the panel.
                    cmdCntrl = panel1.controls.addCommand(toggleIconCmd)
                    cmdCntrl.isPromoted = True

                # Add a second panel to the tab.
                panel2 = testTab.toolbarPanels.add('testPanelTwo', 'Test Panel 2')

                if panel2:
                    # Add a button to toggle the tooltip to the panel by inserting before the existing button.
                    cmdCntrl = panel2.controls.addCommand(toggleTooltipCmd)
                    cmdCntrl.isPromoted = True

                    # Add a button to toggle the name to the panel.
                    cmdCntrl = panel2.controls.addCommand(toggleNameCmd, 'toggleTooltipCmd', True)
                    cmdCntrl.isPromoted = True

                    cmdCntrl = panel2.controls.addSeparator('toolbarSeperator')

                    # Add a drop-down.
                    dropDown = panel2.controls.addDropDown('Drop Down Example','Resources/toggleEnabled', 'DropDownTest')

                    if dropDown:
                        # Add a button to toggle the visibility to the end of the panel.
                        cmdCntrl = dropDown.controls.addCommand(toggleVisibleCmd)
                        cmdCntrl.isPromoted = True

                        # Add a button to toggle the enabled state to the end of the panel.
                        cmdCntrl = dropDown.controls.addCommand(toggleEnabledCmd)
                        cmdCntrl.isPromoted = True

            # Get the "Render" tab.
            renderTab = renderWS.toolbarTabs.itemById('RenderTab');
            
            if renderTab:
                # Get "Render" panel.
                renderPanel = renderTab.toolbarPanels.itemById('RenderPanel')

                if renderPanel:
                    # Add the "Scripts and Add-Ins" command to the Render panel.
                    scriptCmdDef = _ui.commandDefinitions.itemById('ScriptsManagerCommand')

                    cmdCntrl = renderPanel.controls.addCommand(scriptCmdDef)
                    cmdCntrl.isPromoted = True

        _app.log('A new tab named "UI Test Tab" was added to the RENDER workspace.')
        _app.log('This tab contains two panels: "Test Panel 1" and "Test Panel 2".')
        _app.log('"Test Panel 1" contains the commands "Sample Command" and "Toggle Icon".')
        _app.log('"Test Panel 2" contains the commands "Toggle Tooltip", "Toggle Name", "Toggle Visibility", and "Toggle Enabled"')
        _app.log('The "Scripts and Add-Ins" command was also added to the "RENDER" panel in the "RENDER" tab.')
        _app.log('The command with the "S" icon is the sample command and the other commands change things about it.')

        # Connect each of the commands to the command created event handler. For this
        # example, the same event handler is used for all the commands and the handler
        # special cases for each command.
        onCommandCreated = MyCommandCreatedHandler()
        sampleCmd.commandCreated.add(onCommandCreated)
        toggleNameCmd.commandCreated.add(onCommandCreated)
        toggleTooltipCmd.commandCreated.add(onCommandCreated)
        toggleIconCmd.commandCreated.add(onCommandCreated)
        toggleVisibleCmd.commandCreated.add(onCommandCreated)
        toggleEnabledCmd.commandCreated.add(onCommandCreated)
        _handlers.append(onCommandCreated)
    except:
        _ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


# Event handler for the commandCreated event.
class MyCommandCreatedHandler(adsk.core.CommandCreatedEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        try:
            eventArgs = adsk.core.CommandCreatedEventArgs.cast(args)
            command = eventArgs.command

            # Connect to the command execute event.
            onExecute = MyExecuteHandler()
            command.execute.add(onExecute)
            _handlers.append(onExecute)
        except:
            _ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


# Event handler for the execute event.
class MyExecuteHandler(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, eventArgs):
        try:
            # Get the command that's being executed.
            cmd = eventArgs.command
            cmdDef = cmd.parentCommandDefinition

            # Get the sample command, because most of the other commands modify it.
            sampleCmdDef = _ui.commandDefinitions.itemById('SampleCmd')
            buttonDef = sampleCmdDef.controlDefinition

            # Handle the execution of each of the commands. Since this sample is implemented using
            # a single command created and execute event, it special cases for each command and
            # performs the appropriate action for that command.
            if cmdDef.id == 'SampleCmd':
                # Display a message box indicating the sample command was run.
                _ui.messageBox('Executed the sample command.')
            elif cmdDef.id == 'toggleNameCmd':
                _app.log('name Property')
                _app.log(f'   Name before: "{sampleCmdDef.name}".')

                # Toggle the name of the sample command.
                if sampleCmdDef.name == 'Sample Command':
                    sampleCmdDef.name = "Renamed Command"
                else:
                    sampleCmdDef.name = 'Sample Command'

                _app.log(f'   Name after: "{sampleCmdDef.name}".')
            elif cmdDef.id == 'toggleTooltipCmd':
                _app.log('tooltip Property')
                _app.log(f'   Tooltip before: "{sampleCmdDef.tooltip}".')

                # Toggle the tooltip of the sample command.
                if sampleCmdDef.tooltip == 'This is the longer original tooltip.':
                    sampleCmdDef.tooltip = "Modified tooltip."
                else:
                    sampleCmdDef.tooltip = 'This is the longer original tooltip.'

                _app.log(f'   Tooltip after: "{sampleCmdDef.tooltip}".')
            elif cmdDef.id == 'toggleIconCmd':
                _app.log('resourceFolder Property')
                _app.log(f'   Resource Folder before: "{sampleCmdDef.resourceFolder}".')

                # Toggle the icon of the sample command.
                if 'Resources/SampleCmdBW' in sampleCmdDef.resourceFolder:
                    sampleCmdDef.resourceFolder = 'Resources/SampleCmdColor'
                else:
                    sampleCmdDef.resourceFolder = 'Resources/SampleCmdBW'

                _app.log(f'   Resource Folder after: "{sampleCmdDef.resourceFolder}".')
            elif cmdDef.id == 'toggleVisibleCmd':
                _app.log('isVisible Property')
                _app.log(f'   isVisible before: {buttonDef.isVisible}.')

                # Toggle the visibility of the sample command.
                buttonDef.isVisible = not buttonDef.isVisible

                _app.log(f'   isVisible after: {buttonDef.isVisible}.')
            elif cmdDef.id == 'toggleEnabledCmd':
                _app.log('isEnabled Property')
                _app.log(f'   isEnabled before: {buttonDef.isEnabled}.')

                # Toggle the enabled state of the sample command.
                buttonDef.isEnabled = not buttonDef.isEnabled

                _app.log(f'   isEnabled after: {buttonDef.isEnabled}.')
        except:
            _ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
```

