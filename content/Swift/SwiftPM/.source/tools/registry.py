#!/usr/bin/env python3
"""Registry for the Swift Package Manager documentation.

The order and hierarchy come from the site's navigator index
(https://docs.swift.org/latest/index/index.json), and every page is mapped to
the DocC markdown source in the swift-package-manager repository.
"""

from __future__ import annotations

import json
import pathlib

HERE = pathlib.Path(__file__).resolve().parent.parent
REPO = HERE.parents[2]  # .../content
OUTPUT_ROOT = "Swift/SwiftPM"
DOC_ROOT = "swift-package-manager/Sources/PackageManagerDocs/Documentation.docc"

# (section title, directory, Chinese title, [(slug, file stem, Chinese title), ...])
SECTIONS = [
    (
        "Essentials",
        "essentials",
        "基础",
        [
            ("gettingstarted", "1.1-GettingStarted", "快速上手"),
            ("introducingpackages", "1.2-IntroducingPackages", "包的概念"),
            ("packagesecurity", "1.3-PackageSecurity", "包的安全性"),
        ],
    ),
    (
        "Building Packages",
        "buildingpackages",
        "构建包",
        [
            ("creatingswiftpackage", "2.1-CreatingSwiftPackage", "创建 Swift 包"),
            ("settingswifttoolsversion", "2.2-SettingSwiftToolsVersion", "设置 Swift 工具版本"),
            ("usingbuildconfigurations", "2.3-UsingBuildConfigurations", "使用构建配置"),
            (
                "swiftversionspecificpackaging",
                "2.4-SwiftVersionSpecificPackaging",
                "按 Swift 版本打包",
            ),
            ("bundlingresources", "2.5-BundlingResources", "为 Swift 包打包资源"),
            (
                "releasingpublishingapackage",
                "2.6-ReleasingPublishingAPackage",
                "发布与公开 Swift 包",
            ),
            ("generatingsboms", "2.7-GeneratingSBOMs", "生成软件物料清单（SBOM）"),
            ("continuousintegration", "2.8-ContinuousIntegration", "持续集成工作流"),
            ("usingshellcompletion", "2.9-UsingShellCompletion", "使用 shell 补全脚本"),
        ],
    ),
    (
        "Dependencies",
        "dependencies",
        "依赖",
        [
            (
                "addingdependencies",
                "3.1-AddingDependencies",
                "为 Swift 包添加依赖",
                [
                    ("resolvingpackageversions", "3.1.1-ResolvingPackageVersions", "解析与更新依赖"),
                    ("packagetraits", "3.1.2-PackageTraits", "用特性提供可配置的包"),
                    (
                        "resolvingdependencyfailures",
                        "3.1.3-ResolvingDependencyFailures",
                        "解决依赖失败",
                    ),
                    (
                        "addingsystemlibrarydependency",
                        "3.1.4-AddingSystemLibraryDependency",
                        "添加对系统库的依赖",
                    ),
                    (
                        "examplesystemlibrarypkgconfig",
                        "3.1.5-ExampleSystemLibraryPkgConfig",
                        "使用系统库依赖与 pkg-config 的示例",
                    ),
                    (
                        "editingdependencypackage",
                        "3.1.6-EditingDependencyPackage",
                        "编辑包所用的远程依赖",
                    ),
                ],
            ),
            ("usingswiftpackageregistry", "3.2-UsingSwiftPackageRegistry", "使用包注册表"),
            ("bundlingresources", "3.3-BundlingResources", "为 Swift 包打包资源"),
        ],
    ),
    (
        "Targets",
        "targets",
        "目标",
        [
            ("creatingclanguagetargets", "4.1-CreatingCLanguageTargets", "创建 C 语言目标"),
            (
                "modulemaps",
                "4.2-ModuleMaps",
                "创建模块映射",
                [
                    ("modulemapreference", "4.2.1-ModuleMapReference", "模块映射语法参考"),
                    ("debuggingmodulemaps", "4.2.2-DebuggingModuleMaps", "调试模块映射"),
                ],
            ),
            ("modulealiasing", "4.3-ModuleAliasing", "模块别名"),
        ],
    ),
    (
        "Sharing Packages",
        "sharingpackages",
        "共享包",
        [
            (
                "releasingpublishingapackage",
                "5.1-ReleasingPublishingAPackage",
                "发布与公开 Swift 包",
            ),
            ("packagecollections", "5.2-PackageCollections", "包集合"),
        ],
    ),
    (
        "Extending Package Manager",
        "extendingpackagemanager",
        "扩展包管理器",
        [
            (
                "plugins",
                "6.1-Plugins",
                "插件",
                [
                    ("enablecommandplugin", "6.1.1-EnableCommandPlugin", "启用命令插件"),
                    ("enablebuildplugin", "6.1.2-EnableBuildPlugin", "启用构建插件"),
                    ("writingcommandplugin", "6.1.3-WritingCommandPlugin", "编写命令插件"),
                    ("writingbuildtoolplugin", "6.1.4-WritingBuildToolPlugin", "编写构建工具插件"),
                ],
            ),
            ("swiftpmasalibrary", "6.2-SwiftPMAsALibrary", "把包管理器作为库使用"),
        ],
    ),
    (
        "Swift Commands",
        "swiftcommands",
        "swift 命令",
        [
            ("swiftbuild", "7.1-SwiftBuild", "swift build"),
            ("swifttest", "7.2-SwiftTest", "swift test"),
            (
                "swiftpackagecommands",
                "7.3-SwiftPackageCommands",
                "swift package",
                [
                    ("packageinit", "7.3.1-PackageInit", "swift package init"),
                    ("packageupdate", "7.3.2-PackageUpdate", "swift package update"),
                    ("packageresolve", "7.3.3-PackageResolve", "swift package resolve"),
                    ("packageadddependency", "7.3.4-PackageAddDependency", "swift package add-dependency"),
                    ("packageaddproduct", "7.3.5-PackageAddProduct", "swift package add-product"),
                    ("packageaddtarget", "7.3.6-PackageAddTarget", "swift package add-target"),
                    (
                        "packageaddtargetdependency",
                        "7.3.7-PackageAddTargetDependency",
                        "swift package add-target-dependency",
                    ),
                    ("packageaddsetting", "7.3.8-PackageAddSetting", "swift package add-setting"),
                    ("packageedit", "7.3.9-PackageEdit", "swift package edit"),
                    ("packageunedit", "7.3.10-PackageUnedit", "swift package unedit"),
                    ("packagemigrate", "7.3.11-PackageMigrate", "swift package migrate"),
                    ("packageplugin", "7.3.12-PackagePlugin", "swift package plugin"),
                    (
                        "packagediagnoseapibreakingchange",
                        "7.3.13-PackageDiagnoseAPIBreakingChange",
                        "swift package diagnose-api-breaking-changes",
                    ),
                    ("packagedescribe", "7.3.14-PackageDescribe", "swift package describe"),
                    (
                        "packageshowdependencies",
                        "7.3.15-PackageShowDependencies",
                        "swift package show-dependencies",
                    ),
                    (
                        "packageshowexecutables",
                        "7.3.16-PackageShowExecutables",
                        "swift package show-executables",
                    ),
                    ("packageshowtraits", "7.3.17-PackageShowTraits", "swift package show-traits"),
                    ("packagetoolsversion", "7.3.18-PackageToolsVersion", "swift package tools-version"),
                    ("packagedumppackage", "7.3.19-PackageDumpPackage", "swift package dump-package"),
                    (
                        "packagedumpsymbolgraph",
                        "7.3.20-PackageDumpSymbolGraph",
                        "swift package dump-symbol-graph",
                    ),
                    ("packageclean", "7.3.21-PackageClean", "swift package clean"),
                    ("packagereset", "7.3.22-PackageReset", "swift package reset"),
                    ("packagepurgecache", "7.3.23-PackagePurgeCache", "swift package purge-cache"),
                    (
                        "packagearchivesource",
                        "7.3.24-PackageArchiveSource",
                        "swift package archive-source",
                    ),
                    (
                        "packagecomputechecksum",
                        "7.3.25-PackageComputeChecksum",
                        "swift package compute-checksum",
                    ),
                    (
                        "packagecompletiontool",
                        "7.3.26-PackageCompletionTool",
                        "swift package completion-tool",
                    ),
                    (
                        "packageconfigsetmirror",
                        "7.3.27-PackageConfigSetMirror",
                        "swift package config set-mirror",
                    ),
                    (
                        "packageconfigunsetmirror",
                        "7.3.28-PackageConfigUnsetMirror",
                        "swift package config unset-mirror",
                    ),
                    (
                        "packageconfiggetmirror",
                        "7.3.29-PackageConfigGetMirror",
                        "swift package config get-mirror",
                    ),
                    ("packagegeneratesbom", "7.3.30-PackageGenerateSBOM", "swift.package.generate-sbom"),
                    (
                        "packageexperimentalinstall",
                        "7.3.31-PackageExperimentalInstall",
                        "swift package experimental-install",
                    ),
                    (
                        "packageexperimentaluninstall",
                        "7.3.32-PackageExperimentalUninstall",
                        "swift package experimental-uninstall",
                    ),
                ],
            ),
            (
                "swiftsdkcommands",
                "7.4-SwiftSDKCommands",
                "swift sdk",
                [
                    ("sdkinstall", "7.4.1-SDKInstall", "swift sdk install"),
                    ("sdklist", "7.4.2-SDKList", "swift sdk list"),
                    ("sdkremove", "7.4.3-SDKRemove", "swift sdk remove"),
                    ("sdkconfigure", "7.4.4-SDKConfigure", "swift sdk configure"),
                    ("sdkconfigurationset", "7.4.5-SDKConfigurationSet", "swift sdk configuration set"),
                    ("sdkconfigurationshow", "7.4.6-SDKConfigurationShow", "swift sdk configuration show"),
                    ("sdkconfigurationreset", "7.4.7-SDKConfigurationReset", "swift sdk configuration reset"),
                ],
            ),
            (
                "swiftpackageregistrycommands",
                "7.5-SwiftPackageRegistryCommands",
                "swift package-registry",
                [
                    ("packageregistryset", "7.5.1-PackageRegistrySet", "swift package-registry set"),
                    ("packageregistryunset", "7.5.2-PackageRegistryUnset", "swift package-registry unset"),
                    ("packageregistrylogin", "7.5.3-PackageRegistryLogin", "swift package-registry login"),
                    (
                        "packageregistrypublish",
                        "7.5.4-PackageRegistryPublish",
                        "swift package-registry publish",
                    ),
                    ("packageregistrylogout", "7.5.5-PackageRegistryLogout", "swift package-registry logout"),
                ],
            ),
            (
                "swiftpackagecollectioncommands",
                "7.6-SwiftPackageCollectionCommands",
                "swift package-collection",
                [
                    ("packagecollectionadd", "7.6.1-PackageCollectionAdd", "swift package-collection add"),
                    (
                        "packagecollectionsearch",
                        "7.6.2-PackageCollectionSearch",
                        "swift package-collection search",
                    ),
                    (
                        "packagecollectionrefresh",
                        "7.6.3-PackageCollectionRefresh",
                        "swift package-collection refresh",
                    ),
                    (
                        "packagecollectionlist",
                        "7.6.4-PackageCollectionList",
                        "swift package-collection list",
                    ),
                    (
                        "packagecollectiondescribe",
                        "7.6.5-PackageCollectionDescribe",
                        "swift package-collection describe",
                    ),
                    (
                        "packagecollectionremove",
                        "7.6.6-PackageCollectionRemove",
                        "swift package-collection remove",
                    ),
                ],
            ),
            ("swiftrun", "7.7-SwiftRun", "swift run"),
        ],
    ),
    (
        "Design",
        "design",
        "设计",
        [
            (
                "registryserverspecification",
                "8.1-RegistryServerSpecification",
                "Swift 包注册表服务规范",
            ),
        ],
    ),
    (
        "Releases",
        "releases",
        "版本发布说明",
        [
            (
                "releasenotes",
                "9.1-ReleaseNotes",
                "发布说明",
                [
                    ("6.4", "9.1.1-SwiftPM64ReleaseNotes", "SwiftPM 6.4 发布说明"),
                    ("6.3", "9.1.2-SwiftPM63ReleaseNotes", "SwiftPM 6.3 发布说明"),
                    ("5.9", "9.1.3-SwiftPM59ReleaseNotes", "SwiftPM 5.9 发布说明"),
                    ("5.8", "9.1.4-SwiftPM58ReleaseNotes", "SwiftPM 5.8 发布说明"),
                    ("5.7", "9.1.5-SwiftPM57ReleaseNotes", "SwiftPM 5.7 发布说明"),
                    ("5.6", "9.1.6-SwiftPM56ReleaseNotes", "SwiftPM 5.6 发布说明"),
                    ("5.5", "9.1.7-SwiftPM55ReleaseNotes", "SwiftPM 5.5 发布说明"),
                    ("5.4", "9.1.8-SwiftPM54ReleaseNotes", "SwiftPM 5.4 发布说明"),
                    ("5.3", "9.1.9-SwiftPM53ReleaseNotes", "SwiftPM 5.3 发布说明"),
                ],
            ),
        ],
    ),
    (
        "Articles",
        "articles",
        "专题文章",
        [
            ("swiftbuildpreview", "10.1-SwiftBuildPreview", "预览 Swift 构建系统集成"),
        ],
    ),
]


