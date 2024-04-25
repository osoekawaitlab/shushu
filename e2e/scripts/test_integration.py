import json
import os
from tempfile import TemporaryDirectory

from shushu.actions import (
    ClickSelectedElementAction,
    DataProcessorCoreAction,
    MemoryPayload,
    MinimumEnclosingElementWithMultipleTextsSelector,
    OpenUrlAction,
    PythonCodeDataProcessorAction,
    SaveDataAction,
    SelectedElementsPayload,
    SetSelectorAction,
    StorageCoreAction,
    WebAgentCoreAction,
    XPathSelector,
)
from shushu.core import gen_shushu_core
from shushu.logger import get_logger
from shushu.models import Url
from shushu.settings import CoreSettings, LocalFileStorageSettings, LoggerSettings


def test_get_minimum_enclosing_element_with_multiple_texts(http_server_fixture: str) -> None:
    expected = [
        {
            "link": f"{http_server_fixture}/page0.html",
            "title": "始まりの村 - ルナディアの冒険開始",
            "date": "2024-03-31",
            "description": "ルナディア村での初心者向けのクエストと、冒険の第一歩に必要な準備について詳しく解説します。",
        },
        {
            "link": f"{http_server_fixture}/page1.html",
            "title": "ゼルファンの森 - 勇者たちの試練",
            "date": "2024-04-01",
            "description": "ゼルファンの森での勇者たちの試練と、クリアするための戦略や必要な装備について紹介します。",
        },
        {
            "link": f"{http_server_fixture}/page2.html",
            "title": "装備とスキルの基礎知識",
            "date": "2024-04-02",
            "description": "初心者向けに、ゲーム内で入手可能な基本的な装備とスキルの概要を説明します。",
        },
        {
            "link": f"{http_server_fixture}/page3.html",
            "title": "冒険者の港町 - ナルビアの秘密",
            "date": "2024-04-03",
            "description": "港町ナルビアの探索と、隠された秘密やクエストを解き明かす方法について紹介します。",
        },
        {
            "link": f"{http_server_fixture}/page4.html",
            "title": "遺跡の謎 - 古代のパズルを解く",
            "date": "2024-04-04",
            "description": "古代の遺跡で待ち受ける謎とパズルを解くためのヒントと戦略を解説します。",
        },
        {
            "link": f"{http_server_fixture}/page5.html",
            "title": "最終決戦 - 魔王の城への道",
            "date": "2024-04-05",
            "description": "魔王を倒すための最終決戦に挑む前の準備と、攻略のための重要なポイントを説明します。",
        },
    ]
    with TemporaryDirectory() as tempdir:
        settings = CoreSettings(storage_settings=LocalFileStorageSettings(path=tempdir))
        logger = get_logger(settings=LoggerSettings())
        core = gen_shushu_core(settings=settings, logger=logger)
        scraper_action = DataProcessorCoreAction(
            action=PythonCodeDataProcessorAction(
                code="""\
from typing import Sequence
from shushu.models import BaseDataModel, ElementSequence
from shushu.types import TypeId
from pydantic import AnyHttpUrl
from urllib.parse import urljoin


class Datum(BaseDataModel):
    type_id: TypeId = TypeId("01HVVHBNM0PJMN3PEHBP6DB0WF")
    link: AnyHttpUrl
    title: str
    date: str
    description: str

class Data(BaseDataModel):
    type_id: TypeId = TypeId("01HVVHBXEP12V5VNWP9V9FVQ4Z")
    data: Sequence[Datum]

def convert(element_sequence: ElementSequence) -> Data:
    return Data(data=[
        Datum(
            link=element.root.find('a')['href'] if element.root.find('a')['href'].startswith('http') else urljoin(str(element.url.value), element.root.find('a')['href']),
            title=element.root.find('a').text.strip(),
            date=element.root.find('p').text.strip().replace('日付: ', ''),
            description=element.root.find_all('p')[1].text.strip()
        ) for element in element_sequence.elements
    ])
"""  # noqa: E501
            ),
            payload=SelectedElementsPayload(),
        )
        data_dir = os.path.join(tempdir, "01HVVHBNM0PJMN3PEHBP6DB0WF")
        with core:
            core.perform(action=WebAgentCoreAction(action=OpenUrlAction(url=Url(value=http_server_fixture))))
            core.perform(
                action=WebAgentCoreAction(
                    action=SetSelectorAction(
                        selector=MinimumEnclosingElementWithMultipleTextsSelector(target_strings=["始まりの村", "2024"])
                    )
                )
            )
            minelem = core.web_agent.get_selected_element()
            assert minelem.tag_name == "li"
            assert "list-item" in minelem.classes
            core.perform(
                action=WebAgentCoreAction(
                    action=SetSelectorAction(selector=XPathSelector(xpath="//li[contains(@class, 'list-item')]"))
                )
            )
            similar_elems = core.web_agent.get_selected_elements()
            assert len(similar_elems.elements) == 3
            assert "始まりの村" in similar_elems.elements[0].text
            assert "ゼルファンの森" in similar_elems.elements[1].text
            assert "装備とスキル" in similar_elems.elements[2].text

            core.perform(action=scraper_action)

            core.perform(
                action=StorageCoreAction(action=SaveDataAction(), payload=MemoryPayload(attribute="data", expand=True))
            )
            assert len(os.listdir(data_dir)) == 3
            for fn in os.listdir(data_dir):
                with open(os.path.join(data_dir, fn), "r") as f:
                    d = json.load(f)
                    assert any(
                        [all([d[k] == e[k] for k in ("link", "title", "date", "description")]) for e in expected]
                    )

            core.perform(
                action=WebAgentCoreAction(
                    action=SetSelectorAction(selector=XPathSelector(xpath="//a[text()='次のページへ']"))
                )
            )
            core.perform(action=WebAgentCoreAction(action=ClickSelectedElementAction()))
            core.perform(
                action=WebAgentCoreAction(
                    action=SetSelectorAction(selector=XPathSelector(xpath="//li[contains(@class, 'list-item')]"))
                )
            )
            similar_elems2 = core.web_agent.get_selected_elements()
            assert len(similar_elems2.elements) == 3
            assert "冒険者の港町" in similar_elems2.elements[0].text
            assert "遺跡の謎" in similar_elems2.elements[1].text
            assert "最終決戦" in similar_elems2.elements[2].text
            core.perform(action=scraper_action)

            core.perform(
                action=StorageCoreAction(action=SaveDataAction(), payload=MemoryPayload(attribute="data", expand=True))
            )
            assert len(os.listdir(data_dir)) == 6
            for fn in os.listdir(data_dir):
                with open(os.path.join(data_dir, fn), "r") as f:
                    d = json.load(f)
                    assert any(
                        [all([d[k] == e[k] for k in ("link", "title", "date", "description")]) for e in expected]
                    )
