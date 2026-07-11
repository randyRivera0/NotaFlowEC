from nicegui import ui


def apply_theme() -> None:
    ui.colors(primary="#173F5F", secondary="#167D8D", accent="#167D8D")
    ui.add_css("""
    body { background: #f4f7fa; color: #1d2a36; font-family: Inter, Arial, sans-serif; }
    .nf-page { width: 100%; max-width: 1500px; margin: 0 auto; padding: 28px; gap: 20px; }
    .nf-card { border: 1px solid #e3e9ef; border-radius: 12px; box-shadow: 0 2px 8px rgba(24,48,72,.05); }
    .nf-muted { color: #637384; }
    .nf-sidebar { background: #12354f; color: white; }
    .nf-nav { border-radius: 8px; width: 100%; justify-content: flex-start; color: #dbe8f1; }
    """)
