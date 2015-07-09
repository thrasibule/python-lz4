from _lz4 import lib, ffi

def createCompressionContext():
    ctx = ffi.new("LZ4F_compressionContext_t*")
    r = lib.LZ4F_createCompressionContext(ctx, lib.LZ4F_VERSION)
    if lib.LZ4F_isError(r):
        raise NameError(ffi.string(lib.LZ4F_getErrorName(code)))
    else:
        return ctx

def compressBound(src_size, prefs = ffi.NULL):
    return lib.LZ4F_compressBound(src_size, prefs)

def compressBegin(ctx, dst_buf, dst_size, prefs = ffi.NULL):
    n = lib.LZ4F_compressBegin(ctx, dst_buf, dst_size, prefs)
    if lib.LZ4F_isError(n):
        raise NameError(ffi.string(lib.LZ4F_getErrorName(n)))
    else:
        return n

def compressUpdate(ctx, dst_buf, dst_size, src_buf, src_size, comp_opts = ffi.NULL):
    n = lib.LZ4F_compressUpdate(ctx, dst_buf, dst_size, src_buf, src_size, comp_opts)
    if lib.LZ4F_isError(n):
         raise NameError(ffi.string(lib.LZ4F_getErrorName(n)))
    else:
        return n

def compressEnd(ctx, dst_buf, dst_size, comp_opts = ffi.NULL):
    n = lib.LZ4F_compressEnd(ctx, dst_buf, dst_size, comp_opts)
    if lib.LZ4F_isError(n):
         raise NameError(ffi.string(lib.LZ4F_getErrorName(n)))
    else:
        return n

def freeCompressionContext(ctx):
    lib.LZ4F_freeCompressionContext(ctx)
