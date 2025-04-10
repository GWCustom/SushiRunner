from sushi_layouts import MergeRunDataApp
from sushi_layouts import FastqcApp 
from sushi_layouts import FastqScreenApp 
from sushi_layouts import EmptyApp
from sushi_layouts import EdgeR

UNKNOWN_APP = {
    'layout': EmptyApp.layout,
    'sidebar': EmptyApp.sidebar,
    'alerts': EmptyApp.alerts
}

DIRECTORY = {
    'default': UNKNOWN_APP,
    'test': {
        '373': {
            'layout': MergeRunDataApp.layout,
            'sidebar': MergeRunDataApp.sidebar
        },
        '434': {
            'layout': FastqcApp.layout,
            'sidebar': FastqcApp.sidebar,
            'alerts': FastqcApp.alerts
        },
        '111': { #377
            'layout': FastqScreenApp.layout,
            'sidebar': FastqScreenApp.sidebar
        },
        '377': {  # EdgeR_id
            'layout': EdgeR.layout,
            'sidebar': EdgeR.sidebar
        }
    }
}

