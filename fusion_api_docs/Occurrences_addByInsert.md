# Occurrences.addByInsert Method

Parent Object: [Occurrences](Occurrences.md)  

## Description

Method that inserts an existing file.

## Syntax

"occurrences_var" is a variable referencing an [Occurrences](Occurrences.md) object.

```python
returnValue = occurrences_var.addByInsert(dataFile, transform, isReferencedComponent)
```

## Return Value

| Type | Description |
|----|----|
| [Occurrence](Occurrence.md) | Returns the newly created occurrence or null if the insert failed. Insert will fail if the dataFile being inserted is not from the same project as the document it is being inserted into while isReferencedComponent is True. |

## Parameters

| Name | Type | Description |
|----|----|----|
| dataFile | [DataFile](DataFile.md) | The dataFile to insert. |
| transform | [Matrix3D](Matrix3D.md) | A transform that defines the location for the new occurrence. |
| isReferencedComponent | boolean | Indicates if the insert is to be an external reference or embedded within this document. This method will fail if the dataFile being inserted is not from the same project as the document it is being inserted into while isReferencedComponent is True. |

## Samples

| Name | Description |
|----|----|
| [Save and Insert File API Sample](SaveAndInsertSample_Sample.md) | Demonstrates creating save a new file and then inserting it into a design. To use this sample, have a design open that has been saved and run the script. It will create a new design that contains a cylinder, save it to the same folder the active design was saved to, and then insert it into the active design. |

## Version

Introduced in version September 2015  

