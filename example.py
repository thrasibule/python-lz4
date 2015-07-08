from _lz4 import lib, ffi

BUF_SIZE = 16 * 1024
LZ4_HEADER_SIZE = 19
LZ4_FOOTER_SIZE = 4
ctx = ffi.new("LZ4F_compressionContext_t*")

r = lib.LZ4F_createCompressionContext(ctx, lib.LZ4F_VERSION)

lz4_preferences = ffi.new("LZ4F_preferences_t*", {'frameInfo': {'blockSizeID': lib.LZ4F_max256KB,
                                                                'blockMode': lib.LZ4F_blockLinked,
                                                                'contentChecksumFlag': lib.LZ4F_noContentChecksum,
                                                                'frameType': lib.LZ4F_frame,
                                                                'contentSize': 0,
                                                                'reserved': [0, 0]},
                                                  'compressionLevel': 0,
                                                  'autoFlush': 0,
                                                  'reserved': [0, 0, 0, 0]})

if lib.LZ4F_isError(r):
    print("error")
src = ffi.new("char[1024]")
frame_size = lib.LZ4F_compressBound(BUF_SIZE, lz4_preferences)
size = frame_size + LZ4_HEADER_SIZE + LZ4_FOOTER_SIZE
buf = ffi.new("char[]", size)
n = offset = count_out = lib.LZ4F_compressBegin(ctx[0], buf, size, lz4_preferences)
if lib.LZ4F_isError(n):
    print("error")

print(n)
