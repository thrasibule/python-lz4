from lz4f import (createCompressionContext, compressBound,
                  compressBegin, compressUpdate, compressEnd, freeCompressionContext)
from _lz4 import ffi, lib

BUF_SIZE = 16 * 1024
LZ4_HEADER_SIZE = 19
LZ4_FOOTER_SIZE = 4

ctx = createCompressionContext()
lz4_preferences = ffi.new("LZ4F_preferences_t*",
                          {'frameInfo': {'blockSizeID': lib.LZ4F_max256KB,
                                         'blockMode': lib.LZ4F_blockLinked,
                                         'contentChecksumFlag': lib.LZ4F_noContentChecksum,
                                         'frameType': lib.LZ4F_frame,
                                         'contentSize': 0,
                                         'reserved': [0, 0]},
                           'compressionLevel': 0,
                           'autoFlush': 0,
                           'reserved': [0, 0, 0, 0]})

src = ffi.new("char[]", BUF_SIZE)
src_buf = ffi.buffer(src)
frame_size = compressBound(BUF_SIZE, lz4_preferences)
dst_size = frame_size + LZ4_HEADER_SIZE + LZ4_FOOTER_SIZE
dst = ffi.new("char[]", dst_size)
dst_buf = ffi.buffer(dst)
n = offset = count_out = compressBegin(ctx[0], dst, dst_size, lz4_preferences)

infile = open("test.tar", "rb")
outfile = open("test.tar.lz4", "wb")
count_in = 0
offset = 0

while True:
    k = infile.raw.readinto(src_buf)
    if k == 0:
        break
    count_in += k
    n =  compressUpdate(ctx[0], dst + offset, dst_size - offset, src, k)

    offset += n
    count_out +=n

    if dst_size - offset < frame_size + LZ4_FOOTER_SIZE:
        #print("Writing {0} bytes".format(offset))
        k = outfile.raw.write(dst_buf[:offset])
        if k < offset:
            print("Short write")

        offset = 0

n = compressEnd(ctx[0], dst + offset, dst_size - offset)

offset += n
count_out += n
print("Writing {0} bytes".format(offset))
k = outfile.raw.write(dst_buf[:offset])
if k < offset:
    print("Short write")

freeCompressionContext(ctx[0])
infile.close()
outfile.close()
