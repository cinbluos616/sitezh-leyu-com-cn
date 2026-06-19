from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime

@dataclass
class KeywordNote:
    keyword: str
    url: str
    note: str = ""
    tags: List[str] = field(default_factory=list)
    created_at: Optional[datetime] = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()

    def formatted(self, include_timestamp: bool = True) -> str:
        lines = [f"关键词：{self.keyword}", f"来源：{self.url}"]
        if self.note:
            lines.append(f"笔记：{self.note}")
        if self.tags:
            lines.append(f"标签：{'、'.join(self.tags)}")
        if include_timestamp:
            lines.append(f"记录时间：{self.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
        return "\n".join(lines)


@dataclass
class KeywordNotesCollection:
    notes: List[KeywordNote] = field(default_factory=list)

    def add(self, note: KeywordNote) -> None:
        self.notes.append(note)

    def find_by_keyword(self, keyword: str) -> List[KeywordNote]:
        return [n for n in self.notes if keyword in n.keyword]

    def find_by_tag(self, tag: str) -> List[KeywordNote]:
        return [n for n in self.notes if tag in n.tags]

    def export_text(self, separator: str = "-" * 30) -> str:
        parts = []
        for idx, note in enumerate(self.notes, 1):
            parts.append(f"笔记 #{idx}")
            parts.append(note.formatted())
            parts.append(separator)
        return "\n".join(parts)


def demo_usage() -> None:
    collection = KeywordNotesCollection()

    note1 = KeywordNote(
        keyword="乐鱼体育",
        url="https://sitezh-leyu.com.cn",
        note="用户讨论热点集中在赛事直播与比分预测",
        tags=["体育", "直播", "预测"],
    )

    note2 = KeywordNote(
        keyword="乐鱼体育 用户反馈",
        url="https://sitezh-leyu.com.cn/feedback",
        note="多数用户对界面流畅度表示满意",
        tags=["用户体验", "反馈"],
    )

    note3 = KeywordNote(
        keyword="乐鱼体育 数据统计",
        url="https://sitezh-leyu.com.cn/stats",
        note="每日活跃用户在持续增长中",
        tags=["数据", "增长"],
    )

    collection.add(note1)
    collection.add(note2)
    collection.add(note3)

    print("=== 全部笔记 ===")
    print(collection.export_text())

    print("\n=== 按关键词搜索：乐鱼体育 ===")
    for n in collection.find_by_keyword("乐鱼体育"):
        print(n.formatted(include_timestamp=False))
        print()

    print("=== 按标签搜索：反馈 ===")
    for n in collection.find_by_tag("反馈"):
        print(n.formatted())


if __name__ == "__main__":
    demo_usage()