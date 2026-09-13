# Modal presentations

Present content in a separate view that offers focused interaction.

## Overview {#Overview}

To draw attention to an important, narrowly scoped task, you display a modal presentation, like an alert, popover, sheet, or confirmation dialog.

![](./images/modal-presentations-hero@2x.png)

In SwiftUI, you create a modal presentation using a view modifier that defines how the presentation looks and the condition under which SwiftUI presents it. SwiftUI detects when the condition changes and makes the presentation for you. Because you provide a [Binding](https://developer.apple.com/documentation/swiftui/binding) to the condition that initiates the presentation, SwiftUI can reset the underlying value when the user dismisses the presentation.

For design guidance, see [Modality](https://developer.apple.com/design/human-interface-guidelines/modality) in the Human Interface Guidelines.

## Configuring a dialog {#Configuring-a-dialog}

- [DialogSeverity](https://developer.apple.com/documentation/swiftui/dialogseverity) — The severity of an alert or confirmation dialog.

## Showing a sheet, cover, or popover {#Showing-a-sheet-cover-or-popover}

- [sheet(isPresented:onDismiss:content:)](https://developer.apple.com/documentation/swiftui/view/sheet(ispresented:ondismiss:content:)) — Presents a sheet when a binding to a Boolean value that you provide is true.
- [sheet(item:onDismiss:content:)](https://developer.apple.com/documentation/swiftui/view/sheet(item:ondismiss:content:)) — Presents a sheet using the given item as a data source for the sheet’s content.
- [fullScreenCover(isPresented:onDismiss:content:)](https://developer.apple.com/documentation/swiftui/view/fullscreencover(ispresented:ondismiss:content:)) — Presents a modal view that covers as much of the screen as possible when binding to a Boolean value you provide is true.
- [fullScreenCover(item:onDismiss:content:)](https://developer.apple.com/documentation/swiftui/view/fullscreencover(item:ondismiss:content:)) — Presents a modal view that covers as much of the screen as possible using the binding you provide as a data source for the sheet’s content.
- [popover(item:attachmentAnchor:arrowEdge:content:)](https://developer.apple.com/documentation/swiftui/view/popover(item:attachmentanchor:arrowedge:content:)) — Presents a popover using the given item as a data source for the popover’s content.
- [popover(isPresented:attachmentAnchor:arrowEdge:content:)](https://developer.apple.com/documentation/swiftui/view/popover(ispresented:attachmentanchor:arrowedge:content:)) — Presents a popover when a given condition is true.
- [PopoverAttachmentAnchor](https://developer.apple.com/documentation/swiftui/popoverattachmentanchor) — An attachment anchor for a popover.

## Adapting a presentation size {#Adapting-a-presentation-size}

- [presentationCompactAdaptation(horizontal:vertical:)](https://developer.apple.com/documentation/swiftui/view/presentationcompactadaptation(horizontal:vertical:)) — Specifies how to adapt a presentation to horizontally and vertically compact size classes.
- [presentationCompactAdaptation(_:)](https://developer.apple.com/documentation/swiftui/view/presentationcompactadaptation(_:)) — Specifies how to adapt a presentation to compact size classes.
- [PresentationAdaptation](https://developer.apple.com/documentation/swiftui/presentationadaptation) — Strategies for adapting a presentation to a different size class.
- [presentationSizing(_:)](https://developer.apple.com/documentation/swiftui/view/presentationsizing(_:)) — Sets the sizing of the containing presentation.
- [PresentationSizing](https://developer.apple.com/documentation/swiftui/presentationsizing) — A type that defines the size of the presentation content and how the presentation size adjusts to its content’s size changing.
- [PresentationSizingRoot](https://developer.apple.com/documentation/swiftui/presentationsizingroot) — A proxy to a view provided to the presentation with a defined presentation size.
- [PresentationSizingContext](https://developer.apple.com/documentation/swiftui/presentationsizingcontext) — Contextual information about a presentation.

## Configuring a sheet’s height and placement {#Configuring-a-sheets-height-and-placement}

- [presentationDetents(_:)](https://developer.apple.com/documentation/swiftui/view/presentationdetents(_:)) — Sets the available detents for the enclosing sheet.
- [presentationDetents(_:selection:)](https://developer.apple.com/documentation/swiftui/view/presentationdetents(_:selection:)) — Sets the available detents for the enclosing sheet, giving you programmatic control of the currently selected detent.
- [presentationContentInteraction(_:)](https://developer.apple.com/documentation/swiftui/view/presentationcontentinteraction(_:)) — Configures the behavior of swipe gestures on a presentation.
- [presentationDragIndicator(_:)](https://developer.apple.com/documentation/swiftui/view/presentationdragindicator(_:)) — Sets the visibility of the drag indicator on top of a sheet.
- [PresentationDetent](https://developer.apple.com/documentation/swiftui/presentationdetent) — A type that represents a height where a sheet naturally rests.
- [CustomPresentationDetent](https://developer.apple.com/documentation/swiftui/custompresentationdetent) — The definition of a custom detent with a calculated height.
- [PresentationContentInteraction](https://developer.apple.com/documentation/swiftui/presentationcontentinteraction) — A behavior that you can use to influence how a presentation responds to swipe gestures.
- [presentationPlacement(_:)](https://developer.apple.com/documentation/swiftui/view/presentationplacement(_:)) — Sets the placement of a presentation within the presenting view.
- [PresentationPlacement](https://developer.apple.com/documentation/swiftui/presentationplacement) — The placement of a presentation within the presenting view.

## Styling a sheet and its background {#Styling-a-sheet-and-its-background}

- [presentationCornerRadius(_:)](https://developer.apple.com/documentation/swiftui/view/presentationcornerradius(_:)) — Requests that the presentation have a specific corner radius.
- [presentationBackground(_:)](https://developer.apple.com/documentation/swiftui/view/presentationbackground(_:)) — Sets the presentation background of the enclosing sheet using a shape style.
- [presentationBackground(alignment:content:)](https://developer.apple.com/documentation/swiftui/view/presentationbackground(alignment:content:)) — Sets the presentation background of the enclosing sheet to a custom view.
- [presentationBackgroundInteraction(_:)](https://developer.apple.com/documentation/swiftui/view/presentationbackgroundinteraction(_:)) — Controls whether people can interact with the view behind a presentation.
- [PresentationBackgroundInteraction](https://developer.apple.com/documentation/swiftui/presentationbackgroundinteraction) — The kinds of interaction available to views behind a presentation.

## Presenting an alert {#Presenting-an-alert}

- [AlertScene](https://developer.apple.com/documentation/swiftui/alertscene) — A scene that renders itself as a standalone alert dialog.
- [alert(_:isPresented:actions:)](https://developer.apple.com/documentation/swiftui/view/alert(_:ispresented:actions:)) — Presents an alert when a given condition is true, using a localized string resource for the title.
- [alert(_:isPresented:presenting:actions:)](https://developer.apple.com/documentation/swiftui/view/alert(_:ispresented:presenting:actions:)) — Presents an alert using the given data to produce the alert’s content and a localized string resource for a title.
- [alert(_:item:actions:)](https://developer.apple.com/documentation/swiftui/view/alert(_:item:actions:)) — Presents an alert using the given data to produce the alert’s content and a text view as a title.
- [alert(error:actions:)](https://developer.apple.com/documentation/swiftui/view/alert(error:actions:)) — Presents an alert when an error is present.
- [alert(isPresented:error:actions:)](https://developer.apple.com/documentation/swiftui/view/alert(ispresented:error:actions:)) — Presents an alert when an error is present.
- [alert(_:isPresented:actions:message:)](https://developer.apple.com/documentation/swiftui/view/alert(_:ispresented:actions:message:)) — Presents an alert with a message when a given condition is true, using a localized string resource for a title.
- [alert(_:isPresented:presenting:actions:message:)](https://developer.apple.com/documentation/swiftui/view/alert(_:ispresented:presenting:actions:message:)) — Presents an alert with a message using the given data to produce the alert’s content and a localized string resource for a title.
- [alert(_:item:actions:message:)](https://developer.apple.com/documentation/swiftui/view/alert(_:item:actions:message:)) — Presents an alert with a message using the given data to produce the alert’s content and a localized string key for a title.
- [alert(error:actions:message:)](https://developer.apple.com/documentation/swiftui/view/alert(error:actions:message:)) — Presents an alert with a message when an error is present.
- [alert(isPresented:error:actions:message:)](https://developer.apple.com/documentation/swiftui/view/alert(ispresented:error:actions:message:)) — Presents an alert with a message when an error is present.

## Getting confirmation for an action {#Getting-confirmation-for-an-action}

- [confirmationDialog(_:isPresented:titleVisibility:actions:)](https://developer.apple.com/documentation/swiftui/view/confirmationdialog(_:ispresented:titlevisibility:actions:)) — Presents a confirmation dialog when a given condition is true, using a localized string resource for the title.
- [confirmationDialog(_:isPresented:titleVisibility:presenting:actions:)](https://developer.apple.com/documentation/swiftui/view/confirmationdialog(_:ispresented:titlevisibility:presenting:actions:)) — Presents a confirmation dialog using data to produce the dialog’s content and a localized string resource for the title.
- [dismissalConfirmationDialog(_:shouldPresent:actions:)](https://developer.apple.com/documentation/swiftui/view/dismissalconfirmationdialog(_:shouldpresent:actions:)) — Presents a confirmation dialog when a dismiss action has been triggered.

## Showing a confirmation dialog with a message {#Showing-a-confirmation-dialog-with-a-message}

- [confirmationDialog(_:isPresented:titleVisibility:actions:message:)](https://developer.apple.com/documentation/swiftui/view/confirmationdialog(_:ispresented:titlevisibility:actions:message:)) — Presents a confirmation dialog with a message when a given condition is true, using a localized string resource for the title.
- [confirmationDialog(_:isPresented:titleVisibility:presenting:actions:message:)](https://developer.apple.com/documentation/swiftui/view/confirmationdialog(_:ispresented:titlevisibility:presenting:actions:message:)) — Presents a confirmation dialog with a message using data to produce the dialog’s content and a localized string resource for the title.
- [dismissalConfirmationDialog(_:shouldPresent:actions:message:)](https://developer.apple.com/documentation/swiftui/view/dismissalconfirmationdialog(_:shouldpresent:actions:message:)) — Presents a confirmation dialog when a dismiss action has been triggered.

## Configuring a dialog {#Configuring-a-dialog}

- [dialogIcon(_:)](https://developer.apple.com/documentation/swiftui/view/dialogicon(_:)) — Configures the icon used by dialogs within this view.
- [dialogIcon(_:)](https://developer.apple.com/documentation/swiftui/scene/dialogicon(_:)) — Configures the icon used by alerts.
- [dialogSeverity(_:)](https://developer.apple.com/documentation/swiftui/view/dialogseverity(_:))
- [dialogSeverity(_:)](https://developer.apple.com/documentation/swiftui/scene/dialogseverity(_:)) — Sets the severity for alerts.
- [dialogSuppressionToggle(isSuppressed:)](https://developer.apple.com/documentation/swiftui/view/dialogsuppressiontoggle(issuppressed:)) — Enables user suppression of dialogs and alerts presented within `self`, with a default suppression message on macOS. Unused on other platforms.
- [dialogSuppressionToggle(isSuppressed:)](https://developer.apple.com/documentation/swiftui/scene/dialogsuppressiontoggle(issuppressed:)) — Enables user suppression of an alert with a custom suppression message.
- [dialogSuppressionToggle(_:isSuppressed:)](https://developer.apple.com/documentation/swiftui/view/dialogsuppressiontoggle(_:issuppressed:)) — Enables user suppression of dialogs and alerts presented within `self`, with a custom suppression message on macOS. Unused on other platforms.
- [dialogSuppressionToggle(_:isSuppressed:)](https://developer.apple.com/documentation/swiftui/scene/dialogsuppressiontoggle(_:issuppressed:)) — Enables user suppression of an alert with a custom suppression message.
- [dialogPreventsAppTermination(_:)](https://developer.apple.com/documentation/swiftui/view/dialogpreventsapptermination(_:)) — Whether the alert or confirmation dialog prevents the app from being quit/terminated by the system or app termination menu item.

## Exporting to file {#Exporting-to-file}

- [fileExporter(isPresented:document:contentType:defaultFilename:onCompletion:onCancellation:)](https://developer.apple.com/documentation/swiftui/view/fileexporter(ispresented:document:contenttype:defaultfilename:oncompletion:oncancellation:)) — Presents a system dialog for allowing the user to export a `WritableDocument` to a file on disk.
- [fileExporter(isPresented:documents:contentTypes:onCompletion:onCancellation:)](https://developer.apple.com/documentation/swiftui/view/fileexporter(ispresented:documents:contenttypes:oncompletion:oncancellation:)) — Presents a system dialog for allowing the user to export a collection of objects conforming to `WritableDocument` to files on disk.
- [fileExporter(isPresented:item:contentTypes:defaultFilename:onCompletion:onCancellation:)](https://developer.apple.com/documentation/swiftui/view/fileexporter(ispresented:item:contenttypes:defaultfilename:oncompletion:oncancellation:)) — Presents a system dialog allowing the user to export a `Transferable` item to a file on disk.
- [fileExporter(isPresented:items:contentTypes:onCompletion:onCancellation:)](https://developer.apple.com/documentation/swiftui/view/fileexporter(ispresented:items:contenttypes:oncompletion:oncancellation:)) — Presents a system dialog allowing the user to export a collection of `Transferable` items to files on disk.
- [fileExporterFilenameLabel(_:)](https://developer.apple.com/documentation/swiftui/view/fileexporterfilenamelabel(_:)) — On macOS, configures the `fileExporter` with a label for the file name field.

## Importing from file {#Importing-from-file}

- [fileImporter(isPresented:allowedContentTypes:allowsMultipleSelection:onCompletion:)](https://developer.apple.com/documentation/swiftui/view/fileimporter(ispresented:allowedcontenttypes:allowsmultipleselection:oncompletion:)) — Presents a system dialog for allowing the user to import multiple files.
- [fileImporter(isPresented:allowedContentTypes:onCompletion:)](https://developer.apple.com/documentation/swiftui/view/fileimporter(ispresented:allowedcontenttypes:oncompletion:)) — Presents a system dialog for allowing the user to import an existing file.
- [fileImporter(isPresented:allowedContentTypes:allowsMultipleSelection:onCompletion:onCancellation:)](https://developer.apple.com/documentation/swiftui/view/fileimporter(ispresented:allowedcontenttypes:allowsmultipleselection:oncompletion:oncancellation:)) — Presents a system dialog for allowing the user to import multiple files.

## Moving a file {#Moving-a-file}

- [fileMover(isPresented:file:onCompletion:)](https://developer.apple.com/documentation/swiftui/view/filemover(ispresented:file:oncompletion:)) — Presents a system dialog for allowing the user to move an existing file to a new location.
- [fileMover(isPresented:files:onCompletion:)](https://developer.apple.com/documentation/swiftui/view/filemover(ispresented:files:oncompletion:)) — Presents a system dialog for allowing the user to move a collection of existing files to a new location.
- [fileMover(isPresented:file:onCompletion:onCancellation:)](https://developer.apple.com/documentation/swiftui/view/filemover(ispresented:file:oncompletion:oncancellation:)) — Presents a system dialog for allowing the user to move an existing file to a new location.
- [fileMover(isPresented:files:onCompletion:onCancellation:)](https://developer.apple.com/documentation/swiftui/view/filemover(ispresented:files:oncompletion:oncancellation:)) — Presents a system dialog for allowing the user to move a collection of existing files to a new location.

## Configuring a file dialog {#Configuring-a-file-dialog}

- [fileDialogBrowserOptions(_:)](https://developer.apple.com/documentation/swiftui/view/filedialogbrowseroptions(_:)) — On macOS, configures the `fileExporter`, `fileImporter`, or `fileMover` to provide a refined URL search experience: include or exclude hidden files, allow searching by tag, etc.
- [fileDialogConfirmationLabel(_:)](https://developer.apple.com/documentation/swiftui/view/filedialogconfirmationlabel(_:)) — On macOS, configures the `fileExporter`, `fileImporter`, or `fileMover` with a custom confirmation button label.
- [fileDialogCustomizationID(_:)](https://developer.apple.com/documentation/swiftui/view/filedialogcustomizationid(_:)) — On macOS, configures the `fileExporter`, `fileImporter`, or `fileMover` to persist and restore the file dialog configuration.
- [fileDialogDefaultDirectory(_:)](https://developer.apple.com/documentation/swiftui/view/filedialogdefaultdirectory(_:)) — Configures the `fileExporter`, `fileImporter`, or `fileMover` to open with the specified default directory.
- [fileDialogImportsUnresolvedAliases(_:)](https://developer.apple.com/documentation/swiftui/view/filedialogimportsunresolvedaliases(_:)) — On macOS, configures the `fileExporter`, `fileImporter`, or `fileMover` behavior when a user chooses an alias.
- [fileDialogMessage(_:)](https://developer.apple.com/documentation/swiftui/view/filedialogmessage(_:)) — On macOS, configures the `fileExporter`, `fileImporter`, or `fileMover` with a custom message that is presented to the user, similar to a title.
- [fileDialogURLEnabled(_:)](https://developer.apple.com/documentation/swiftui/view/filedialogurlenabled(_:)) — On macOS, configures the `fileImporter` or `fileMover` to conditionally disable presented URLs.
- [FileDialogBrowserOptions](https://developer.apple.com/documentation/swiftui/filedialogbrowseroptions) — The way that file dialogs present the file system.

## Presenting an inspector {#Presenting-an-inspector}

- [inspector(isPresented:content:)](https://developer.apple.com/documentation/swiftui/view/inspector(ispresented:content:)) — Inserts an inspector at the applied position in the view hierarchy.
- [inspectorColumnWidth(_:)](https://developer.apple.com/documentation/swiftui/view/inspectorcolumnwidth(_:)) — Sets a fixed, preferred width for the inspector containing this view when presented as a trailing column.
- [inspectorColumnWidth(min:ideal:max:)](https://developer.apple.com/documentation/swiftui/view/inspectorcolumnwidth(min:ideal:max:)) — Sets a flexible, preferred width for the inspector in a trailing-column presentation.

## Dismissing a presentation {#Dismissing-a-presentation}

- [isPresented](https://developer.apple.com/documentation/swiftui/environmentvalues/ispresented) — A Boolean value that indicates whether the view associated with this environment is currently presented.
- [dismiss](https://developer.apple.com/documentation/swiftui/environmentvalues/dismiss) — An action that dismisses the current presentation.
- [DismissAction](https://developer.apple.com/documentation/swiftui/dismissaction) — An action that dismisses a presentation.
- [interactiveDismissDisabled(_:)](https://developer.apple.com/documentation/swiftui/view/interactivedismissdisabled(_:)) — Conditionally prevents interactive dismissal of presentations like popovers, sheets, and inspectors.

## Deprecated {#Deprecated}

- [Alert](https://developer.apple.com/documentation/swiftui/alert) — A representation of an alert presentation.
- [ActionSheet](https://developer.apple.com/documentation/swiftui/actionsheet) — A representation of an action sheet presentation.
- [fileExporter(isPresented:document:contentType:defaultFilename:onCompletion:)](https://developer.apple.com/documentation/swiftui/view/fileexporter(ispresented:document:contenttype:defaultfilename:oncompletion:)) — Presents a system dialog for exporting a document that’s stored in a value type, like a structure, to a file on disk.
- [fileExporter(isPresented:documents:contentType:onCompletion:)](https://developer.apple.com/documentation/swiftui/view/fileexporter(ispresented:documents:contenttype:oncompletion:)) — Presents a system dialog for exporting a collection of value type documents to files on disk.
- [fileExporter(isPresented:document:contentTypes:defaultFilename:onCompletion:onCancellation:)](https://developer.apple.com/documentation/swiftui/view/fileexporter(ispresented:document:contenttypes:defaultfilename:oncompletion:oncancellation:)) — Presents a system dialog for allowing the user to export a `FileDocument` to a file on disk.