def _github_path(slug: str) -> str:
    """Find the DocC markdown source file for a page slug."""
    root = HERE / "swift-package-manager" / "Sources" / "PackageManagerDocs" / "Documentation.docc"
    candidates = [p for p in root.rglob("*.md") if p.stem.lower() == slug.lower()]
    if not candidates:
        raise SystemExit(f"no source file for {slug}")
    return str(candidates[0].relative_to(HERE / "swift-package-manager"))


def pages():
    result = []
    for section_index, entry in enumerate(SECTIONS, start=1):
        section, directory, section_cn = entry[:3]
        chapters = entry[3]
        for weight, chapter in enumerate(chapters, start=1):
            slug, stem, cn_title = chapter[:3]
            children = chapter[3] if len(chapter) > 3 else []
            result.append(
                {
                    "slug": slug,
                    "section": section,
                    "section_cn": section_cn,
                    "section_dir": directory,
                    "section_weight": section_index,
                    "stem": stem,
                    "cn_title": cn_title,
                    "weight": weight,
                    "is_collection": bool(children),
                    "file": f"{OUTPUT_ROOT}/{directory}/{stem}.md"
                    if not children
                    else f"{OUTPUT_ROOT}/{directory}/{stem}/_index.md",
                    "children": [
                        {
                            "slug": c_slug,
                            "stem": c_stem,
                            "cn_title": c_cn,
                            "weight": c_weight,
                            "file": f"{OUTPUT_ROOT}/{directory}/{stem}/{c_stem}.md",
                        }
                        for c_weight, (c_slug, c_stem, c_cn) in enumerate(children, start=1)
                    ],
                    "source": _github_path(slug),
                }
            )
    return result


def flat_pages():
    """Every page, including nested chapter pages."""
    result = []
    for page in pages():
        if page["is_collection"]:
            result.append(page)
            for child in page["children"]:
                result.append(
                    {
                        "slug": child["slug"],
                        "section": page["section"],
                        "section_dir": page["section_dir"],
                        "parent": page["stem"],
                        "stem": child["stem"],
                        "cn_title": child["cn_title"],
                        "weight": child["weight"],
                        "is_collection": False,
                        "children": [],
                        "file": child["file"],
                        "source": _github_path(child["slug"]),
                    }
                )
        else:
            result.append(page)
    return result


if __name__ == "__main__":
    print(json.dumps(flat_pages(), indent=1, ensure_ascii=False))
