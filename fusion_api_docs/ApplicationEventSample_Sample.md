# Application Event API Sample

## Description

Add-In that demonstrates application events. To use this sample, create a new folder using the name you want to use for the new add-in. Inside the folder, create a new file that is the same name as the folder but has a .py extension. Copy the code below into the .py file. Create another file that is the same name as the folder but has a .manifest extension and copy the JSON data below into that file. { "autodeskProduct": "Fusion360", "type": "addin", "author": "", "description": { "": "" }, "supportedOS": "windows\|mac", "editEnabled": true } Run the "Scripts and Add-Ins" command and click the green plus button near the top of the dialog. Browse to the location where you created the folder and select the folder. The add-in should now be displayed in the list of add-ins on the "Add-Ins" tab of the dialog. Select the add-in and click the "Run" button. This will load the add-in and when any of the application events occurr that it is watching for it will report them in the TEXT COMMAND window.

## Code Samples

| Copy Code |
|----------:|

```python
import adsk.core, traceback

# global set of event handlers to keep them referenced
handlers = []
app = adsk.core.Application.get()

# Event handler for the documentOpened event.
class MyDocumentOpenedHandler(adsk.core.DocumentEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        eventArgs = adsk.core.DocumentEventArgs.cast(args)

        # Code to react to the event.
        app.log('In MyDocumentOpenedHandler event handler.')

# Event handler for the documentOpening event.
class MyDocumentOpeningHandler(adsk.core.DocumentEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        eventArgs = adsk.core.DocumentEventArgs.cast(args)

        # Code to react to the event.
        app.log('In MyDocumentOpeningHandler event handler.')

# Event handler for the startupCompleted event.
class StartupCompletedHandler(adsk.core.ApplicationEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        try:
           app.log('Startup completed')
        except:
           app.log('Startup completed event failed: {}'.format(traceback.format_exc()))

# Event handler for the onlineStatusChanged event.
class OnlineStatusChangedHandler(adsk.core.ApplicationEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        try:
           status = 'Online'
           if args.isOffLine:
               status = 'Offline'
           app.log('Online status changed: ' + status)
        except:
           app.log('Online status changed event failed: {}'.format(traceback.format_exc()))

# Event handler for the documentCreated event.
class MyDocumentCreatedHandler(adsk.core.DocumentEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        eventArgs = adsk.core.DocumentEventArgs.cast(args)

        # Code to react to the event.
        app.log('In MyDocumentCreatedHandler event handler.')        

# Event handler for the documentSaved event.
class MyDocumentSavedHandler(adsk.core.DocumentEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        eventArgs = adsk.core.DocumentEventArgs.cast(args)

        # Code to react to the event.
        app.log('In MyDocumentSavedHandler event handler.')   
        
# Event handler for the documentSaving event.
class MyDocumentSavingHandler(adsk.core.DocumentEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        eventArgs = adsk.core.DocumentEventArgs.cast(args)

        # Code to react to the event.
        app.log('In MyDocumentSavingHandler event handler.')     

# Event handler for the documentClosing event.
class MyDocumentClosingHandler(adsk.core.DocumentEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        eventArgs = adsk.core.DocumentEventArgs.cast(args)

        # Code to react to the event.
        app.log('In MyDocumentClosingHandler event handler.')     
        
# Event handler for the documentClosed event.
class MyDocumentClosedHandler(adsk.core.DocumentEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        eventArgs = adsk.core.DocumentEventArgs.cast(args)

        # Code to react to the event.
        app.log('In MyDocumentClosedHandler event handler.')     

# Event handler for the documentDeactivated event.
class MyDocumentDeactivatedHandler(adsk.core.DocumentEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        eventArgs = adsk.core.DocumentEventArgs.cast(args)

        # Code to react to the event.
        app.log('In MyDocumentDeactivatedHandler event handler.\ndocument: {}'.format(eventArgs.document.name))    

# Event handler for the documentActivated event.
class MyDocumentActivatedHandler(adsk.core.DocumentEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        eventArgs = adsk.core.DocumentEventArgs.cast(args)

        # Code to react to the event.
        app.log('In MyDocumentActivatedHandler event handler.\ndocument: {}'.format(eventArgs.document.name))    

# Event handler for the documentDeactivating event.
class MyDocumentDeactivatingHandler(adsk.core.DocumentEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        eventArgs = adsk.core.DocumentEventArgs.cast(args)

        # Code to react to the event.
        app.log('In MyDocumentDeactivatingHandler event handler.\ndocument: {}'.format(eventArgs.document.name))    

# Event handler for the documentActivating event.
class MyDocumentActivatingHandler(adsk.core.DocumentEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        eventArgs = adsk.core.DocumentEventArgs.cast(args)
        
        # Code to react to the event.
        app.log('In MyDocumentActivatingHandler event handler.\ndocument: {}'.format(eventArgs.document.name))    
                 
def run(context):
    try:
        onStartupCompleted = StartupCompletedHandler()
        app.startupCompleted.add(onStartupCompleted)
        handlers.append(onStartupCompleted)
        
        onOnlineStatusChanged = OnlineStatusChangedHandler()
        app.onlineStatusChanged.add(onOnlineStatusChanged)
        handlers.append(onOnlineStatusChanged)
        
        onDocumentCreated = MyDocumentCreatedHandler()
        app.documentCreated.add(onDocumentCreated)
        handlers.append(onDocumentCreated)
        
        onDocumentSaved = MyDocumentSavedHandler()
        app.documentSaved.add(onDocumentSaved)
        handlers.append(onDocumentSaved)
        
        onDocumentSaving = MyDocumentSavingHandler()
        app.documentSaving.add(onDocumentSaving)
        handlers.append(onDocumentSaving)
     
        onDocumentOpened = MyDocumentOpenedHandler()
        app.documentOpened.add(onDocumentOpened)
        handlers.append(onDocumentOpened)   
        
        onDocumentOpening = MyDocumentOpeningHandler()
        app.documentOpening.add(onDocumentOpening)
        handlers.append(onDocumentOpening)    
        
        onDocumentClosing = MyDocumentClosingHandler()
        app.documentClosing.add(onDocumentClosing)
        handlers.append(onDocumentClosing)   
        
        onDocumentClosed = MyDocumentClosedHandler()
        app.documentClosed.add(onDocumentClosed)
        handlers.append(onDocumentClosed)           
        
        onDocumentDeactivated = MyDocumentDeactivatedHandler()
        app.documentDeactivated.add(onDocumentDeactivated)
        handlers.append(onDocumentDeactivated)    
        
        onDocumentActivated = MyDocumentActivatedHandler()
        app.documentActivated.add(onDocumentActivated)
        handlers.append(onDocumentActivated)
        
        onDocumentDeactivating = MyDocumentDeactivatingHandler()
        app.documentDeactivating.add(onDocumentDeactivating)
        handlers.append(onDocumentDeactivating)   
        
        onDocumentActivating = MyDocumentActivatingHandler()
        app.documentActivating.add(onDocumentActivating)
        handlers.append(onDocumentActivating)   
    except:
        app.log('AddIn Start Failed:\n{}'.format(traceback.format_exc()))


def stop(context):
    try:
        pass
    except:
        app.log('AddIn Stop Failed: {}'.format(traceback.format_exc()))
```

