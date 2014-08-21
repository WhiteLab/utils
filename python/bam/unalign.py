#!/usr/bin/env python

import sys
import logging
import argparse

import pysam

def unalign(ifs,ofs):
  '''
  Convert aligned bam IFS to unaligned bam OFS.
  '''

  for read in ifs:
    # TODO delete alignment fields
    ofs.write(read)

def main(args):

  # Set up basic logging.
  logging.basicConfig(
    level = args.loglevel,
    format = '%(asctime)s %(name)-6s %(levelname)-4s %(message)s',
  )

  # Unalign the bam file.
  logging.info('Unaligning %s to %s' % (args.bam,args.out))
  ifs = pysam.Samfile(args.bam)
  ofs = pysam.Samfile(args.out,'wb',header = ifs.header)
  unalign(ifs,ofs)

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Signpost Daemon')

  # Flag arguments.
  parser.add_argument('-d','--debug',dest='loglevel',action='store_const',
                      const=logging.DEBUG,default=logging.INFO,
                      help='Set logging level to DEBUG.')
  parser.add_argument('-o','--out',dest='out',default=sys.stdout,
                      help='File for output. [STDOUT]')

  # Positional arguments.
  parser.add_argument('bam',help='Bam file to unalign.')

  main(parser.parse_args())
