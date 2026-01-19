# UserInterface.getText Method

Parent Object: [UserInterface](UserInterface.md)  

## Description

Get the localized text for a specific application text string. The strings used by Fusion are stored in localized XML files that are installed with Fusion. On Windows, you can find them here:  

%LocalAppData%\Autodesk\webdeploy\production\VERSION_CODE\StringTable  

And on Mac, you can find them here:  

~/Library/Application Support/Autodesk/webdeploy/production/VERSION_CODE/Autodesk Fusion.app/Contents/Libraries/Neutron/StringTable  

There is a folder for each language that Fusion supports, and the strings for that language are defined in files within that folder. Fusion will use the language specified by the user in their preferences.

## Syntax

"userInterface_var" is a variable referencing a [UserInterface](UserInterface.md) object.

```python
returnValue = userInterface_var.getText(module, id, defaultValue)
```

## Return Value

| Type   | Description                                                   |
|--------|---------------------------------------------------------------|
| string | The localized string or the defaultValue if one is not found. |

## Parameters

| Name | Type | Description |
|----|----|----|
| module | string | The module name. This is the same as the StringTable .xml filename without the .xml extension and without the version number. For example, the file NaFusionUI10.xml contains many of the strings used for Fusion's modeling commands. When specifying the module, this is specified as "NaFusionUI". |
| id | string | The id of the text. This is the same as the 'commandName' field in the StringTable .xml file. |
| defaultValue | string | A default string value to return if the module or string id is not found in the current locale. |

## Version

Introduced in version March 2021  

