from typing import List

STYLE_MAP = {
    "professional": "专业严谨，用词精准，逻辑严密",
    "detailed": "详细全面，不遗漏任何细节",
    "concise": "简洁精炼，直击要点",
}

STYLE_MAP_EN = {
    "professional": "be professional, precise, and logically rigorous",
    "detailed": "be comprehensive and thorough, omitting no details",
    "concise": "be concise and to the point",
}


def generate_prompt(desc: str, scene: str, style: str, lang: str) -> str:
    s = STYLE_MAP.get(style, STYLE_MAP["professional"])
    s_en = STYLE_MAP_EN.get(style, STYLE_MAP_EN["professional"])

    if scene == "image":
        if lang == "zh":
            return (
                f"你是一位资深 AI 绘画提示词工程师。请根据以下需求生成高质量的图片生成提示词：\n\n"
                f"需求描述：{desc}\n\n"
                f"要求：\n- {s}，确保提示词能精准引导图像生成\n"
                f"- 使用英文输出提示词（适用于 Stable Diffusion / Midjourney / DALL-E 等）\n"
                f"- 包含主体、风格、光线、色彩、构图、氛围等关键要素\n"
                f"- 提供 3 个不同方向的提示词方案\n"
                f"- 每个方案附带简短的中文说明\n\n"
                f"请直接输出提示词方案，不需要额外解释。"
            )
        else:
            return (
                f"You are a senior AI image prompt engineer. Please generate high-quality image generation prompts based on the following request:\n\n"
                f"Request: {desc}\n\n"
                f"Requirements:\n- {s_en}, ensure prompts precisely guide image generation\n"
                f"- Include subject, style, lighting, color, composition, atmosphere\n"
                f"- Provide 3 different prompt variations\n"
                f"- Each with a brief description\n\n"
                f"Output the prompts directly without extra explanation."
            )

    if scene == "copywriting":
        if lang == "zh":
            return (
                f"你是一位资深文案策划专家。请根据以下需求创作文案：\n\n"
                f"需求：{desc}\n\n"
                f"要求：\n- {s}，确保文案有感染力和传播力\n"
                f"- 结构清晰，包含标题、正文、结尾\n"
                f"- 提供 2-3 个不同风格的版本供选择\n"
                f"- 注意目标受众和投放渠道的语言风格\n"
                f"- 结尾给出使用建议或行动号召\n\n"
                f"请直接输出文案内容，不需要额外解释。"
            )
        else:
            return (
                f"You are a senior copywriting expert. Please create copy based on the following request:\n\n"
                f"Request: {desc}\n\n"
                f"Requirements:\n- {s_en}, ensure the copy is compelling and shareable\n"
                f"- Clear structure: headline, body, conclusion\n"
                f"- Provide 2-3 style variations\n"
                f"- Match the tone to the target audience and channel\n"
                f"- End with a call to action or usage recommendation\n\n"
                f"Output the copy directly without extra explanation."
            )

    if scene == "coding":
        if lang == "zh":
            return (
                f"你是一位资深软件工程师。请完成以下编程任务：\n\n"
                f"任务：{desc}\n\n"
                f"要求：\n- 编写清晰、可维护、符合最佳实践的代码\n"
                f"- 添加必要的注释说明关键逻辑\n"
                f"- 考虑边界情况和错误处理\n"
                f"- 如果涉及算法，请先说明思路再给出代码\n"
                f"- 代码使用标准格式，便于直接运行\n\n"
                f"请直接输出代码和说明。"
            )
        else:
            return (
                f"You are a senior software engineer. Please complete the following coding task:\n\n"
                f"Task: {desc}\n\n"
                f"Requirements:\n- Write clean, maintainable code following best practices\n"
                f"- Add necessary comments explaining key logic\n"
                f"- Consider edge cases and error handling\n"
                f"- If algorithms are involved, explain the approach first, then provide code\n"
                f"- Use standard formatting for immediate execution\n\n"
                f"Output code and explanation directly."
            )

    if scene == "analysis":
        if lang == "zh":
            return (
                f"你是一位专业分析师。请对以下内容进行深入分析：\n\n"
                f"分析对象：{desc}\n\n"
                f"要求：\n- 采用结构化分析框架（背景-现状-问题-建议）\n"
                f"- 多角度思考，列出至少3个不同视角\n"
                f"- 每个观点提供数据支撑\n"
                f"- 最后给出明确的结论和可执行建议\n"
                f"- 如有数据，请标注来源或假设条件\n\n"
                f"请直接输出分析结果。"
            )
        else:
            return (
                f"You are a professional analyst. Please conduct an in-depth analysis of the following:\n\n"
                f"Subject: {desc}\n\n"
                f"Requirements:\n- Use a structured framework (Context-Current State-Issues-Recommendations)\n"
                f"- Think from multiple angles, list at least 3 perspectives\n"
                f"- Provide evidence for each viewpoint\n"
                f"- End with clear conclusions and actionable recommendations\n"
                f"- Cite data sources or assumptions if applicable\n\n"
                f"Output the analysis directly."
            )

    # fallback
    if lang == "zh":
        return (
            f"你是一位领域专家。请根据以下需求完成任务：\n\n"
            f"需求：{desc}\n\n"
            f"要求：\n- {s}，确保内容有深度和可读性\n"
            f"- 结构清晰，使用合适的标题和段落划分\n"
            f"- 提供具体案例或数据支撑观点\n"
            f"- 结尾给出总结或行动建议\n"
            f"- 保持语言流畅，避免冗余表达\n\n"
            f"请直接输出内容，不需要额外解释。"
        )
    else:
        return (
            f"You are a domain expert. Please complete the task based on the following request:\n\n"
            f"Task: {desc}\n\n"
            f"Requirements:\n- {s_en}, ensure depth and readability\n"
            f"- Clear structure with appropriate headings and paragraphs\n"
            f"- Provide concrete examples or data to support viewpoints\n"
            f"- End with a summary or actionable advice\n"
            f"- Keep language fluent and avoid redundancy\n\n"
            f"Output the content directly without extra explanation."
        )


