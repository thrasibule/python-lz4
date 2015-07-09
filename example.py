from lz4f import (createCompressionContext, compressBound,
                  compressBegin, compressUpdate, compressEnd, freeCompressionContext)
from _lz4 import ffi, lib

SRC_SIZE = 16 * 1024

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

src = ffi.new("char[]", SRC_SIZE)
src_buf = ffi.buffer(src)
dst_size = compressBound(SRC_SIZE, lz4_preferences)

dst = ffi.new("char[]", dst_size)
dst_buf = ffi.buffer(dst)

infile = open("test.tar", "rb")
outfile = open("test.tar.lz4", "wb")
filesize = 0
compressedfilesize = 0

read_size = infile.raw.readinto(src_buf)
filesize += read_size

header_size = compressBegin(ctx[0], dst, dst_size, lz4_preferences)
size_check = outfile.write(dst_buf[:header_size])
compressedfilesize += header_size

while read_size > 0:
    out_size =  compressUpdate(ctx[0], dst, dst_size, src, read_size)
    size_check = outfile.write(dst_buf[:out_size])
    compressedfilesize += out_size
    read_size = infile.raw.readinto(src_buf)
    filesize += read_size

footer_size = compressEnd(ctx[0], dst, dst_size)
size_check = outfile.write(dst_buf[:footer_size])
compressedfilesize += footer_size

freeCompressionContext(ctx[0])
infile.close()
outfile.close()
