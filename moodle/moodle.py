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

from typing import Any

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
    startdate: int
    enddate: int
    marker: int
    lastaccess: int
    isfavourite: bool
    hidden: bool
    overviewfiles: list[str]
    showactivitydates: bool
    showcompletionconditions: bool
    timemodified: int


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
    timemodified: int
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
    contentfiles: list[MoodleFile]
    tobemigrated: int
    legacyfiles: int
    legacyfileslast: None
    display: int
    displayoptions: str
    filterfiles: int
    revision: int
    timemodified: int


class MoodleInContent(ImmutableModel):
    type: str
    filename: str
    filepath: str
    filesize: int
    fileurl: str
    timecreated: int
    timemodified: int
    sortorder: int
    mimetype: str
    isexternalfile: bool
    userid: int
    author: str
    license: str


class MoodleInContentInfo(ImmutableModel):
    filescount: int
    filessize: int
    lastmodified: int
    mimetypes: list[str]
    repositorytype: str


class MoodleDate(ImmutableModel):
    label: str
    timestamp: int
    dataid: str


class MoodleRuleValue(ImmutableModel):
    status: int
    description: str


class MoodleRule(ImmutableModel):
    rulename: str
    rulevalue: MoodleRuleValue


class MoodleCompletionData(ImmutableModel):
    state: int
    timecompleted: int
    overrideby: None
    valueused: bool
    hascompletion: bool
    isautomatic: bool
    istrackeduser: bool
    uservisible: bool
    details: list[MoodleRule]
    isoverallcomplete: bool


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
    modname: str
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
    contents: list[MoodleInContent] | None = None
    contentsinfo: MoodleInContentInfo | None = None


class MoodleContent(ImmutableModel):
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
    modules: list[MoodleModule]
