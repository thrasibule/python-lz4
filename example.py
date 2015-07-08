from _lz4 import lib, ffi

ctx = ffi.new("LZ4F_compressionContext_t*")

r = lib.LZ4F_createCompressionContext(ctx, lib.LZ4F_VERSION)
