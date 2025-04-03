from sushi_layouts import MergeRunDataApp
from sushi_layouts import FastqcApp 
from sushi_layouts import FastqScreenApp 


DIRECTORY = {
    'test': {
        '488': {
            'callback': MergeRunDataApp.callback,
            'layout': MergeRunDataApp.layout,
            'sidebar': MergeRunDataApp.sidebar,
            'title': MergeRunDataApp.title
        },
        '434': {
            'callback': FastqcApp.callback,
            'layout': FastqcApp.layout,
            'sidebar': FastqcApp.sidebar,
            'title': FastqcApp.title
        },
        '489': {
            'callback': FastqScreenApp.callback,
            'layout': FastqScreenApp.layout,
            'sidebar': FastqScreenApp.sidebar,
            'title': FastqScreenApp.title
        }
    }
}