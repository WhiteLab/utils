#!/usr/bin/env python

import sys
import logging
import argparse

import pysam

def unalign(ifs,ofs,tags=None):
  '''
  Convert aligned bam IFS to unaligned bam OFS.
  '''

  # Generate a new read that we'll use as the base.
  unaligned = pysam.AlignedRead()

  # Prepare the tag set to keep.
  tags = tags and set(tags) or set([])

  for read in ifs:
    # Copy the query name of the read.
    unaligned.qname = read.qname

    # Copy the sequence and the quality string.
    unaligned.seq   = read.seq
    unaligned.qual  = read.qual

    # Copy reference to paired sequence, if exists.
    unaligned.rnext = read.rnext

    # Set target reference and position to unknown.
    unaligned.tid = -1
    unaligned.pos = -1
    unaligned.rnext = -1
    unaligned.pnext = -1

    # Copy any applicable flags.
    if read.is_paired: unaligned.flag = 0x1   | unaligned.flag
    if read.is_read1:  unaligned.flag = 0x40  | unaligned.flag
    else:              unaligned.flag = 0x80  | unaligned.flag

    # Copy tags specified by the user.
    unaligned.tags = []
    for tag in read.tags:
      if tag[0] in tags: unaligned.tags += [tag]

    # Write the new unaligned copy.
    ofs.write(unaligned)

def main(args):

  # Set up basic logging.
  logging.basicConfig(
    level = args.loglevel,
    format = '%(asctime)s %(name)-6s %(levelname)-4s %(message)s',
  )

  # Unalign the bam file.
  logging.info('Unaligning %s to %s' % (args.bam,args.out))

  ifs = pysam.Samfile(args.bam)

  header = ifs.header
  if 'PG' in header: del header['PG']

  ofs = pysam.Samfile(args.out,'wb',header = header)
  unalign(ifs,ofs,args.tags)
  ofs.close()

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Signpost Daemon')

  # Flag arguments.
  parser.add_argument('-d','--debug',dest='loglevel',action='store_const',
                      const=logging.DEBUG,default=logging.INFO,
                      help='Set logging level to DEBUG.')
  parser.add_argument('-o','--out',dest='out',default=sys.stdout,
                      help='File for output. [STDOUT]')
  parser.add_argument('-t','--tag',dest='tags',action='append',default=[],
                      help='Tags to keep.')

  # Positional arguments.
  parser.add_argument('bam',help='Bam file to unalign.')

  main(parser.parse_args())
