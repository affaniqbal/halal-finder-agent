import json
from datetime import datetime


HALAL_BADGE = {
    "LIKELY HALAL": ('<span class="badge likely">✓ Likely Halal</span>', "#22c55e"),
    "POSSIBLY HALAL": ('<span class="badge possibly">~ Possibly Halal</span>', "#f59e0b"),
    "UNVERIFIED": ('<span class="badge unverified">? Unverified</span>', "#94a3b8"),
}


def render_html(data: dict, output_path: str = "results.html"):
    results = data.get("results", [])
    query = data.get("query", "")
    summary = data.get("summary", "")
    timestamp = datetime.now().strftime("%d %b %Y, %H:%M")

    cards_html = ""
    for r in results:
        badge_html, _ = HALAL_BADGE.get(r.get("halal_status", "UNVERIFIED"), HALAL_BADGE["UNVERIFIED"])
        rating = r.get("rating", "N/A")
        stars = "★" * int(rating) + "☆" * (5 - int(rating)) if isinstance(rating, (int, float)) else ""
        website_html = f'<a href="{r["website"]}" target="_blank">Website</a> · ' if r.get("website") else ""
        phone_html = f'<span class="phone">{r["phone"]}</span> · ' if r.get("phone") else ""

        cards_html += f"""
        <div class="card">
            <div class="card-header">
                <div>
                    <h2>{r.get("name", "")}</h2>
                    <p class="cuisine">{r.get("cuisine", "")}</p>
                </div>
                {badge_html}
            </div>
            <p class="address">📍 {r.get("address", "")}</p>
            <p class="rating">{stars} <span>{rating}</span> <span class="review-count">({r.get("review_count", "")} reviews)</span></p>
            <p class="evidence">💬 {r.get("halal_evidence", "No halal information found")}</p>
            <div class="links">
                {phone_html}
                {website_html}
                <a href="{r.get("maps_link", "#")}" target="_blank">View on Maps</a>
            </div>
        </div>
        """

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Halal Finder — {query}</title>
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #f8fafc; color: #1e293b; padding: 2rem; }}
        .container {{ max-width: 800px; margin: 0 auto; }}
        header {{ margin-bottom: 2rem; }}
        header h1 {{ font-size: 1.5rem; font-weight: 700; }}
        header p {{ color: #64748b; font-size: 0.9rem; margin-top: 0.25rem; }}
        .summary {{ background: #e0f2fe; border-left: 4px solid #0284c7; padding: 0.75rem 1rem; border-radius: 4px; margin-bottom: 1.5rem; font-size: 0.95rem; }}
        .card {{ background: white; border-radius: 12px; padding: 1.5rem; margin-bottom: 1rem; box-shadow: 0 1px 3px rgba(0,0,0,0.08); }}
        .card-header {{ display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.75rem; }}
        .card h2 {{ font-size: 1.1rem; font-weight: 600; }}
        .cuisine {{ color: #64748b; font-size: 0.85rem; margin-top: 0.2rem; }}
        .badge {{ font-size: 0.75rem; font-weight: 600; padding: 0.3rem 0.7rem; border-radius: 20px; white-space: nowrap; }}
        .badge.likely {{ background: #dcfce7; color: #15803d; }}
        .badge.possibly {{ background: #fef9c3; color: #a16207; }}
        .badge.unverified {{ background: #f1f5f9; color: #64748b; }}
        .address {{ font-size: 0.9rem; color: #475569; margin-bottom: 0.5rem; }}
        .rating {{ font-size: 0.9rem; margin-bottom: 0.5rem; color: #f59e0b; }}
        .rating span {{ color: #1e293b; }}
        .review-count {{ color: #94a3b8; font-size: 0.85rem; }}
        .evidence {{ font-size: 0.85rem; color: #475569; margin-bottom: 1rem; font-style: italic; }}
        .links {{ font-size: 0.85rem; }}
        .links a {{ color: #0284c7; text-decoration: none; }}
        .links a:hover {{ text-decoration: underline; }}
        .phone {{ color: #475569; }}
        footer {{ text-align: center; color: #94a3b8; font-size: 0.8rem; margin-top: 2rem; }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Halal Finder</h1>
            <p>Query: "{query}" · {timestamp}</p>
        </header>
        <div class="summary">{summary}</div>
        {cards_html}
        <footer>Results sourced from Google Places. Halal status based on available reviews — always verify directly with the restaurant.</footer>
    </div>
</body>
</html>"""

    with open(output_path, "w") as f:
        f.write(html)

    return output_path
