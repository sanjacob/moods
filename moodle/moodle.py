"""
Moodle Model Classes
"""

# Copyright (C) 2024, Jacob Sánchez Pérez

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA  02110-1301, USA.

from enum import Enum
from typing import Any
from datetime import datetime
from pathvalidate import sanitize_filename

from pydantic import BaseModel, ConfigDict


class ImmutableModel(BaseModel):
    """Model with const attributes."""
    model_config = ConfigDict(frozen=True)


class MoodleToken(ImmutableModel):
    token: str
    privatetoken: str | None = None


class MoodlePreference(ImmutableModel):
    name: str
    value: str | int | None


class MoodleFeature(ImmutableModel):
    name: str
    value: int


class MoodleFunction(ImmutableModel):
    name: str
    version: str


class MoodleSiteInfo(ImmutableModel):
    sitename: str
    username: str
    firstname: str
    lastname: str
    fullname: str
    lang: str
    userid: int
    siteurl: str
    userpictureurl: str
    functions: list[MoodleFunction]
    downloadfiles: int
    uploadfiles: int
    release: str
    version: str
    mobilecssurl: str
    advancedfeatures: list[MoodleFeature]
    usercanmanageownfiles: bool
    userquota: int
    usermaxuploadfilesize: int
    userhomepage: int
    userprivateaccesskey: str
    siteid: int
    sitecalendartype: str
    usercalendartype: str
    userissiteadmin: bool
    theme: str
    limitconcurrentlogins: int
    policyagreed: int


class MoodleCourse(ImmutableModel):
    id: int
    shortname: str
    fullname: str
    displayname: str
    enrolledusercount: int
    idnumber: str
    visible: int
    summary: str
    summaryformat: int
    format: str
    courseimage: str
    showgrades: bool
    lang: str
    enablecompletion: bool
    completionhascriteria: bool
    completionusertracked: bool
    category: int
    progress: int | None
    completed: bool
    startdate: datetime
    enddate: datetime
    marker: int
    lastaccess: datetime
    isfavourite: bool
    hidden: bool
    overviewfiles: list[str]
    showactivitydates: bool
    showcompletionconditions: bool
    timemodified: datetime

    @property
    def code(self) -> str:
        return self.idnumber or str(self.id)

    @property
    def title(self) -> str:
        return self.displayname or self.fullname

    @property
    def created(self) -> datetime:
        return self.startdate

    @property
    def availability(self) -> bool:
        return not self.hidden


class MoodlePrivateFilesInfo(ImmutableModel):
    filecount: int
    foldercount: int
    filesize: int
    filesizewithoutreferences: int
    warnings: list[str]


class MoodleUserPreferences(ImmutableModel):
    preferences: list[MoodlePreference]
    warnings: list[str]


class MoodleFile(ImmutableModel):
    filename: str
    filepath: str
    filesize: int
    fileurl: str
    timemodified: datetime
    mimetype: str
    isexternalfile: bool
    icon: str


class MoodleResource(ImmutableModel):
    id: int
    coursemodule: int
    course: int
    name: str
    intro: str
    introformat: int
    introfiles: list[Any]
    section: int
    visible: bool
    groupmode: int
    groupingid: int
    lang: str
    contentfiles: list[MoodleFile] = []
    tobemigrated: int
    legacyfiles: int
    legacyfileslast: None
    display: int
    displayoptions: str
    filterfiles: int
    revision: int
    timemodified: datetime


class MoodleContentType(str, Enum):
    """Different resource types on Moodle."""

    File = 'file'
    Url = 'url'
    Other = '__moods_other'

    @classmethod
    def _missing_(cls, value: Any) -> 'MoodleContentType':
        return cls.Other


class MoodleContent(ImmutableModel):
    type: MoodleContentType
    filename: str
    filepath: str | None = None
    filesize: int
    fileurl: str | None = None
    timecreated: datetime | None
    timemodified: datetime | None
    sortorder: int | None = None
    mimetype: str | None = None
    isexternalfile: bool = False
    userid: int | None = None
    author: str | None = None
    license: str | None = None

    @property
    def mimeType(self) -> str | None:
        return self.mimetype

    @property
    def fileName(self) -> str:
        return f"{self.filepath} {self.filename}"

    @property
    def id(self) -> str | None:
        return self.fileurl


class MoodleContentInfo(ImmutableModel):
    filescount: int
    filessize: int
    lastmodified: int
    mimetypes: list[str]
    repositorytype: str


class MoodleDate(ImmutableModel):
    label: str
    timestamp: datetime
    dataid: str


class MoodleRuleValue(ImmutableModel):
    status: int
    description: str


class MoodleRule(ImmutableModel):
    rulename: str
    rulevalue: MoodleRuleValue


class MoodleCompletionData(ImmutableModel):
    state: int
    timecompleted: datetime
    overrideby: None
    valueused: bool
    hascompletion: bool
    isautomatic: bool
    istrackeduser: bool
    uservisible: bool
    details: list[MoodleRule]
    isoverallcomplete: bool


class MoodleModuleType(str, Enum):
    """Different module types on Moodle."""

    Forum = 'forum'
    Lti = 'lti'
    Resource = 'resource'
    Quiz = 'quiz'
    Folder = 'folder'
    Url = 'url'
    Other = '__moods_mod_other'

    @classmethod
    def _missing_(cls, value: Any) -> 'MoodleModuleType':
        return cls.Other


class MoodleModule(ImmutableModel):
    id: int
    url: str
    name: str
    instance: int
    contextid: int
    visible: int
    uservisible: bool
    visibleoncoursepage: int
    modicon: str
    modname: MoodleModuleType
    purpose: str
    branded: bool
    modplural: str
    indent: int
    onclick: str
    afterlink: None
    activitybadge: list[Any] | None = None
    customdata: str
    noviewlink: bool
    completion: int
    completiondata: MoodleCompletionData | None = None
    downloadcontent: int
    dates: list[MoodleDate]
    groupmode: int
    contents: list[MoodleContent] = []
    contentsinfo: MoodleContentInfo | None = None

    @property
    def contentHandler(self) -> MoodleModuleType:
        return self.modname

    @property
    def title(self) -> str:
        return self.name

    @property
    def title_path_safe(self) -> str:
        return sanitize_filename(self.name) or 'Untitled'

    @property
    def body(self) -> None:
        return None

    @property
    def modified(self) -> None:
        return None

    @property
    def availability(self) -> bool:
        return self.uservisible

    @property
    def hasChildren(self) -> bool:
        return bool(self.contents)


class MoodleSection(ImmutableModel):
    id: int
    name: str
    visible: int
    summary: str
    summaryformat: int
    section: int
    hiddenbynumsections: int
    uservisible: bool
    component: Any
    itemid: Any
    modules: list[MoodleModule] = []
