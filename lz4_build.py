from cffi import FFI

ffi = FFI()
ffi.set_source("_lz4", """
#define LZ4F_DISABLE_OBSOLETE_ENUMS
#include <lz4frame.h>""", libraries=['lz4'])

ffi.cdef("typedef ... LZ4F_preferences_t;")
ffi.cdef("""
typedef size_t LZ4F_errorCode_t;
unsigned LZ4F_isError(LZ4F_errorCode_t code);
unsigned LZ4F_isError(LZ4F_errorCode_t code);
""")

ffi.cdef("size_t LZ4F_compressFrameBound(size_t srcSize, const LZ4F_preferences_t* preferencesPtr);")
ffi.cdef("size_t LZ4F_compressFrame(void* dstBuffer, size_t dstMaxSize, const void* srcBuffer, size_t srcSize, const LZ4F_preferences_t* preferencesPtr);")

ffi.cdef("""
typedef struct LZ4F_cctx_s* LZ4F_compressionContext_t;
typedef struct {
  unsigned stableSrc;    /* 1 == src content will remain available on future calls to LZ4F_compress(); avoid saving src content within tmp buffer as future dictionary */
  unsigned reserved[3];
} LZ4F_compressOptions_t;
""")

ffi.cdef("""
#define LZ4F_VERSION 100
LZ4F_errorCode_t LZ4F_createCompressionContext(LZ4F_compressionContext_t* cctxPtr, unsigned version);
LZ4F_errorCode_t LZ4F_freeCompressionContext(LZ4F_compressionContext_t cctx);
""")


ffi.cdef("""
size_t LZ4F_compressBegin(LZ4F_compressionContext_t cctx, void* dstBuffer, size_t dstMaxSize, const LZ4F_preferences_t* prefsPtr);
size_t LZ4F_compressBound(size_t srcSize, const LZ4F_preferences_t* prefsPtr);
size_t LZ4F_compressUpdate(LZ4F_compressionContext_t cctx, void* dstBuffer, size_t dstMaxSize, const void* srcBuffer, size_t srcSize, const LZ4F_compressOptions_t* cOptPtr);
size_t LZ4F_flush(LZ4F_compressionContext_t cctx, void* dstBuffer, size_t dstMaxSize, const LZ4F_compressOptions_t* cOptPtr);
size_t LZ4F_compressEnd(LZ4F_compressionContext_t cctx, void* dstBuffer, size_t dstMaxSize, const LZ4F_compressOptions_t* cOptPtr);""")

if __name__ == "__main__":
    ffi.compile()
