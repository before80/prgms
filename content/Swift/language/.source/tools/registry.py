#!/usr/bin/env python3
"""Registry for the generated book structure.

This is the single source of truth for
  * the order of the chapters as they appear in the sidebar of
    https://docs.swift.org/latest/documentation/the-swift-programming-language
  * the DocC page slug of every chapter
  * the directory / file name used in the Hugo content tree
  * the chapter number and the Chinese title
"""

from __future__ import annotations

import json
import pathlib

HERE = pathlib.Path(__file__).resolve().parent.parent
OUTPUT_ROOT = "Swift/language"

# (section title, directory name, [(slug, file stem, Chinese title), ...])
SECTIONS = [
    (
        "Welcome to Swift",
        "welcometoswift",
        [
            ("AboutSwift", "1.1-AboutSwift", "关于 Swift"),
            ("Compatibility", "1.2-Compatibility", "兼容性"),
            ("GuidedTour", "1.3-GuidedTour", "Swift 初览"),
        ],
    ),
    (
        "Language Guide",
        "languageguide",
        [
            ("TheBasics", "2.1-TheBasics", "基础"),
            ("BasicOperators", "2.2-BasicOperators", "基本运算符"),
            ("StringsAndCharacters", "2.3-StringsAndCharacters", "字符串与字符"),
            ("CollectionTypes", "2.4-CollectionTypes", "集合类型"),
            ("ControlFlow", "2.5-ControlFlow", "控制流"),
            ("Functions", "2.6-Functions", "函数"),
            ("Closures", "2.7-Closures", "闭包"),
            ("Enumerations", "2.8-Enumerations", "枚举"),
            ("ClassesAndStructures", "2.9-ClassesAndStructures", "类与结构体"),
            ("Properties", "2.10-Properties", "属性"),
            ("Methods", "2.11-Methods", "方法"),
            ("Subscripts", "2.12-Subscripts", "下标"),
            ("Inheritance", "2.13-Inheritance", "继承"),
            ("Initialization", "2.14-Initialization", "初始化"),
            ("Deinitialization", "2.15-Deinitialization", "反初始化"),
            ("OptionalChaining", "2.16-OptionalChaining", "可选链"),
            ("ErrorHandling", "2.17-ErrorHandling", "错误处理"),
            ("Concurrency", "2.18-Concurrency", "并发"),
            ("Macros", "2.19-Macros", "宏"),
            ("TypeCasting", "2.20-TypeCasting", "类型转换"),
            ("NestedTypes", "2.21-NestedTypes", "嵌套类型"),
            ("Extensions", "2.22-Extensions", "扩展"),
            ("Protocols", "2.23-Protocols", "协议"),
            ("Generics", "2.24-Generics", "泛型"),
            ("OpaqueTypes", "2.25-OpaqueTypes", "不透明类型"),
            (
                "AutomaticReferenceCounting",
                "2.26-AutomaticReferenceCounting",
                "自动引用计数",
            ),
            ("MemorySafety", "2.27-MemorySafety", "内存安全"),
            ("AccessControl", "2.28-AccessControl", "访问控制"),
            ("AdvancedOperators", "2.29-AdvancedOperators", "高级运算符"),
        ],
    ),
    (
        "Language Reference",
        "languagereference",
        [
            (
                "AboutTheLanguageReference",
                "3.1-AboutTheLanguageReference",
                "关于语言参考",
            ),
            ("LexicalStructure", "3.2-LexicalStructure", "词法结构"),
            ("Types", "3.3-Types", "类型"),
            ("Expressions", "3.4-Expressions", "表达式"),
            ("Statements", "3.5-Statements", "语句"),
            ("Declarations", "3.6-Declarations", "声明"),
            ("Attributes", "3.7-Attributes", "属性特性"),
            ("Patterns", "3.8-Patterns", "模式"),
            (
                "GenericParametersAndArguments",
                "3.9-GenericParametersAndArguments",
                "泛型形参与实参",
            ),
            ("SummaryOfTheGrammar", "3.10-SummaryOfTheGrammar", "语法概要"),
        ],
    ),
    (
        "Revision History",
        "revisionhistory",
        [
            ("revisionhistory", "4.1-RevisionHistory", "修订历史"),
        ],
    ),
]

SECTION_TITLES_CN = {
    "Welcome to Swift": "欢迎使用 Swift",
    "Language Guide": "语言指南",
    "Language Reference": "语言参考",
    "Revision History": "修订历史",
}


def pages():
    """Yield every chapter as a dict."""
    result = []
    for section_index, (section, directory, chapters) in enumerate(SECTIONS, start=1):
        for weight, (slug, stem, cn_title) in enumerate(chapters, start=1):
            result.append(
                {
                    "slug": slug,
                    "section": section,
                    "section_dir": directory,
                    "section_weight": section_index,
                    "stem": stem,
                    "cn_title": cn_title,
                    "weight": weight,
                    "file": f"{OUTPUT_ROOT}/{directory}/{stem}.md",
                    "url_dir": f"/{OUTPUT_ROOT}/{directory}/{stem}/",
                    "source": f"TSPL.docc/{_github_path(slug)}",
                }
            )
    return result


def _github_path(slug: str) -> str:
    # 这里的目录名是上游 swift-book 仓库里的原始大小写
    for directory in ("GuidedTour", "LanguageGuide", "ReferenceManual", "RevisionHistory"):
        if (HERE / "swift-book" / "TSPL.docc" / directory / f"{slug}.md").exists():
            return f"{directory}/{slug}.md"
    raise SystemExit(f"no source file found for {slug}")


def as_dict():
    return {page["slug"]: page for page in pages()}


if __name__ == "__main__":
    print(json.dumps(pages(), indent=1, ensure_ascii=False))
