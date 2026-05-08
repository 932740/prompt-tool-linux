import os
from typing import List
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

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


def get_openai_client():
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        return None
    base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1").strip()
    return AsyncOpenAI(api_key=api_key, base_url=base_url)


def get_model() -> str:
    return os.getenv("OPENAI_MODEL", "gpt-4o-mini").strip()


async def call_llm(system_prompt: str, user_prompt: str) -> str | None:
    client = get_openai_client()
    if client is None:
        return None
    try:
        resp = await client.chat.completions.create(
            model=get_model(),
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.7,
            max_tokens=2000,
        )
        return resp.choices[0].message.content.strip()
    except Exception:
        return None


def build_system_prompt(scene: str, style: str, lang: str) -> str:
    s = STYLE_MAP.get(style, STYLE_MAP["professional"])
    s_en = STYLE_MAP_EN.get(style, STYLE_MAP_EN["professional"])

    if scene == "image":
        if lang == "zh":
            return (
                "你是一位顶级 AI 绘画提示词工程师。用户会描述他们想要的画面，"
                "你要直接输出高质量的英文图片生成提示词，适用于 Stable Diffusion / Midjourney / DALL-E。\n"
                "\n"
                "输出要求：\n"
                f"- 风格：{s}\n"
                "- 每个提示词必须完整、可直接复制使用，不需要额外解释\n"
                "- 包含主体、风格、光线、色彩、构图、氛围、画质等关键要素\n"
                "- 提供 3 个不同方向的提示词方案\n"
                "- 每个方案前用 \"方案X：\" 标注，后跟英文提示词，再空一行\n"
                "- 不要输出任何系统性的说明文字，只输出提示词本身"
            )
        else:
            return (
                "You are a top-tier AI image prompt engineer. The user describes the image they want. "
                "You must output high-quality, ready-to-use English image generation prompts directly.\n"
                "\n"
                "Requirements:\n"
                f"- Style: {s_en}\n"
                "- Each prompt must be complete and copy-paste ready, no extra explanation\n"
                "- Include subject, style, lighting, color, composition, atmosphere, quality\n"
                "- Provide 3 distinct prompt variations\n"
                "- Prefix each with \"Option X:\", followed by the English prompt, then a blank line\n"
                "- Do NOT output any meta-instructions or system text, only the prompts themselves"
            )

    if scene == "copywriting":
        if lang == "zh":
            return (
                "你是一位资深文案策划专家。用户会描述文案需求，你要直接输出完整可用的文案内容。\n"
                "\n"
                "输出要求：\n"
                f"- 风格：{s}\n"
                "- 直接输出文案内容，不需要角色介绍或使用说明\n"
                "- 结构清晰：标题、正文、结尾\n"
                "- 提供 2-3 个不同风格的版本供选择\n"
                "- 注意目标受众和投放渠道的语言风格\n"
                "- 结尾给出行动号召\n"
                "- 不要输出任何系统性的说明文字"
            )
        else:
            return (
                "You are a senior copywriting expert. The user describes their copy needs. "
                "You must output complete, ready-to-use copy directly.\n"
                "\n"
                "Requirements:\n"
                f"- Style: {s_en}\n"
                "- Output the copy directly, no role intro or usage instructions\n"
                "- Clear structure: headline, body, conclusion\n"
                "- Provide 2-3 style variations\n"
                "- Match tone to target audience and channel\n"
                "- End with a call to action\n"
                "- Do NOT output any meta-instructions or system text"
            )

    if scene == "coding":
        if lang == "zh":
            return (
                f"你是一位资深软件工程师。用户会描述编程需求，你要直接输出可直接运行的高质量代码。\n"
                f"\n"
                f"输出要求：\n"
                f"- 风格：{s}\n"
                f"- 编写清晰、可维护、符合最佳实践的代码\n"
                f"- 添加必要的注释说明关键逻辑\n"
                f"- 考虑边界情况和错误处理\n"
                f"- 如果涉及算法，先简要说明思路，再给出代码\n"
                f"- 代码使用标准格式，便于直接复制运行\n"
                f"- 不要输出任何与代码无关的寒暄或系统说明"
            )
        else:
            return (
                f"You are a senior software engineer. The user describes a coding task. "
                f"You must output clean, runnable code directly.\n"
                f"\n"
                f"Requirements:\n"
                f"- Style: {s_en}\n"
                f"- Write clean, maintainable code following best practices\n"
                f"- Add necessary comments for key logic\n"
                f"- Consider edge cases and error handling\n"
                f"- If algorithms are involved, briefly explain the approach first, then provide code\n"
                f"- Use standard formatting for immediate execution\n"
                f"- Do NOT output any greetings or meta-instructions"
            )

    if scene == "analysis":
        if lang == "zh":
            return (
                f"你是一位专业分析师。用户会提供分析对象或问题，你要直接输出深入、结构化的分析报告。\n"
                f"\n"
                f"输出要求：\n"
                f"- 风格：{s}\n"
                f"- 采用结构化分析框架（背景-现状-问题-建议）\n"
                f"- 多角度思考，列出至少 3 个不同视角\n"
                f"- 每个观点提供具体支撑\n"
                f"- 最后给出明确的结论和可执行建议\n"
                f"- 不要输出任何系统性的说明文字"
            )
        else:
            return (
                f"You are a professional analyst. The user provides a subject or question. "
                f"You must output an in-depth, structured analysis directly.\n"
                f"\n"
                f"Requirements:\n"
                f"- Style: {s_en}\n"
                f"- Use a structured framework (Context-Current State-Issues-Recommendations)\n"
                f"- Think from multiple angles, list at least 3 perspectives\n"
                f"- Provide concrete evidence for each viewpoint\n"
                f"- End with clear conclusions and actionable recommendations\n"
                f"- Do NOT output any meta-instructions or system text"
            )

    # fallback
    if lang == "zh":
        return (
            f"你是一位领域专家。用户会描述需求，你要直接输出完整可用的结果内容。\n"
            f"\n"
            f"输出要求：\n"
            f"- 风格：{s}\n"
            f"- 直接输出内容，不需要额外说明\n"
            f"- 结构清晰，使用合适的标题和段落划分\n"
            f"- 提供具体案例或数据支撑观点\n"
            f"- 结尾给出总结或行动建议\n"
            f"- 不要输出任何系统性的说明文字"
        )
    else:
        return (
            f"You are a domain expert. The user describes a task. "
            f"You must output complete, ready-to-use content directly.\n"
            f"\n"
            f"Requirements:\n"
            f"- Style: {s_en}\n"
            f"- Output directly, no extra explanation\n"
            f"- Clear structure with appropriate headings and paragraphs\n"
            f"- Provide concrete examples or data to support viewpoints\n"
            f"- End with a summary or actionable advice\n"
            f"- Do NOT output any meta-instructions or system text"
        )


