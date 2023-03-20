from crud.base import CRUDBase
from models import Action
from schemas import ActionCreate, ActionUpdate


class CRUDAction(CRUDBase[Action, ActionCreate, ActionUpdate]):
    pass


action = CRUDAction(Action)
