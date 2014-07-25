#-*- coding: utf-8 -*-
##Script to reformat nyt annotated corpus
import re, os, codecs, sys, glob


###################
def sentence_segmenter(paragr):
    MIN_SENTLENGTH = 0
    MAX_SENTLENGTH = 512

    terpat = re.compile('[\*\.\?!]\s+[A-Z\"]')

    # source: LbjNerTagger1.11.release/Data/KnownLists/known_title.lst from
    # University of Illinois with editing
    ABBREV_LIST = ['J.P.', 'U.S.','mrs.', 'ms.', 'mr.', 'dr.', 'gov.', 'sr.', 'rev.', 'r.n.',
                   'pres.', 'treas.', 'sect.', 'maj.', 'ph.d.', 'ed. psy.',
                   'proc.', 'fr.', 'asst.', 'p.f.c.', 'prof.', 'admr.',
                   'engr.', 'mgr.', 'supt.', 'admin.', 'assoc.', 'voc.',
                   'hon.', 'm.d.', 'dpty.',  'sec.', 'capt.', 'c.e.o.',
                   'c.f.o.', 'c.i.o.', 'c.o.o.', 'c.p.a.', 'c.n.a.', 'acct.',
                   'llc.', 'inc.', 'dir.', 'esq.', 'lt.', 'd.d.', 'ed.',
                   'revd.', 'psy.d.', 'v.p.',  'senr.', 'gen.', 'prov.',
                   'cmdr.', 'sgt.', 'sen.', 'col.', 'lieut.', 'cpl.', 'pfc.',
                   'k.p.h.', 'cent.', 'deg.', 'doz.', 'Fahr.', 'Cel.', 'F.',
                   'C.', 'K.', 'ft.', 'fur.',  'gal.', 'gr.', 'in.', 'kg.',
                   'km.', 'kw.', 'l.', 'lat.', 'lb.', 'lb per sq in.', 'long.',
                   'mg.', 'mm.,, m.p.g.', 'm.p.h.', 'cc.', 'qr.', 'qt.', 'sq.',
                   't.', 'vol.',  'w.', 'wt.']

    sentlist = []
    # controls skipping over non-terminal conditions
    searchstart = 0
    terloc = terpat.search(paragr)
    while terloc:
        isok = True
        if paragr[terloc.start()] == '.':
            if (paragr[terloc.start() - 1].isupper() and
                    paragr[terloc.start() - 2] == ' '):
                        isok = False      # single initials
            else:
                # check abbreviations
                loc = paragr.rfind(' ', 0, terloc.start() - 1)
                if loc > 0:
                    if paragr[loc + 1:terloc.start() + 1].lower() in ABBREV_LIST:
                        isok = True
        if paragr[:terloc.start()].count('(') != paragr[:terloc.start()].count(')'):
            isok = False
        if paragr[:terloc.start()].count('"') % 2 != 0:
            isok = False
        if isok:
            if (len(paragr[:terloc.start()]) > MIN_SENTLENGTH and
                    len(paragr[:terloc.start()]) < MAX_SENTLENGTH):
                sentlist.append(paragr[:terloc.start() + 2])
            paragr = paragr[terloc.end() - 1:]
            searchstart = 0
        else:
            searchstart = terloc.start() + 2

        terloc = terpat.search(paragr, searchstart)

    if (len(paragr) > MIN_SENTLENGTH and len(paragr) < MAX_SENTLENGTH):
        sentlist.append(paragr)

    return sentlist

###################

year = '2002'
index = open('/Users/muhammedyidris/git/bootstrapping_classes/nyt/nyt_index.txt', 'a')

months = range(1, 13)
days = range(0, 32)

for m in months:
  out = open('/Users/muhammedyidris/git/bootstrapping_classes/nyt/formatted_nyt/'+year+'-'+str(m).zfill(2)+'.txt', 'w+')

  for d in days:
    path = '/Volumes/MYI_PASS/data/nyt_corpus/data/'+year+'/'+str(m).zfill(2)+'/'+str(d).zfill(2)
    filelist = glob.glob( os.path.join(path, '*.xml') )
    for fullfile in filelist:
      filename = fullfile.split('data/')[-1]
      print 'processing: '+filename
      f = open(fullfile).read()
      head, sep, tail = f.partition('<title>')
      head, sep, tail = tail.partition('</title>')
      print >> out, head
      print >> index, filename+'\t'+head

      head, sep, tail = tail.partition('<block class="full_text">')
      head, sep, tail = tail.partition('</block>')
      foo = head.split('</p>')
      del foo[-1]

      for i in foo:
        if len(i)<100:
          print >> out, i.strip().replace('<p>', '')
        else:
          foos = sentence_segmenter(i.strip())
          for j in foos:
            print >> out, j.strip().replace('<p>', '')

      print >> out, '\n'
  out.close()

index.close()