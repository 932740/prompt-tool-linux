from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum


class Scene(str, Enum):
    image = "image"
    copywriting = "copywriting"
    coding = "coding"
    analysis = "analysis"


class Style(str, Enum):
    professional = "professional"
    detailed = "detailed"
    concise = "concise"


class Lang(str, Enum):
    zh = "zh"
    en = "en"


class Goal(str, Enum):
    clarity = "clarity"
    structure = "structure"
    detail = "detail"
    concise = "concise"
    role = "role"


class GenerateRequest(BaseModel):
    desc: str = Field(..., min_length=1, description="需求描述")
    scene: Scene = Field(default=Scene.copywriting, description="场景类型")
    style: Style = Field(default=Style.professional, description="输出风格")
    lang: Lang = Field(default=Lang.zh, description="输出语言")


class OptimizeRequest(BaseModel):
    input: str = Field(..., min_length=1, description="原始提示词")
    goal: Goal = Field(default=Goal.clarity, description="优化目标")
    scene: str = Field(default="general", description="场景")
    lang: Lang = Field(default=Lang.zh, description="输出语言")


class OptimizeResponse(BaseModel):
    suggestions: List[str]
    result: str


class PromptItem(BaseModel):
    id: int
    title: str
    content: str
    scene: str = "general"
    created: str


class PromptCreate(BaseModel):
    title: str = Field(..., min_length=1)
    content: str = Field(..., min_length=1)
    scene: Optional[str] = "general"


class PromptLibrary(BaseModel):
    prompts: List[PromptItem]
    total: int
