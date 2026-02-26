from pydantic import BaseModel
from typing import List, Generic, TypeVar, Optional

T = TypeVar('T') 


class PaginatedResponse(BaseModel, Generic[T]):
    '''
        Generic paginated response model for API endpoints that return lists of items with pagination.
    '''

    items: List[T]
    page: int
    total_items: int
    total_pages: Optional[int] = None
    skip: int
    limit: int

    @property
    def has_next(self) -> bool:
        return (self.skip + self.limit) < self.total_items

    @property
    def has_previous(self) -> bool:
        return self.skip > 0