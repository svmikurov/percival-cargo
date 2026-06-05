"""Abstract base classes for domain interfaces."""

from abc import ABC, abstractmethod

from . import model

class AbstractRepository(ABC):
    """Protocol for repository interface."""

    @abstractmethod 
    def add(self, batch: model.Batch):
        raise NotImplementedError
    
    @abstractmethod
    def get(self, reference) -> model.Batch:
        raise NotImplementedError