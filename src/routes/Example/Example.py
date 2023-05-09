import inject
from flask import Blueprint
from ...domains.actions import Example_action

@inject.autoparams()
def Example(Example_action: Example_action) -> Blueprint:
    Example = Blueprint('Example', __name__)

    @Example.record_once
    def example_record_once(state):
        Example_action.execute()
    
    return Example


