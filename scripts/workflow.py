from gwf import Workflow, AnonymousTarget

gwf = Workflow()

"""
Workflow for LDA analysis of ASCAT data
"""

sample = '/home/janneae/TCGA/DerivedData/PanCancer/TCGA_ASCAT_RAW_PVL/ASCAT_TCGA/TCGA*.segments.raw.txt' 
centromereinfo = '../data/chrominfo.snp6.txt'
ascat = '../data/filteredAscat.txt'
gc = '../data/gc.content.txt'
updatedascat = '../data/filteredAscatRaw.txt'

nfeat = 10
featurefile = f'../steps/discFeatures_{nfeat}.txt'
# ncomponents = 8
start = 2
ntopics = 15


def update_ascat(samplefiles, ascat):
    updatedascat = '../data/filteredAscatRaw.txt'
    inputs = [ascat]
    outputs = [updatedascat]
    options = {
        'memory': '8g',
        'walltime': '4-00:00:00'
    }
    spec = f'''
    
    python update_ascat.py {samplefiles} {ascat} {updatedascat}

    '''

    return AnonymousTarget(inputs=inputs, outputs=outputs, options=options, spec=spec)

def create_feature_file(ascat, centromere, gc, output): 
    inputs = [centromere, ascat, gc]
    outputs = [output]
    options = {
        'memory': '5g',
        'walltime': '10:00:00'
    }
    
    spec = f'''
    
    python create_feature_file.py {ascat} {centromere} {gc} {output}
    
    '''

    return AnonymousTarget(inputs=inputs, outputs=outputs, options=options, spec=spec)

def lda_analysis(features, ncomponents, nfeat):
    outputname = f'../steps/lda/ldares_{nfeat}_{ncomponents}.txt'

    inputs = [features]
    outputs = [outputname]
    options = {
        'memory': '10g',
        'walltime': '3-00:00:00'
    }

    spec = f'''
    
    python lda_fit.py {features} {ncomponents} {outputname}

    '''

    return AnonymousTarget(inputs=inputs, outputs=outputs, options=options, spec=spec)

def nmf_analysis(features, ncomponents, nfeat):
    outputname = f'../steps/nmf/nmfres_{nfeat}_{ncomponents}.txt'

    inputs = [features]
    outputs = [outputname]
    options = {
        'memory': '10g',
        'walltime': '3-00:00:00'
    }

    spec = f'''
    
    python nmf_fit.py {features} {ncomponents} {outputname}

    '''

    return AnonymousTarget(inputs=inputs, outputs=outputs, options=options, spec=spec)

def gensim(features, ntopics, nfeat):
    outputname = f'../figures/optimalalpha_{nfeat}.pdf'

    inputs = [features]
    outputs = [outputname]
    options = {
        'memory': '10g',
        'walltime': '7-00:00:00'
    }

    spec = f'''
    
    python gensimLDA.py {features} {ntopics} {outputname}

    '''

    return AnonymousTarget(inputs=inputs, outputs=outputs, options=options, spec=spec)

def gensimLDA(features, ntopics, nfeat):
    outputname = f'../steps/gensim/lda_t{ntopics}_f{nfeat}.model'

    inputs = [features]
    outputs = [outputname]
    options = {
        'memory': '10g',
        'walltime': '3-00:00:00'
    }

    spec = f'''
    
    python gensimLDA2.py {features} {ntopics} {outputname}

    '''

    return AnonymousTarget(inputs=inputs, outputs=outputs, options=options, spec=spec)

def gensimHDP(features, nfeat):
    outputname = f'../steps/gensim/hdp_f{nfeat}.model'

    inputs = [features]
    outputs = [outputname]
    options = {
        'memory': '10g',
        'walltime': '1-00:00:00'
    }

    spec = f'''
    
    python gensimHDP.py {features} {outputname}

    '''

    return AnonymousTarget(inputs=inputs, outputs=outputs, options=options, spec=spec)

gwf.target_from_template(
    name='UpdateAscat',
    template=update_ascat(
        samplefiles=sample,
        ascat=ascat
    )
)

gwf.target_from_template(
    name='CreateFeatures',
    template=create_feature_file(
        ascat = updatedascat,
        centromere = centromereinfo,
        gc = gc,
        output = featurefile
    )
)

for i in range(start, ntopics + 1):

    gwf.target_from_template(
        name=f'LDA_{i}',
        template=lda_analysis(
            features=featurefile,
            ncomponents=i,
            nfeat=nfeat
        )
    )

    gwf.target_from_template(
        name=f'NMF_{i}',
        template=nmf_analysis(
            features=featurefile,
            ncomponents=i,
            nfeat=nfeat
        )
    )

    gwf.target_from_template(
        name=f'gensimLDA2_t{i}_f{nfeat}',
        template=gensimLDA(
            features=featurefile,
            ntopics=i,
            nfeat=nfeat
        )
    )

gwf.target_from_template(
    name=f'gensimLDA_t{ntopics}_f{nfeat}',
    template=gensim(
        features=featurefile,
        ntopics=4,
        nfeat=nfeat
    )
)

gwf.target_from_template(
    name=f'gensimHDP_f{nfeat}',
    template=gensimHDP(
        features=featurefile,
        nfeat=nfeat
    )
)