from sushi_layouts import (
    MergeRunDataApp,
    FastqcApp,
    FastqScreenApp,
    EmptyApp,
    EdgeR,
    DESeq2,
    STAR,
    Bowtie2,
    CountQCApp,
    FeatureCounts,
    CellRanger,
    Fastqc10xApp,
    FastqScreen10xApp
)


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
        '377': {
            'layout': EdgeR.layout,
            'sidebar': EdgeR.sidebar,
            'alerts': EdgeR.alerts
        },
        '333': {
            'layout': DESeq2.layout,
            'sidebar': DESeq2.sidebar,
            'alerts': DESeq2.alerts
        },
        '444': {
            'layout': STAR.layout,
            'sidebar': STAR.sidebar,
            'alerts': STAR.alerts
        },
        '555': {
            'layout': Bowtie2.layout,
            'sidebar': Bowtie2.sidebar,
            'alerts': Bowtie2.alerts
        },
        '666': {
            'layout': CountQCApp.layout,
            'sidebar': CountQCApp.sidebar,
            'alerts': CountQCApp.alerts,
        },
        '777': {
            'layout': FeatureCounts.layout,
            'sidebar': FeatureCounts.sidebar,
            'alerts': FeatureCounts.alerts
        },
        '888': {
            'layout': CellRanger.layout,
            'sidebar': CellRanger.sidebar,
            'alerts': CellRanger.alerts
        },
        '111': {
            'layout': Fastqc10xApp.layout,
            'sidebar': Fastqc10xApp.sidebar,
            'alerts': Fastqc10xApp.alerts
        },
        '999': {
            'layout': FastqScreen10xApp.layout,
            'sidebar': FastqScreen10xApp.sidebar,
            'alerts': FastqScreen10xApp.alerts
        },
    } 
}