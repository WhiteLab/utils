import pysam

def filter_reads(sam,filters=list()):
  '''
  Returns a generator of pysam reads which have passed all filters.
  Filters must take a pysam read and return:
    False - read is not to be filtered (keep it)
    True  - read is to be filtered (discard it)
  '''
  return (r for r in pysam.Samfile(sam) if not filter(lambda f: f(r), filters))
