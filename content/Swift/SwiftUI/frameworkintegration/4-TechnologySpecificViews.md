+++
title = "4 技术专用视图"
date = 2026-09-12T12:47:47+08:00
weight = 4
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++


> 原文链接: [https://developer.apple.com/documentation/swiftui/technology-specific-views](https://developer.apple.com/documentation/swiftui/technology-specific-views)

# 4 技术专用视图

使用其他 Apple 框架提供的 SwiftUI 视图。

## 概述 {#Overview}

要访问其他框架定义的 SwiftUI 视图，请在使用该视图的文件中同时导入 SwiftUI 和那个框架。你可以通过查看该视图文档页面上的可用性信息来确定要导入哪个框架。

![](./images/technology-specific-views-hero@2x.png)

例如，要在应用中使用 [Map](https://developer.apple.com/documentation/mapkit/map) 视图，请同时导入 SwiftUI 和 MapKit。

```swift
import SwiftUI
import MapKit

struct MyMapView: View {
    // 把地图的中心放在约书亚树国家公园。
    var region = MKCoordinateRegion(
            center: CLLocationCoordinate2D(latitude: 34.011_286, longitude: -116.166_868),
            span: MKCoordinateSpan(latitudeDelta: 0.2, longitudeDelta: 0.2)
        )

    var body: some View {
        Map(initialPosition: .region(region))
    }
}
```

关于设计指导，请参阅 Human Interface Guidelines 中的 [技术](https://developer.apple.com/design/human-interface-guidelines/technologies)。

## 显示网页内容 {#Displaying-web-content}

- [WebView](https://developer.apple.com/documentation/webkit/webview-swift.struct) — 一种显示网页内容的视图。
- [WebPage](https://developer.apple.com/documentation/webkit/webpage) — 一个控制和交互式网页内容行为的对象。
- [onWebViewImmersiveEnvironmentRequest(shouldAllow:present:dismiss:)](https://developer.apple.com/documentation/swiftui/view/onwebviewimmersiveenvironmentrequest(shouldallow:present:dismiss:)) — 管理网站请求的沉浸式环境的生命周期。
- [webViewBackForwardNavigationGestures(_:)](https://developer.apple.com/documentation/swiftui/view/webviewbackforwardnavigationgestures(_:)) — 决定水平轻扫手势是否触发页面的后退和前进导航。
- [webViewContentBackground(_:)](https://developer.apple.com/documentation/swiftui/view/webviewcontentbackground(_:)) — 指定该视图中网页原生背景色的可见性。
- [webViewContextMenu(menu:)](https://developer.apple.com/documentation/swiftui/view/webviewcontextmenu(menu:)) — 为 WebView 添加基于项目的上下文菜单，替换默认的上下文菜单项目集合。
- [webViewElementFullscreenBehavior(_:)](https://developer.apple.com/documentation/swiftui/view/webviewelementfullscreenbehavior(_:)) — 决定网页视图是否可以全屏显示内容。
- [webViewLinkPreviews(_:)](https://developer.apple.com/documentation/swiftui/view/webviewlinkpreviews(_:)) — 决定按下链接时是否显示该链接目标的预览。
- [webViewMagnificationGestures(_:)](https://developer.apple.com/documentation/swiftui/view/webviewmagnificationgestures(_:)) — 决定放大手势是否会改变视图的放大倍数。
- [webViewOnScrollGeometryChange(for:of:action:)](https://developer.apple.com/documentation/swiftui/view/webviewonscrollgeometrychange(for:of:action:)) — 添加一个动作，当由滚动的几何信息生成的值发生变化时执行。
- [webViewScrollInputBehavior(_:for:)](https://developer.apple.com/documentation/swiftui/view/webviewscrollinputbehavior(_:for:)) — 启用或停用使用特定输入时网页视图中的滚动。
- [webViewScrollPosition(_:)](https://developer.apple.com/documentation/swiftui/view/webviewscrollposition(_:)) — 把一个滚动位置的绑定关联到网页视图。
- [webViewTextSelection(_:)](https://developer.apple.com/documentation/swiftui/view/webviewtextselection(_:)) — 决定是否允许人们选择文本或以其他方式与文本交互。

## 访问 Apple Pay 和钱包 {#Accessing-Apple-Pay-and-Wallet}

- [PayWithApplePayButton](https://developer.apple.com/documentation/passkit/paywithapplepaybutton) — 一种提供使用 Apple Pay 付款按钮的类型。
- [AddPassToWalletButton](https://developer.apple.com/documentation/passkit/addpasstowalletbutton) — 一种提供按钮的类型，让人们可以把新的或现有的凭证添加到 Apple 钱包。
- [VerifyIdentityWithWalletButton](https://developer.apple.com/documentation/passkit/verifyidentitywithwalletbutton) — 一种显示按钮、用于呈现身份验证流程的类型。
- [addOrderToWalletButtonStyle(_:)](https://developer.apple.com/documentation/swiftui/view/addordertowalletbuttonstyle(_:)) — 设置按钮的样式。
- [addPassToWalletButtonStyle(_:)](https://developer.apple.com/documentation/swiftui/view/addpasstowalletbuttonstyle(_:)) — 设置按钮要使用的样式。（参见 `PKAddPassButtonStyle`）。
- [onApplePayCouponCodeChange(perform:)](https://developer.apple.com/documentation/swiftui/view/onapplepaycouponcodechange(perform:)) — 当用户输入或更新优惠码时调用。如果要求用户提供优惠码，则必须实现这一项。
- [onApplePayPaymentMethodChange(perform:)](https://developer.apple.com/documentation/swiftui/view/onapplepaypaymentmethodchange(perform:)) — 当付款方式发生变化并请求更新付款请求时调用。如果未提供该修饰符，钱包会假定付款方式是有效的。
- [onApplePayShippingContactChange(perform:)](https://developer.apple.com/documentation/swiftui/view/onapplepayshippingcontactchange(perform:)) — 当用户选择收货地址时调用。如果要求用户提供收货联系人，则必须实现这一项。
- [onApplePayShippingMethodChange(perform:)](https://developer.apple.com/documentation/swiftui/view/onapplepayshippingmethodchange(perform:)) — 当用户选择配送方式时调用。如果要求用户提供配送方式，则必须实现这一项。
- [payLaterViewAction(_:)](https://developer.apple.com/documentation/swiftui/view/paylaterviewaction(_:)) — 设置 PayLaterView 上的动作。参见 `PKPayLaterAction`。
- [payLaterViewDisplayStyle(_:)](https://developer.apple.com/documentation/swiftui/view/paylaterviewdisplaystyle(_:)) — 设置 PayLaterView 上的显示样式。参见 `PKPayLaterDisplayStyle`。
- [payWithApplePayButtonDisableCardArt()](https://developer.apple.com/documentation/swiftui/view/paywithapplepaybuttondisablecardart()) — 设置付款按钮上允许显示的功能。
- [payWithApplePayButtonStyle(_:)](https://developer.apple.com/documentation/swiftui/view/paywithapplepaybuttonstyle(_:)) — 设置按钮要使用的样式。（参见 `PayWithApplePayButtonStyle`）。
- [verifyIdentityWithWalletButtonStyle(_:)](https://developer.apple.com/documentation/swiftui/view/verifyidentitywithwalletbuttonstyle(_:)) — 设置按钮要使用的样式。（参见 `PKIdentityButtonStyle`）。
- [AsyncShareablePassConfiguration](https://developer.apple.com/documentation/passkit/asyncshareablepassconfiguration)
- [transactionTask(_:action:)](https://developer.apple.com/documentation/swiftui/view/transactiontask(_:action:)) — 提供一个在该视图出现之前执行的任务

## 授权与认证 {#Authorizing-and-authenticating}

- [LocalAuthenticationView](https://developer.apple.com/documentation/localauthentication/localauthenticationview) — 一种显示认证界面的 SwiftUI 视图。
- [SignInWithAppleButton](https://developer.apple.com/documentation/authenticationservices/signinwithapplebutton) — 一种创建用于显示的“通过 Apple 登录”按钮的 SwiftUI 视图。
- [signInWithAppleButtonStyle(_:)](https://developer.apple.com/documentation/swiftui/view/signinwithapplebuttonstyle(_:)) — 设置用于显示该控件的样式（参见 `SignInWithAppleButton.Style`）。
- [authorizationController](https://developer.apple.com/documentation/swiftui/environmentvalues/authorizationcontroller) — SwiftUI 环境中提供的一个值，视图可以用它来执行授权请求。
- [webAuthenticationSession](https://developer.apple.com/documentation/swiftui/environmentvalues/webauthenticationsession) — SwiftUI 环境中提供的一个值，视图可以用它来通过 Web 服务认证用户。

## 配置家人共享 {#Configuring-Family-Sharing}

- [FamilyActivityPicker](https://developer.apple.com/documentation/familycontrols/familyactivitypicker) — 一种视图，用户可以在其中指定应用、网域和类别，而不会把他们的选择透露给应用。
- [familyActivityPicker(isPresented:selection:)](https://developer.apple.com/documentation/swiftui/view/familyactivitypicker(ispresented:selection:)) — 以工作表形式呈现活动选择器视图。
- [familyActivityPicker(headerText:footerText:isPresented:selection:)](https://developer.apple.com/documentation/swiftui/view/familyactivitypicker(headertext:footertext:ispresented:selection:)) — 以工作表形式呈现活动选择器视图。
- [familyActivityPicker(title:headerText:footerText:isPresented:selection:)](https://developer.apple.com/documentation/swiftui/view/familyactivitypicker(title:headertext:footertext:ispresented:selection:)) — 呈现一个活动选择器工作表，用于选择要管理的应用和网站。

## 报告设备活动 {#Reporting-on-device-activity}

- [DeviceActivityReport](https://developer.apple.com/documentation/deviceactivity/deviceactivityreport) — 一种以保护隐私的方式报告用户应用、类别和网域活动的视图。

## 使用受管理的设备 {#Working-with-managed-devices}

- [managedContentStyle(_:)](https://developer.apple.com/documentation/swiftui/view/managedcontentstyle(_:)) — 为该视图应用受管理内容样式。
- [automatedDeviceEnrollmentAddition(isPresented:)](https://developer.apple.com/documentation/swiftui/view/automateddeviceenrollmentaddition(ispresented:)) — 呈现一个模态视图，让用户可以把设备加入到自己的组织中。

## 创建图形 {#Creating-graphics}

- [Chart](https://developer.apple.com/documentation/charts/chart) — 一种显示图表的 SwiftUI 视图。
- [SceneView](https://developer.apple.com/documentation/scenekit/sceneview) — 一种用于显示三维 SceneKit 内容的 SwiftUI 视图。
- [SpriteView](https://developer.apple.com/documentation/spritekit/spriteview) — 一种渲染 SpriteKit 场景的 SwiftUI 视图。

## 获取位置信息 {#Getting-location-information}

- [LocationButton](https://developer.apple.com/documentation/corelocationui/locationbutton) — 一种授予一次性位置授权的 SwiftUI 按钮。
- [Map](https://developer.apple.com/documentation/mapkit/map) — 一种显示嵌入式地图界面的视图。
- [mapStyle(_:)](https://developer.apple.com/documentation/swiftui/view/mapstyle(_:)) — 指定要使用的地图样式。
- [mapScope(_:)](https://developer.apple.com/documentation/swiftui/view/mapscope(_:)) — 创建一个 mapScope，SwiftUI 用它把地图控件关联到相应的地图。
- [mapFeatureSelectionDisabled(_:)](https://developer.apple.com/documentation/swiftui/view/mapfeatureselectiondisabled(_:)) — 指定哪些地图要素应停用选择。
- [mapFeatureSelectionAccessory(_:)](https://developer.apple.com/documentation/swiftui/view/mapfeatureselectionaccessory(_:)) — 指定要为 `MapFeature` 显示的选择辅助视图
- [mapFeatureSelectionContent(content:)](https://developer.apple.com/documentation/swiftui/view/mapfeatureselectioncontent(content:)) — 为当前选中的要素指定自定义呈现方式。
- [mapControls(_:)](https://developer.apple.com/documentation/swiftui/view/mapcontrols(_:)) — 把关联环境中的所有 `Map` 视图配置为具有标准尺寸和位置的控件
- [mapControlVisibility(_:)](https://developer.apple.com/documentation/swiftui/view/mapcontrolvisibility(_:)) — 把环境中的所有地图控件配置为具有指定的可见性
- [mapCameraKeyframeAnimator(trigger:keyframes:)](https://developer.apple.com/documentation/swiftui/view/mapcamerakeyframeanimator(trigger:keyframes:)) — 当给定的触发值变化时，使用给定的关键帧为 `Map` 的相机添加动画。
- [lookAroundViewer(isPresented:scene:allowsNavigation:showsRoadLabels:pointsOfInterest:onDismiss:)](https://developer.apple.com/documentation/swiftui/view/lookaroundviewer(ispresented:scene:allowsnavigation:showsroadlabels:pointsofinterest:ondismiss:))
- [lookAroundViewer(isPresented:initialScene:allowsNavigation:showsRoadLabels:pointsOfInterest:onDismiss:)](https://developer.apple.com/documentation/swiftui/view/lookaroundviewer(ispresented:initialscene:allowsnavigation:showsroadlabels:pointsofinterest:ondismiss:))
- [onMapCameraChange(frequency:_:)](https://developer.apple.com/documentation/swiftui/view/onmapcamerachange(frequency:_:)) — 当地图相机取景发生变化时执行一个动作
- [mapItemDetailPopover(isPresented:item:displaysMap:attachmentAnchor:)](https://developer.apple.com/documentation/swiftui/view/mapitemdetailpopover(ispresented:item:displaysmap:attachmentanchor:)) — 呈现一个地图项目详情浮层。
- [mapItemDetailPopover(isPresented:item:displaysMap:attachmentAnchor:arrowEdge:)](https://developer.apple.com/documentation/swiftui/view/mapitemdetailpopover(ispresented:item:displaysmap:attachmentanchor:arrowedge:)) — 呈现一个地图项目详情浮层。
- [mapItemDetailPopover(item:displaysMap:attachmentAnchor:)](https://developer.apple.com/documentation/swiftui/view/mapitemdetailpopover(item:displaysmap:attachmentanchor:)) — 呈现一个地图项目详情浮层。
- [mapItemDetailPopover(item:displaysMap:attachmentAnchor:arrowEdge:)](https://developer.apple.com/documentation/swiftui/view/mapitemdetailpopover(item:displaysmap:attachmentanchor:arrowedge:)) — 呈现一个地图项目详情浮层。
- [mapItemDetailSheet(isPresented:item:displaysMap:)](https://developer.apple.com/documentation/swiftui/view/mapitemdetailsheet(ispresented:item:displaysmap:)) — 呈现一个地图项目详情工作表。
- [mapItemDetailSheet(item:displaysMap:)](https://developer.apple.com/documentation/swiftui/view/mapitemdetailsheet(item:displaysmap:)) — 呈现一个地图项目详情工作表。

## 显示媒体 {#Displaying-media}

- [CameraView](https://developer.apple.com/documentation/homekit/cameraview) — 一种 SwiftUI 视图，视频流或图像快照会渲染到其中。
- [NowPlayingView](https://developer.apple.com/documentation/watchkit/nowplayingview) — 一种显示系统“正在播放”界面的视图，让用户可以控制音频。
- [VideoPlayer](https://developer.apple.com/documentation/avkit/videoplayer) — 一种显示播放器内容并提供原生播放控制界面的视图。
- [continuityDevicePicker(isPresented:onDidConnect:)](https://developer.apple.com/documentation/swiftui/view/continuitydevicepicker(ispresented:ondidconnect:)) — 应使用 `continuityDevicePicker` 通过按钮界面或其他激活形式来发现并连接附近的连续互通设备。在 tvOS 上，选中时会呈现全屏的连续互通设备选择器体验。当给定条件为 true 时，该模态视图会尽可能覆盖 `self` 的屏幕。
- [cameraAnchor(isActive:)](https://developer.apple.com/documentation/swiftui/view/cameraanchor(isactive:)) — 指定应用哪个视图作为 Apple Vision Pro 二维 Persona 流的虚拟相机。
- [foveatedStreamingPauseSheet(session:)](https://developer.apple.com/documentation/swiftui/view/foveatedstreamingpausesheet(session:)) — 告诉系统在注视点流式传输会话暂停时，呈现一个带有继续或结束该会话控件的工作表。

## 支持同播共享活动 {#Supporting-Group-Activities}

- [groupActivityAssociation(_:)](https://developer.apple.com/documentation/swiftui/view/groupactivityassociation(_:)) — 指定视图应如何与当前的 SharePlay 同播共享活动关联。

## 选择照片 {#Selecting-photos}

- [PhotosPicker](https://developer.apple.com/documentation/photosui/photospicker) — 一种显示照片选择器的视图，用于从照片图库中挑选资源。
- [photosPicker(isPresented:selection:matching:preferredItemEncoding:)](https://developer.apple.com/documentation/swiftui/view/photospicker(ispresented:selection:matching:preferreditemencoding:)) — 呈现一个选择 `PhotosPickerItem` 的照片选择器。
- [photosPicker(isPresented:selection:matching:preferredItemEncoding:photoLibrary:)](https://developer.apple.com/documentation/swiftui/view/photospicker(ispresented:selection:matching:preferreditemencoding:photolibrary:)) — 呈现一个从给定照片图库中选择 `PhotosPickerItem` 的照片选择器。
- [photosPicker(isPresented:selection:maxSelectionCount:selectionBehavior:matching:preferredItemEncoding:)](https://developer.apple.com/documentation/swiftui/view/photospicker(ispresented:selection:maxselectioncount:selectionbehavior:matching:preferreditemencoding:)) — 呈现一个选择一组 `PhotosPickerItem` 的照片选择器。
- [photosPicker(isPresented:selection:maxSelectionCount:selectionBehavior:matching:preferredItemEncoding:photoLibrary:)](https://developer.apple.com/documentation/swiftui/view/photospicker(ispresented:selection:maxselectioncount:selectionbehavior:matching:preferreditemencoding:photolibrary:)) — 呈现一个从给定照片图库中选择一组 `PhotosPickerItem` 的照片选择器。
- [photosPickerAccessoryVisibility(_:edges:)](https://developer.apple.com/documentation/swiftui/view/photospickeraccessoryvisibility(_:edges:)) — 设置照片选择器辅助元素的可见性。辅助元素包括内容与边缘之间的任何东西，例如导航栏或边栏。
- [photosPickerDisabledCapabilities(_:)](https://developer.apple.com/documentation/swiftui/view/photospickerdisabledcapabilities(_:)) — 停用照片选择器的部分能力。
- [photosPickerSearchText(_:)](https://developer.apple.com/documentation/swiftui/view/photospickersearchtext(_:)) — 设置照片选择器的搜索文本。
- [photosPickerStyle(_:)](https://developer.apple.com/documentation/swiftui/view/photospickerstyle(_:)) — 设置照片选择器的模式。
- [photosPickerMetadataOptions(_:)](https://developer.apple.com/documentation/swiftui/view/photospickermetadataoptions(_:)) — 设置照片选择器的元数据选项。
- [photosSharedAlbumCreationSheet(isPresented:defaultTitle:defaultSharingPolicy:photoLibrary:onCompletion:)](https://developer.apple.com/documentation/swiftui/view/photossharedalbumcreationsheet(ispresented:defaulttitle:defaultsharingpolicy:photolibrary:oncompletion:)) — 呈现一个让用户创建新的共享相簿的视图。
- [photosSharedAlbumCustomizationSheet(isPresented:albumIdentifier:photoLibrary:onCompletion:)](https://developer.apple.com/documentation/swiftui/view/photossharedalbumcustomizationsheet(ispresented:albumidentifier:photolibrary:oncompletion:)) — 呈现一个让用户自定义指定共享相簿的视图。
- [photosSharedAlbumPostingSheet(isPresented:items:defaultAlbumIdentifier:photoLibrary:completion:)](https://developer.apple.com/documentation/swiftui/view/photossharedalbumpostingsheet(ispresented:items:defaultalbumidentifier:photolibrary:completion:)) — 呈现一个“添加到共享相簿”工作表，让用户把给定项目发布到共享相簿。

## 生成图像 {#Generating-images}

- [imagePlaygroundGenerationStyle(_:in:)](https://developer.apple.com/documentation/swiftui/view/imageplaygroundgenerationstyle(_:in:)) — 设置显示图像生成工作表时要使用的已选样式和允许的样式。
- [imagePlaygroundOptions(_:)](https://developer.apple.com/documentation/swiftui/view/imageplaygroundoptions(_:)) — 设置生成图像时要使用的选项。
- [imagePlaygroundSheet(isPresented:concept:sourceImage:onCompletion:onCancellation:)](https://developer.apple.com/documentation/swiftui/view/imageplaygroundsheet(ispresented:concept:sourceimage:oncompletion:oncancellation:)) — 呈现系统工作表，使用指定的字符串和可选的起始图像创建图像。
- [imagePlaygroundSheet(isPresented:concept:sourceImage:onCompletion:onAdaptiveImageGlyphCreation:onCancellation:)](https://developer.apple.com/documentation/swiftui/view/imageplaygroundsheet(ispresented:concept:sourceimage:oncompletion:onadaptiveimageglyphcreation:oncancellation:)) — 呈现系统工作表，根据指定的输入创建图像。
- [imagePlaygroundSheet(isPresented:concept:sourceImageURL:onCompletion:onCancellation:)](https://developer.apple.com/documentation/swiftui/view/imageplaygroundsheet(ispresented:concept:sourceimageurl:oncompletion:oncancellation:)) — 呈现系统工作表，使用指定的字符串和图像 URL 创建图像。
- [imagePlaygroundSheet(isPresented:concept:sourceImageURL:onCompletion:onAdaptiveImageGlyphCreation:onCancellation:)](https://developer.apple.com/documentation/swiftui/view/imageplaygroundsheet(ispresented:concept:sourceimageurl:oncompletion:onadaptiveimageglyphcreation:oncancellation:)) — 呈现系统工作表，使用指定的字符串和图像 URL 创建图像或 Genmoji。
- [imagePlaygroundSheet(isPresented:concepts:sourceImage:onCompletion:onCancellation:)](https://developer.apple.com/documentation/swiftui/view/imageplaygroundsheet(ispresented:concepts:sourceimage:oncompletion:oncancellation:)) — 呈现系统工作表，使用一个或多个概念以及可选的起始图像创建图像。
- [imagePlaygroundSheet(isPresented:concepts:sourceImage:onCompletion:onAdaptiveImageGlyphCreation:onCancellation:)](https://developer.apple.com/documentation/swiftui/view/imageplaygroundsheet(ispresented:concepts:sourceimage:oncompletion:onadaptiveimageglyphcreation:oncancellation:)) — 呈现系统工作表，使用一个或多个概念以及可选的起始图像创建图像或 Genmoji。
- [imagePlaygroundSheet(isPresented:concepts:sourceImageURL:onCompletion:onCancellation:)](https://developer.apple.com/documentation/swiftui/view/imageplaygroundsheet(ispresented:concepts:sourceimageurl:oncompletion:oncancellation:)) — 呈现系统工作表，使用一个或多个概念以及图像 URL 创建图像。
- [imagePlaygroundSheet(isPresented:concepts:sourceImageURL:onCompletion:onAdaptiveImageGlyphCreation:onCancellation:)](https://developer.apple.com/documentation/swiftui/view/imageplaygroundsheet(ispresented:concepts:sourceimageurl:oncompletion:onadaptiveimageglyphcreation:oncancellation:)) — 呈现系统工作表，使用一个或多个概念以及图像 URL 创建图像或 Genmoji。

## 预览内容 {#Previewing-content}

- [quickLookPreview(_:)](https://developer.apple.com/documentation/swiftui/view/quicklookpreview(_:)) — 呈现单个 URL 内容的快速查看预览。
- [quickLookPreview(_:in:)](https://developer.apple.com/documentation/swiftui/view/quicklookpreview(_:in:)) — 呈现你提供的各个 URL 的快速查看预览。

## 与联网设备交互 {#Interacting-with-networked-devices}

- [DevicePicker](https://developer.apple.com/documentation/devicediscoveryui/devicepicker) — 一种显示网络上其他设备、并与运行在该设备上的你的应用副本建立加密连接的 SwiftUI 视图。
- [devicePickerSupports](https://developer.apple.com/documentation/swiftui/environmentvalues/devicepickersupports) — 检查是否支持呈现 DevicePicker。

## 配置实时活动 {#Configuring-a-Live-Activity}

- [activitySystemActionForegroundColor(_:)](https://developer.apple.com/documentation/swiftui/view/activitysystemactionforegroundcolor(_:)) — 系统在锁定屏幕上实时活动旁边显示的辅助操作按钮的文本颜色。
- [activityBackgroundTint(_:)](https://developer.apple.com/documentation/swiftui/view/activitybackgroundtint(_:)) — 设置出现在锁定屏幕上的实时活动背景的着色颜色。
- [isActivityFullscreen](https://developer.apple.com/documentation/swiftui/environmentvalues/isactivityfullscreen) — 一个布尔值，指示实时活动是否以全屏呈现方式显示。
- [activityFamily](https://developer.apple.com/documentation/swiftui/environmentvalues/activityfamily) — 当前实时活动的尺寸系列。

## 与 App Store 和 Apple Music 交互 {#Interacting-with-the-App-Store-and-Apple-Music}

- [appStoreOverlay(isPresented:configuration:)](https://developer.apple.com/documentation/swiftui/view/appstoreoverlay(ispresented:configuration:)) — 当给定条件为 true 时呈现一个 StoreKit 浮层。
- [manageSubscriptionsSheet(isPresented:)](https://developer.apple.com/documentation/swiftui/view/managesubscriptionssheet(ispresented:))
- [refundRequestSheet(for:isPresented:onDismiss:)](https://developer.apple.com/documentation/swiftui/view/refundrequestsheet(for:ispresented:ondismiss:)) — 为给定交易显示退款请求工作表。
- [offerCodeRedemption(options:isPresented:onCompletion:)](https://developer.apple.com/documentation/swiftui/view/offercoderedemption(options:ispresented:oncompletion:)) — 呈现一个工作表，让顾客可以兑换你在 App Store Connect 中配置的优惠码。
- [musicPicker(isPresented:title:selection:)](https://developer.apple.com/documentation/swiftui/view/musicpicker(ispresented:title:selection:)) — 呈现一个音乐选择器，用于从 Apple Music 目录和用户的音乐资料库中选择项目。
- [musicSubscriptionOffer(isPresented:options:onLoadCompletion:)](https://developer.apple.com/documentation/swiftui/view/musicsubscriptionoffer(ispresented:options:onloadcompletion:)) — 当 `isPresented` 绑定为 `true` 时，开始呈现带有 Apple Music 订阅优惠的工作表。
- [currentEntitlementTask(for:priority:action:)](https://developer.apple.com/documentation/swiftui/view/currententitlementtask(for:priority:action:)) — 声明该视图依赖于某个 App 内购买项目的权益，并返回一个修改后的视图。
- [inAppPurchaseOptions(_:)](https://developer.apple.com/documentation/swiftui/view/inapppurchaseoptions(_:)) — 添加一个函数，在该视图内从 StoreKit 视图发起购买之前调用，为这次购买提供一组选项。
- [manageSubscriptionsSheet(isPresented:subscriptionGroupID:)](https://developer.apple.com/documentation/swiftui/view/managesubscriptionssheet(ispresented:subscriptiongroupid:))
- [onInAppPurchaseCompletion(perform:)](https://developer.apple.com/documentation/swiftui/view/oninapppurchasecompletion(perform:)) — 添加一个动作，当从该视图内的 StoreKit 视图发起的购买完成时执行。
- [onInAppPurchaseStart(perform:)](https://developer.apple.com/documentation/swiftui/view/oninapppurchasestart(perform:)) — 添加一个动作，当用户触发该视图内 StoreKit 视图上的购买按钮时执行。
- [productIconBorder()](https://developer.apple.com/documentation/swiftui/view/producticonborder()) — 为 App 内购买项目的图标添加标准边框。
- [productViewStyle(_:)](https://developer.apple.com/documentation/swiftui/view/productviewstyle(_:)) — 设置视图中 App 内购买项目视图的样式。
- [productDescription(_:)](https://developer.apple.com/documentation/swiftui/view/productdescription(_:)) — 配置视图中显示 App 内购买项目说明的标签的可见性。
- [storeButton(_:for:)](https://developer.apple.com/documentation/swiftui/view/storebutton(_:for:)) — 指定商店视图和订阅商店视图实例可能使用的辅助按钮的可见性。
- [storeProductTask(for:priority:action:)](https://developer.apple.com/documentation/swiftui/view/storeproducttask(for:priority:action:)) — 声明该视图依赖于某个 App 内购买项目，并返回一个修改后的视图。
- [storeProductsTask(for:priority:action:)](https://developer.apple.com/documentation/swiftui/view/storeproductstask(for:priority:action:)) — 声明该视图依赖于一组 App 内购买项目，并返回一个修改后的视图。
- [subscriptionStatusTask(for:priority:action:)](https://developer.apple.com/documentation/swiftui/view/subscriptionstatustask(for:priority:action:)) — 声明该视图依赖于某个自动续订订阅组的状态，并返回一个修改后的视图。
- [subscriptionStoreButtonLabel(_:)](https://developer.apple.com/documentation/swiftui/view/subscriptionstorebuttonlabel(_:)) — 把视图内的订阅商店视图实例配置为使用提供的按钮标签。
- [subscriptionStoreControlIcon(icon:)](https://developer.apple.com/documentation/swiftui/view/subscriptionstorecontrolicon(icon:)) — 设置一个视图，用于装饰订阅商店视图中的各个订阅选项。
- [subscriptionStoreControlStyle(_:)](https://developer.apple.com/documentation/swiftui/view/subscriptionstorecontrolstyle(_:)) — 设置视图中订阅商店视图的控件样式。
- [subscriptionStoreControlStyle(_:placement:)](https://developer.apple.com/documentation/swiftui/view/subscriptionstorecontrolstyle(_:placement:)) — 设置视图中订阅商店视图的控件样式和控件位置。
- [subscriptionStoreOptionGroupStyle(_:)](https://developer.apple.com/documentation/swiftui/view/subscriptionstoreoptiongroupstyle(_:)) — 设置该视图内订阅商店视图用来显示订阅选项组的样式。
- [subscriptionStorePickerItemBackground(_:)](https://developer.apple.com/documentation/swiftui/view/subscriptionstorepickeritembackground(_:)) — 设置视图中订阅商店视图实例选择器项目的背景样式。
- [subscriptionStorePickerItemBackground(_:in:)](https://developer.apple.com/documentation/swiftui/view/subscriptionstorepickeritembackground(_:in:)) — 设置视图中订阅商店视图选择器项目的背景形状和样式。
- [subscriptionStorePolicyDestination(for:destination:)](https://developer.apple.com/documentation/swiftui/view/subscriptionstorepolicydestination(for:destination:)) — 把一个视图配置为订阅商店视图中政策按钮操作的目标。
- [subscriptionStorePolicyDestination(url:for:)](https://developer.apple.com/documentation/swiftui/view/subscriptionstorepolicydestination(url:for:)) — 把一个 URL 配置为订阅商店视图中政策按钮操作的目标。
- [subscriptionStorePolicyForegroundStyle(_:)](https://developer.apple.com/documentation/swiftui/view/subscriptionstorepolicyforegroundstyle(_:)) — 设置订阅商店视图中服务条款和隐私政策按钮的样式。
- [subscriptionStorePolicyForegroundStyle(_:_:)](https://developer.apple.com/documentation/swiftui/view/subscriptionstorepolicyforegroundstyle(_:_:)) — 设置订阅商店视图中服务条款和隐私政策按钮的主要与次要样式。
- [subscriptionStoreSignInAction(_:)](https://developer.apple.com/documentation/swiftui/view/subscriptionstoresigninaction(_:)) — 添加一个动作，当有人使用视图内订阅商店视图上的登录按钮时执行。
- [subscriptionStoreControlBackground(_:)](https://developer.apple.com/documentation/swiftui/view/subscriptionstorecontrolbackground(_:)) — 设置用于该视图中订阅商店视图控件背景的标准效果。
- [subscriptionPromotionalOffer(offer:compactJWS:)](https://developer.apple.com/documentation/swiftui/view/subscriptionpromotionaloffer(offer:compactjws:)) — 选择要应用于顾客从订阅商店视图进行购买的促销优惠。
- [subscriptionIntroductoryOffer(applyOffer:compactJWS:)](https://developer.apple.com/documentation/swiftui/view/subscriptionintroductoryoffer(applyoffer:compactjws:)) — 选择要应用于顾客从订阅商店视图进行购买的介绍性优惠资格偏好。
- [subscriptionOfferViewButtonVisibility(_:for:)](https://developer.apple.com/documentation/swiftui/view/subscriptionofferviewbuttonvisibility(_:for:))
- [subscriptionOfferViewDetailAction(_:)](https://developer.apple.com/documentation/swiftui/view/subscriptionofferviewdetailaction(_:))
- [subscriptionOfferViewStyle(_:)](https://developer.apple.com/documentation/swiftui/view/subscriptionofferviewstyle(_:))
- [preferredSubscriptionOffer(_:)](https://developer.apple.com/documentation/swiftui/view/preferredsubscriptionoffer(_:)) — 选择要应用于顾客从订阅商店视图、商店视图或产品视图进行购买的订阅优惠。
- [preferredSubscriptionPricingTerms(_:)](https://developer.apple.com/documentation/swiftui/view/preferredsubscriptionpricingterms(_:))

## 访问健康数据 {#Accessing-health-data}

- [healthDataAccessRequest(store:objectType:predicate:trigger:completion:)](https://developer.apple.com/documentation/swiftui/view/healthdataaccessrequest(store:objecttype:predicate:trigger:completion:)) — 异步请求读取某种需要按对象授权的数据类型的权限（例如视力处方）。
- [healthDataAccessRequest(store:readTypes:trigger:completion:)](https://developer.apple.com/documentation/swiftui/view/healthdataaccessrequest(store:readtypes:trigger:completion:)) — 请求读取指定 HealthKit 数据类型的权限。
- [healthDataAccessRequest(store:shareTypes:readTypes:trigger:completion:)](https://developer.apple.com/documentation/swiftui/view/healthdataaccessrequest(store:sharetypes:readtypes:trigger:completion:)) — 请求保存和读取指定 HealthKit 数据类型的权限。
- [workoutPreview(_:isPresented:)](https://developer.apple.com/documentation/swiftui/view/workoutpreview(_:ispresented:)) — 以模态工作表形式呈现体能训练内容的预览

## 提供提示 {#Providing-tips}

- [popoverTip(_:arrowEdge:action:)](https://developer.apple.com/documentation/swiftui/view/popovertip(_:arrowedge:action:)) — 在被修改的视图上呈现一个浮层提示。
- [popoverTip(_:isPresented:attachmentAnchor:arrowEdge:action:)](https://developer.apple.com/documentation/swiftui/view/popovertip(_:ispresented:attachmentanchor:arrowedge:action:)) — 在被修改的视图上呈现一个浮层提示。
- [popoverTip(_:isPresented:attachmentAnchor:arrowEdges:action:)](https://developer.apple.com/documentation/swiftui/view/popovertip(_:ispresented:attachmentanchor:arrowedges:action:)) — 在被修改的视图上呈现一个浮层提示。
- [tipAnchor(_:)](https://developer.apple.com/documentation/swiftui/view/tipanchor(_:)) — 为指定的提示锚点设置一个值，用于把提示视图锚定到视图的 `.bounds`。
- [tipBackground(_:)](https://developer.apple.com/documentation/swiftui/view/tipbackground(_:)) — 把提示的视图背景设置为某种样式。
- [tipBackgroundInteraction(_:)](https://developer.apple.com/documentation/swiftui/view/tipbackgroundinteraction(_:)) — 控制人们是否可以与所呈现提示后面的视图交互。
- [tipCornerRadius(_:antialiased:)](https://developer.apple.com/documentation/swiftui/view/tipcornerradius(_:antialiased:)) — 设置内联提示视图的圆角半径。
- [tipImageSize(_:)](https://developer.apple.com/documentation/swiftui/view/tipimagesize(_:)) — 设置提示图像的尺寸。
- [tipViewStyle(_:)](https://developer.apple.com/documentation/swiftui/view/tipviewstyle(_:)) — 为视图层级中的 TipView 设置给定的样式。
- [tipImageStyle(_:)](https://developer.apple.com/documentation/swiftui/view/tipimagestyle(_:)) — 设置提示图像的样式。
- [tipImageStyle(_:_:)](https://developer.apple.com/documentation/swiftui/view/tipimagestyle(_:_:)) — 设置提示图像的样式。
- [tipImageStyle(_:_:_:)](https://developer.apple.com/documentation/swiftui/view/tipimagestyle(_:_:_:)) — 设置提示图像的样式。

## 显示翻译 {#Showing-a-translation}

- [translationPresentation(isPresented:text:attachmentAnchor:arrowEdge:replacementAction:)](https://developer.apple.com/documentation/swiftui/view/translationpresentation(ispresented:text:attachmentanchor:arrowedge:replacementaction:)) — 当给定条件为 true 时呈现一个翻译浮层。
- [translationTask(_:action:)](https://developer.apple.com/documentation/swiftui/view/translationtask(_:action:)) — 添加一个在该视图出现之前或翻译配置变化时执行的任务。
- [translationTask(source:target:action:)](https://developer.apple.com/documentation/swiftui/view/translationtask(source:target:action:)) — 添加一个在该视图出现之前或指定的源语言或目标语言变化时执行的任务。
- [translationTask(source:target:preferredStrategy:action:)](https://developer.apple.com/documentation/swiftui/view/translationtask(source:target:preferredstrategy:action:)) — 添加一个在该视图出现之前或指定的源语言或目标语言变化时执行的任务。

## 呈现日志建议 {#Presenting-journaling-suggestions}

- [journalingSuggestionsPicker(isPresented:onCompletion:)](https://developer.apple.com/documentation/swiftui/view/journalingsuggestionspicker(ispresented:oncompletion:)) — 呈现一个可视化选择器界面，其中包含事件和图像，用户可以选择它们以获取更多信息。
- [journalingSuggestionsPicker(isPresented:journalingSuggestionToken:onCompletion:)](https://developer.apple.com/documentation/swiftui/view/journalingsuggestionspicker(ispresented:journalingsuggestiontoken:oncompletion:)) — 呈现一个可视化选择器界面，其中包含事件和图像，用户可以选择它们以获取更多信息。

## 管理联系人访问权限 {#Managing-contact-access}

- [contactAccessButtonCaption(_:)](https://developer.apple.com/documentation/swiftui/view/contactaccessbuttoncaption(_:))
- [contactAccessButtonStyle(_:)](https://developer.apple.com/documentation/swiftui/view/contactaccessbuttonstyle(_:))
- [contactAccessPicker(isPresented:completionHandler:)](https://developer.apple.com/documentation/swiftui/view/contactaccesspicker(ispresented:completionhandler:)) — 以模态方式呈现界面，让用户选择你的应用可以访问哪些联系人。

## 同步游戏存档 {#Syncing-game-saves}

- [gameSaveSyncingAlert(directory:finishedLoading:)](https://developer.apple.com/documentation/swiftui/view/gamesavesyncingalert(directory:finishedloading:)) — 在游戏的同步目录载入期间呈现一个模态视图。

## 处理游戏控制器事件 {#Handling-game-controller-events}

- [handlesGameControllerEvents(matching:)](https://developer.apple.com/documentation/swiftui/view/handlesgamecontrollerevents(matching:)) — 指定当该视图或其某个后代视图拥有焦点时，应通过 GameController 框架传递哪些游戏控制器事件。

## 创建桌面游戏 {#Creating-a-tabletop-game}

- [tabletopGame(_:parent:automaticUpdate:)](https://developer.apple.com/documentation/swiftui/view/tabletopgame(_:parent:automaticupdate:)) — 为一个视图添加桌面游戏。
- [tabletopGame(_:parent:automaticUpdate:interaction:)](https://developer.apple.com/documentation/swiftui/view/tabletopgame(_:parent:automaticupdate:interaction:)) — 提供一个在需要时返回新交互的闭包。

## 配置相机控制 {#Configuring-camera-controls}

- [realityViewCameraControls](https://developer.apple.com/documentation/swiftui/environmentvalues/realityviewcameracontrols) — 现实视图的相机控制。
- [realityViewCameraControls(_:)](https://developer.apple.com/documentation/swiftui/view/realityviewcameracontrols(_:)) — 添加控制虚拟相机位置和方向的手势。
- [realityViewLayoutBehavior(_:)](https://developer.apple.com/documentation/swiftui/view/realityviewlayoutbehavior(_:)) — 一种视图修饰符，控制 `RealityView` 的框架尺寸和内容对齐行为

## 与交易交互 {#Interacting-with-transactions}

- [transactionPicker(isPresented:selection:)](https://developer.apple.com/documentation/swiftui/view/transactionpicker(ispresented:selection:)) — 呈现一个选择一组交易的选择器。
