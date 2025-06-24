def get_theme(theme_name="canva_blue"):
    themes = {
        "canva_blue": {
            "primary_color": (52, 152, 219),       # Biru muda
            "text_color": (33, 33, 33),            # Abu gelap
            "header_text_color": (255, 255, 255),  # Putih
            "line_color": (220, 220, 220),         # Abu terang
        },
        "soft_green": {
            "primary_color": (46, 204, 113),       # Hijau segar
            "text_color": (44, 62, 80),
            "header_text_color": (255, 255, 255),
            "line_color": (200, 255, 200),
        },
        "minimal_dark": {
            "primary_color": (52, 73, 94),
            "text_color": (255, 255, 255),
            "header_text_color": (255, 255, 255),
            "line_color": (100, 100, 100),
        },
        "pink_peach": {
            "primary_color": (255, 121, 121),
            "text_color": (80, 0, 0),
            "header_text_color": (255, 255, 255),
            "line_color": (255, 200, 200),
        },
        "professional_gray": {
            "primary_color": (120, 120, 120),
            "text_color": (30, 30, 30),
            "header_text_color": (255, 255, 255),
            "line_color": (180, 180, 180),
        },
    }
    return themes.get(theme_name, themes["canva_blue"])

def get_all_theme_names():
    return [
        "canva_blue",
        "soft_green",
        "minimal_dark",
        "pink_peach",
        "professional_gray"
    ]
