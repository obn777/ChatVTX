import logging
from typing import Dict, Any, List

from core.behavior.modes.analytic import AnalyticMode
from core.behavior.modes.opponent import OpponentMode
from core.behavior.modes.strategic import StrategicMode
from core.behavior.modes.engineering import EngineeringMode
from core.behavior.intent_router import IntentRouter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ModeManager")

class ModeManager:
    """
    Централизованный диспетчер когнитивных режимов.
    Адаптирован для автономной работы на Nitro.
    """

    def __init__(self):
        self._router = IntentRouter()

        self._modes: Dict[str, Any] = {
            "analysis": AnalyticMode,
            "engineering": EngineeringMode,
            "debate": OpponentMode,
            "strategic": StrategicMode,
            "info": AnalyticMode,
            "clarification": AnalyticMode,
        }

        self._current_mode_name: str = "analysis"
        self._current_mode = self._modes[self._current_mode_name]()

        logger.info(
            f"[ModeManager] Система готова. Базовый режим: '{self._current_mode_name}'"
        )

    def set_mode(self, mode_name: str) -> bool:
        """Явная смена режима."""
        if mode_name not in self._modes:
            logger.warning(f"[ModeManager] Режим '{mode_name}' отсутствует.")
            return False

        if self._current_mode_name == mode_name:
            return True

        self._current_mode_name = mode_name
        self._current_mode = self._modes[mode_name]()

        logger.info(f"[ModeManager] Активирован режим '{mode_name.upper()}'")
        return True

    def resolve_mode(self, query: str) -> bool:
        """Определяет intent запроса и выбирает режим."""
        intent = self._router.detect(query)

        # Жёсткое сопоставление intent → режим
        mapping = {
            "engineering": "engineering",
            "debate": "debate",
            "analysis": "analysis",
            "info": "info",
            "clarification": "clarification",
            "strategic": "strategic"
        }

        target_mode = mapping.get(intent, "analysis")
        return self.set_mode(target_mode)

    def auto_detect_mode(self, text: str):
        """
        Алиас для resolve_mode. 
        Необходим для совместимости с LogicProcessor и app.py (строка 176).
        """
        return self.resolve_mode(text)

    def get_mode(self):
        """Возвращает объект активного режима."""
        return self._current_mode

    def get_mode_name(self) -> str:
        """Возвращает строковое имя режима."""
        return self._current_mode_name

    def list_modes(self) -> List[str]:
        """Список доступных режимов."""
        return list(self._modes.keys())
