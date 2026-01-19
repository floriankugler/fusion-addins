# CAMTemplate.createFromFile Method

Parent Object: [CAMTemplate](CAMTemplate.md)  

## Description

Create a CAMTemplate from a file on disk, i.e. Import the template file. Invalid files will produce errors

## Syntax

This is a static method.  

```python

returnValue = adsk.cam.CAMTemplate.createFromFile(filePath)
```

## Return Value

| Type                           | Description                         |
|--------------------------------|-------------------------------------|
| [CAMTemplate](CAMTemplate.md) | Returns the newly created template. |

## Parameters

| Name     | Type   | Description                  |
|----------|--------|------------------------------|
| filePath | string | The path to a template file. |

## Version

Introduced in version April 2023  