async def generate_prompt(desc: str, scene: str, style: str, lang: str) -> str:
    system_prompt = build_system_prompt(scene, style, lang)
    user_prompt = desc

    llm_result = await call_llm(system_prompt, user_prompt)
    if llm_result:
        return llm_result

    # fallback: generate usable content directly when LLM unavailable
    # All fallbacks now respect scene + style + lang

    def _fallback_image(d: str, l: str, st: str) -> str:
        kw = d.strip()
        if l == "zh":
            if st == "detailed":
                return (
                    f"【方案一】超写实风格\n"
                    f"主体：{kw}\n"
                    f"提示词：{kw}, hyperrealistic, extremely detailed, intricate textures, lifelike materials, ambient occlusion, subsurface scattering, global illumination, ray tracing, 16k resolution, Unreal Engine 5 render, photorealistic, masterpiece, best quality\n\n"
                    f"【方案二】幻想艺术风格\n"
                    f"主体：{kw}\n"
                    f"提示词：{kw}, fantasy art, highly detailed, magical atmosphere, ethereal lighting, intricate details, elaborate background, vibrant color palette, concept art, trending on ArtStation, 8k, ultra detailed, best quality\n\n"
                    f"【方案三】电影级风格\n"
                    f"主体：{kw}\n"
                    f"提示词：{kw}, cinematic shot, dramatic lighting, atmospheric fog, lens flare, chromatic aberration, film grain, anamorphic lens, color grading, IMAX quality, 8k, photorealistic, highly detailed, masterpiece"
                )
            if st == "concise":
                return (
                    f"【方案一】\n"
                    f"{kw}, photorealistic, 8k, best quality\n\n"
                    f"【方案二】\n"
                    f"{kw}, cinematic, detailed, vibrant\n\n"
                    f"【方案三】\n"
                    f"{kw}, minimalist, elegant, sharp focus"
                )
            # professional (default)
            return (
                f"【方案一】写实风格\n"
                f"主体：{kw}\n"
                f"提示词：{kw}, photorealistic, highly detailed, professional photography, sharp focus, 8k resolution, masterpiece, best quality, studio lighting, clean composition\n\n"
                f"【方案二】艺术风格\n"
                f"主体：{kw}\n"
                f"提示词：{kw}, artistic illustration, cinematic lighting, depth of field, ultra detailed, vibrant colors, golden hour, professional color grading\n\n"
                f"【方案三】极简风格\n"
                f"主体：{kw}\n"
                f"提示词：{kw}, minimalist design, pure white background, soft lighting, elegant, high-end product photography, 8k, sharp focus"
            )
        # English
        if st == "detailed":
            return (
                f"[Option 1] Hyper-realistic Style\n"
                f"Subject: {kw}\n"
                f"Prompt: {kw}, hyperrealistic, extremely detailed, intricate textures, lifelike materials, ambient occlusion, subsurface scattering, global illumination, ray tracing, 16k resolution, Unreal Engine 5 render, photorealistic, masterpiece, best quality\n\n"
                f"[Option 2] Fantasy Art Style\n"
                f"Subject: {kw}\n"
                f"Prompt: {kw}, fantasy art, highly detailed, magical atmosphere, ethereal lighting, intricate details, elaborate background, vibrant color palette, concept art, trending on ArtStation, 8k, ultra detailed, best quality\n\n"
                f"[Option 3] Cinematic Style\n"
                f"Subject: {kw}\n"
                f"Prompt: {kw}, cinematic shot, dramatic lighting, atmospheric fog, lens flare, chromatic aberration, film grain, anamorphic lens, color grading, IMAX quality, 8k, photorealistic, highly detailed, masterpiece"
            )
        if st == "concise":
            return (
                f"[Option 1]\n"
                f"{kw}, photorealistic, 8k, best quality\n\n"
                f"[Option 2]\n"
                f"{kw}, cinematic, detailed, vibrant\n\n"
                f"[Option 3]\n"
                f"{kw}, minimalist, elegant, sharp focus"
            )
        # professional
        return (
            f"[Option 1] Realistic Style\n"
            f"Subject: {kw}\n"
            f"Prompt: {kw}, photorealistic, highly detailed, professional photography, sharp focus, 8k resolution, masterpiece, best quality, studio lighting, clean composition\n\n"
            f"[Option 2] Artistic Style\n"
            f"Subject: {kw}\n"
            f"Prompt: {kw}, artistic illustration, cinematic lighting, depth of field, ultra detailed, vibrant colors, golden hour, professional color grading\n\n"
            f"[Option 3] Minimalist Style\n"
            f"Subject: {kw}\n"
            f"Prompt: {kw}, minimalist design, pure white background, soft lighting, elegant, high-end product photography, 8k, sharp focus"
        )

    def _fallback_copywriting(d: str, l: str, st: str) -> str:
        if l == "zh":
            if st == "detailed":
                return (
                    "【版本一】\n\n"
                    "标题：🔥 全网都在找的宝藏好物！不看后悔！\n\n"
                    "正文：\n"
                    "姐妹们！今天必须给大家安利这款我私藏已久的神仙产品！\n"
                    "首先颜值就赢了，设计感满满，摆在桌上就是一件艺术品。\n"
                    "然后功能真的绝了，每一个细节都考虑到位，用起来超顺手。\n"
                    "价格更是良心，对比了市面上同类产品，这个性价比真的没谁了。\n"
                    "不管是送闺蜜、送男友还是自用，都超合适！\n"
                    "我已经安利给身边所有朋友了，人手一个！\n\n"
                    "结尾：现在下单还有优惠，手慢无！\n\n"
                    "---\n\n"
                    "【版本二】\n\n"
                    "标题：亲测分享 | 这款好物为什么让我回购三次？\n\n"
                    "正文：\n"
                    "作为一个挑剔的消费者，我对产品要求一直很高。\n"
                    "但这款产品真的让我改观了，来给大家说说真实体验：\n"
                    "1. 开箱体验：包装精致，拆箱仪式感满满\n"
                    "2. 使用感受：上手简单，效果超出预期\n"
                    "3. 长期价值：用了一个月，越用越喜欢\n"
                    "4. 售后保障：客服响应快，问题处理及时\n\n"
                    "如果你还在犹豫，我的建议是：直接冲！\n\n"
                    "结尾：评论区告诉我你的使用体验！"
                )
            if st == "concise":
                return (
                    "【版本一】\n\n"
                    "标题：必入好物\n\n"
                    "正文：质量过硬，价格实在，值得入手。\n\n"
                    "结尾：立即购买\n\n"
                    "---\n\n"
                    "【版本二】\n\n"
                    "标题：为什么选它？\n\n"
                    "正文：三个理由：质量好、功能全、性价比高。\n\n"
                    "结尾：下单就对了"
                )
            # professional
            return (
                "【版本一】\n\n"
                "标题：[专业推荐] 值得信赖的选择\n\n"
                "正文：\n"
                "我们很高兴向您推荐这款经过严格筛选的产品。从专业角度来看，它在质量、功能和性价比方面均表现出色。\n"
                "无论是个人使用还是商务场景，都能满足高标准需求。\n\n"
                "结尾：立即了解更多详情。\n\n"
                "---\n\n"
                "【版本二】\n\n"
                "标题：深度评测 | 专业视角下的全面分析\n\n"
                "正文：\n"
                "经过全面评估，我们总结出以下核心优势：\n"
                "1. 质量可靠：通过多项专业认证\n"
                "2. 功能完善：覆盖主要使用场景\n"
                "3. 性价比高：在同品类中表现突出\n\n"
                "如需进一步了解，欢迎咨询。\n\n"
                "结尾：联系我们获取更多信息。"
            )
        # English
        if st == "detailed":
            return (
                "[Version 1]\n\n"
                "Headline: 🔥 Everyone's Searching for This Hidden Gem!\n\n"
                "Body:\n"
                "Hey guys! I have to share this amazing product I've been loving!\n"
                "First, the design is absolutely stunning—it looks like art on your desk.\n"
                "The functionality is incredible, every detail is thoughtfully designed.\n"
                "The price is unbeatable compared to similar products on the market.\n"
                "Perfect for gifting or personal use—I've already recommended it to all my friends!\n\n"
                "Closing: Grab yours now while the discount lasts!\n\n"
                "---\n\n"
                "[Version 2]\n\n"
                "Headline: Honest Review | Why I Bought This Three Times\n\n"
                "Body:\n"
                "As a picky consumer, I have high standards.\n"
                "But this product exceeded my expectations. Here's my honest experience:\n"
                "1. Unboxing: Premium packaging with a luxury feel\n"
                "2. Usability: Intuitive and effective right out of the box\n"
                "3. Long-term value: Still loving it after a month of daily use\n"
                "4. Support: Responsive customer service, quick issue resolution\n\n"
                "If you're on the fence, my advice is: just go for it!\n\n"
                "Closing: Share your experience in the comments!"
            )
        if st == "concise":
            return (
                "[Version 1]\n\n"
                "Headline: Must-Have Item\n\n"
                "Body: Great quality, fair price. Worth every penny.\n\n"
                "Closing: Buy now\n\n"
                "---\n\n"
                "[Version 2]\n\n"
                "Headline: Why Choose This?\n\n"
                "Body: Three reasons: quality, features, value.\n\n"
                "Closing: Order today"
            )
        # professional
        return (
            "[Version 1]\n\n"
            "Headline: [Professional Recommendation] A Choice You Can Trust\n\n"
            "Body:\n"
            "We are pleased to recommend this carefully selected product. From a professional standpoint, it excels in quality, functionality, and cost performance.\n"
            "Suitable for both personal and business use, meeting high standards across the board.\n\n"
            "Closing: Learn more details today.\n\n"
            "---\n\n"
            "[Version 2]\n\n"
            "Headline: In-Depth Review | Comprehensive Analysis from a Professional Perspective\n\n"
            "Body:\n"
            "After thorough evaluation, here are the key strengths:\n"
            "1. Reliable quality: certified by multiple professional standards\n"
            "2. Comprehensive features: covering major use cases\n"
            "3. Excellent value: outperforming competitors in the same category\n\n"
            "For further information, please reach out.\n\n"
            "Closing: Contact us for more details."
        )

    def _fallback_coding(d: str, l: str, st: str) -> str:
        if l == "zh":
            if st == "detailed":
                return (
                    f"# ============================================================\n"
                    f"# 模块名称: solution.py\n"
                    f"# 功能描述: {d}\n"
                    f"# 作者: AI Assistant\n"
                    f"# 版本: 1.0.0\n"
                    f"# ============================================================\n\n"
                    f"from typing import Any, Optional, List, Dict\n"
                    f"import logging\n\n"
                    f"logger = logging.getLogger(__name__)\n\n"
                    f"def validate_inputs(data: Any) -> bool:\n"
                    f'    """\n'
                    f"    验证输入数据的合法性\n"
                    f"    Args:\n"
                    f"        data: 输入数据\n"
                    f"    Returns:\n"
                    f"        bool: 验证结果\n"
                    f'    """\n'
                    f"    if data is None:\n"
                    f'        logger.error("输入数据不能为空")\n'
                    f"        return False\n"
                    f"    return True\n\n"
                    f"def process(data: Any) -> Any:\n"
                    f'    """\n'
                    f"    核心处理逻辑\n"
                    f"    Args:\n"
                    f"        data: 输入数据\n"
                    f"    Returns:\n"
                    f"        Any: 处理结果\n"
                    f'    """\n'
                    f"    try:\n"
                    f"        # TODO: 实现具体处理逻辑\n"
                    f"        result = None\n"
                    f"        return result\n"
                    f"    except Exception as e:\n"
                    f'        logger.exception(f"590474065f025e38: {{e}}")\n'
                    f"        raise\n\n"
                    f"def solve(data: Any) -> Any:\n"
                    f'    """\n'
                    f"    主入口函数\n"
                    f"    完整的处理流程：验证 → 处理 → 返回\n"
                    f'    """\n'
                    f"    if not validate_inputs(data):\n"
                    f'        raise ValueError("输入验证失败")\n'
                    f"    return process(data)\n\n"
                    f'if __name__ == "__main__":\n'
                    f"    # 测试用例\n"
                    f"    test_data = None\n"
                    f"    try:\n"
                    f"        output = solve(test_data)\n"
                    f'        print(f"7ed3679c: {{output}}")\n'
                    f"    except Exception as e:\n"
                    f'        print(f"95198bef: {{e}}")\n'
                )
            if st == "concise":
                return (
                    f"def solve(data):\n"
                    f"    # TODO: implement\n"
                    f"    return data\n\n"
                    f"print(solve(data))\n"
                )
            # professional
            return (
                f"# 基于需求的代码框架\n"
                f"# 需求：{d}\n\n"
                f"def solve():\n"
                f'    """核心处理函数"""\n'
                f"    # 参数校验\n"
                f"    if not validate_inputs():\n"
                f"        raise ValueError('Invalid inputs')\n\n"
                f"    # 核心逻辑\n"
                f"    result = process()\n\n"
                f"    return result\n\n"
                f"def validate_inputs():\n"
                f"    # TODO: 实现校验逻辑\n"
                f"    return True\n\n"
                f"def process():\n"
                f"    # TODO: 实现具体逻辑\n"
                f"    return None\n\n"
                f'if __name__ == "__main__":\n'
                f"    print(solve())\n"
            )
        # English
        if st == "detailed":
            return (
                f"# ============================================================\n"
                f"# Module: solution.py\n"
                f"# Description: {d}\n"
                f"# Author: AI Assistant\n"
                f"# Version: 1.0.0\n"
                f"# ============================================================\n\n"
                f"from typing import Any, Optional, List, Dict\n"
                f"import logging\n\n"
                f"logger = logging.getLogger(__name__)\n\n"
                f"def validate_inputs(data: Any) -> bool:\n"
                f'    """Validate input data."""\n'
                f"    if data is None:\n"
                f"        logger.error('Input data cannot be None')\n"
                f"        return False\n"
                f"    return True\n\n"
                f"def process(data: Any) -> Any:\n"
                f'    """Core processing logic."""\n'
                f"    try:\n"
                f"        # TODO: implement specific logic\n"
                f"        result = None\n"
                f"        return result\n"
                f"    except Exception as e:\n"
                f"        logger.exception(f'Processing error: {{e}}')\n"
                f"        raise\n\n"
                f"def solve(data: Any) -> Any:\n"
                f'    """Main entry point."""\n'
                f"    if not validate_inputs(data):\n"
                f"        raise ValueError('Input validation failed')\n"
                f"    return process(data)\n\n"
                f'if __name__ == "__main__":\n'
                f"    test_data = None\n"
                f"    try:\n"
                f"        output = solve(test_data)\n"
                f"        print(f'Result: {{output}}')\n"
                f"    except Exception as e:\n"
                f"        print(f'Error: {{e}}')\n"
            )
        if st == "concise":
            return (
                f"def solve(data):\n"
                f"    # TODO: implement\n"
                f"    return data\n\n"
                f"print(solve(data))\n"
            )
        # professional
        return (
            f"# Code Skeleton\n"
            f"# Requirement: {d}\n\n"
            f"def solve():\n"
            f'    """Core processing function."""\n'
            f"    # Validate inputs\n"
            f"    if not validate_inputs():\n"
            f"        raise ValueError('Invalid inputs')\n\n"
            f"    # Core logic\n"
            f"    result = process()\n\n"
            f"    return result\n\n"
            f"def validate_inputs():\n"
            f"    # TODO: implement validation\n"
            f"    return True\n\n"
            f"def process():\n"
            f"    # TODO: implement specific logic\n"
            f"    return None\n\n"
            f'if __name__ == "__main__":\n'
            f"    print(solve())\n"
        )

    def _fallback_analysis(d: str, l: str, st: str) -> str:
        if l == "zh":
            if st == "detailed":
                return (
                    f"# 深度分析报告\n\n"
                    f"## 分析主题：{d}\n\n"
                    f"### 一、研究背景与意义\n"
                    f"[详细阐述该主题的研究价值和现实背景]\n\n"
                    f"### 二、多维度现状分析\n"
                    f"#### 2.1 宏观环境分析\n"
                    f"- 政策法规环境\n"
                    f"- 经济技术环境\n"
                    f"- 社会文化环境\n\n"
                    f"#### 2.2 中观行业分析\n"
                    f"- 市场规模与增长趋势\n"
                    f"- 竞争格局与主要参与者\n"
                    f"- 产业链上下游关系\n\n"
                    f"#### 2.3 微观技术/方法分析\n"
                    f"- 核心技术原理与发展历程\n"
                    f"- 当前主流方案对比\n"
                    f"- 技术成熟度评估\n\n"
                    f"### 三、核心问题深度识别\n"
                    f"1. **结构性问题**：...\n"
                    f"2. **操作性障碍**：...\n"
                    f"3. **战略性挑战**：...\n\n"
                    f"### 四、数据支撑与案例验证\n"
                    f"- [相关数据指标]\n"
                    f"- [典型案例分析]\n\n"
                    f"### 五、系统性建议\n"
                    f"#### 5.1 短期行动（0-6个月）\n"
                    f"#### 5.2 中期规划（6-18个月）\n"
                    f"#### 5.3 长期战略（1-3年）"
                )
            if st == "concise":
                return (
                    f"# 分析结论\n\n"
                    f"主题：{d}\n\n"
                    f"核心发现：\n"
                    f"1. [关键发现一]\n"
                    f"2. [关键发现二]\n"
                    f"3. [关键发现三]\n\n"
                    f"建议：\n"
                    f"- 立即行动：...\n"
                    f"- 持续关注：..."
                )
            # professional
            return (
                f"# 分析报告\n\n"
                f"分析主题：{d}\n\n"
                f"## 一、背景\n"
                f"[简要概述分析主题的背景信息]\n\n"
                f"## 二、现状分析\n"
                f"1. 市场整体发展态势\n"
                f"2. 主要技术/方法进展\n"
                f"3. 核心参与者概况\n\n"
                f"## 三、关键问题\n"
                f"1. [核心问题一]\n"
                f"2. [核心问题二]\n"
                f"3. [核心问题三]\n\n"
                f"## 四、建议\n"
                f"- 短期：采取针对性措施\n"
                f"- 中期：制定系统方案\n"
                f"- 长期：建立持续机制"
            )
        # English
        if st == "detailed":
            return (
                f"# In-Depth Analysis Report\n\n"
                f"## Subject: {d}\n\n"
                f"### 1. Research Background & Significance\n"
                f"[Detailed exposition of the subject's research value and real-world context]\n\n"
                f"### 2. Multi-Dimensional Current State Analysis\n"
                f"#### 2.1 Macro Environment\n"
                f"- Policy and regulatory environment\n"
                f"- Economic and technological environment\n"
                f"- Socio-cultural environment\n\n"
                f"#### 2.2 Meso Industry Analysis\n"
                f"- Market size and growth trends\n"
                f"- Competitive landscape and key players\n"
                f"- Upstream and downstream industry chain\n\n"
                f"#### 2.3 Micro Technology/Methodology Analysis\n"
                f"- Core technical principles and development history\n"
                f"- Comparison of current mainstream solutions\n"
                f"- Technology maturity assessment\n\n"
                f"### 3. Core Issue Deep Dive\n"
                f"1. **Structural Issues**: ...\n"
                f"2. **Operational Barriers**: ...\n"
                f"3. **Strategic Challenges**: ...\n\n"
                f"### 4. Data Support & Case Validation\n"
                f"- [Relevant data metrics]\n"
                f"- [Typical case analysis]\n\n"
                f"### 5. Systematic Recommendations\n"
                f"#### 5.1 Short-term Actions (0-6 months)\n"
                f"#### 5.2 Medium-term Planning (6-18 months)\n"
                f"#### 5.3 Long-term Strategy (1-3 years)"
            )
        if st == "concise":
            return (
                f"# Analysis Summary\n\n"
                f"Subject: {d}\n\n"
                f"Key Findings:\n"
                f"1. [Key finding one]\n"
                f"2. [Key finding two]\n"
                f"3. [Key finding three]\n\n"
                f"Recommendations:\n"
                f"- Immediate action: ...\n"
                f"- Monitor closely: ..."
            )
        # professional
        return (
            f"# Analysis Report\n\n"
            f"Subject: {d}\n\n"
            f"## 1. Context\n"
            f"[Brief overview of the subject background]\n\n"
            f"## 2. Current State\n"
            f"1. Overall market development trends\n"
            f"2. Key technology/methodology progress\n"
            f"3. Core participant profiles\n\n"
            f"## 3. Key Issues\n"
            f"1. [Core issue one]\n"
            f"2. [Core issue two]\n"
            f"3. [Core issue three]\n\n"
            f"## 4. Recommendations\n"
            f"- Short-term: take targeted measures\n"
            f"- Medium-term: develop systematic solutions\n"
            f"- Long-term: establish sustainable mechanisms"
        )

    if scene == "image":
        return _fallback_image(desc, lang, style)
    if scene == "copywriting":
        return _fallback_copywriting(desc, lang, style)
    if scene == "coding":
        return _fallback_coding(desc, lang, style)
    if scene == "analysis":
        return _fallback_analysis(desc, lang, style)

    if lang == "zh":
        return f"【结果】\n\n{desc}\n\n（提示：配置 API Key 后可获得由 AI 生成的更优质内容）"
    return f"[Result]\n\n{desc}\n\n(Tip: Configure an API Key for AI-generated premium content.)"


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


