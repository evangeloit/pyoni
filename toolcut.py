import onifile as oni
import struct

def copy(args,a,b):
    r = oni.Reader(a)
    print "firstheader",r.h0
    w = oni.Writer(b,r.h0)
    while True:
        h = r.next()
        if h is None:
            break
        elif h["rt"] == oni.RECORD_SEEK_TABLE:
        	w.emitseek(h["nid"])
        elif h["rt"] == oni.RECORD_NEW_DATA:
            hh = oni.parsedatahead(a,h)            
            print dict(nid=h["nid"],ps=h["ps"],fs=h["fs"],frameid=hh["frameid"],timestamp=hh["timestamp"])
            w.addframe(h["nid"],hh["frameid"],hh["timestamp"],a.read(h["ps"]))
        else:
        	w.copyblock(h,a)

    w.finalize()

"""
def strip(args,action,a,b):
    # scan all and keep pre and last
    r = oni.Reader(a)
    w = oni.Writer(b)

    if action == "stripcolor":
        id = 1
    else:
        id = 2
    while True:
            h = oni.readrechead(a)
            if h is None:
                    break
            prelast = last
            last = h
            if h["nid"] == id:                
                if h["rt"] == oni.RECORD_SEEK_TABLE: # skip
                    break
                    #st = loadseek(a,h)
                    print "seek loaded and skipped, needs update"
                    a.seek(h["nextheader"],0) #h["fs"]-HEADER_SIZE+h["ps"],1)
                    continue
                oni.writehead(b,h)
                d = a.read(h["ps"]+h["fs"]-oni.HEADER_SIZE)
                b.write(d)
                # TODO recompute seek table
                if h["rt"] == oni.RECORD_NEW_DATA:
                    pd = oni.parsedatahead(a,h)
                    print pd["frameid"],h["ps"]
            if h["rt"] == oni.RECORD_END:
                oni.writeend(b)
                continue
            a.seek(h["nextheader"],0)
    needclose = True	

def cut(args,action,a,b):
    while True:
            h = oni.readrechead(a)
            if h is None:
                    break
            if h["rt"] == oni.RECORD_NEW_DATA:
                t = oni.parsedatahead(a,h)["timestamp"]
                q = stats[h["nid"]]
                good = False
                if target[0] == "frame":
                    good = q.oldframes >= target[1][0] and q.oldframes <= target[1][1]
                else:
                    good = t >= target[1][0] and t <= target[1][1]
                if good:
                    # retime
                    if q.newframes == 0:
                        q.oldbasetime = t
                    t2 = t-q.oldbasetime

                    #q.newtime(t2)
                    #q.addframe() 
                    #q.copyblock()
                    #self.framesoffset.append((b.tell(),q.newframe))

                q.oldframes += 1
            elif h["rt"] == oni.RECORD_NODE_ADDED:
                hh = oni.parseadded(a,h)
                q = stats[h["nid"]]
                self.headerblock = h
                self.headerdata = hh
                # append block
            elif h["rt"] == oni.RECORD_SEEK_TABLE:
                # append new seektable
                pass
            else:
                # append block
                pass

            # next record
            a.seek(h["nextheader"]) #h["fs"]-HEADER_SIZE+h["ps"]+pt,0)      
    needclose = True

def skip(args,action,a):
    while True:
            h = oni.readrechead(a)
            if h is None:
                    break
            prelast = last
            last = h
            if h["nid"] > mid:
                    mid = h["nid"]
            if h["rt"] == oni.RECORD_SEEK_TABLE:
                # TODO gen seek
                pass
            elif h["rt"] == oni.RECORD_NODE_ADDED:
                hh = oni.parseadded(a,h)
                stats[h["nid"]].assignheader(h,hh) 
            elif h["rt"] == oni.RECORD_NEW_DATA:
                hh = oni.parsedatahead(a,h)
                q = stats[h["nid"]]
                if (q.oldframes % args.skipframes) == 0:
                    q.addframe(h,hh,b)
                    oni.copyblock(a,h,b,frame=q.newframes-1,timestamp=q.newtimestamp)
                q.oldframes += 1
            a.seek(h["nextheader"])
    needclose = True


def dupframes(args,a):
    while True:
            h = oni.readrechead(a)
            if h is None:
                    break
            prelast = last
            last = h
            if h["nid"] > mid:
                    mid = h["nid"]
            if h["rt"] == oni.RECORD_SEEK_TABLE:
                # TODO gen seek
                pass
            elif h["rt"] == oni.RECORD_NEW_DATA:
                hh = oni.parsedatahead(a,h)
                q = stats[h["nid"]]
                for i in range(0,args.dupframes):
                    q.addframe(h,hh,b)
                    oni.copyblock(a,h,b,frame=q.newframe-1,timestamp=q.timestamp)
            a.seek(h["nextheader"])
"""