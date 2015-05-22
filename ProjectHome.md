I've kept all sent&recv sms on the same memory card over many years, until eventually the old n73 took 30+seconds to open a message!

So I took a cp -rp of Private/1000484b/Mail2/ and wrote this perl script to walk the datafiles.

Hope its of some use to someone

TODO
  * better message parsing
  * telephone contact lookup hook
  * as\_xml output
  * to/from flag
  * VCF and MMS handling

CAVEATS
  * the date/time of the SMS is determined from the filestamp mtime.
  * requires no additional perl modules but is currently set to output as html table.