async def optimize_prompt(input_text: str, goal: str, scene: str, lang: str) -> str:
    """
    Optimize a raw prompt into a scene-specific, ready-to-use prompt.
    Supports image / copywriting / coding / analysis / general scenes.
    """

    # Build system prompt based on scene and language
    def _sys_image() -> str:
        if lang == "zh":
            return (
                "你是一位顶级 AI 绘画提示词优化专家。用户会提供一个原始描述，"
                "你需要将其优化成可以直接用于 Stable Diffusion / Midjourney / DALL-E 的高质量英文提示词。\n"
                "\n"
                "要求：\n"
                "- 提取核心视觉元素，转化为精确的英文关键词\n"
                "- 包含主体、风格、光线、色彩、构图、氛围、画质等要素\n"
                "- 不要输出任何解释、说明或元提示\n"
                "- 直接输出优化后的英文提示词，可直接复制使用"
            )
        return (
            "You are a top-tier AI image prompt optimization expert. The user provides a raw description. "
            "You must optimize it into a high-quality English prompt for Stable Diffusion / Midjourney / DALL-E.\n"
            "\n"
            "Requirements:\n"
            "- Extract core visual elements and convert to precise English keywords\n"
            "- Include subject, style, lighting, color, composition, atmosphere, quality\n"
            "- Do NOT output any explanations, instructions, or meta-text\n"
            "- Output only the optimized English prompt, ready to copy and use"
        )

    def _sys_copywriting() -> str:
        if lang == "zh":
            return (
                "你是一位资深文案提示词优化专家。用户会提供一个原始文案需求，"
                "你需要优化成一个可以让 AI 直接生成高质量文案的提示词。\n"
                "\n"
                "要求：\n"
                "- 明确角色身份、目标受众、文案类型\n"
                "- 补充风格、语气、字数、结构要求\n"
                "- 补充行动号召和投放渠道信息\n"
                "- 不要输出任何解释或元提示\n"
                "- 直接输出优化后的提示词"
            )
        return (
            "You are a senior copywriting prompt optimization expert. The user provides a raw copy request. "
            "You must optimize it into a prompt that lets AI generate high-quality copy directly.\n"
            "\n"
            "Requirements:\n"
            "- Clarify role, target audience, copy type\n"
            "- Add style, tone, length, structure requirements\n"
            "- Include call-to-action and channel info\n"
            "- Do NOT output any explanations or meta-text\n"
            "- Output only the optimized prompt"
        )

    def _sys_coding() -> str:
        if lang == "zh":
            return (
                "你是一位资深编程提示词优化专家。用户会提供一个原始编程需求，"
                "你需要优化成一个可以让 AI 直接生成高质量代码的提示词。\n"
                "\n"
                "要求：\n"
                "- 明确编程语言、框架、版本要求\n"
                "- 补充功能需求、输入输出格式\n"
                "- 补充边界条件、错误处理、性能要求\n"
                "- 指定代码风格和注释规范\n"
                "- 不要输出任何解释或元提示\n"
                "- 直接输出优化后的提示词"
            )
        return (
            "You are a senior coding prompt optimization expert. The user provides a raw coding request. "
            "You must optimize it into a prompt that lets AI generate high-quality code directly.\n"
            "\n"
            "Requirements:\n"
            "- Clarify programming language, framework, version requirements\n"
            "- Add functional requirements, input/output format\n"
            "- Include edge cases, error handling, performance requirements\n"
            "- Specify code style and comment conventions\n"
            "- Do NOT output any explanations or meta-text\n"
            "- Output only the optimized prompt"
        )

    def _sys_analysis() -> str:
        if lang == "zh":
            return (
                "你是一位专业分析提示词优化专家。用户会提供一个原始分析需求，"
                "你需要优化成一个可以让 AI 直接生成深入分析报告的提示词。\n"
                "\n"
                "要求：\n"
                "- 明确分析框架、视角和方法论\n"
                "- 补充数据支撑要求和证据标准\n"
                "- 明确输出格式、结构和深度要求\n"
                "- 补充行业背景和限制条件\n"
                "- 不要输出任何解释或元提示\n"
                "- 直接输出优化后的提示词"
            )
        return (
            "You are a professional analysis prompt optimization expert. The user provides a raw analysis request. "
            "You must optimize it into a prompt that lets AI generate an in-depth analysis directly.\n"
            "\n"
            "Requirements:\n"
            "- Clarify analysis framework, perspectives, and methodology\n"
            "- Add data support requirements and evidence standards\n"
            "- Specify output format, structure, and depth requirements\n"
            "- Include industry context and constraints\n"
            "- Do NOT output any explanations or meta-text\n"
            "- Output only the optimized prompt"
        )

    def _sys_general() -> str:
        if lang == "zh":
            return (
                "你是一位通用提示词优化专家。用户会提供一个原始提示词，"
                "你需要将其优化成更结构化、更清晰、更可用的版本。\n"
                "\n"
                "要求：\n"
                "- 明确角色和任务目标\n"
                "- 补充格式、风格、长度等约束\n"
                "- 使用清晰的标题和段落划分\n"
                "- 不要输出任何解释或元提示\n"
                "- 直接输出优化后的提示词"
            )
        return (
            "You are a general prompt optimization expert. The user provides a raw prompt. "
            "You must optimize it into a more structured, clearer, and more usable version.\n"
            "\n"
            "Requirements:\n"
            "- Clarify role and task objective\n"
            "- Add format, style, length constraints\n"
            "- Use clear headings and paragraph divisions\n"
            "- Do NOT output any explanations or meta-text\n"
            "- Output only the optimized prompt"
        )

    goal_desc_zh = {
        "clarity": "提高清晰度：去除歧义，让需求更明确",
        "structure": "增强结构化：使用明确的标题和段落\n"
                     "按照背景 → 任务 → 要求 → 输出格式 的结构重组",
        "detail": "增加细节约束：补充具体参数、范围、标准\n"
                  "考虑边界情况和限制条件",
        "concise": "精简表达：删除冗余，保留核心信息\n"
                   "使用简短有力的表达",
        "role": "强化角色设定：明确 AI 身份、专业领域和能力边界\n"
                "用第一人称\"我\"回答，保持角色一致性",
    }
    goal_desc_en = {
        "clarity": "Improve clarity: remove ambiguity and make requirements explicit",
        "structure": "Enhance structure: use clear headings and paragraphs\n"
                     "Reorganize into Background → Task → Requirements → Output Format",
        "detail": "Add detail constraints: supplement specific parameters, scope, standards\n"
                  "Consider edge cases and limiting conditions",
        "concise": "Be concise: remove redundancy while keeping core info\n"
                   "Use short, powerful expressions",
        "role": "Strengthen role setting: clarify AI identity, expertise, and boundaries\n"
                "Answer in first person 'I', maintain role consistency",
    }

    goal_desc = goal_desc_zh.get(goal, goal_desc_zh["clarity"]) if lang == "zh" else goal_desc_en.get(goal, goal_desc_en["clarity"])

    scene_sys_map = {
        "image": _sys_image,
        "copywriting": _sys_copywriting,
        "coding": _sys_coding,
        "analysis": _sys_analysis,
    }
    system_prompt = scene_sys_map.get(scene, _sys_general)()

    user_prompt = (
        f"{'原始提示词' if lang == 'zh' else 'Original prompt'}:\n{input_text}\n\n"
        f"{'优化目标' if lang == 'zh' else 'Optimization goal'}: {goal_desc}\n\n"
        f"{'请直接输出优化后的提示词，不要输出任何解释。' if lang == 'zh' else 'Please output only the optimized prompt, no explanations.'}"
    )

    llm_result = await call_llm(system_prompt, user_prompt)
    if llm_result:
        return llm_result

    # --- Fallback: scene-specific templates, differentiated by goal ---
    def _fb_image(d: str) -> str:
        kw = d.strip()
        if lang == "zh":
            if goal == "clarity":
                return (
                    f"【优化后的提示词】\n\n"
                    f"主体：{kw}\n"
                    f"风格：photorealistic\n"
                    f"光线：soft natural lighting\n"
                    f"色彩：vibrant colors\n"
                    f"构图：clean composition\n"
                    f"画质：8k resolution, highly detailed, masterpiece, best quality\n"
                    f"氛围：serene, professional photography\n\n"
                    f"要求：上述提示词清晰明确，无歧义，可直接复制使用。"
                )
            if goal == "structure":
                return (
                    f"【优化后的提示词】\n\n"
                    f"1. 主体：{kw}\n"
                    f"2. 风格：photorealistic, highly detailed\n"
                    f"3. 光线：soft natural lighting, golden hour\n"
                    f"4. 色彩：vibrant colors, warm tones\n"
                    f"5. 构图：cinematic composition, depth of field\n"
                    f"6. 画质：8k resolution, masterpiece, best quality\n"
                    f"7. 氛围：serene, professional photography\n\n"
                    f"要求：按上述结构化顺序组织提示词。"
                )
            if goal == "detail":
                return (
                    f"【优化后的提示词】\n\n"
                    f"主体：{kw}\n"
                    f"风格：photorealistic, hyperrealistic, extremely detailed, intricate textures, lifelike materials\n"
                    f"光线：soft natural lighting, ambient occlusion, subsurface scattering, global illumination, ray tracing\n"
                    f"色彩：vibrant colors, warm tones, professional color grading\n"
                    f"构图：cinematic composition, depth of field, rule of thirds, leading lines\n"
                    f"画质：16k resolution, Unreal Engine 5 render, masterpiece, best quality\n"
                    f"氛围：serene, magical atmosphere, ethereal lighting\n\n"
                    f"要求：包含尽可能多的细节参数，确保提示词完整全面。"
                )
            if goal == "concise":
                return (
                    f"【优化后的提示词】\n\n"
                    f"{kw}, photorealistic, 8k, best quality, highly detailed\n\n"
                    f"要求：保留核心关键词，删除冗余描述。"
                )
            if goal == "role":
                return (
                    f"【优化后的提示词】\n\n"
                    f"你是一位顶级摄影师。请拍摄一张关于 {kw} 的照片。\n"
                    f"我需要你用专业的视角，把 {kw} 的美感和细节完美呈现出来。\n"
                    f"风格：photorealistic, highly detailed, professional photography\n"
                    f"光线：soft natural lighting\n"
                    f"色彩：vibrant colors\n"
                    f"构图：clean composition\n"
                    f"画质：8k resolution, masterpiece, best quality\n\n"
                    f"要求：保持摄影师角色一致性，用第一人称描述创作思路。"
                )
            return (
                f"【优化后的提示词】\n\n"
                f"主体：{kw}\n"
                f"风格：photorealistic\n"
                f"光线：soft natural lighting\n"
                f"色彩：vibrant colors\n"
                f"构图：clean composition\n"
                f"画质：8k resolution, highly detailed, masterpiece, best quality\n"
                f"氛围：serene, professional photography"
            )
        if goal == "clarity":
            return (
                f"[Optimized Prompt]\n\n"
                f"Subject: {kw}\n"
                f"Style: photorealistic\n"
                f"Lighting: soft natural lighting\n"
                f"Color: vibrant colors\n"
                f"Composition: clean composition\n"
                f"Quality: 8k resolution, highly detailed, masterpiece, best quality\n"
                f"Atmosphere: serene, professional photography\n\n"
                f"Requirement: The prompt above is clear and unambiguous, ready to use directly."
            )
        if goal == "structure":
            return (
                f"[Optimized Prompt]\n\n"
                f"1. Subject: {kw}\n"
                f"2. Style: photorealistic, highly detailed\n"
                f"3. Lighting: soft natural lighting, golden hour\n"
                f"4. Color: vibrant colors, warm tones\n"
                f"5. Composition: cinematic composition, depth of field\n"
                f"6. Quality: 8k resolution, masterpiece, best quality\n"
                f"7. Atmosphere: serene, professional photography\n\n"
                f"Requirement: Organize the prompt in the structured order above."
            )
        if goal == "detail":
            return (
                f"[Optimized Prompt]\n\n"
                f"Subject: {kw}\n"
                f"Style: photorealistic, hyperrealistic, extremely detailed, intricate textures, lifelike materials\n"
                f"Lighting: soft natural lighting, ambient occlusion, subsurface scattering, global illumination, ray tracing\n"
                f"Color: vibrant colors, warm tones, professional color grading\n"
                f"Composition: cinematic composition, depth of field, rule of thirds, leading lines\n"
                f"Quality: 16k resolution, Unreal Engine 5 render, masterpiece, best quality\n"
                f"Atmosphere: serene, magical atmosphere, ethereal lighting\n\n"
                f"Requirement: Include as many detail parameters as possible to ensure completeness."
            )
        if goal == "concise":
            return (
                f"[Optimized Prompt]\n\n"
                f"{kw}, photorealistic, 8k, best quality, highly detailed\n\n"
                f"Requirement: Keep only core keywords, remove redundant descriptions."
            )
        if goal == "role":
            return (
                f"[Optimized Prompt]\n\n"
                f"You are a top-tier photographer. Please take a photo of {kw}.\n"
                f"I need you to present the beauty and details of {kw} from a professional perspective.\n"
                f"Style: photorealistic, highly detailed, professional photography\n"
                f"Lighting: soft natural lighting\n"
                f"Color: vibrant colors\n"
                f"Composition: clean composition\n"
                f"Quality: 8k resolution, masterpiece, best quality\n\n"
                f"Requirement: Maintain photographer role consistency, describe creative approach in first person."
            )
        return (
            f"[Optimized Prompt]\n\n"
            f"Subject: {kw}\n"
            f"Style: photorealistic\n"
            f"Lighting: soft natural lighting\n"
            f"Color: vibrant colors\n"
            f"Composition: clean composition\n"
            f"Quality: 8k resolution, highly detailed, masterpiece, best quality\n"
            f"Atmosphere: serene, professional photography"
        )

    def _fb_copywriting(d: str) -> str:
        if lang == "zh":
            if goal == "clarity":
                return (
                    f"【优化后的提示词】\n\n"
                    f"角色：你是一位资深文案策划专家。\n\n"
                    f"任务：根据以下需求生成高质量文案。\n"
                    f"需求：{d}\n\n"
                    f"要求：\n"
                    f"- 文案必须清晰明确，无歧义\n"
                    f"- 突出核心价值，避免空泛表达\n"
                    f"- 语言简洁有力，直击要点\n"
                    f"- 结尾给出明确的行动号召"
                )
            if goal == "structure":
                return (
                    f"【优化后的提示词】\n\n"
                    f"【角色】\n你是一位资深文案策划专家。\n\n"
                    f"【背景】\n简要介绍文案的背景和目标受众。\n\n"
                    f"【任务】\n根据以下需求生成高质量文案：\n{d}\n\n"
                    f"【要求】\n"
                    f"1. 标题：吸引人、点明主题\n"
                    f"2. 引言：引发兴趣，建立连接\n"
                    f"3. 正文：分点阐述，逻辑清晰\n"
                    f"4. 结尾：行动号召，强化转化\n\n"
                    f"【输出格式】\n标题、引言、正文、结尾四部分。"
                )
            if goal == "detail":
                return (
                    f"【优化后的提示词】\n\n"
                    f"【角色】\n你是一位资深文案策划专家，拥有10年行业经验。\n\n"
                    f"【任务】\n根据以下需求生成高质量文案：\n{d}\n\n"
                    f"【目标受众】\n25-40岁城市白领，注重品质与性价比。\n\n"
                    f"【投放渠道】\n微信公众号、朋友圈。\n\n"
                    f"【文案类型】\n推荐类软文。\n\n"
                    f"【风格与语气】\n亲切自然，有信任感，避免过度营销。\n\n"
                    f"【字数要求】\n800-1200字。\n\n"
                    f"【结构要求】\n"
                    f"- 标题：20字以内，含关键词\n"
                    f"- 引言：50-80字，引发共鸣\n"
                    f"- 正文：分为3-4个小节，每节500-800字\n"
                    f"- 结尾：行动号召，含优惠/时间限制\n\n"
                    f"【其他约束】\n"
                    f"- 使用第一人称\n"
                    f"- 含具体案例或数据\n"
                    f"- 结尾加一个问句引导互动"
                )
            if goal == "concise":
                return (
                    f"【优化后的提示词】\n\n"
                    f"你是一位文案专家。写一段关于 {d} 的文案。\n"
                    f"要求：\n"
                    f"- 50字以内\n"
                    f"- 突出核心价值\n"
                    f"- 含行动号召\n"
                    f"- 不要冗余"
                )
            if goal == "role":
                return (
                    f"【优化后的提示词】\n\n"
                    f"你是一位知名广告创意总监，拥有15年行业经验。\n"
                    f"你擅长用极致的文案触达用户内心，曾服务于多个国际大牌。\n\n"
                    f"现在请你以这个身份，为 {d} 写一篇推荐文案。\n\n"
                    f"要求：\n"
                    f"- 始终保持创意总监角色\n"
                    f"- 用第一人称\"我\"叙述\n"
                    f"- 文案风格专业且有温度\n"
                    f"- 结尾加行动号召"
                )
            return (
                f"【优化后的提示词】\n\n"
                f"角色：你是一位资深文案策划专家。\n\n"
                f"任务：根据以下需求生成高质量文案。\n"
                f"需求：{d}\n\n"
                f"要求：\n"
                f"- 文案必须清晰明确，无歧义\n"
                f"- 突出核心价值，避免空泛表达\n"
                f"- 语言简洁有力，直击要点\n"
                f"- 结尾给出明确的行动号召"
            )
        if goal == "clarity":
            return (
                f"[Optimized Prompt]\n\n"
                f"Role: You are a senior copywriting expert.\n\n"
                f"Task: Generate high-quality copy based on the following request.\n"
                f"Request: {d}\n\n"
                f"Requirements:\n"
                f"- The copy must be clear and unambiguous\n"
                f"- Highlight core value, avoid empty rhetoric\n"
                f"- Use concise and powerful language\n"
                f"- End with a clear call to action"
            )
        if goal == "structure":
            return (
                f"[Optimized Prompt]\n\n"
                f"[Role]\nYou are a senior copywriting expert.\n\n"
                f"[Background]\nBriefly introduce the copy context and target audience.\n\n"
                f"[Task]\nGenerate high-quality copy based on the following request:\n{d}\n\n"
                f"[Requirements]\n"
                f"1. Headline: attractive and on-point\n"
                f"2. Hook: build interest and connection\n"
                f"3. Body: clear points, logical flow\n"
                f"4. Conclusion: call to action, drive conversion\n\n"
                f"[Output Format]\nHeadline, Hook, Body, Conclusion in four parts."
            )
        if goal == "detail":
            return (
                f"[Optimized Prompt]\n\n"
                f"[Role]\nYou are a senior copywriting expert with 10 years of industry experience.\n\n"
                f"[Task]\nGenerate high-quality copy based on the following request:\n{d}\n\n"
                f"[Target Audience]\nUrban professionals aged 25-40, value quality and cost performance.\n\n"
                f"[Channels]\nWeChat Official Account, Moments.\n\n"
                f"[Copy Type]\nRecommendation soft article.\n\n"
                f"[Style & Tone]\nFriendly and natural, trustworthy, avoid over-marketing.\n\n"
                f"[Length]\n500-800 words.\n\n"
                f"[Structure]\n"
                f"- Headline: within 15 words, include keywords\n"
                f"- Hook: 30-50 words, build resonance\n"
                f"- Body: 3-4 sections, 100-150 words each\n"
                f"- Conclusion: call to action with offer/time limit\n\n"
                f"[Other Constraints]\n"
                f"- Use first person\n"
                f"- Include specific examples or data\n"
                f"- End with a question to drive engagement"
            )
        if goal == "concise":
            return (
                f"[Optimized Prompt]\n\n"
                f"You are a copywriting expert. Write a short piece about {d}.\n"
                f"Requirements:\n"
                f"- Within 30 words\n"
                f"- Highlight core value\n"
                f"- Include call to action\n"
                f"- No redundancy"
            )
        if goal == "role":
            return (
                f"[Optimized Prompt]\n\n"
                f"You are a renowned creative director with 15 years of industry experience.\n"
                f"You excel at crafting copy that touches users deeply, having served multiple international brands.\n\n"
                f"Now please write a recommendation piece for {d} in this role.\n\n"
                f"Requirements:\n"
                f"- Always maintain the creative director persona\n"
                f"- Use first person 'I'\n"
                f"- Professional yet warm tone\n"
                f"- End with call to action"
            )
        return (
            f"[Optimized Prompt]\n\n"
            f"Role: You are a senior copywriting expert.\n\n"
            f"Task: Generate high-quality copy based on the following request.\n"
            f"Request: {d}\n\n"
            f"Requirements:\n"
            f"- The copy must be clear and unambiguous\n"
            f"- Highlight core value, avoid empty rhetoric\n"
            f"- Use concise and powerful language\n"
            f"- End with a clear call to action"
        )

    def _fb_coding(d: str) -> str:
        if lang == "zh":
            if goal == "clarity":
                return (
                    f"【优化后的提示词】\n\n"
                    f"你是一位资深软件工程师。\n\n"
                    f"任务：根据以下需求编写清晰易懂的代码。\n"
                    f"需求：{d}\n\n"
                    f"要求：\n"
                    f"- 代码逻辑清晰，注释简明\n"
                    f"- 变量名称有意义\n"
                    f"- 避免多余复杂的工具类\n"
                    f"- 输出格式统一\n"
                    f"- 含简单使用示例"
                )
            if goal == "structure":
                return (
                    f"【优化后的提示词】\n\n"
                    f"【角色】\n你是一位资深软件工程师。\n\n"
                    f"【任务】\n根据以下需求编写代码：\n{d}\n\n"
                    f"【输出格式】\n"
                    f"1. 算法思路说明（50字以内）\n"
                    f"2. 完整代码（含注释）\n"
                    f"3. 复杂度分析\n"
                    f"4. 测试用例\n\n"
                    f"【要求】\n"
                    f"- 代码按上述结构组织\n"
                    f"- 使用标准命名规范\n"
                    f"- 含错误处理"
                )
            if goal == "detail":
                return (
                    f"【优化后的提示词】\n\n"
                    f"【角色】\n你是一位拥有10年经验的架构师。\n\n"
                    f"【任务】\n根据以下需求编写生产级代码：\n{d}\n\n"
                    f"【技术栈】\nPython 3.11, 不使用外部框架\n\n"
                    f"【输出要求】\n"
                    f"- 完整的模块结构（含文件头注释）\n"
                    f"- 详细的函数文档字符串（Google Style）\n"
                    f"- 类型注解\n"
                    f"- 单元测试（覆盖90%以上分支）\n"
                    f"- 错误处理和日志记录\n"
                    f"- 时间/空间复杂度分析\n\n"
                    f"【边界条件】\n"
                    f"- 输入范围限制\n"
                    f"- 非法输入处理\n"
                    f"- 性能要求（时间复杂度 O(n log n)）"
                )
            if goal == "concise":
                return (
                    f"【优化后的提示词】\n\n"
                    f"你是一位软件工程师。实现 {d} 。\n"
                    f"要求：\n"
                    f"- 代码不超过10行\n"
                    f"- 含简要注释\n"
                    f"- 时间复杂度最优"
                )
            if goal == "role":
                return (
                    f"【优化后的提示词】\n\n"
                    f"你是一位拥有10年经验的架构师，专注高性能系统设计。\n"
                    f"你对代码质量有极高的要求，追求简洁而优雅的解决方案。\n\n"
                    f"现在请你以这个身份，实现 {d} 。\n\n"
                    f"要求：\n"
                    f"- 始终保持架构师角色\n"
                    f"- 用第一人称解释设计思路\n"
                    f"- 代码符合最佳实践\n"
                    f"- 含复杂度分析"
                )
            return (
                f"【优化后的提示词】\n\n"
                f"你是一位资深软件工程师。\n\n"
                f"任务：根据以下需求编写清晰易懂的代码。\n"
                f"需求：{d}\n\n"
                f"要求：\n"
                f"- 代码逻辑清晰，注释简明\n"
                f"- 变量名称有意义\n"
                f"- 避免多余复杂的工具类\n"
                f"- 输出格式统一\n"
                f"- 含简单使用示例"
            )
        if goal == "clarity":
            return (
                f"[Optimized Prompt]\n\n"
                f"You are a senior software engineer.\n\n"
                f"Task: Write clear, easy-to-understand code for the following requirement.\n"
                f"Requirement: {d}\n\n"
                f"Requirements:\n"
                f"- Code logic must be clear, comments concise\n"
                f"- Variable names must be meaningful\n"
                f"- Avoid redundant complex utilities\n"
                f"- Uniform output format\n"
                f"- Include a simple usage example"
            )
        if goal == "structure":
            return (
                f"[Optimized Prompt]\n\n"
                f"[Role]\nYou are a senior software engineer.\n\n"
                f"[Task]\nWrite code for the following requirement:\n{d}\n\n"
                f"[Output Format]\n"
                f"1. Algorithm explanation (within 50 words)\n"
                f"2. Complete code (with comments)\n"
                f"3. Complexity analysis\n"
                f"4. Test cases\n\n"
                f"[Requirements]\n"
                f"- Code follows the structure above\n"
                f"- Use standard naming conventions\n"
                f"- Include error handling"
            )
        if goal == "detail":
            return (
                f"[Optimized Prompt]\n\n"
                f"[Role]\nYou are an architect with 10 years of experience.\n\n"
                f"[Task]\nWrite production-level code for the following requirement:\n{d}\n\n"
                f"[Tech Stack]\nPython 3.11, no external frameworks\n\n"
                f"[Output Requirements]\n"
                f"- Complete module structure (with file header comments)\n"
                f"- Detailed function docstrings (Google Style)\n"
                f"- Type annotations\n"
                f"- Unit tests (covering 90%+ branches)\n"
                f"- Error handling and logging\n"
                f"- Time/space complexity analysis\n\n"
                f"[Boundary Conditions]\n"
                f"- Input range limits\n"
                f"- Invalid input handling\n"
                f"- Performance requirements (time complexity O(n log n))"
            )
        if goal == "concise":
            return (
                f"[Optimized Prompt]\n\n"
                f"You are a software engineer. Implement {d}.\n"
                f"Requirements:\n"
                f"- Code under 10 lines\n"
                f"- Brief comments\n"
                f"- Optimal time complexity"
            )
        if goal == "role":
            return (
                f"[Optimized Prompt]\n\n"
                f"You are an architect with 10 years of experience, specializing in high-performance system design.\n"
                f"You have extremely high standards for code quality, pursuing simple yet elegant solutions.\n\n"
                f"Now please implement {d} in this role.\n\n"
                f"Requirements:\n"
                f"- Always maintain the architect persona\n"
                f"- Explain design approach in first person\n"
                f"- Code follows best practices\n"
                f"- Include complexity analysis"
            )
        return (
            f"[Optimized Prompt]\n\n"
            f"You are a senior software engineer.\n\n"
            f"Task: Write clear, easy-to-understand code for the following requirement.\n"
            f"Requirement: {d}\n\n"
            f"Requirements:\n"
            f"- Code logic must be clear, comments concise\n"
            f"- Variable names must be meaningful\n"
            f"- Avoid redundant complex utilities\n"
            f"- Uniform output format\n"
            f"- Include a simple usage example"
        )

    def _fb_analysis(d: str) -> str:
        if lang == "zh":
            if goal == "clarity":
                return (
                    f"【优化后的提示词】\n\n"
                    f"你是一位专业分析师。\n\n"
                    f"任务：清晰地分析 {d} 。\n\n"
                    f"要求：\n"
                    f"- 分析结果必须清晰明确，无歧义\n"
                    f"- 每个观点有具体例子支撑\n"
                    f"- 结论简明扼要\n"
                    f"- 避免专业术语过多\n"
                    f"- 结构简单直观"
                )
            if goal == "structure":
                return (
                    f"【优化后的提示词】\n\n"
                    f"【角色】\n你是一位专业分析师。\n\n"
                    f"【背景】\n简要介绍 {d} 的背景信息。\n\n"
                    f"【分析任务】\n对 {d} 进行系统性分析。\n\n"
                    f"【分析框架】\n"
                    f"1. 背景介绍\n"
                    f"2. 现状分析（多角度）\n"
                    f"3. 核心问题识别\n"
                    f"4. 数据与证据支撑\n"
                    f"5. 结论与建议\n\n"
                    f"【输出要求】\n"
                    f"- 严格按照上述框架组织内容\n"
                    f"- 每部分用清晰的标题标注"
                )
            if goal == "detail":
                return (
                    f"【优化后的提示词】\n\n"
                    f"【角色】\n你是一位顶尖行业顾问，拥有15年分析经验。\n\n"
                    f"【分析主题】\n{d}\n\n"
                    f"【分析框架】\n"
                    f"### 1. 宏观环境分析\n"
                    f"- 政策法规\n"
                    f"- 经济技术环境\n"
                    f"- 社会文化\n\n"
                    f"### 2. 中观行业分析\n"
                    f"- 市场规模与增长\n"
                    f"- 竞争格局\n"
                    f"- 产业链\n\n"
                    f"### 3. 微观技术/方法分析\n"
                    f"- 核心原理\n"
                    f"- 主流方案对比\n"
                    f"- 技术成熟度\n\n"
                    f"### 4. 数据支撑\n"
                    f"- 关键指标数据\n"
                    f"- 典型案例\n\n"
                    f"### 5. 建议\n"
                    f"- 短期（0-6个月）\n"
                    f"- 中期（6-18个月）\n"
                    f"- 长期（1-3年）\n\n"
                    f"【要求】\n"
                    f"- 每个部分提供具体数据或案例\n"
                    f"- 观点有出处\n"
                    f"- 建议可执行"
                )
            if goal == "concise":
                return (
                    f"【优化后的提示词】\n\n"
                    f"你是一位分析师。对 {d} 做简要分析。\n"
                    f"要求：\n"
                    f"- 3个核心发现\n"
                    f"- 2条行动建议\n"
                    f"- 不超过200字"
                )
            if goal == "role":
                return (
                    f"【优化后的提示词】\n\n"
                    f"你是一位顶尖行业顾问，曾为多家世界500强企业提供战略咨询。\n"
                    f"你擅长从宏观视角分析问题，给出深刻而可执行的建议。\n\n"
                    f"现在请你以这个身份，分析 {d} 。\n\n"
                    f"要求：\n"
                    f"- 始终保持顾问角色\n"
                    f"- 用第一人称分析\n"
                    f"- 给出具体数据支撑\n"
                    f"- 建议可执行"
                )
            return (
                f"【优化后的提示词】\n\n"
                f"你是一位专业分析师。\n\n"
                f"任务：清晰地分析 {d} 。\n\n"
                f"要求：\n"
                f"- 分析结果必须清晰明确，无歧义\n"
                f"- 每个观点有具体例子支撑\n"
                f"- 结论简明扼要\n"
                f"- 避免专业术语过多\n"
                f"- 结构简单直观"
            )
        if goal == "clarity":
            return (
                f"[Optimized Prompt]\n\n"
                f"You are a professional analyst.\n\n"
                f"Task: Clearly analyze {d}.\n\n"
                f"Requirements:\n"
                f"- Analysis results must be clear and unambiguous\n"
                f"- Each viewpoint supported by specific examples\n"
                f"- Conclusions concise and to the point\n"
                f"- Avoid excessive jargon\n"
                f"- Simple and intuitive structure"
            )
        if goal == "structure":
            return (
                f"[Optimized Prompt]\n\n"
                f"[Role]\nYou are a professional analyst.\n\n"
                f"[Background]\nBriefly introduce the background of {d}.\n\n"
                f"[Analysis Task]\nConduct a systematic analysis of {d}.\n\n"
                f"[Analysis Framework]\n"
                f"1. Background Introduction\n"
                f"2. Current State Analysis (multi-angle)\n"
                f"3. Core Issue Identification\n"
                f"4. Data and Evidence Support\n"
                f"5. Conclusions and Recommendations\n\n"
                f"[Output Requirements]\n"
                f"- Strictly follow the framework above\n"
                f"- Each part has clear headings"
            )
        if goal == "detail":
            return (
                f"[Optimized Prompt]\n\n"
                f"[Role]\nYou are a top industry consultant with 15 years of analysis experience.\n\n"
                f"[Subject]\n{d}\n\n"
                f"[Analysis Framework]\n"
                f"### 1. Macro Environment\n"
                f"- Policy and regulations\n"
                f"- Economic and technology environment\n"
                f"- Social culture\n\n"
                f"### 2. Meso Industry\n"
                f"- Market size and growth\n"
                f"- Competitive landscape\n"
                f"- Industry chain\n\n"
                f"### 3. Micro Technology/Methodology\n"
                f"- Core principles\n"
                f"- Mainstream solutions comparison\n"
                f"- Technology maturity\n\n"
                f"### 4. Data Support\n"
                f"- Key metrics\n"
                f"- Typical cases\n\n"
                f"### 5. Recommendations\n"
                f"- Short-term (0-6 months)\n"
                f"- Medium-term (6-18 months)\n"
                f"- Long-term (1-3 years)\n\n"
                f"[Requirements]\n"
                f"- Each part provides specific data or cases\n"
                f"- Viewpoints have sources\n"
                f"- Recommendations are actionable"
            )
        if goal == "concise":
            return (
                f"[Optimized Prompt]\n\n"
                f"You are an analyst. Provide a brief analysis of {d}.\n"
                f"Requirements:\n"
                f"- 3 key findings\n"
                f"- 2 action recommendations\n"
                f"- Under 150 words"
            )
        if goal == "role":
            return (
                f"[Optimized Prompt]\n\n"
                f"You are a top industry consultant who has provided strategic consulting to multiple Fortune 500 companies.\n"
                f"You excel at analyzing problems from a macro perspective and providing deep yet actionable advice.\n\n"
                f"Now please analyze {d} in this role.\n\n"
                f"Requirements:\n"
                f"- Always maintain the consultant persona\n"
                f"- Analyze in first person\n"
                f"- Provide specific data support\n"
                f"- Recommendations must be actionable"
            )
        return (
            f"[Optimized Prompt]\n\n"
            f"You are a professional analyst.\n\n"
            f"Task: Clearly analyze {d}.\n\n"
            f"Requirements:\n"
            f"- Analysis results must be clear and unambiguous\n"
            f"- Each viewpoint supported by specific examples\n"
            f"- Conclusions concise and to the point\n"
            f"- Avoid excessive jargon\n"
            f"- Simple and intuitive structure"
        )

    def _fb_general(d: str) -> str:
        if lang == "zh":
            if goal == "clarity":
                return (
                    f"【优化后的提示词】\n\n"
                    f"你是一位领域专家。\n\n"
                    f"任务：清晰地完成以下任务。\n"
                    f"需求：{d}\n\n"
                    f"要求：\n"
                    f"- 需求必须清晰明确，无歧义\n"
                    f"- 输出结果直接明了\n"
                    f"- 不要模糊的表达\n"
                    f"- 如有不确定之处，明确标注"
                )
            if goal == "structure":
                return (
                    f"【优化后的提示词】\n\n"
                    f"【角色】\n你是一位领域专家。\n\n"
                    f"【背景】\n简要介绍任务背景。\n\n"
                    f"【任务】\n{d}\n\n"
                    f"【要求】\n"
                    f"1. 先确认理解正确\n"
                    f"2. 使用清晰有条理的结构\n"
                    f"3. 关键结论优先\n"
                    f"4. 细节补充在后\n\n"
                    f"【输出格式】\n分点阐述，每点独立成段。"
                )
            if goal == "detail":
                return (
                    f"【优化后的提示词】\n\n"
                    f"【角色】\n你是一位顶尖行业顾问，拥有15年经验。\n\n"
                    f"【任务】\n{d}\n\n"
                    f"【背景信息】\n请在此补充相关上下文。\n\n"
                    f"【详细要求】\n"
                    f"1. 输出前先列出你的理解和计划\n"
                    f"2. 每个论点提供具体例子或数据支撑\n"
                    f"3. 考虑至少3种不同情况\n"
                    f"4. 说明推理过程，不只是结论\n"
                    f"5. 标注任何假设条件\n"
                    f"6. 结尾给出总结和行动建议"
                )
            if goal == "concise":
                return (
                    f"【优化后的提示词】\n\n"
                    f"你是一位领域专家。完成以下任务：\n{d}\n\n"
                    f"要求：\n"
                    f"- 只输出最关键的信息\n"
                    f"- 删除冗余表达\n"
                    f"- 直接给出答案或结论"
                )
            if goal == "role":
                return (
                    f"【优化后的提示词】\n\n"
                    f"你是一位拥有15年经验的顶尖行业顾问。\n"
                    f"你专注于用通俗易懂的语言解释复杂问题。\n\n"
                    f"现在请你以这个角色完成任务：\n{d}\n\n"
                    f"要求：\n"
                    f"- 始终保持顾问角色\n"
                    f"- 用第一人称\"我\"回答\n"
                    f"- 简洁有力，不绕弯子\n"
                    f"- 遇到不确定的问题诚实告知"
                )
            return (
                f"【优化后的提示词】\n\n"
                f"你是一位领域专家。\n\n"
                f"任务：清晰地完成以下任务。\n"
                f"需求：{d}\n\n"
                f"要求：\n"
                f"- 需求必须清晰明确，无歧义\n"
                f"- 输出结果直接明了\n"
                f"- 不要模糊的表达\n"
                f"- 如有不确定之处，明确标注"
            )
        if goal == "clarity":
            return (
                f"[Optimized Prompt]\n\n"
                f"You are a domain expert.\n\n"
                f"Task: Complete the following task clearly.\n"
                f"Requirement: {d}\n\n"
                f"Requirements:\n"
                f"- Requirements must be clear and unambiguous\n"
                f"- Output results directly and clearly\n"
                f"- No vague expressions\n"
                f"- Flag any uncertainties explicitly"
            )
        if goal == "structure":
            return (
                f"[Optimized Prompt]\n\n"
                f"[Role]\nYou are a domain expert.\n\n"
                f"[Background]\nBriefly introduce the task context.\n\n"
                f"[Task]\n{d}\n\n"
                f"[Requirements]\n"
                f"1. Confirm understanding first\n"
                f"2. Use clear, structured organization\n"
                f"3. Key conclusions first\n"
                f"4. Details later\n\n"
                f"[Output Format]\nBullet points, each point in a separate paragraph."
            )
        if goal == "detail":
            return (
                f"[Optimized Prompt]\n\n"
                f"[Role]\nYou are a top industry consultant with 15 years of experience.\n\n"
                f"[Task]\n{d}\n\n"
                f"[Background]\nPlease supplement relevant context here.\n\n"
                f"[Detailed Requirements]\n"
                f"1. List your understanding and plan before outputting\n"
                f"2. Provide specific examples or data for each point\n"
                f"3. Consider at least 3 different scenarios\n"
                f"4. Explain reasoning process, not just conclusions\n"
                f"5. Flag any assumptions\n"
                f"6. End with summary and actionable advice"
            )
        if goal == "concise":
            return (
                f"[Optimized Prompt]\n\n"
                f"You are a domain expert. Complete the following task:\n{d}\n\n"
                f"Requirements:\n"
                f"- Output only the most critical information\n"
                f"- Remove redundant expressions\n"
                f"- Directly give the answer or conclusion"
            )
        if goal == "role":
            return (
                f"[Optimized Prompt]\n\n"
                f"You are a top industry consultant with 15 years of experience.\n"
                f"You specialize in explaining complex problems in simple terms.\n\n"
                f"Now please complete the task in this role:\n{d}\n\n"
                f"Requirements:\n"
                f"- Always maintain the consultant persona\n"
                f"- Use first person 'I'\n"
                f"- Concise and powerful, no beating around the bush\n"
                f"- Honestly acknowledge any uncertainties"
            )
        return (
            f"[Optimized Prompt]\n\n"
            f"You are a domain expert.\n\n"
            f"Task: Complete the following task clearly.\n"
            f"Requirement: {d}\n\n"
            f"Requirements:\n"
            f"- Requirements must be clear and unambiguous\n"
            f"- Output results directly and clearly\n"
            f"- No vague expressions\n"
            f"- Flag any uncertainties explicitly"
        )

    fb_map = {
        "image": _fb_image,
        "copywriting": _fb_copywriting,
        "coding": _fb_coding,
        "analysis": _fb_analysis,
    }
    return fb_map.get(scene, _fb_general)(input_text)
