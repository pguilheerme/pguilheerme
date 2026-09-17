from pathlib import Path
import os
import html

OUTPUT = Path("info-card.svg")
STATIC = os.getenv("STATIC") == "1"

WIDTH = 720
HEIGHT = 290

rows = [
    (
        "Now",
        ["Technology and Innovation Supervisor"],
        95,
    ),
    (
        "Prev",
        ["StageTree • Software Developer"],
        135,
    ),
    (
        "Stack",
        [
            "React • Next.js • React Native • Node.js",
            "TypeScript • NestJS • PostgreSQL",
        ],
        175,
    ),
    (
        "Highlights",
        ["SIMOV • SISAT • Mobile • Data & BI"],
        235,
    ),
]

ACCENT = "#7aa2f7"
TEXT = "#c0caf5"
MUTED = "#565f89"
BACKGROUND = "#1a1b26"
BORDER = "#292e42"


def escape(value: str) -> str:
    return html.escape(value)


def make_row(
    index: int,
    key: str,
    values: list[str],
    y: int,
) -> str:
    if STATIC:
        animation = ""
        transform = ""
        opacity = "1"
    else:
        delay = 0.15 + (index * 0.12)

        animation = f"""
        <animate
            attributeName="opacity"
            from="0"
            to="1"
            dur="0.35s"
            begin="{delay}s"
            fill="freeze"
        />

        <animateTransform
            attributeName="transform"
            type="translate"
            from="12 0"
            to="0 0"
            dur="0.35s"
            begin="{delay}s"
            fill="freeze"
        />
        """

        transform = 'transform="translate(12 0)"'
        opacity = "0"

    value_lines = ""

    for line_index, line in enumerate(values):
        dy = "0" if line_index == 0 else "20"

        value_lines += f"""
            <tspan
                x="150"
                dy="{dy}"
            >{escape(line)}</tspan>
        """

    return f"""
    <g opacity="{opacity}" {transform}>
        <text
            x="34"
            y="{y}"
            class="key"
        >{escape(key)}</text>

        <text
            x="150"
            y="{y}"
            class="value"
        >
            {value_lines}
        </text>

        {animation}
    </g>
    """


rows_svg = "\n".join(
    make_row(index, key, values, y)
    for index, (key, values, y) in enumerate(rows)
)

svg = f"""<svg
    xmlns="http://www.w3.org/2000/svg"
    width="{WIDTH}"
    height="{HEIGHT}"
    viewBox="0 0 {WIDTH} {HEIGHT}"
>

<style>
    .title {{
        font-family: "Courier New", monospace;
        font-size: 17px;
        font-weight: bold;
        fill: {TEXT};
    }}

    .prompt {{
        font-family: "Courier New", monospace;
        font-size: 14px;
        fill: {MUTED};
    }}

    .key {{
        font-family: "Courier New", monospace;
        font-size: 14px;
        font-weight: bold;
        fill: {ACCENT};
    }}

    .value {{
        font-family: "Courier New", monospace;
        font-size: 14px;
        fill: {TEXT};
    }}
</style>

<!-- Card -->
<rect
    x="1"
    y="1"
    width="{WIDTH - 2}"
    height="{HEIGHT - 2}"
    rx="12"
    fill="{BACKGROUND}"
    stroke="{BORDER}"
/>

<!-- Top bar -->
<circle
    cx="22"
    cy="21"
    r="5"
    fill="#f7768e"
/>

<circle
    cx="39"
    cy="21"
    r="5"
    fill="#e0af68"
/>

<circle
    cx="56"
    cy="21"
    r="5"
    fill="#9ece6a"
/>

<text
    x="82"
    y="26"
    class="title"
>
    pguilheerme@github
</text>

<line
    x1="0"
    y1="42"
    x2="{WIDTH}"
    y2="42"
    stroke="{BORDER}"
/>

<!-- Command -->
<text
    x="34"
    y="69"
    class="prompt"
>
    $ neofetch --about
</text>

{rows_svg}

</svg>
"""

OUTPUT.write_text(svg, encoding="utf-8")

print(f"✓ {OUTPUT} criado com sucesso")