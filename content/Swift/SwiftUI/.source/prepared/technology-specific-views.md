# Technology-specific views

Use SwiftUI views that other Apple frameworks provide.

## Overview {#Overview}

To access SwiftUI views that another framework defines, import both SwiftUI and the other framework into the file where you use the view. You can find the framework to import by looking at the availability information on the view’s documentation page.

![](./images/technology-specific-views-hero@2x.png)

For example, to use the [Map](https://developer.apple.com/documentation/mapkit/map) view in your app, import both SwiftUI and MapKit.

```swift
import SwiftUI
import MapKit

struct MyMapView: View {
    // Center the map on Joshua Tree National Park.
    var region = MKCoordinateRegion(
            center: CLLocationCoordinate2D(latitude: 34.011_286, longitude: -116.166_868),
            span: MKCoordinateSpan(latitudeDelta: 0.2, longitudeDelta: 0.2)
        )

    var body: some View {
        Map(initialPosition: .region(region))
    }
}
```

For design guidance, see [Technologies](https://developer.apple.com/design/human-interface-guidelines/technologies) in the Human Interface Guidelines.

## Displaying web content {#Displaying-web-content}

- [WebView](https://developer.apple.com/documentation/webkit/webview-swift.struct) — A view that displays some web content.
- [WebPage](https://developer.apple.com/documentation/webkit/webpage) — An object that controls and manages the behavior of interactive web content.
- [onWebViewImmersiveEnvironmentRequest(shouldAllow:present:dismiss:)](https://developer.apple.com/documentation/swiftui/view/onwebviewimmersiveenvironmentrequest(shouldallow:present:dismiss:)) — Manages the lifecycle of immersive environments requested by websites.
- [webViewBackForwardNavigationGestures(_:)](https://developer.apple.com/documentation/swiftui/view/webviewbackforwardnavigationgestures(_:)) — Determines whether horizontal swipe gestures trigger backward and forward page navigation.
- [webViewContentBackground(_:)](https://developer.apple.com/documentation/swiftui/view/webviewcontentbackground(_:)) — Specifies the visibility of the webpage’s natural background color within this view.
- [webViewContextMenu(menu:)](https://developer.apple.com/documentation/swiftui/view/webviewcontextmenu(menu:)) — Adds an item-based context menu to a WebView, replacing the default set of context menu items.
- [webViewElementFullscreenBehavior(_:)](https://developer.apple.com/documentation/swiftui/view/webviewelementfullscreenbehavior(_:)) — Determines whether a web view can display content full screen.
- [webViewLinkPreviews(_:)](https://developer.apple.com/documentation/swiftui/view/webviewlinkpreviews(_:)) — Determines whether pressing a link displays a preview of the destination for the link.
- [webViewMagnificationGestures(_:)](https://developer.apple.com/documentation/swiftui/view/webviewmagnificationgestures(_:)) — Determines whether magnify gestures change the view’s magnification.
- [webViewOnScrollGeometryChange(for:of:action:)](https://developer.apple.com/documentation/swiftui/view/webviewonscrollgeometrychange(for:of:action:)) — Adds an action to be performed when a value, created from a scroll geometry, changes.
- [webViewScrollInputBehavior(_:for:)](https://developer.apple.com/documentation/swiftui/view/webviewscrollinputbehavior(_:for:)) — Enables or disables scrolling in web views when using particular inputs.
- [webViewScrollPosition(_:)](https://developer.apple.com/documentation/swiftui/view/webviewscrollposition(_:)) — Associates a binding to a scroll position with the web view.
- [webViewTextSelection(_:)](https://developer.apple.com/documentation/swiftui/view/webviewtextselection(_:)) — Determines whether to allow people to select or otherwise interact with text.

## Accessing Apple Pay and Wallet {#Accessing-Apple-Pay-and-Wallet}

- [PayWithApplePayButton](https://developer.apple.com/documentation/passkit/paywithapplepaybutton) — A type that provides a button to pay with Apple pay.
- [AddPassToWalletButton](https://developer.apple.com/documentation/passkit/addpasstowalletbutton) — A type that provides a button that enables people to add a new or existing pass to Apple Wallet.
- [VerifyIdentityWithWalletButton](https://developer.apple.com/documentation/passkit/verifyidentitywithwalletbutton) — A type that displays a button to present the identity verification flow.
- [addOrderToWalletButtonStyle(_:)](https://developer.apple.com/documentation/swiftui/view/addordertowalletbuttonstyle(_:)) — Sets the button’s style.
- [addPassToWalletButtonStyle(_:)](https://developer.apple.com/documentation/swiftui/view/addpasstowalletbuttonstyle(_:)) — Sets the style to be used by the button. (see `PKAddPassButtonStyle`).
- [onApplePayCouponCodeChange(perform:)](https://developer.apple.com/documentation/swiftui/view/onapplepaycouponcodechange(perform:)) — Called when a user has entered or updated a coupon code. This is required if the user is being asked to provide a coupon code.
- [onApplePayPaymentMethodChange(perform:)](https://developer.apple.com/documentation/swiftui/view/onapplepaypaymentmethodchange(perform:)) — Called when a payment method has changed and asks for an update payment request. If this modifier isn’t provided Wallet will assume the payment method is valid.
- [onApplePayShippingContactChange(perform:)](https://developer.apple.com/documentation/swiftui/view/onapplepayshippingcontactchange(perform:)) — Called when a user selected a shipping address. This is required if the user is being asked to provide a shipping contact.
- [onApplePayShippingMethodChange(perform:)](https://developer.apple.com/documentation/swiftui/view/onapplepayshippingmethodchange(perform:)) — Called when a user selected a shipping method. This is required if the user is being asked to provide a shipping method.
- [payLaterViewAction(_:)](https://developer.apple.com/documentation/swiftui/view/paylaterviewaction(_:)) — Sets the action on the PayLaterView. See `PKPayLaterAction`.
- [payLaterViewDisplayStyle(_:)](https://developer.apple.com/documentation/swiftui/view/paylaterviewdisplaystyle(_:)) — Sets the display style on the PayLaterView. See `PKPayLaterDisplayStyle`.
- [payWithApplePayButtonDisableCardArt()](https://developer.apple.com/documentation/swiftui/view/paywithapplepaybuttondisablecardart()) — Sets the features that should be allowed to show on the payment buttons.
- [payWithApplePayButtonStyle(_:)](https://developer.apple.com/documentation/swiftui/view/paywithapplepaybuttonstyle(_:)) — Sets the style to be used by the button. (see `PayWithApplePayButtonStyle`).
- [verifyIdentityWithWalletButtonStyle(_:)](https://developer.apple.com/documentation/swiftui/view/verifyidentitywithwalletbuttonstyle(_:)) — Sets the style to be used by the button. (see `PKIdentityButtonStyle`).
- [AsyncShareablePassConfiguration](https://developer.apple.com/documentation/passkit/asyncshareablepassconfiguration)
- [transactionTask(_:action:)](https://developer.apple.com/documentation/swiftui/view/transactiontask(_:action:)) — Provides a task to perform before this view appears

## Authorizing and authenticating {#Authorizing-and-authenticating}

- [LocalAuthenticationView](https://developer.apple.com/documentation/localauthentication/localauthenticationview) — A SwiftUI view that displays an authentication interface.
- [SignInWithAppleButton](https://developer.apple.com/documentation/authenticationservices/signinwithapplebutton) — A SwiftUI view that creates the Sign in with Apple button for display.
- [signInWithAppleButtonStyle(_:)](https://developer.apple.com/documentation/swiftui/view/signinwithapplebuttonstyle(_:)) — Sets the style used for displaying the control (see `SignInWithAppleButton.Style`).
- [authorizationController](https://developer.apple.com/documentation/swiftui/environmentvalues/authorizationcontroller) — A value provided in the SwiftUI environment that views can use to perform authorization requests.
- [webAuthenticationSession](https://developer.apple.com/documentation/swiftui/environmentvalues/webauthenticationsession) — A value provided in the SwiftUI environment that views can use to authenticate a user through a web service.

## Configuring Family Sharing {#Configuring-Family-Sharing}

- [FamilyActivityPicker](https://developer.apple.com/documentation/familycontrols/familyactivitypicker) — A view in which users specify applications, web domains, and categories without revealing their choices to the app.
- [familyActivityPicker(isPresented:selection:)](https://developer.apple.com/documentation/swiftui/view/familyactivitypicker(ispresented:selection:)) — Presents an activity picker view as a sheet.
- [familyActivityPicker(headerText:footerText:isPresented:selection:)](https://developer.apple.com/documentation/swiftui/view/familyactivitypicker(headertext:footertext:ispresented:selection:)) — Presents an activity picker view as a sheet.
- [familyActivityPicker(title:headerText:footerText:isPresented:selection:)](https://developer.apple.com/documentation/swiftui/view/familyactivitypicker(title:headertext:footertext:ispresented:selection:)) — Present an activity picker sheet for selecting apps and websites to manage.

## Reporting on device activity {#Reporting-on-device-activity}

- [DeviceActivityReport](https://developer.apple.com/documentation/deviceactivity/deviceactivityreport) — A view that reports the user’s application, category, and web domain activity in a privacy-preserving way.

## Working with managed devices {#Working-with-managed-devices}

- [managedContentStyle(_:)](https://developer.apple.com/documentation/swiftui/view/managedcontentstyle(_:)) — Applies a managed content style to the view.
- [automatedDeviceEnrollmentAddition(isPresented:)](https://developer.apple.com/documentation/swiftui/view/automateddeviceenrollmentaddition(ispresented:)) — Presents a modal view that enables users to add devices to their organization.

## Creating graphics {#Creating-graphics}

- [Chart](https://developer.apple.com/documentation/charts/chart) — A SwiftUI view that displays a chart.
- [SceneView](https://developer.apple.com/documentation/scenekit/sceneview) — A SwiftUI view for displaying 3D SceneKit content.
- [SpriteView](https://developer.apple.com/documentation/spritekit/spriteview) — A SwiftUI view that renders a SpriteKit scene.

## Getting location information {#Getting-location-information}

- [LocationButton](https://developer.apple.com/documentation/corelocationui/locationbutton) — A SwiftUI button that grants one-time location authorization.
- [Map](https://developer.apple.com/documentation/mapkit/map) — A view that displays an embedded map interface.
- [mapStyle(_:)](https://developer.apple.com/documentation/swiftui/view/mapstyle(_:)) — Specifies the map style to be used.
- [mapScope(_:)](https://developer.apple.com/documentation/swiftui/view/mapscope(_:)) — Creates a mapScope that SwiftUI uses to connect map controls to an associated map.
- [mapFeatureSelectionDisabled(_:)](https://developer.apple.com/documentation/swiftui/view/mapfeatureselectiondisabled(_:)) — Specifies which map features should have selection disabled.
- [mapFeatureSelectionAccessory(_:)](https://developer.apple.com/documentation/swiftui/view/mapfeatureselectionaccessory(_:)) — Specifies the selection accessory to display for a `MapFeature`
- [mapFeatureSelectionContent(content:)](https://developer.apple.com/documentation/swiftui/view/mapfeatureselectioncontent(content:)) — Specifies a custom presentation for the currently selected feature.
- [mapControls(_:)](https://developer.apple.com/documentation/swiftui/view/mapcontrols(_:)) — Configures all `Map` views in the associated environment to have standard size and position controls
- [mapControlVisibility(_:)](https://developer.apple.com/documentation/swiftui/view/mapcontrolvisibility(_:)) — Configures all Map controls in the environment to have the specified visibility
- [mapCameraKeyframeAnimator(trigger:keyframes:)](https://developer.apple.com/documentation/swiftui/view/mapcamerakeyframeanimator(trigger:keyframes:)) — Uses the given keyframes to animate the camera of a `Map` when the given trigger value changes.
- [lookAroundViewer(isPresented:scene:allowsNavigation:showsRoadLabels:pointsOfInterest:onDismiss:)](https://developer.apple.com/documentation/swiftui/view/lookaroundviewer(ispresented:scene:allowsnavigation:showsroadlabels:pointsofinterest:ondismiss:))
- [lookAroundViewer(isPresented:initialScene:allowsNavigation:showsRoadLabels:pointsOfInterest:onDismiss:)](https://developer.apple.com/documentation/swiftui/view/lookaroundviewer(ispresented:initialscene:allowsnavigation:showsroadlabels:pointsofinterest:ondismiss:))
- [onMapCameraChange(frequency:_:)](https://developer.apple.com/documentation/swiftui/view/onmapcamerachange(frequency:_:)) — Performs an action when Map camera framing changes
- [mapItemDetailPopover(isPresented:item:displaysMap:attachmentAnchor:)](https://developer.apple.com/documentation/swiftui/view/mapitemdetailpopover(ispresented:item:displaysmap:attachmentanchor:)) — Presents a map item detail popover.
- [mapItemDetailPopover(isPresented:item:displaysMap:attachmentAnchor:arrowEdge:)](https://developer.apple.com/documentation/swiftui/view/mapitemdetailpopover(ispresented:item:displaysmap:attachmentanchor:arrowedge:)) — Presents a map item detail popover.
- [mapItemDetailPopover(item:displaysMap:attachmentAnchor:)](https://developer.apple.com/documentation/swiftui/view/mapitemdetailpopover(item:displaysmap:attachmentanchor:)) — Presents a map item detail popover.
- [mapItemDetailPopover(item:displaysMap:attachmentAnchor:arrowEdge:)](https://developer.apple.com/documentation/swiftui/view/mapitemdetailpopover(item:displaysmap:attachmentanchor:arrowedge:)) — Presents a map item detail popover.
- [mapItemDetailSheet(isPresented:item:displaysMap:)](https://developer.apple.com/documentation/swiftui/view/mapitemdetailsheet(ispresented:item:displaysmap:)) — Presents a map item detail sheet.
- [mapItemDetailSheet(item:displaysMap:)](https://developer.apple.com/documentation/swiftui/view/mapitemdetailsheet(item:displaysmap:)) — Presents a map item detail sheet.

## Displaying media {#Displaying-media}

- [CameraView](https://developer.apple.com/documentation/homekit/cameraview) — A SwiftUI view into which a video stream or an image snapshot is rendered.
- [NowPlayingView](https://developer.apple.com/documentation/watchkit/nowplayingview) — A view that displays the system’s Now Playing interface so that the user can control audio.
- [VideoPlayer](https://developer.apple.com/documentation/avkit/videoplayer) — A view that displays content from a player and a native user interface to control playback.
- [continuityDevicePicker(isPresented:onDidConnect:)](https://developer.apple.com/documentation/swiftui/view/continuitydevicepicker(ispresented:ondidconnect:)) — A `continuityDevicePicker` should be used to discover and connect nearby continuity device through a button interface or other form of activation. On tvOS, this presents a fullscreen continuity device picker experience when selected. The modal view covers as much the screen of `self` as possible when a given condition is true.
- [cameraAnchor(isActive:)](https://developer.apple.com/documentation/swiftui/view/cameraanchor(isactive:)) — Specifies the view that should act as the virtual camera for Apple Vision Pro 2D Persona stream.
- [foveatedStreamingPauseSheet(session:)](https://developer.apple.com/documentation/swiftui/view/foveatedstreamingpausesheet(session:)) — Tells the system to present a sheet with controls for resuming or ending the foveated streaming session when it pauses.

## Supporting Group Activities {#Supporting-Group-Activities}

- [groupActivityAssociation(_:)](https://developer.apple.com/documentation/swiftui/view/groupactivityassociation(_:)) — Specifies how a view should be associated with the current SharePlay group activity.

## Selecting photos {#Selecting-photos}

- [PhotosPicker](https://developer.apple.com/documentation/photosui/photospicker) — A view that displays a Photos picker for choosing assets from the photo library.
- [photosPicker(isPresented:selection:matching:preferredItemEncoding:)](https://developer.apple.com/documentation/swiftui/view/photospicker(ispresented:selection:matching:preferreditemencoding:)) — Presents a Photos picker that selects a `PhotosPickerItem`.
- [photosPicker(isPresented:selection:matching:preferredItemEncoding:photoLibrary:)](https://developer.apple.com/documentation/swiftui/view/photospicker(ispresented:selection:matching:preferreditemencoding:photolibrary:)) — Presents a Photos picker that selects a `PhotosPickerItem` from a given photo library.
- [photosPicker(isPresented:selection:maxSelectionCount:selectionBehavior:matching:preferredItemEncoding:)](https://developer.apple.com/documentation/swiftui/view/photospicker(ispresented:selection:maxselectioncount:selectionbehavior:matching:preferreditemencoding:)) — Presents a Photos picker that selects a collection of `PhotosPickerItem`.
- [photosPicker(isPresented:selection:maxSelectionCount:selectionBehavior:matching:preferredItemEncoding:photoLibrary:)](https://developer.apple.com/documentation/swiftui/view/photospicker(ispresented:selection:maxselectioncount:selectionbehavior:matching:preferreditemencoding:photolibrary:)) — Presents a Photos picker that selects a collection of `PhotosPickerItem` from a given photo library.
- [photosPickerAccessoryVisibility(_:edges:)](https://developer.apple.com/documentation/swiftui/view/photospickeraccessoryvisibility(_:edges:)) — Sets the accessory visibility of the Photos picker. Accessories include anything between the content and the edge, like the navigation bar or the sidebar.
- [photosPickerDisabledCapabilities(_:)](https://developer.apple.com/documentation/swiftui/view/photospickerdisabledcapabilities(_:)) — Disables capabilities of the Photos picker.
- [photosPickerSearchText(_:)](https://developer.apple.com/documentation/swiftui/view/photospickersearchtext(_:)) — Sets search text of the Photos picker.
- [photosPickerStyle(_:)](https://developer.apple.com/documentation/swiftui/view/photospickerstyle(_:)) — Sets the mode of the Photos picker.
- [photosPickerMetadataOptions(_:)](https://developer.apple.com/documentation/swiftui/view/photospickermetadataoptions(_:)) — Sets metadata options for the Photos picker.
- [photosSharedAlbumCreationSheet(isPresented:defaultTitle:defaultSharingPolicy:photoLibrary:onCompletion:)](https://developer.apple.com/documentation/swiftui/view/photossharedalbumcreationsheet(ispresented:defaulttitle:defaultsharingpolicy:photolibrary:oncompletion:)) — Presents a view for allowing the user to create a new shared album.
- [photosSharedAlbumCustomizationSheet(isPresented:albumIdentifier:photoLibrary:onCompletion:)](https://developer.apple.com/documentation/swiftui/view/photossharedalbumcustomizationsheet(ispresented:albumidentifier:photolibrary:oncompletion:)) — Presents a view for allowing the user to customize a specified shared album.
- [photosSharedAlbumPostingSheet(isPresented:items:defaultAlbumIdentifier:photoLibrary:completion:)](https://developer.apple.com/documentation/swiftui/view/photossharedalbumpostingsheet(ispresented:items:defaultalbumidentifier:photolibrary:completion:)) — Presents an “Add to Shared Album” sheet that allows the user to post the given items to a shared album.

## Generating images {#Generating-images}

- [imagePlaygroundGenerationStyle(_:in:)](https://developer.apple.com/documentation/swiftui/view/imageplaygroundgenerationstyle(_:in:)) — Sets the selected and allowed styles to use when displaying the image generation sheet.
- [imagePlaygroundOptions(_:)](https://developer.apple.com/documentation/swiftui/view/imageplaygroundoptions(_:)) — Sets the options to use when generating an image.
- [imagePlaygroundSheet(isPresented:concept:sourceImage:onCompletion:onCancellation:)](https://developer.apple.com/documentation/swiftui/view/imageplaygroundsheet(ispresented:concept:sourceimage:oncompletion:oncancellation:)) — Presents the system sheet to create an image using the specified string and optional starting image.
- [imagePlaygroundSheet(isPresented:concept:sourceImage:onCompletion:onAdaptiveImageGlyphCreation:onCancellation:)](https://developer.apple.com/documentation/swiftui/view/imageplaygroundsheet(ispresented:concept:sourceimage:oncompletion:onadaptiveimageglyphcreation:oncancellation:)) — Presents the system sheet to create images from the specified input.
- [imagePlaygroundSheet(isPresented:concept:sourceImageURL:onCompletion:onCancellation:)](https://developer.apple.com/documentation/swiftui/view/imageplaygroundsheet(ispresented:concept:sourceimageurl:oncompletion:oncancellation:)) — Presents the system sheet to create an image using the specified string and image URL.
- [imagePlaygroundSheet(isPresented:concept:sourceImageURL:onCompletion:onAdaptiveImageGlyphCreation:onCancellation:)](https://developer.apple.com/documentation/swiftui/view/imageplaygroundsheet(ispresented:concept:sourceimageurl:oncompletion:onadaptiveimageglyphcreation:oncancellation:)) — Presents the system sheet to create an image or Genmoji using the specified string and image URL.
- [imagePlaygroundSheet(isPresented:concepts:sourceImage:onCompletion:onCancellation:)](https://developer.apple.com/documentation/swiftui/view/imageplaygroundsheet(ispresented:concepts:sourceimage:oncompletion:oncancellation:)) — Presents the system sheet to create an image using one or more concepts and an optional starting image.
- [imagePlaygroundSheet(isPresented:concepts:sourceImage:onCompletion:onAdaptiveImageGlyphCreation:onCancellation:)](https://developer.apple.com/documentation/swiftui/view/imageplaygroundsheet(ispresented:concepts:sourceimage:oncompletion:onadaptiveimageglyphcreation:oncancellation:)) — Presents the system sheet to create an image or Genmoji using one or more concepts and an optional starting image.
- [imagePlaygroundSheet(isPresented:concepts:sourceImageURL:onCompletion:onCancellation:)](https://developer.apple.com/documentation/swiftui/view/imageplaygroundsheet(ispresented:concepts:sourceimageurl:oncompletion:oncancellation:)) — Presents the system sheet to create an image using one or more concepts and an image URL.
- [imagePlaygroundSheet(isPresented:concepts:sourceImageURL:onCompletion:onAdaptiveImageGlyphCreation:onCancellation:)](https://developer.apple.com/documentation/swiftui/view/imageplaygroundsheet(ispresented:concepts:sourceimageurl:oncompletion:onadaptiveimageglyphcreation:oncancellation:)) — Presents the system sheet to create an image or Genmoji using one or more concepts and an image URL.

## Previewing content {#Previewing-content}

- [quickLookPreview(_:)](https://developer.apple.com/documentation/swiftui/view/quicklookpreview(_:)) — Presents a Quick Look preview of the contents of a single URL.
- [quickLookPreview(_:in:)](https://developer.apple.com/documentation/swiftui/view/quicklookpreview(_:in:)) — Presents a Quick Look preview of the URLs you provide.

## Interacting with networked devices {#Interacting-with-networked-devices}

- [DevicePicker](https://developer.apple.com/documentation/devicediscoveryui/devicepicker) — A SwiftUI view that displays other devices on the network, and creates an encrypted connection to a copy of your app running on that device.
- [devicePickerSupports](https://developer.apple.com/documentation/swiftui/environmentvalues/devicepickersupports) — Checks for support to present a DevicePicker.

## Configuring a Live Activity {#Configuring-a-Live-Activity}

- [activitySystemActionForegroundColor(_:)](https://developer.apple.com/documentation/swiftui/view/activitysystemactionforegroundcolor(_:)) — The text color for the auxiliary action button that the system shows next to a Live Activity on the Lock Screen.
- [activityBackgroundTint(_:)](https://developer.apple.com/documentation/swiftui/view/activitybackgroundtint(_:)) — Sets the tint color for the background of a Live Activity that appears on the Lock Screen.
- [isActivityFullscreen](https://developer.apple.com/documentation/swiftui/environmentvalues/isactivityfullscreen) — A Boolean value that indicates whether the Live Activity appears in a full-screen presentation.
- [activityFamily](https://developer.apple.com/documentation/swiftui/environmentvalues/activityfamily) — The size family of the current Live Activity.

## Interacting with the App Store and Apple Music {#Interacting-with-the-App-Store-and-Apple-Music}

- [appStoreOverlay(isPresented:configuration:)](https://developer.apple.com/documentation/swiftui/view/appstoreoverlay(ispresented:configuration:)) — Presents a StoreKit overlay when a given condition is true.
- [manageSubscriptionsSheet(isPresented:)](https://developer.apple.com/documentation/swiftui/view/managesubscriptionssheet(ispresented:))
- [refundRequestSheet(for:isPresented:onDismiss:)](https://developer.apple.com/documentation/swiftui/view/refundrequestsheet(for:ispresented:ondismiss:)) — Display the refund request sheet for the given transaction.
- [offerCodeRedemption(options:isPresented:onCompletion:)](https://developer.apple.com/documentation/swiftui/view/offercoderedemption(options:ispresented:oncompletion:)) — Presents a sheet that enables customers to redeem offer codes that you configure in App Store Connect.
- [musicPicker(isPresented:title:selection:)](https://developer.apple.com/documentation/swiftui/view/musicpicker(ispresented:title:selection:)) — Presents a music picker to select items from the Apple Music catalog and the user’s music library.
- [musicSubscriptionOffer(isPresented:options:onLoadCompletion:)](https://developer.apple.com/documentation/swiftui/view/musicsubscriptionoffer(ispresented:options:onloadcompletion:)) — Initiates the process of presenting a sheet with subscription offers for Apple Music when the `isPresented` binding is `true`.
- [currentEntitlementTask(for:priority:action:)](https://developer.apple.com/documentation/swiftui/view/currententitlementtask(for:priority:action:)) — Declares the view as dependent on the entitlement of an In-App Purchase product, and returns a modified view.
- [inAppPurchaseOptions(_:)](https://developer.apple.com/documentation/swiftui/view/inapppurchaseoptions(_:)) — Add a function to call before initiating a purchase from StoreKit view within this view, providing a set of options for the purchase.
- [manageSubscriptionsSheet(isPresented:subscriptionGroupID:)](https://developer.apple.com/documentation/swiftui/view/managesubscriptionssheet(ispresented:subscriptiongroupid:))
- [onInAppPurchaseCompletion(perform:)](https://developer.apple.com/documentation/swiftui/view/oninapppurchasecompletion(perform:)) — Add an action to perform when a purchase initiated from a StoreKit view within this view completes.
- [onInAppPurchaseStart(perform:)](https://developer.apple.com/documentation/swiftui/view/oninapppurchasestart(perform:)) — Add an action to perform when a user triggers the purchase button on a StoreKit view within this view.
- [productIconBorder()](https://developer.apple.com/documentation/swiftui/view/producticonborder()) — Adds a standard border to an in-app purchase product’s icon .
- [productViewStyle(_:)](https://developer.apple.com/documentation/swiftui/view/productviewstyle(_:)) — Sets the style for In-App Purchase product views within a view.
- [productDescription(_:)](https://developer.apple.com/documentation/swiftui/view/productdescription(_:)) — Configure the visibility of labels displaying an in-app purchase product description within the view.
- [storeButton(_:for:)](https://developer.apple.com/documentation/swiftui/view/storebutton(_:for:)) — Specifies the visibility of auxiliary buttons that store view and subscription store view instances may use.
- [storeProductTask(for:priority:action:)](https://developer.apple.com/documentation/swiftui/view/storeproducttask(for:priority:action:)) — Declares the view as dependent on an In-App Purchase product and returns a modified view.
- [storeProductsTask(for:priority:action:)](https://developer.apple.com/documentation/swiftui/view/storeproductstask(for:priority:action:)) — Declares the view as dependent on a collection of In-App Purchase products and returns a modified view.
- [subscriptionStatusTask(for:priority:action:)](https://developer.apple.com/documentation/swiftui/view/subscriptionstatustask(for:priority:action:)) — Declares the view as dependent on the status of an auto-renewable subscription group, and returns a modified view.
- [subscriptionStoreButtonLabel(_:)](https://developer.apple.com/documentation/swiftui/view/subscriptionstorebuttonlabel(_:)) — Configures subscription store view instances within a view to use the provided button label.
- [subscriptionStoreControlIcon(icon:)](https://developer.apple.com/documentation/swiftui/view/subscriptionstorecontrolicon(icon:)) — Sets a view to use to decorate individual subscription options within a subscription store view.
- [subscriptionStoreControlStyle(_:)](https://developer.apple.com/documentation/swiftui/view/subscriptionstorecontrolstyle(_:)) — Sets the control style for subscription store views within a view.
- [subscriptionStoreControlStyle(_:placement:)](https://developer.apple.com/documentation/swiftui/view/subscriptionstorecontrolstyle(_:placement:)) — Sets the control style and control placement for subscription store views within a view.
- [subscriptionStoreOptionGroupStyle(_:)](https://developer.apple.com/documentation/swiftui/view/subscriptionstoreoptiongroupstyle(_:)) — Sets the style subscription store views within this view use to display groups of subscription options.
- [subscriptionStorePickerItemBackground(_:)](https://developer.apple.com/documentation/swiftui/view/subscriptionstorepickeritembackground(_:)) — Sets the background style for picker items of the subscription store view instances within a view.
- [subscriptionStorePickerItemBackground(_:in:)](https://developer.apple.com/documentation/swiftui/view/subscriptionstorepickeritembackground(_:in:)) — Sets the background shape and style for subscription store view picker items within a view.
- [subscriptionStorePolicyDestination(for:destination:)](https://developer.apple.com/documentation/swiftui/view/subscriptionstorepolicydestination(for:destination:)) — Configures a view as the destination for a policy button action in subscription store views.
- [subscriptionStorePolicyDestination(url:for:)](https://developer.apple.com/documentation/swiftui/view/subscriptionstorepolicydestination(url:for:)) — Configures a URL as the destination for a policy button action in subscription store views.
- [subscriptionStorePolicyForegroundStyle(_:)](https://developer.apple.com/documentation/swiftui/view/subscriptionstorepolicyforegroundstyle(_:)) — Sets the style for the terms of service and privacy policy buttons within a subscription store view.
- [subscriptionStorePolicyForegroundStyle(_:_:)](https://developer.apple.com/documentation/swiftui/view/subscriptionstorepolicyforegroundstyle(_:_:)) — Sets the primary and secondary style for the terms of service and privacy policy buttons within a subscription store view.
- [subscriptionStoreSignInAction(_:)](https://developer.apple.com/documentation/swiftui/view/subscriptionstoresigninaction(_:)) — Adds an action to perform when a person uses the sign-in button on a subscription store view within a view.
- [subscriptionStoreControlBackground(_:)](https://developer.apple.com/documentation/swiftui/view/subscriptionstorecontrolbackground(_:)) — Set a standard effect to use for the background of subscription store view controls within the view.
- [subscriptionPromotionalOffer(offer:compactJWS:)](https://developer.apple.com/documentation/swiftui/view/subscriptionpromotionaloffer(offer:compactjws:)) — Selects a promotional offer to apply to a purchase a customer makes from a subscription store view.
- [subscriptionIntroductoryOffer(applyOffer:compactJWS:)](https://developer.apple.com/documentation/swiftui/view/subscriptionintroductoryoffer(applyoffer:compactjws:)) — Selects the introductory offer eligibility preference to apply to a purchase a customer makes from a subscription store view.
- [subscriptionOfferViewButtonVisibility(_:for:)](https://developer.apple.com/documentation/swiftui/view/subscriptionofferviewbuttonvisibility(_:for:))
- [subscriptionOfferViewDetailAction(_:)](https://developer.apple.com/documentation/swiftui/view/subscriptionofferviewdetailaction(_:))
- [subscriptionOfferViewStyle(_:)](https://developer.apple.com/documentation/swiftui/view/subscriptionofferviewstyle(_:))
- [preferredSubscriptionOffer(_:)](https://developer.apple.com/documentation/swiftui/view/preferredsubscriptionoffer(_:)) — Selects a subscription offer to apply to a purchase that a customer makes from a subscription store view, a store view, or a product view.
- [preferredSubscriptionPricingTerms(_:)](https://developer.apple.com/documentation/swiftui/view/preferredsubscriptionpricingterms(_:))

## Accessing health data {#Accessing-health-data}

- [healthDataAccessRequest(store:objectType:predicate:trigger:completion:)](https://developer.apple.com/documentation/swiftui/view/healthdataaccessrequest(store:objecttype:predicate:trigger:completion:)) — Asynchronously requests permission to read a data type that requires per-object authorization (such as vision prescriptions).
- [healthDataAccessRequest(store:readTypes:trigger:completion:)](https://developer.apple.com/documentation/swiftui/view/healthdataaccessrequest(store:readtypes:trigger:completion:)) — Requests permission to read the specified HealthKit data types.
- [healthDataAccessRequest(store:shareTypes:readTypes:trigger:completion:)](https://developer.apple.com/documentation/swiftui/view/healthdataaccessrequest(store:sharetypes:readtypes:trigger:completion:)) — Requests permission to save and read the specified HealthKit data types.
- [workoutPreview(_:isPresented:)](https://developer.apple.com/documentation/swiftui/view/workoutpreview(_:ispresented:)) — Presents a preview of the workout contents as a modal sheet

## Providing tips {#Providing-tips}

- [popoverTip(_:arrowEdge:action:)](https://developer.apple.com/documentation/swiftui/view/popovertip(_:arrowedge:action:)) — Presents a popover tip on the modified view.
- [popoverTip(_:isPresented:attachmentAnchor:arrowEdge:action:)](https://developer.apple.com/documentation/swiftui/view/popovertip(_:ispresented:attachmentanchor:arrowedge:action:)) — Presents a popover tip on the modified view.
- [popoverTip(_:isPresented:attachmentAnchor:arrowEdges:action:)](https://developer.apple.com/documentation/swiftui/view/popovertip(_:ispresented:attachmentanchor:arrowedges:action:)) — Presents a popover tip on the modified view.
- [tipAnchor(_:)](https://developer.apple.com/documentation/swiftui/view/tipanchor(_:)) — Sets a value for the specified tip anchor to be used to anchor a tip view to the `.bounds` of the view.
- [tipBackground(_:)](https://developer.apple.com/documentation/swiftui/view/tipbackground(_:)) — Sets the tip’s view background to a style.
- [tipBackgroundInteraction(_:)](https://developer.apple.com/documentation/swiftui/view/tipbackgroundinteraction(_:)) — Controls whether people can interact with the view behind a presented tip.
- [tipCornerRadius(_:antialiased:)](https://developer.apple.com/documentation/swiftui/view/tipcornerradius(_:antialiased:)) — Sets the corner radius for an inline tip view.
- [tipImageSize(_:)](https://developer.apple.com/documentation/swiftui/view/tipimagesize(_:)) — Sets the size for a tip’s image.
- [tipViewStyle(_:)](https://developer.apple.com/documentation/swiftui/view/tipviewstyle(_:)) — Sets the given style for TipView within the view hierarchy.
- [tipImageStyle(_:)](https://developer.apple.com/documentation/swiftui/view/tipimagestyle(_:)) — Sets the style for a tip’s image.
- [tipImageStyle(_:_:)](https://developer.apple.com/documentation/swiftui/view/tipimagestyle(_:_:)) — Sets the style for a tip’s image.
- [tipImageStyle(_:_:_:)](https://developer.apple.com/documentation/swiftui/view/tipimagestyle(_:_:_:)) — Sets the style for a tip’s image.

## Showing a translation {#Showing-a-translation}

- [translationPresentation(isPresented:text:attachmentAnchor:arrowEdge:replacementAction:)](https://developer.apple.com/documentation/swiftui/view/translationpresentation(ispresented:text:attachmentanchor:arrowedge:replacementaction:)) — Presents a translation popover when a given condition is true.
- [translationTask(_:action:)](https://developer.apple.com/documentation/swiftui/view/translationtask(_:action:)) — Adds a task to perform before this view appears or when the translation configuration changes.
- [translationTask(source:target:action:)](https://developer.apple.com/documentation/swiftui/view/translationtask(source:target:action:)) — Adds a task to perform before this view appears or when the specified source or target languages change.
- [translationTask(source:target:preferredStrategy:action:)](https://developer.apple.com/documentation/swiftui/view/translationtask(source:target:preferredstrategy:action:)) — Adds a task to perform before this view appears or when the specified source or target languages change.

## Presenting journaling suggestions {#Presenting-journaling-suggestions}

- [journalingSuggestionsPicker(isPresented:onCompletion:)](https://developer.apple.com/documentation/swiftui/view/journalingsuggestionspicker(ispresented:oncompletion:)) — Presents a visual picker interface that contains events and images that a person can select to retrieve more information.
- [journalingSuggestionsPicker(isPresented:journalingSuggestionToken:onCompletion:)](https://developer.apple.com/documentation/swiftui/view/journalingsuggestionspicker(ispresented:journalingsuggestiontoken:oncompletion:)) — Presents a visual picker interface that contains events and images that a person can select to retrieve more information.

## Managing contact access {#Managing-contact-access}

- [contactAccessButtonCaption(_:)](https://developer.apple.com/documentation/swiftui/view/contactaccessbuttoncaption(_:))
- [contactAccessButtonStyle(_:)](https://developer.apple.com/documentation/swiftui/view/contactaccessbuttonstyle(_:))
- [contactAccessPicker(isPresented:completionHandler:)](https://developer.apple.com/documentation/swiftui/view/contactaccesspicker(ispresented:completionhandler:)) — Modally present UI which allows the user to select which contacts your app has access to.

## Syncing game saves {#Syncing-game-saves}

- [gameSaveSyncingAlert(directory:finishedLoading:)](https://developer.apple.com/documentation/swiftui/view/gamesavesyncingalert(directory:finishedloading:)) — Presents a modal view while the game synced directory loads.

## Handling game controller events {#Handling-game-controller-events}

- [handlesGameControllerEvents(matching:)](https://developer.apple.com/documentation/swiftui/view/handlesgamecontrollerevents(matching:)) — Specifies the game controllers events which should be delivered through the GameController framework when the view, or one of its descendants has focus.

## Creating a tabletop game {#Creating-a-tabletop-game}

- [tabletopGame(_:parent:automaticUpdate:)](https://developer.apple.com/documentation/swiftui/view/tabletopgame(_:parent:automaticupdate:)) — Adds a tabletop game to a view.
- [tabletopGame(_:parent:automaticUpdate:interaction:)](https://developer.apple.com/documentation/swiftui/view/tabletopgame(_:parent:automaticupdate:interaction:)) — Supplies a closure which returns a new interaction whenever needed.

## Configuring camera controls {#Configuring-camera-controls}

- [realityViewCameraControls](https://developer.apple.com/documentation/swiftui/environmentvalues/realityviewcameracontrols) — The camera controls for the reality view.
- [realityViewCameraControls(_:)](https://developer.apple.com/documentation/swiftui/view/realityviewcameracontrols(_:)) — Adds gestures that control the position and direction of a virtual camera.
- [realityViewLayoutBehavior(_:)](https://developer.apple.com/documentation/swiftui/view/realityviewlayoutbehavior(_:)) — A view modifier that controls the frame sizing and content alignment behavior for `RealityView`

## Interacting with transactions {#Interacting-with-transactions}

- [transactionPicker(isPresented:selection:)](https://developer.apple.com/documentation/swiftui/view/transactionpicker(ispresented:selection:)) — Presents a picker that selects a collection of transactions.
