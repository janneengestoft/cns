import argparse
import feature_func as features

parser = argparse.ArgumentParser(description='Create feature files')
parser.add_argument('ascat', help='File containing ploidy information')
parser.add_argument('centroinfo', help='File containing centromere information')
parser.add_argument('gccontent', help='File containing GC content')
parser.add_argument('outputfile', help='Path and name of the output')

args = parser.parse_args()

def fullDF(ascat, centroinfo, gccontent, output):
    feature_df = features.makefeatfile(ascat, centroinfo, gccontent)

    feature_df = features.discretize(feature_df)
    feature_df.to_csv(output, header=True, index=False, sep='\t')

    return feature_df

fullDF(args.ascat, args.centroinfo, args.gccontent, args.outputfile)

 
# centromereinfo = '/home/janneae/cns/data/chrominfo.snp6.txt'
# ascat = '/home/janneae/cns/data/filteredAscatRaw.txt'
# gc = '/home/janneae/cns/data/gc.content.txt'
# output = '/home/janneae/cns/steps/test.txt'

# full = fullDF(ascat, centromereinfo, gc, output)

