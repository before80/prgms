# Presentation modifiers

Define additional views for the view to present under specified conditions.

## Overview {#Overview}

Use presentation modifiers to show different kinds of modal presentations, like alerts, popovers, sheets, and confirmation dialogs.

Because SwiftUI is a declarative framework, you don’t call a method at the moment you want to present the modal. Rather, you define how the presentation looks and the condition under which SwiftUI should present it. SwiftUI detects when the condition changes and makes the presentation for you. Because you provide a [Binding](https://developer.apple.com/documentation/swiftui/binding) to the condition that initiates the presentation, SwiftUI can reset the underlying value when the user dismisses the presentation.

For more information about how to use these modifiers, see [Modal presentations](../../../appstructure/7-ModalPresentations/).

## Alerts {#Alerts}

- [alert(_:isPresented:actions:)](https://developer.apple.com/documentation/swiftui/view/alert(_:ispresented:actions:)) — Presents an alert when a given condition is true, using a localized string resource for the title.
- [alert(_:isPresented:presenting:actions:)](https://developer.apple.com/documentation/swiftui/view/alert(_:ispresented:presenting:actions:)) — Presents an alert using the given data to produce the alert’s content and a localized string resource for a title.
- [alert(_:item:actions:)](https://developer.apple.com/documentation/swiftui/view/alert(_:item:actions:)) — Presents an alert using the given data to produce the alert’s content and a text view as a title.
- [alert(error:actions:)](https://developer.apple.com/documentation/swiftui/view/alert(error:actions:)) — Presents an alert when an error is present.
- [alert(isPresented:error:actions:)](https://developer.apple.com/documentation/swiftui/view/alert(ispresented:error:actions:)) — Presents an alert when an error is present.

## Alerts with a message {#Alerts-with-a-message}

- [alert(_:isPresented:actions:message:)](https://developer.apple.com/documentation/swiftui/view/alert(_:ispresented:actions:message:)) — Presents an alert with a message when a given condition is true, using a localized string resource for a title.
- [alert(_:isPresented:presenting:actions:message:)](https://developer.apple.com/documentation/swiftui/view/alert(_:ispresented:presenting:actions:message:)) — Presents an alert with a message using the given data to produce the alert’s content and a localized string resource for a title.
- [alert(_:item:actions:message:)](https://developer.apple.com/documentation/swiftui/view/alert(_:item:actions:message:)) — Presents an alert with a message using the given data to produce the alert’s content and a localized string key for a title.
- [alert(error:actions:message:)](https://developer.apple.com/documentation/swiftui/view/alert(error:actions:message:)) — Presents an alert with a message when an error is present.
- [alert(isPresented:error:actions:message:)](https://developer.apple.com/documentation/swiftui/view/alert(ispresented:error:actions:message:)) — Presents an alert with a message when an error is present.

## Confirmation dialogs {#Confirmation-dialogs}

- [confirmationDialog(_:isPresented:titleVisibility:actions:)](https://developer.apple.com/documentation/swiftui/view/confirmationdialog(_:ispresented:titlevisibility:actions:)) — Presents a confirmation dialog when a given condition is true, using a localized string resource for the title.
- [confirmationDialog(_:isPresented:titleVisibility:presenting:actions:)](https://developer.apple.com/documentation/swiftui/view/confirmationdialog(_:ispresented:titlevisibility:presenting:actions:)) — Presents a confirmation dialog using data to produce the dialog’s content and a localized string resource for the title.
- [confirmationDialog(_:item:titleVisibility:actions:)](https://developer.apple.com/documentation/swiftui/view/confirmationdialog(_:item:titlevisibility:actions:)) — Presents a confirmation dialog using data to produce the dialog’s content and a text view for the title.
- [dismissalConfirmationDialog(_:shouldPresent:actions:)](https://developer.apple.com/documentation/swiftui/view/dismissalconfirmationdialog(_:shouldpresent:actions:)) — Presents a confirmation dialog when a dismiss action has been triggered.

## Confirmation dialogs with a message {#Confirmation-dialogs-with-a-message}

- [confirmationDialog(_:isPresented:titleVisibility:actions:message:)](https://developer.apple.com/documentation/swiftui/view/confirmationdialog(_:ispresented:titlevisibility:actions:message:)) — Presents a confirmation dialog with a message when a given condition is true, using a localized string resource for the title.
- [confirmationDialog(_:isPresented:titleVisibility:presenting:actions:message:)](https://developer.apple.com/documentation/swiftui/view/confirmationdialog(_:ispresented:titlevisibility:presenting:actions:message:)) — Presents a confirmation dialog with a message using data to produce the dialog’s content and a localized string resource for the title.
- [confirmationDialog(_:item:titleVisibility:actions:message:)](https://developer.apple.com/documentation/swiftui/view/confirmationdialog(_:item:titlevisibility:actions:message:)) — Presents a confirmation dialog with a message using data to produce the dialog’s content and a text view for the message.
- [dismissalConfirmationDialog(_:shouldPresent:actions:message:)](https://developer.apple.com/documentation/swiftui/view/dismissalconfirmationdialog(_:shouldpresent:actions:message:)) — Presents a confirmation dialog when a dismiss action has been triggered.

## Dialog configuration {#Dialog-configuration}

- [dialogIcon(_:)](https://developer.apple.com/documentation/swiftui/view/dialogicon(_:)) — Configures the icon used by dialogs within this view.
- [dialogSeverity(_:)](https://developer.apple.com/documentation/swiftui/view/dialogseverity(_:))
- [dialogSuppressionToggle(isSuppressed:)](https://developer.apple.com/documentation/swiftui/view/dialogsuppressiontoggle(issuppressed:)) — Enables user suppression of dialogs and alerts presented within `self`, with a default suppression message on macOS. Unused on other platforms.
- [dialogSuppressionToggle(_:isSuppressed:)](https://developer.apple.com/documentation/swiftui/view/dialogsuppressiontoggle(_:issuppressed:)) — Enables user suppression of dialogs and alerts presented within `self`, with a custom suppression message on macOS. Unused on other platforms.
- [dialogPreventsAppTermination(_:)](https://developer.apple.com/documentation/swiftui/view/dialogpreventsapptermination(_:)) — Whether the alert or confirmation dialog prevents the app from being quit/terminated by the system or app termination menu item.

## Sheets {#Sheets}

- [sheet(isPresented:onDismiss:content:)](https://developer.apple.com/documentation/swiftui/view/sheet(ispresented:ondismiss:content:)) — Presents a sheet when a binding to a Boolean value that you provide is true.
- [sheet(item:onDismiss:content:)](https://developer.apple.com/documentation/swiftui/view/sheet(item:ondismiss:content:)) — Presents a sheet using the given item as a data source for the sheet’s content.
- [fullScreenCover(isPresented:onDismiss:content:)](https://developer.apple.com/documentation/swiftui/view/fullscreencover(ispresented:ondismiss:content:)) — Presents a modal view that covers as much of the screen as possible when binding to a Boolean value you provide is true.
- [fullScreenCover(item:onDismiss:content:)](https://developer.apple.com/documentation/swiftui/view/fullscreencover(item:ondismiss:content:)) — Presents a modal view that covers as much of the screen as possible using the binding you provide as a data source for the sheet’s content.

## Popovers {#Popovers}

- [popover(item:attachmentAnchor:arrowEdge:content:)](https://developer.apple.com/documentation/swiftui/view/popover(item:attachmentanchor:arrowedge:content:)) — Presents a popover using the given item as a data source for the popover’s content.
- [popover(isPresented:attachmentAnchor:arrowEdge:content:)](https://developer.apple.com/documentation/swiftui/view/popover(ispresented:attachmentanchor:arrowedge:content:)) — Presents a popover when a given condition is true.

## Sheet and popover configuration {#Sheet-and-popover-configuration}

- [interactiveDismissDisabled(_:)](https://developer.apple.com/documentation/swiftui/view/interactivedismissdisabled(_:)) — Conditionally prevents interactive dismissal of presentations like popovers, sheets, and inspectors.
- [presentationDetents(_:)](https://developer.apple.com/documentation/swiftui/view/presentationdetents(_:)) — Sets the available detents for the enclosing sheet.
- [presentationDetents(_:selection:)](https://developer.apple.com/documentation/swiftui/view/presentationdetents(_:selection:)) — Sets the available detents for the enclosing sheet, giving you programmatic control of the currently selected detent.
- [presentationDragIndicator(_:)](https://developer.apple.com/documentation/swiftui/view/presentationdragindicator(_:)) — Sets the visibility of the drag indicator on top of a sheet.
- [presentationBackground(_:)](https://developer.apple.com/documentation/swiftui/view/presentationbackground(_:)) — Sets the presentation background of the enclosing sheet using a shape style.
- [presentationBackground(alignment:content:)](https://developer.apple.com/documentation/swiftui/view/presentationbackground(alignment:content:)) — Sets the presentation background of the enclosing sheet to a custom view.
- [presentationBackgroundInteraction(_:)](https://developer.apple.com/documentation/swiftui/view/presentationbackgroundinteraction(_:)) — Controls whether people can interact with the view behind a presentation.
- [presentationCompactAdaptation(horizontal:vertical:)](https://developer.apple.com/documentation/swiftui/view/presentationcompactadaptation(horizontal:vertical:)) — Specifies how to adapt a presentation to horizontally and vertically compact size classes.
- [presentationCompactAdaptation(_:)](https://developer.apple.com/documentation/swiftui/view/presentationcompactadaptation(_:)) — Specifies how to adapt a presentation to compact size classes.
- [presentationContentInteraction(_:)](https://developer.apple.com/documentation/swiftui/view/presentationcontentinteraction(_:)) — Configures the behavior of swipe gestures on a presentation.
- [presentationCornerRadius(_:)](https://developer.apple.com/documentation/swiftui/view/presentationcornerradius(_:)) — Requests that the presentation have a specific corner radius.
- [presentationSizing(_:)](https://developer.apple.com/documentation/swiftui/view/presentationsizing(_:)) — Sets the sizing of the containing presentation.
- [presentationBreakthroughEffect(_:)](https://developer.apple.com/documentation/swiftui/view/presentationbreakthrougheffect(_:)) — Changes the way the enclosing presentation breaks through content occluding it.
- [presentationPreventsAppTermination(_:)](https://developer.apple.com/documentation/swiftui/view/presentationpreventsapptermination(_:)) — Whether a presentation prevents the app from being terminated/quit by the system or app termination menu item.
- [presentationPlacement(_:)](https://developer.apple.com/documentation/swiftui/view/presentationplacement(_:)) — Sets the placement of a presentation within the presenting view.
- [PresentationPlacement](https://developer.apple.com/documentation/swiftui/presentationplacement) — The placement of a presentation within the presenting view.

## File exporter {#File-exporter}

- [fileExporter(isPresented:document:contentType:defaultFilename:onCompletion:onCancellation:)](https://developer.apple.com/documentation/swiftui/view/fileexporter(ispresented:document:contenttype:defaultfilename:oncompletion:oncancellation:)) — Presents a system dialog for allowing the user to export a `WritableDocument` to a file on disk.
- [fileExporter(isPresented:documents:contentTypes:onCompletion:onCancellation:)](https://developer.apple.com/documentation/swiftui/view/fileexporter(ispresented:documents:contenttypes:oncompletion:oncancellation:)) — Presents a system dialog for allowing the user to export a collection of objects conforming to `WritableDocument` to files on disk.
- [fileExporter(isPresented:item:contentTypes:defaultFilename:onCompletion:onCancellation:)](https://developer.apple.com/documentation/swiftui/view/fileexporter(ispresented:item:contenttypes:defaultfilename:oncompletion:oncancellation:)) — Presents a system dialog allowing the user to export a `Transferable` item to a file on disk.
- [fileExporter(isPresented:items:contentTypes:onCompletion:onCancellation:)](https://developer.apple.com/documentation/swiftui/view/fileexporter(ispresented:items:contenttypes:oncompletion:oncancellation:)) — Presents a system dialog allowing the user to export a collection of `Transferable` items to files on disk.
- [fileExporterFilenameLabel(_:)](https://developer.apple.com/documentation/swiftui/view/fileexporterfilenamelabel(_:)) — On macOS, configures the `fileExporter` with a label for the file name field.
- [fileExporter(isPresented:document:contentType:defaultFilename:onCompletion:)](https://developer.apple.com/documentation/swiftui/view/fileexporter(ispresented:document:contenttype:defaultfilename:oncompletion:)) — Presents a system dialog for exporting a document that’s stored in a value type, like a structure, to a file on disk.
- [fileExporter(isPresented:documents:contentType:onCompletion:)](https://developer.apple.com/documentation/swiftui/view/fileexporter(ispresented:documents:contenttype:oncompletion:)) — Presents a system dialog for exporting a collection of value type documents to files on disk.
- [fileExporter(isPresented:document:contentTypes:defaultFilename:onCompletion:onCancellation:)](https://developer.apple.com/documentation/swiftui/view/fileexporter(ispresented:document:contenttypes:defaultfilename:oncompletion:oncancellation:)) — Presents a system dialog for allowing the user to export a `FileDocument` to a file on disk.

## File importer {#File-importer}

- [fileImporter(isPresented:allowedContentTypes:allowsMultipleSelection:onCompletion:)](https://developer.apple.com/documentation/swiftui/view/fileimporter(ispresented:allowedcontenttypes:allowsmultipleselection:oncompletion:)) — Presents a system dialog for allowing the user to import multiple files.
- [fileImporter(isPresented:allowedContentTypes:onCompletion:)](https://developer.apple.com/documentation/swiftui/view/fileimporter(ispresented:allowedcontenttypes:oncompletion:)) — Presents a system dialog for allowing the user to import an existing file.
- [fileImporter(isPresented:allowedContentTypes:allowsMultipleSelection:onCompletion:onCancellation:)](https://developer.apple.com/documentation/swiftui/view/fileimporter(ispresented:allowedcontenttypes:allowsmultipleselection:oncompletion:oncancellation:)) — Presents a system dialog for allowing the user to import multiple files.

## File mover {#File-mover}

- [fileMover(isPresented:file:onCompletion:)](https://developer.apple.com/documentation/swiftui/view/filemover(ispresented:file:oncompletion:)) — Presents a system dialog for allowing the user to move an existing file to a new location.
- [fileMover(isPresented:files:onCompletion:)](https://developer.apple.com/documentation/swiftui/view/filemover(ispresented:files:oncompletion:)) — Presents a system dialog for allowing the user to move a collection of existing files to a new location.
- [fileMover(isPresented:file:onCompletion:onCancellation:)](https://developer.apple.com/documentation/swiftui/view/filemover(ispresented:file:oncompletion:oncancellation:)) — Presents a system dialog for allowing the user to move an existing file to a new location.
- [fileMover(isPresented:files:onCompletion:onCancellation:)](https://developer.apple.com/documentation/swiftui/view/filemover(ispresented:files:oncompletion:oncancellation:)) — Presents a system dialog for allowing the user to move a collection of existing files to a new location.

## File dialog configuration {#File-dialog-configuration}

- [fileDialogBrowserOptions(_:)](https://developer.apple.com/documentation/swiftui/view/filedialogbrowseroptions(_:)) — On macOS, configures the `fileExporter`, `fileImporter`, or `fileMover` to provide a refined URL search experience: include or exclude hidden files, allow searching by tag, etc.
- [fileDialogConfirmationLabel(_:)](https://developer.apple.com/documentation/swiftui/view/filedialogconfirmationlabel(_:)) — On macOS, configures the `fileExporter`, `fileImporter`, or `fileMover` with a custom confirmation button label.
- [fileDialogCustomizationID(_:)](https://developer.apple.com/documentation/swiftui/view/filedialogcustomizationid(_:)) — On macOS, configures the `fileExporter`, `fileImporter`, or `fileMover` to persist and restore the file dialog configuration.
- [fileDialogDefaultDirectory(_:)](https://developer.apple.com/documentation/swiftui/view/filedialogdefaultdirectory(_:)) — Configures the `fileExporter`, `fileImporter`, or `fileMover` to open with the specified default directory.
- [fileDialogImportsUnresolvedAliases(_:)](https://developer.apple.com/documentation/swiftui/view/filedialogimportsunresolvedaliases(_:)) — On macOS, configures the `fileExporter`, `fileImporter`, or `fileMover` behavior when a user chooses an alias.
- [fileDialogMessage(_:)](https://developer.apple.com/documentation/swiftui/view/filedialogmessage(_:)) — On macOS, configures the `fileExporter`, `fileImporter`, or `fileMover` with a custom message that is presented to the user, similar to a title.
- [fileDialogURLEnabled(_:)](https://developer.apple.com/documentation/swiftui/view/filedialogurlenabled(_:)) — On macOS, configures the `fileImporter` or `fileMover` to conditionally disable presented URLs.

## Foveated streaming {#Foveated-streaming}

- [foveatedStreamingPauseSheet(session:)](https://developer.apple.com/documentation/swiftui/view/foveatedstreamingpausesheet(session:)) — Tells the system to present a sheet with controls for resuming or ending the foveated streaming session when it pauses.

## Screen capture {#Screen-capture}

- [recordingEditor(_:)](https://developer.apple.com/documentation/swiftui/view/recordingeditor(_:)) — Presents the recording editor for the given recording URL.
- [recordingEditor(_:mode:)](https://developer.apple.com/documentation/swiftui/view/recordingeditor(_:mode:)) — Presents the recording editor for the given recording URL with a specific mode.

## Document browser {#Document-browser}

- [documentLaunchTitle(_:)](https://developer.apple.com/documentation/swiftui/view/documentlaunchtitle(_:)) — Sets the title displayed on the document launch card.
- [documentLaunchSubtitle(_:)](https://developer.apple.com/documentation/swiftui/view/documentlaunchsubtitle(_:)) — Sets the subtitle displayed beneath the title on the document launch card.
- [documentBrowserContextMenu(_:)](https://developer.apple.com/documentation/swiftui/view/documentbrowsercontextmenu(_:)) — Adds to a `DocumentLaunchView` actions that accept a list of selected files as their parameter.

## Inspectors {#Inspectors}

- [inspector(isPresented:content:)](https://developer.apple.com/documentation/swiftui/view/inspector(ispresented:content:)) — Inserts an inspector at the applied position in the view hierarchy.
- [inspectorColumnWidth(_:)](https://developer.apple.com/documentation/swiftui/view/inspectorcolumnwidth(_:)) — Sets a fixed, preferred width for the inspector containing this view when presented as a trailing column.
- [inspectorColumnWidth(min:ideal:max:)](https://developer.apple.com/documentation/swiftui/view/inspectorcolumnwidth(min:ideal:max:)) — Sets a flexible, preferred width for the inspector in a trailing-column presentation.

## Quick look previews {#Quick-look-previews}

- [quickLookPreview(_:)](https://developer.apple.com/documentation/swiftui/view/quicklookpreview(_:)) — Presents a Quick Look preview of the contents of a single URL.
- [quickLookPreview(_:in:)](https://developer.apple.com/documentation/swiftui/view/quicklookpreview(_:in:)) — Presents a Quick Look preview of the URLs you provide.

## Family Sharing {#Family-Sharing}

- [familyActivityPicker(isPresented:selection:)](https://developer.apple.com/documentation/swiftui/view/familyactivitypicker(ispresented:selection:)) — Presents an activity picker view as a sheet.
- [familyActivityPicker(headerText:footerText:isPresented:selection:)](https://developer.apple.com/documentation/swiftui/view/familyactivitypicker(headertext:footertext:ispresented:selection:)) — Presents an activity picker view as a sheet.
- [familyActivityPicker(title:headerText:footerText:isPresented:selection:)](https://developer.apple.com/documentation/swiftui/view/familyactivitypicker(title:headertext:footertext:ispresented:selection:)) — Present an activity picker sheet for selecting apps and websites to manage.

## Live Activities {#Live-Activities}

- [activitySystemActionForegroundColor(_:)](https://developer.apple.com/documentation/swiftui/view/activitysystemactionforegroundcolor(_:)) — The text color for the auxiliary action button that the system shows next to a Live Activity on the Lock Screen.
- [activityBackgroundTint(_:)](https://developer.apple.com/documentation/swiftui/view/activitybackgroundtint(_:)) — Sets the tint color for the background of a Live Activity that appears on the Lock Screen.

## Game saving {#Game-saving}

- [gameSaveSyncingAlert(directory:finishedLoading:)](https://developer.apple.com/documentation/swiftui/view/gamesavesyncingalert(directory:finishedloading:)) — Presents a modal view while the game synced directory loads.

## Apple Music {#Apple-Music}

- [musicSubscriptionOffer(isPresented:options:onLoadCompletion:)](https://developer.apple.com/documentation/swiftui/view/musicsubscriptionoffer(ispresented:options:onloadcompletion:)) — Initiates the process of presenting a sheet with subscription offers for Apple Music when the `isPresented` binding is `true`.

## Contacts {#Contacts}

- [contactAccessButtonCaption(_:)](https://developer.apple.com/documentation/swiftui/view/contactaccessbuttoncaption(_:))
- [contactAccessButtonStyle(_:)](https://developer.apple.com/documentation/swiftui/view/contactaccessbuttonstyle(_:))
- [contactAccessPicker(isPresented:completionHandler:)](https://developer.apple.com/documentation/swiftui/view/contactaccesspicker(ispresented:completionhandler:)) — Modally present UI which allows the user to select which contacts your app has access to.

## StoreKit {#StoreKit}

- [appStoreOverlay(isPresented:configuration:)](https://developer.apple.com/documentation/swiftui/view/appstoreoverlay(ispresented:configuration:)) — Presents a StoreKit overlay when a given condition is true.
- [appStoreMerchandising(isPresented:kind:onDismiss:)](https://developer.apple.com/documentation/swiftui/view/appstoremerchandising(ispresented:kind:ondismiss:)) — Display a merchandising view.
- [manageSubscriptionsSheet(isPresented:)](https://developer.apple.com/documentation/swiftui/view/managesubscriptionssheet(ispresented:))
- [refundRequestSheet(for:isPresented:onDismiss:)](https://developer.apple.com/documentation/swiftui/view/refundrequestsheet(for:ispresented:ondismiss:)) — Display the refund request sheet for the given transaction.
- [offerCodeRedemption(options:isPresented:onCompletion:)](https://developer.apple.com/documentation/swiftui/view/offercoderedemption(options:ispresented:oncompletion:)) — Presents a sheet that enables customers to redeem offer codes that you configure in App Store Connect.

## PhotoKit {#PhotoKit}

- [photosPicker(isPresented:selection:matching:preferredItemEncoding:)](https://developer.apple.com/documentation/swiftui/view/photospicker(ispresented:selection:matching:preferreditemencoding:)) — Presents a Photos picker that selects a `PhotosPickerItem`.
- [photosPicker(isPresented:selection:matching:preferredItemEncoding:photoLibrary:)](https://developer.apple.com/documentation/swiftui/view/photospicker(ispresented:selection:matching:preferreditemencoding:photolibrary:)) — Presents a Photos picker that selects a `PhotosPickerItem` from a given photo library.
- [photosPicker(isPresented:selection:maxSelectionCount:selectionBehavior:matching:preferredItemEncoding:)](https://developer.apple.com/documentation/swiftui/view/photospicker(ispresented:selection:maxselectioncount:selectionbehavior:matching:preferreditemencoding:)) — Presents a Photos picker that selects a collection of `PhotosPickerItem`.
- [photosPicker(isPresented:selection:maxSelectionCount:selectionBehavior:matching:preferredItemEncoding:photoLibrary:)](https://developer.apple.com/documentation/swiftui/view/photospicker(ispresented:selection:maxselectioncount:selectionbehavior:matching:preferreditemencoding:photolibrary:)) — Presents a Photos picker that selects a collection of `PhotosPickerItem` from a given photo library.
- [photosPickerAccessoryVisibility(_:edges:)](https://developer.apple.com/documentation/swiftui/view/photospickeraccessoryvisibility(_:edges:)) — Sets the accessory visibility of the Photos picker. Accessories include anything between the content and the edge, like the navigation bar or the sidebar.
- [photosPickerDisabledCapabilities(_:)](https://developer.apple.com/documentation/swiftui/view/photospickerdisabledcapabilities(_:)) — Disables capabilities of the Photos picker.
- [photosPickerSearchText(_:)](https://developer.apple.com/documentation/swiftui/view/photospickersearchtext(_:)) — Sets search text of the Photos picker.
- [photosPickerStyle(_:)](https://developer.apple.com/documentation/swiftui/view/photospickerstyle(_:)) — Sets the mode of the Photos picker.
- [photosSharedAlbumCreationSheet(isPresented:defaultTitle:defaultSharingPolicy:photoLibrary:onCompletion:)](https://developer.apple.com/documentation/swiftui/view/photossharedalbumcreationsheet(ispresented:defaulttitle:defaultsharingpolicy:photolibrary:oncompletion:)) — Presents a view for allowing the user to create a new shared album.
- [photosSharedAlbumCustomizationSheet(isPresented:albumIdentifier:photoLibrary:onCompletion:)](https://developer.apple.com/documentation/swiftui/view/photossharedalbumcustomizationsheet(ispresented:albumidentifier:photolibrary:oncompletion:)) — Presents a view for allowing the user to customize a specified shared album.
- [photosSharedAlbumPostingSheet(isPresented:items:defaultAlbumIdentifier:photoLibrary:completion:)](https://developer.apple.com/documentation/swiftui/view/photossharedalbumpostingsheet(ispresented:items:defaultalbumidentifier:photolibrary:completion:)) — Presents an “Add to Shared Album” sheet that allows the user to post the given items to a shared album.

## Translation {#Translation}

- [translationPresentation(isPresented:text:attachmentAnchor:arrowEdge:replacementAction:)](https://developer.apple.com/documentation/swiftui/view/translationpresentation(ispresented:text:attachmentanchor:arrowedge:replacementaction:)) — Presents a translation popover when a given condition is true.
- [translationTask(_:action:)](https://developer.apple.com/documentation/swiftui/view/translationtask(_:action:)) — Adds a task to perform before this view appears or when the translation configuration changes.
- [translationTask(source:target:action:)](https://developer.apple.com/documentation/swiftui/view/translationtask(source:target:action:)) — Adds a task to perform before this view appears or when the specified source or target languages change.
- [translationTask(source:target:preferredStrategy:action:)](https://developer.apple.com/documentation/swiftui/view/translationtask(source:target:preferredstrategy:action:)) — Adds a task to perform before this view appears or when the specified source or target languages change.

## Security {#Security}

- [certificateSheet(trust:title:message:help:)](https://developer.apple.com/documentation/swiftui/view/certificatesheet(trust:title:message:help:)) — Displays a certificate sheet using the provided certificate trust.
