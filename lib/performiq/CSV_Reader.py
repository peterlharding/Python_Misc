
import csv
import sys

#=========================================================================

class CSV_Reader:

    #---------------------------------------------------------------------

    @classmethod
    def read(cls, fname, skip=0, obj=None, limit=0):
        csv_data  = []

        try:
            f_in      = open(fname, "rb")
        except IOError, msg:
            sys.stderr.write(cls.log_file + ': cannot open: ' + `msg` + '\n')
            sys.exit(1)

        reader = csv.reader(f_in)

        cnt   = 0

        for row in reader:
           cnt += 1

           if skip > 0:
               skip -= 1
               continue   # Skip headings

           if obj:
               data = obj(row)
           else:
               data = row

           # print data

           csv_data.append(data)

           if limit and (cnt < limit): continue

        f_in.close()  # Explicitly close the file *NOW*

        no_lines  = len(csv_data)

        print "Read %d data items..." % no_lines
        print "                 -> Total data  %d" % cnt

        return csv_data

    #---------------------------------------------------------------------

#=========================================================================

