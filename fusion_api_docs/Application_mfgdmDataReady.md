# Application.mfgdmDataReady Event

Parent Object: [Application](Application.md)  

## Description

The mfgdmDataReady event fires when the MFGDM data structure for a document has been updated and properties to IDs and structure from the data model is ready.

## Syntax

- [Python Using fusion360utils](#PythonUsingFusion360Utils)

*-------- Global variables ---------*  

```python
# Global variable used to maintain a reference to all event handlers.
handlers = []
```

*-------- Connect the handler to the event. ---------*  

```python
# "application_var" is a variable referencing an Application object.
# "MyMfgdmDataReadyHandler" is the name of the class that handles the event.
onMfgdmDataReady = MyMfgdmDataReadyHandler()
application_var.mfgdmDataReady.add(onMfgdmDataReady)
handlers.append(onMfgdmDataReady)
```

*-------- Event handler class definition ---------*  

```python
# Event handler for the mfgdmDataReady event.
class MyMfgdmDataReadyHandler(adsk.core.MFGDMDataEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args: adsk.core.MFGDMDataEventArgs):
        # Code to react to the event.
        app.log('In MyMfgdmDataReadyHandler event handler.')
```

## Property Value

This is an event property that returns a [MFGDMDataEvent](MFGDMDataEvent.md).

## Samples

| Name | Description |
|----|----|
| [Gets all properties using GraphQL](FetchBulkComponentProperties_Sample.md) | Fetches bulk component properties of the root component and from occurrences via single GraphQL query. |
| [Get part number using GraphQL](FetchPartNumberForComponents_Sample.md) | Fetches part number of root component and from occurrences via GQL query. |
| [Set part number using GraphQL](SetPartNumberUsingGraphQL_Sample.md) | Sets part number of root component and from occurrences via GQL query. |

## Version

Introduced in version July 2025  

