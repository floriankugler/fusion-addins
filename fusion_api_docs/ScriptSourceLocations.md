# ScriptSourceLocations Enumerator

## Description

Defines the different locations where Fusion looks for scripts and add-ins.  

## Methods

| Name | Value | Description |
|----|----|----|
| AppStoreScriptSourceLocation | 0 | The location where add-ins are installed from the Autodesk App Store. Windows - %appdata%\Autodesk\ApplicationPlugins Mac - ~/Library/Application Support/Autodesk/ApplicationPlugins |
| InternalScriptSourceLocation | 3 | One of the internal folders where add-ins are installed with Fusion. |
| LinkedScriptSourceLocation | 5 | The script or add-in can be located anywhere and has been manually added to the known list of scripts and add-ins as a link. |
| OtherInstalledScriptSourceLocation | 1 | The folder where non-App Store add-ins are installed. Windows - %appdata%\Autodesk\FusionAddins Mac - ~/Library/Application Support/Autodesk/FusionAddins |
| SamplesScriptSourceLocation | 4 | One of the sample folders where sample scripts and add-ins are installed with Fusion. |
| UserDefinedScriptSourceLocation | 2 | The folder defined in the API tab of the Preferences dialog. |

## Version

Introduced in version January 2025  

