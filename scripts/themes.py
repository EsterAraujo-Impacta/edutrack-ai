"""scripts/themes.py – Design Tokens semânticos e paletas temáticas do EduTrack AI."""

from dataclasses import dataclass
import urllib.parse


def _emoji_bg_pattern(emojis: list[str], opacity: float = 0.22) -> str:
  """Gera um padrão de fundo repetitivo em SVG com emojis visíveis e suaves."""
  e1 = emojis[0]
  e2 = emojis[1] if len(emojis) > 1 else emojis[0]
  e3 = emojis[2] if len(emojis) > 2 else e1
  svg = (
      f'<svg xmlns="http://www.w3.org/2000/svg" width="150" height="150">'
      f'<text x="15" y="42" font-size="26" opacity="{opacity}">{e1}</text>'
      f'<text x="85" y="95" font-size="24" opacity="{opacity}">{e2}</text>'
      f'<text x="30" y="138" font-size="22" opacity="{opacity}">{e3}</text>'
      f"</svg>"
  )
  encoded = urllib.parse.quote(svg)
  return f'url("data:image/svg+xml,{encoded}")'


@dataclass(frozen=True)
class ThemeTokens:
  """Define os Design Tokens semânticos de um tema."""

  key: str
  label: str
  is_dark: bool
  # Tokens de cor semânticos
  bg_primary: str
  surface: str
  sidebar_bg: str
  text_primary: str
  text_secondary: str
  border_color: str
  accent_color: str
  accent_hover: str
  accent_text: str
  bg_pattern: str = "none"


THEMES: dict[str, ThemeTokens] = {
    "claro": ThemeTokens(
        key="claro",
        label="☀️ Claro (Padrão)",
        is_dark=False,
        bg_primary="#F8FAFC",
        surface="#FFFFFF",
        sidebar_bg="#F1F5F9",
        text_primary="#0F172A",
        text_secondary="#475569",
        border_color="#CBD5E1",
        accent_color="#2563EB",
        accent_hover="#1D4ED8",
        accent_text="#FFFFFF",
    ),
    "escuro": ThemeTokens(
        key="escuro",
        label="🌙 Escuro (Noturno)",
        is_dark=True,
        bg_primary="#121212",
        surface="#1E1E1E",
        sidebar_bg="#18181B",
        text_primary="#F8FAFC",
        text_secondary="#CBD5E1",
        border_color="#334155",
        accent_color="#60A5FA",
        accent_hover="#3B82F6",
        accent_text="#0F172A",
    ),
    "alto_contraste": ThemeTokens(
        key="alto_contraste",
        label="👁️ Alto Contraste",
        is_dark=True,
        bg_primary="#000000",
        surface="#0D0D0D",
        sidebar_bg="#000000",
        text_primary="#FFFFFF",
        text_secondary="#FFE600",
        border_color="#FFFFFF",
        accent_color="#FFE600",
        accent_hover="#FFD000",
        accent_text="#000000",
    ),
    "musica": ThemeTokens(
        key="musica",
        label="🎵 Música",
        is_dark=False,
        bg_primary="#F5F3FF",     # Lavanda / Roxo bem clarinho
        surface="#FFFFFF",
        sidebar_bg="#EDE9FE",     # Lilás suave
        text_primary="#2E1065",   # Roxo escuro bem legível
        text_secondary="#5B21B6",
        border_color="#C4B5FD",
        accent_color="#7C3AED",   # Roxo vibrante
        accent_hover="#6D28D9",
        accent_text="#FFFFFF",
        bg_pattern=_emoji_bg_pattern(["🎵", "🎶", "🎧"], opacity=0.22),
    ),
    "gatinho": ThemeTokens(
        key="gatinho",
        label="🐱 Gatinho",
        is_dark=False,
        bg_primary="#FFFBEB",     # Amarelo bem clarinho
        surface="#FFFFFF",
        sidebar_bg="#FEF3C7",     # Amarelo pastel suave
        text_primary="#451A03",
        text_secondary="#78350F",
        border_color="#FCD34D",
        accent_color="#D97706",
        accent_hover="#B45309",
        accent_text="#FFFFFF",
        bg_pattern=_emoji_bg_pattern(["🐱", "🐾", "🧶"], opacity=0.22),
    ),
    "cachorro": ThemeTokens(
        key="cachorro",
        label="🐶 Cachorro",
        is_dark=False,
        bg_primary="#FBF7F2",
        surface="#FFFFFF",
        sidebar_bg="#F3E8D8",
        text_primary="#2C1E16",
        text_secondary="#5C4333",
        border_color="#D6BEA2",
        accent_color="#B45309",
        accent_hover="#92400E",
        accent_text="#FFFFFF",
        bg_pattern=_emoji_bg_pattern(["🐶", "🦴", "🐾"], opacity=0.20),
    ),
    "flores": ThemeTokens(
        key="flores",
        label="🌸 Flores",
        is_dark=False,
        bg_primary="#FFF5F8",     # Rosa bem clarinho
        surface="#FFFFFF",
        sidebar_bg="#FCE7F0",     # Rosa pastel suave
        text_primary="#4A102A",
        text_secondary="#831843",
        border_color="#F9A8D4",
        accent_color="#DB2777",
        accent_hover="#BE185D",
        accent_text="#FFFFFF",
        bg_pattern=_emoji_bg_pattern(["🌸", "🌷", "🌺"], opacity=0.22),
    ),
    "carros": ThemeTokens(
        key="carros",
        label="🏎️ Carros",
        is_dark=True,
        bg_primary="#141619",
        surface="#1F2328",
        sidebar_bg="#181B20",
        text_primary="#F9FAFB",
        text_secondary="#D1D5DB",
        border_color="#4B5563",
        accent_color="#EF4444",
        accent_hover="#DC2626",
        accent_text="#FFFFFF",
        bg_pattern=_emoji_bg_pattern(["🏎️", "🏁", "⚡"], opacity=0.20),
    ),
    "foguetes": ThemeTokens(
        key="foguetes",
        label="🚀 Foguetes",
        is_dark=True,
        bg_primary="#0B1021",
        surface="#131B36",
        sidebar_bg="#0E152B",
        text_primary="#F1F5F9",
        text_secondary="#CBD5E1",
        border_color="#334780",
        accent_color="#38BDF8",
        accent_hover="#0284C7",
        accent_text="#0B1021",
        bg_pattern=_emoji_bg_pattern(["🚀", "🪐", "⭐"], opacity=0.22),
    ),
}

DEFAULT_THEME_KEY = "claro"