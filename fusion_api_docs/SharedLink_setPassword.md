# SharedLink.setPassword Method

Parent Object: [SharedLink](SharedLink.md)  

## Description

Sets the password to access the web page to view the file. Setting a password makes using the password required to access the page. The password takes effect immediately for anyone using the URL. To turn off the password requirement, set the isPasswordRequired property to false.

## Syntax

"sharedLink_var" is a variable referencing a [SharedLink](SharedLink.md) object.

```python
returnValue = sharedLink_var.setPassword(password)
```

## Return Value

| Type    | Description                                          |
|---------|------------------------------------------------------|
| boolean | Returns true if setting the password was successful. |

## Parameters

| Name     | Type   | Description          |
|----------|--------|----------------------|
| password | string | The password to use. |

## Version

Introduced in version May 2024  

