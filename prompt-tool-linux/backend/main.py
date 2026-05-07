import json
import os
import sqlite3
from datetime import datetime
from typing import List

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles

from models import GenerateRequest, OptimizeRequest, PromptCreate, PromptItem, PromptLibrary
from services import generate_prompt, optimize_prompt, analyze_prompt

DATA_DIR = "/app/data"
DB_PATH = os.path.join(DATA_DIR, "prompts.db")


def init_db():
    os.makedirs(DATA_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS prompts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            scene TEXT DEFAULT 'general',
            created TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def db_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def row_to_dict(row) -> dict:
    return {
        "id": row["id"],
        "title": row["title"],
        "content": row["content"],
        "scene": row["scene"],
        "created": row["created"],
    }


app = FastAPI(title="AI 提示词工具箱 API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    init_db()


@app.post("/api/generate")
def api_generate(req: GenerateRequest):
    result = generate_prompt(req.desc, req.scene.value, req.style.value, req.lang.value)
    return {"result": result}


@app.post("/api/optimize")
def api_optimize(req: OptimizeRequest):
    suggestions = analyze_prompt(req.input)
    result = optimize_prompt(req.input, req.goal.value, req.scene)
    return {"suggestions": suggestions, "result": result}


@app.get("/api/prompts", response_model=PromptLibrary)
def list_prompts(q: str = "", scene: str = ""):
    conn = db_conn()
    cursor = conn.cursor()
    sql = "SELECT * FROM prompts WHERE 1=1"
    params = []
    if q:
        sql += " AND (title LIKE ? OR content LIKE ?)"
        params.extend([f"%{q}%", f"%{q}%"])
    if scene:
        sql += " AND scene = ?"
        params.append(scene)
    sql += " ORDER BY id DESC"
    cursor.execute(sql, params)
    rows = cursor.fetchall()
    conn.close()
    items = [PromptItem(**row_to_dict(r)) for r in rows]
    return PromptLibrary(prompts=items, total=len(items))


@app.post("/api/prompts", response_model=PromptItem)
def create_prompt(req: PromptCreate):
    conn = db_conn()
    cursor = conn.cursor()
    created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(
        "INSERT INTO prompts (title, content, scene, created) VALUES (?, ?, ?, ?)",
        (req.title, req.content, req.scene or "general", created),
    )
    new_id = cursor.lastrowid
    conn.commit()
    cursor.execute("SELECT * FROM prompts WHERE id = ?", (new_id,))
    row = cursor.fetchone()
    conn.close()
    return PromptItem(**row_to_dict(row))


@app.delete("/api/prompts/{prompt_id}")
def delete_prompt(prompt_id: int):
    conn = db_conn()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM prompts WHERE id = ?", (prompt_id,))
    conn.commit()
    conn.close()
    return {"ok": True}


@app.get("/api/prompts/export")
def export_prompts():
    conn = db_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM prompts ORDER BY id DESC")
    rows = [row_to_dict(r) for r in cursor.fetchall()]
    conn.close()
    content = json.dumps(rows, ensure_ascii=False, indent=2)
    filename = f"prompts_{datetime.now().strftime('%Y%m%d')}.json"

    def iter_content():
        yield content.encode("utf-8")

    return StreamingResponse(
        iter_content(),
        media_type="application/json",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@app.post("/api/prompts/import")
def import_prompts(payload: List[dict]):
    conn = db_conn()
    cursor = conn.cursor()
    imported = 0
    for item in payload:
        if not item.get("content"):
            continue
        title = item.get("title", item["content"].split("\n")[0][:40])
        scene = item.get("scene", "general")
        created = item.get("created", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        cursor.execute(
            "INSERT INTO prompts (title, content, scene, created) VALUES (?, ?, ?, ?)",
            (title, item["content"], scene, created),
        )
        imported += 1
    conn.commit()
    cursor.execute("SELECT COUNT(*) as cnt FROM prompts")
    total = cursor.fetchone()["cnt"]
    conn.close()
    return {"imported": imported, "total": total}


# Static files
frontend_dir = os.path.join(os.path.dirname(__file__), "..", "frontend")
if os.path.isdir(frontend_dir):
    app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8088)
