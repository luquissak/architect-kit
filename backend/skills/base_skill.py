from abc import ABC, abstractmethod

class BaseSkill(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    async def run(self, context: dict) -> dict:
        """
        Executa a lógica da skill.
        context: Dicionário contendo dados como 'code', 'provider', etc.
        Retorna um dicionário com os resultados da skill.
        """
        pass