def analyze_prompt(input_text: str) -> List[str]:
    suggestions = []
    if len(input_text) < 20:
        suggestions.append("提示词过于简短，建议增加具体需求和约束条件")
    if "角色" not in input_text and "扮演" not in input_text and "你是" not in input_text and "你是一位" not in input_text:
        suggestions.append("缺少角色设定，建议明确AI的身份和专业领域")
    if "要求" not in input_text and "请" not in input_text and "需要" not in input_text and "输出" not in input_text:
        suggestions.append("缺少明确的输出要求，建议补充格式、风格、长度等约束")
    if "示例" not in input_text and "例如" not in input_text and "样例" not in input_text and "例子" not in input_text:
        suggestions.append("如适用，可添加示例帮助AI理解期望的输出格式")
    if "和" in input_text and "还有" in input_text and input_text.count("。") < 3:
        suggestions.append("多个需求混杂在一句中，建议分条列出")
    if not suggestions:
        suggestions.append("提示词结构较好，建议进一步细化输出格式和边界条件")
    return suggestions


def optimize_prompt(input_text: str, goal: str, scene: str) -> str:
    role_map = {
        "coding": "资深工程师" if scene == "coding" else "技术专家",
        "copywriting": "文案专家" if scene == "copywriting" else "写作顾问",
        "analysis": "资深分析师" if scene == "analysis" else "领域专家",
        "image": "AI绘画提示词专家" if scene == "image" else "创意专家",
    }
    role = role_map.get(scene, "领域专家")

    if goal == "clarity":
        return (
            f"【角色】\n你是一位{role}。\n\n"
            f"【任务】\n{input_text}\n\n"
            f"【要求】\n"
            f"1. 先理解任务核心，确认理解无误后再开始输出\n"
            f"2. 使用清晰有条理的结构呈现结果\n"
            f"3. 关键结论优先，细节补充在后\n"
            f"4. 如有不确定之处，明确标注并说明原因"
        )
    elif goal == "structure":
        return (
            f"【角色设定】\n你是一位{role}。\n\n"
            f"【背景信息】\n（请在此补充相关上下文）\n\n"
            f"【具体任务】\n{input_text}\n\n"
            f"【输出要求】\n"
            f"- 格式：使用标题和分段组织内容\n"
            f"- 结构：背景 → 分析 → 结论 → 建议\n"
            f"- 每部分用清晰的标题标注\n"
            f"- 重要观点使用加粗或编号强调"
        )
    elif goal == "detail":
        return (
            f"【角色】\n你是一位{role}。\n\n"
            f"【任务】\n{input_text}\n\n"
            f"【详细要求】\n"
            f"1. 输出前请先列出你的理解和执行计划\n"
            f"2. 每个论点提供具体例子或数据支撑\n"
            f"3. 考虑至少3种不同情况或方案\n"
            f"4. 说明你的推理过程，不只是结论\n"
            f"5. 标注任何假设条件或限制范围\n"
            f"6. 输出长度控制在适当范围，确保信息完整"
        )
    elif goal == "concise":
        return (
            f"【角色】效率专家\n\n"
            f"【任务】{input_text}\n\n"
            f"【要求】\n"
            f"- 只输出最关键的信息，删除冗余表达\n"
            f"- 使用 bullet points 或编号列表\n"
            f"- 每点控制在30字以内\n"
            f"- 如无必要，不提供背景解释\n"
            f"- 直接给出答案或结论"
        )
    elif goal == "role":
        role_detailed = {
            "coding": "拥有10年经验的架构师",
            "copywriting": "知名广告创意总监",
            "analysis": "顶尖行业顾问",
            "image": "专业AI绘画提示词工程师",
        }.get(scene, "顶尖行业顾问")
        return (
            f"请你扮演一位{role_detailed}。\n\n"
            f"你的特点是：\n"
            f"- 专业知识深厚，经验丰富\n"
            f"- 善于用通俗语言解释复杂问题\n"
            f"- 回答简洁有力，不绕弯子\n"
            f"- 遇到不确定的问题会诚实告知\n\n"
            f"现在请你以这个角色回应以下任务：\n\n"
            f"{input_text}\n\n"
            f"注意：始终保持角色一致性，用第一人称\"我\"回答。"
        )
    else:
        return input_text
